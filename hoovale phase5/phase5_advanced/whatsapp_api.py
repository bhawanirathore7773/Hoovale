"""
HOOVALE WhatsApp Business API Integration
==========================================
Automates lead capture, sends auto-replies, manages catalog sharing.

WhatsApp Business API is a paid service via Meta (Facebook). You need:
1. Meta Business account
2. WhatsApp Business API access (via Meta or Business Solution Provider)
3. Verified business phone number
4. Approved message templates

Pricing: ~₹0.30-1.50 per conversation (varies). Free for first 1000/month
typically. Marketing/business messages cost more than utility/auth messages.

This module provides:
- send_message() - send text message to a WhatsApp number
- send_template() - send approved template message
- send_catalog() - send product catalog
- log_enquiry() - log incoming WhatsApp leads to database
- webhook_handler() - receive incoming messages and auto-reply

Place at: integrations/whatsapp_api.py
"""
import requests
import json
import logging
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================
# Add to settings.py:
# WHATSAPP_API_TOKEN = "EAAxxxx..." (your Meta access token)
# WHATSAPP_PHONE_NUMBER_ID = "1234567890" (your business phone number ID)
# WHATSAPP_VERIFY_TOKEN = "your_random_verify_string" (for webhook setup)
# WHATSAPP_API_VERSION = "v18.0" (or current)

API_BASE_URL = f"https://graph.facebook.com/{getattr(settings, 'WHATSAPP_API_VERSION', 'v18.0')}"


# ============================================================================
# MODEL FOR LEAD TRACKING
# ============================================================================
class WhatsAppLead(models.Model):
    """Track incoming WhatsApp enquiries."""
    phone_number = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=200, blank=True)
    initial_message = models.TextField()
    enquiry_type = models.CharField(max_length=50, blank=True, 
                                     choices=[
                                         ('catalog', 'Catalog Request'),
                                         ('quote', 'Quote Request'),
                                         ('custom_logo', 'Custom Logo Enquiry'),
                                         ('bulk_order', 'Bulk Order'),
                                         ('oem', 'OEM Manufacturing'),
                                         ('general', 'General Enquiry'),
                                     ])
    status = models.CharField(max_length=20, default='new',
                              choices=[
                                  ('new', 'New'),
                                  ('contacted', 'Contacted'),
                                  ('qualified', 'Qualified'),
                                  ('quoted', 'Quoted'),
                                  ('converted', 'Converted'),
                                  ('lost', 'Lost'),
                              ])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.phone_number} - {self.enquiry_type} - {self.status}"


class WhatsAppMessage(models.Model):
    """Log all WhatsApp messages (incoming and outgoing)."""
    lead = models.ForeignKey(WhatsAppLead, on_delete=models.CASCADE, 
                              related_name='messages')
    direction = models.CharField(max_length=10, 
                                  choices=[('in', 'Incoming'), ('out', 'Outgoing')])
    message_type = models.CharField(max_length=20, default='text')
    content = models.TextField()
    message_id = models.CharField(max_length=100, blank=True)  # WhatsApp message ID
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']


# ============================================================================
# CORE API FUNCTIONS
# ============================================================================
def _make_request(endpoint, method='POST', data=None):
    """Make authenticated request to WhatsApp Business API."""
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    try:
        if method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"WhatsApp API error: {e}")
        return None


def send_message(phone_number, message_text):
    """
    Send a text message to a WhatsApp number.
    
    Note: Can only send free-form messages within 24 hours of customer's
    last message. Outside this window, must use approved templates.
    
    Args:
        phone_number: Recipient's phone with country code (e.g., '919876543210')
        message_text: Plain text message
    
    Returns:
        dict with message ID, or None on failure
    """
    endpoint = f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message_text}
    }
    
    result = _make_request(endpoint, data=data)
    
    if result and 'messages' in result:
        message_id = result['messages'][0]['id']
        logger.info(f"WhatsApp message sent to {phone_number}: {message_id}")
        return {"success": True, "message_id": message_id}
    
    return None


def send_template(phone_number, template_name, parameters=None, language='en'):
    """
    Send an approved template message (can send outside 24-hour window).
    
    Template must be pre-approved by Meta. Common HOOVALE templates:
    - 'catalog_share' - Share catalog with customer
    - 'quote_request_received' - Confirm quote request received
    - 'order_confirmation' - Confirm bulk order
    - 'production_update' - Notify on production status
    - 'dispatch_notification' - Notify on dispatch
    
    Args:
        phone_number: Recipient's phone with country code
        template_name: Name of approved template
        parameters: List of parameter values for template placeholders
        language: Template language code (en, hi for Hindi, ar for Arabic)
    """
    endpoint = f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language}
        }
    }
    
    # Add parameters if provided
    if parameters:
        data["template"]["components"] = [{
            "type": "body",
            "parameters": [{"type": "text", "text": str(p)} for p in parameters]
        }]
    
    result = _make_request(endpoint, data=data)
    
    if result and 'messages' in result:
        return {"success": True, "message_id": result['messages'][0]['id']}
    
    return None


def send_catalog_pdf(phone_number, catalog_url, caption=""):
    """
    Send catalog PDF document to WhatsApp number.
    
    Args:
        phone_number: Recipient's phone with country code
        catalog_url: Public URL of the catalog PDF
        caption: Optional caption text
    """
    endpoint = f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "document",
        "document": {
            "link": catalog_url,
            "filename": "HOOVALE-Catalog-2026.pdf",
            "caption": caption or "HOOVALE wall clock catalog. Visit hoovale.com for full range."
        }
    }
    
    return _make_request(endpoint, data=data)


def send_product_image(phone_number, image_url, caption=""):
    """Send a product image to WhatsApp."""
    endpoint = f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "image",
        "image": {"link": image_url, "caption": caption}
    }
    return _make_request(endpoint, data=data)


# ============================================================================
# WEBHOOK HANDLER FOR INCOMING MESSAGES
# ============================================================================
@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    """
    WhatsApp webhook endpoint.
    
    GET: Verification challenge from Meta during webhook setup
    POST: Incoming messages and events from customers
    
    Add to urls.py:
        path('whatsapp/webhook/', whatsapp_webhook),
    """
    
    # ===== GET: Webhook verification =====
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
            return JsonResponse(int(challenge), safe=False)
        return JsonResponse({"error": "Verification failed"}, status=403)
    
    # ===== POST: Incoming message =====
    try:
        data = json.loads(request.body)
        
        # Parse WhatsApp webhook payload
        entries = data.get('entry', [])
        for entry in entries:
            changes = entry.get('changes', [])
            for change in changes:
                value = change.get('value', {})
                messages = value.get('messages', [])
                contacts = value.get('contacts', [])
                
                for msg in messages:
                    _handle_incoming_message(msg, contacts)
        
        return JsonResponse({"status": "received"})
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def _handle_incoming_message(message, contacts):
    """Process a single incoming WhatsApp message."""
    phone = message.get('from')
    msg_type = message.get('type')
    msg_id = message.get('id')
    
    # Extract name from contacts list
    name = ""
    for contact in contacts:
        if contact.get('wa_id') == phone:
            name = contact.get('profile', {}).get('name', '')
            break
    
    # Extract message text
    text = ""
    if msg_type == 'text':
        text = message.get('text', {}).get('body', '')
    elif msg_type == 'interactive':
        # Button reply
        interactive = message.get('interactive', {})
        if interactive.get('type') == 'button_reply':
            text = f"[Button: {interactive['button_reply']['title']}]"
    elif msg_type == 'image':
        text = "[Customer sent image]"
    
    # Detect enquiry type from message content
    enquiry_type = _detect_enquiry_type(text)
    
    # Find or create lead
    lead, created = WhatsAppLead.objects.get_or_create(
        phone_number=phone,
        defaults={
            'name': name,
            'initial_message': text,
            'enquiry_type': enquiry_type,
            'status': 'new',
        }
    )
    
    if not created and name and not lead.name:
        lead.name = name
        lead.save()
    
    # Log message
    WhatsAppMessage.objects.create(
        lead=lead,
        direction='in',
        message_type=msg_type,
        content=text,
        message_id=msg_id,
    )
    
    # Send auto-reply (only on first message or specific triggers)
    if created or _should_send_auto_reply(text):
        auto_reply = _generate_auto_reply(text, enquiry_type, name)
        if auto_reply:
            result = send_message(phone, auto_reply)
            if result:
                WhatsAppMessage.objects.create(
                    lead=lead,
                    direction='out',
                    message_type='text',
                    content=auto_reply,
                    message_id=result.get('message_id', ''),
                )
    
    # Notify sales team for new leads
    if created:
        _notify_sales_team(lead)


def _detect_enquiry_type(text):
    """Detect enquiry type from message content."""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['catalog', 'catalogue', 'brochure']):
        return 'catalog'
    if any(word in text_lower for word in ['quote', 'price', 'cost', 'rate']):
        return 'quote'
    if any(word in text_lower for word in ['logo', 'custom', 'branding', 'print']):
        return 'custom_logo'
    if any(word in text_lower for word in ['bulk', 'wholesale', 'volume']):
        return 'bulk_order'
    if any(word in text_lower for word in ['oem', 'private label', 'own brand']):
        return 'oem'
    
    return 'general'


def _should_send_auto_reply(text):
    """Determine if we should send auto-reply (avoid spam)."""
    # Only auto-reply to specific triggers
    text_lower = text.lower()
    triggers = ['catalog', 'price', 'quote', 'hi', 'hello', 'namaste', 
                'info', 'enquiry', 'help']
    return any(trigger in text_lower for trigger in triggers)


def _generate_auto_reply(text, enquiry_type, name):
    """Generate appropriate auto-reply based on enquiry type."""
    
    greeting = f"Hi {name}," if name else "Hi,"
    
    if enquiry_type == 'catalog':
        return (
            f"{greeting} thanks for your interest in HOOVALE!\n\n"
            f"📦 Sharing our catalog: https://hoovale.com/catalog.pdf\n\n"
            f"For specific designs or custom logo printing, please share:\n"
            f"• Quantity needed\n"
            f"• Specific design preference\n"
            f"• Delivery location\n\n"
            f"Our team will respond with detailed pricing within 2 hours."
        )
    
    elif enquiry_type == 'quote':
        return (
            f"{greeting} we'd be happy to share pricing!\n\n"
            f"To prepare your quote quickly, please share:\n\n"
            f"1️⃣ Quantity needed\n"
            f"2️⃣ Wall clock type (wooden/plastic/designer)\n"
            f"3️⃣ Size preference (10/12/14 inch)\n"
            f"4️⃣ Custom logo? (yes/no)\n"
            f"5️⃣ Delivery city\n\n"
            f"Reply with details and we'll send quote in 2 hours."
        )
    
    elif enquiry_type == 'custom_logo':
        return (
            f"{greeting} thanks for considering HOOVALE for custom logo wall clocks!\n\n"
            f"🎨 Custom logo MOQ: 100 pieces (free above 200)\n"
            f"🖨️ UV printing — sharp, fade-resistant 5+ years\n"
            f"⏱️ Production: 7-15 days\n\n"
            f"Please share:\n"
            f"• Quantity\n"
            f"• Logo file (vector preferred: AI/EPS/SVG/PDF)\n"
            f"• Delivery location\n\n"
            f"We'll send free digital mockup in 24 hours."
        )
    
    elif enquiry_type == 'bulk_order':
        return (
            f"{greeting} thanks for your bulk enquiry!\n\n"
            f"📦 HOOVALE bulk pricing tiers:\n"
            f"• 200+ pieces: 20-25% discount\n"
            f"• 500+ pieces: 30-35% discount\n"
            f"• 2000+ pieces: 40-50% discount\n\n"
            f"To send accurate quote, please share:\n"
            f"• Approximate quantity\n"
            f"• Use case (corporate gifting/retail/hotel etc.)\n"
            f"• Custom branding needed?\n"
            f"• Target delivery date\n"
            f"• Delivery location\n\n"
            f"Detailed quote within 2 hours."
        )
    
    elif enquiry_type == 'oem':
        return (
            f"{greeting} thanks for your OEM enquiry!\n\n"
            f"🏭 HOOVALE OEM private label service:\n"
            f"• MOQ: 100 pieces (path A: our design + your branding)\n"
            f"• MOQ: 200-500 pieces (path B: fully custom design)\n"
            f"• NDA available — your designs stay confidential\n"
            f"• Custom packaging available\n\n"
            f"To discuss your requirement, please share:\n"
            f"• Your brand name\n"
            f"• Annual volume estimate\n"
            f"• Custom design or use existing?\n"
            f"• Target markets\n\n"
            f"Our team will schedule a call to discuss further."
        )
    
    else:  # general
        return (
            f"{greeting} thanks for contacting HOOVALE!\n\n"
            f"We're Jaipur's leading wall clock manufacturer.\n\n"
            f"How can we help you today?\n\n"
            f"1️⃣ Reply 'CATALOG' — get product catalog\n"
            f"2️⃣ Reply 'QUOTE' — get pricing\n"
            f"3️⃣ Reply 'CUSTOM' — custom logo enquiry\n"
            f"4️⃣ Reply 'OEM' — private label enquiry\n\n"
            f"Or just describe your requirement and we'll respond within 2 hours."
        )


def _notify_sales_team(lead):
    """Notify sales team of new lead (via email, Slack, etc.)."""
    # Implement based on your team's communication channel
    # Example: send email to sales@hoovale.com
    
    try:
        from django.core.mail import send_mail
        
        subject = f"🔔 New WhatsApp Lead: {lead.enquiry_type} from {lead.phone_number}"
        message = (
            f"New WhatsApp lead received!\n\n"
            f"Phone: {lead.phone_number}\n"
            f"Name: {lead.name or 'Not provided'}\n"
            f"Type: {lead.get_enquiry_type_display()}\n"
            f"Message: {lead.initial_message}\n\n"
            f"Time: {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Login to admin to track: https://hoovale.com/admin/integrations/whatsapplead/{lead.id}/"
        )
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.SALES_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to notify sales team: {e}")


# ============================================================================
# UTILITY: Trigger from website forms
# ============================================================================
def trigger_whatsapp_from_form(phone_number, name, enquiry_type, details):
    """
    Trigger WhatsApp message when customer submits website form.
    
    Use this in your Django views when an enquiry form is submitted.
    
    Example:
        # In views.py
        def submit_enquiry(request):
            # ... save enquiry to DB ...
            trigger_whatsapp_from_form(
                phone_number=cleaned_data['phone'],
                name=cleaned_data['name'],
                enquiry_type='bulk_order',
                details=f"Need {qty} pieces"
            )
    """
    # Format phone number with country code
    if not phone_number.startswith('+'):
        phone_number = '91' + phone_number  # Default to India
    phone_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
    
    # Send template message (template must be pre-approved)
    return send_template(
        phone_number=phone_number,
        template_name='enquiry_received',  # Must be pre-approved template
        parameters=[name, enquiry_type, details],
        language='en'
    )


# ============================================================================
# EXAMPLE INSTALLATION/SETUP
# ============================================================================
"""
SETUP INSTRUCTIONS:

1. Get WhatsApp Business API access:
   - Visit business.facebook.com
   - Set up WhatsApp Business Account
   - Get phone number ID and access token
   - (Or use a BSP like Twilio, Gupshup, AiSensy for easier setup)

2. Configure Django settings:
   # settings.py
   WHATSAPP_API_TOKEN = os.environ.get('WHATSAPP_API_TOKEN')
   WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
   WHATSAPP_VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN')
   WHATSAPP_API_VERSION = "v18.0"
   SALES_EMAIL = 'sales@hoovale.com'

3. Create integrations app:
   python manage.py startapp integrations
   # Add 'integrations' to INSTALLED_APPS

4. Place this file as: integrations/whatsapp_api.py

5. Configure webhook in Meta Business Manager:
   - Webhook URL: https://hoovale.com/whatsapp/webhook/
   - Verify Token: (match your WHATSAPP_VERIFY_TOKEN)
   - Subscribe to: messages, message_status

6. Add URL routing:
   # hoovale_project/urls.py
   from integrations.whatsapp_api import whatsapp_webhook
   urlpatterns += [
       path('whatsapp/webhook/', whatsapp_webhook),
   ]

7. Pre-approve message templates in Meta Business Manager:
   - 'enquiry_received' (utility template)
   - 'catalog_share' (utility template)
   - 'order_confirmation' (utility template)
   - 'production_update' (utility template)
   - 'dispatch_notification' (utility template)

8. Run migrations:
   python manage.py makemigrations integrations
   python manage.py migrate

9. Test:
   - Send WhatsApp message to your business number
   - Check admin: WhatsAppLead model should have new entry
   - Verify auto-reply sent back

EXPECTED LEAD VOLUME:
- Initial: 5-15 leads/month from website WhatsApp button
- After SEO matures: 30-100+ leads/month
- 24-hour response time becomes critical at scale

PRICING (Meta WhatsApp API):
- Conversation-based pricing (NOT per-message)
- Business-initiated conversation: ₹0.50-1.50 per conversation
- User-initiated conversation: free for 24 hours
- ~₹1,000-5,000/month for typical SMB usage

ALTERNATIVES (Business Solution Providers):
- AiSensy (Indian): ₹999-₹9,999/month plans
- Gupshup (Indian): Pay-as-you-go
- Twilio: International pricing
- WATI: User-friendly UI

For Indian SMB scale, AiSensy or Gupshup typically simpler than direct Meta API.
"""
