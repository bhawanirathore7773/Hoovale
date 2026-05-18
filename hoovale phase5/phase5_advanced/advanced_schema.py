"""
HOOVALE Advanced Schema Template Tags
======================================
Phase 5 advanced schemas for AI search optimization (AIO/GEO/AEO).

Adds to Phase 1's basic schema (Organization, LocalBusiness, Product, FAQPage):
- Speakable schema (voice search + AI extraction)
- HowTo schema (procedural content)
- Service schema (service pages)
- ImageObject schema (product images for AI vision)
- VideoObject schema (when video added)
- Article schema (blog posts)
- Person schema (author bios)
- Review schema (testimonials)
- AggregateRating schema (overall ratings)
- ContactPoint schema (multiple contact methods)

Place at: products/templatetags/advanced_schema.py

Usage in templates:
    {% load advanced_schema %}
    {% speakable_schema %}
    {% howto_schema steps %}
    {% service_schema service %}
"""
import json
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


# ============================================================================
# SPEAKABLE SCHEMA — for voice search & AI extraction
# ============================================================================
@register.simple_tag
def speakable_schema(css_selectors=None):
    """
    Marks specific content as "speakable" — optimized for voice search
    and AI engine extraction.
    
    Usage in template:
        {% speakable_schema ".direct-answer,.faq-answer,.summary" %}
    
    Then in HTML:
        <div class="direct-answer">[40-word direct answer here]</div>
        <div class="faq-answer">[FAQ answer]</div>
    """
    if css_selectors is None:
        css_selectors = ".direct-answer,.summary,.faq-answer,.key-takeaway"
    
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": css_selectors.split(",")
        }
    }
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# HOWTO SCHEMA — for procedural content
# ============================================================================
@register.simple_tag
def howto_schema(name, description, total_time=None, supplies=None, steps=None, image=None):
    """
    HowTo schema for procedural content (e.g., how to order, how to choose).
    
    Usage in template:
        {% howto_schema 
            name="How to Order Bulk Wall Clocks"
            description="Step-by-step guide to ordering bulk wall clocks from HOOVALE"
            total_time="PT7D"
            steps=order_steps %}
    
    Where order_steps is a list like:
        [
            {"name": "Browse catalog", "text": "Visit hoovale.com/products/"},
            {"name": "Request quote", "text": "WhatsApp +91 9462207356"},
            ...
        ]
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
    }
    
    if total_time:
        schema["totalTime"] = total_time  # ISO 8601 duration (e.g., PT7D = 7 days)
    
    if image:
        schema["image"] = image
    
    if supplies:
        schema["supply"] = [{"@type": "HowToSupply", "name": s} for s in supplies]
    
    if steps:
        schema["step"] = [
            {
                "@type": "HowToStep",
                "position": idx + 1,
                "name": step.get("name", f"Step {idx + 1}"),
                "text": step.get("text", ""),
                **({"image": step["image"]} if step.get("image") else {}),
                **({"url": step["url"]} if step.get("url") else {}),
            }
            for idx, step in enumerate(steps)
        ]
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# SERVICE SCHEMA — for service pages
# ============================================================================
@register.simple_tag
def service_schema(service):
    """
    Service schema for service pages (bulk supply, custom logo, OEM, etc.).
    
    Usage in template:
        {% service_schema service %}
    
    Where 'service' is a ServicePage model instance.
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service.service_name,
        "description": getattr(service, 'description', '') or getattr(service, 'intro_content', '')[:300],
        "provider": {
            "@type": "Organization",
            "name": "HOOVALE",
            "url": "https://hoovale.com",
            "logo": "https://hoovale.com/static/img/logo.png",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Jaipur",
                "addressRegion": "Rajasthan",
                "postalCode": "302001",
                "addressCountry": "IN"
            },
            "telephone": "+91-9462207356"
        },
        "serviceType": getattr(service, 'service_type', 'Wall Clock Manufacturing'),
        "areaServed": {
            "@type": "Country",
            "name": "India"
        },
    }
    
    # Add price range if available
    if hasattr(service, 'price_range') and service.price_range:
        schema["offers"] = {
            "@type": "Offer",
            "priceRange": service.price_range,
            "priceCurrency": "INR",
            "availability": "https://schema.org/InStock"
        }
    
    # Add MOQ as a service attribute
    if hasattr(service, 'min_order_quantity') and service.min_order_quantity:
        schema["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": f"{service.service_name} - Minimum Order: {service.min_order_quantity} pieces",
        }
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# IMAGEOBJECT SCHEMA — for product images
# ============================================================================
@register.simple_tag
def image_schema(image_url, name, description=None, width=None, height=None):
    """
    ImageObject schema for product images. Helps AI vision engines understand
    product images better.
    
    Usage in template:
        {% image_schema 
            image_url=product.image.url 
            name=product.name 
            description=product.description %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "contentUrl": image_url,
        "name": name,
    }
    
    if description:
        schema["description"] = description
    
    if width:
        schema["width"] = width
    
    if height:
        schema["height"] = height
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# VIDEO SCHEMA — for video content (when added)
# ============================================================================
@register.simple_tag
def video_schema(name, description, upload_date, thumbnail_url, embed_url=None, content_url=None, duration=None):
    """
    VideoObject schema for embedded videos (YouTube embeds, factory tours, etc.).
    
    Usage:
        {% video_schema 
            name="HOOVALE Factory Tour" 
            description="Tour of HOOVALE wall clock manufacturing facility"
            upload_date="2026-01-15"
            thumbnail_url="https://hoovale.com/static/img/factory-tour-thumb.jpg"
            embed_url="https://www.youtube.com/embed/VIDEO_ID"
            duration="PT5M30S" %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": name,
        "description": description,
        "uploadDate": upload_date,
        "thumbnailUrl": thumbnail_url,
    }
    
    if embed_url:
        schema["embedUrl"] = embed_url
    
    if content_url:
        schema["contentUrl"] = content_url
    
    if duration:
        schema["duration"] = duration  # ISO 8601 (PT5M30S = 5 min 30 sec)
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# ARTICLE SCHEMA — for blog posts
# ============================================================================
@register.simple_tag
def article_schema(article, author_name=None, author_url=None, image_url=None):
    """
    Article schema for blog posts.
    
    Usage:
        {% article_schema blog author_name=blog.author_name %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.title,
        "description": article.meta_description or article.title,
        "datePublished": article.created_at.isoformat() if hasattr(article, 'created_at') else "",
        "dateModified": article.updated_at.isoformat() if hasattr(article, 'updated_at') else "",
        "author": {
            "@type": "Person",
            "name": author_name or "HOOVALE Team",
            "url": author_url or "https://hoovale.com/about/",
        },
        "publisher": {
            "@type": "Organization",
            "name": "HOOVALE",
            "logo": {
                "@type": "ImageObject",
                "url": "https://hoovale.com/static/img/logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://hoovale.com/blog/{article.slug}/" if hasattr(article, 'slug') else ""
        }
    }
    
    if image_url:
        schema["image"] = image_url
    elif hasattr(article, 'featured_image') and article.featured_image:
        schema["image"] = f"https://hoovale.com{article.featured_image.url}"
    
    if hasattr(article, 'category') and article.category:
        schema["articleSection"] = article.category
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# PERSON SCHEMA — for author bios
# ============================================================================
@register.simple_tag
def person_schema(name, job_title, organization, description=None, image_url=None, linkedin_url=None):
    """
    Person schema for author bios. Critical for E-E-A-T signals.
    
    Usage:
        {% person_schema 
            name="Founder Name" 
            job_title="Founder, HOOVALE"
            organization="HOOVALE"
            description="20 years in wall clock manufacturing..."
            image_url="https://hoovale.com/static/img/founder.jpg"
            linkedin_url="https://linkedin.com/in/foundername" %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name,
        "jobTitle": job_title,
        "worksFor": {
            "@type": "Organization",
            "name": organization,
            "url": "https://hoovale.com"
        }
    }
    
    if description:
        schema["description"] = description
    
    if image_url:
        schema["image"] = image_url
    
    if linkedin_url:
        schema["sameAs"] = [linkedin_url]
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# REVIEW SCHEMA — for individual testimonials
# ============================================================================
@register.simple_tag
def review_schema(testimonial):
    """
    Review schema for individual testimonials.
    
    Usage:
        {% for testimonial in testimonials %}
            {% review_schema testimonial %}
        {% endfor %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Review",
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": str(testimonial.rating),
            "bestRating": "5",
            "worstRating": "1"
        },
        "author": {
            "@type": "Person",
            "name": testimonial.customer_name
        },
        "reviewBody": testimonial.review_text,
        "itemReviewed": {
            "@type": "Organization",
            "name": "HOOVALE"
        }
    }
    
    if hasattr(testimonial, 'created_at') and testimonial.created_at:
        schema["datePublished"] = testimonial.created_at.strftime('%Y-%m-%d')
    
    if hasattr(testimonial, 'customer_company') and testimonial.customer_company:
        schema["author"]["worksFor"] = {
            "@type": "Organization",
            "name": testimonial.customer_company
        }
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# AGGREGATERATING SCHEMA — for overall ratings (homepage)
# ============================================================================
@register.simple_tag
def aggregate_rating_schema(avg_rating=4.7, total_reviews=150):
    """
    AggregateRating schema for overall organization rating.
    
    Usage in homepage template:
        {% aggregate_rating_schema avg_rating=4.7 total_reviews=150 %}
    
    NOTE: Only use if you actually have this many genuine reviews.
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "HOOVALE",
        "url": "https://hoovale.com",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(avg_rating),
            "bestRating": "5",
            "worstRating": "1",
            "ratingCount": str(total_reviews),
            "reviewCount": str(total_reviews),
        }
    }
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# CONTACTPOINT SCHEMA — multiple contact methods
# ============================================================================
@register.simple_tag
def contact_point_schema():
    """
    ContactPoint schema for multiple ways to reach HOOVALE.
    Important for AI engines that might recommend contact methods.
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "HOOVALE",
        "url": "https://hoovale.com",
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": "+91-9462207356",
                "contactType": "customer service",
                "areaServed": "IN",
                "availableLanguage": ["English", "Hindi"],
                "contactOption": "TollFree",
                "hoursAvailable": "Mo-Sa 09:00-19:00"
            },
            {
                "@type": "ContactPoint",
                "telephone": "+91-9462207356",
                "contactType": "sales",
                "areaServed": "IN",
                "availableLanguage": ["English", "Hindi"],
            },
            {
                "@type": "ContactPoint",
                "telephone": "+91-9462207356",
                "contactType": "WhatsApp",
                "areaServed": "IN",
                "availableLanguage": ["English", "Hindi"],
            },
            {
                "@type": "ContactPoint",
                "email": "info@hoovale.com",
                "contactType": "customer service",
                "areaServed": "IN",
                "availableLanguage": ["English"],
            }
        ]
    }
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# PRODUCT SCHEMA — enhanced version with all attributes
# ============================================================================
@register.simple_tag
def enhanced_product_schema(product):
    """
    Enhanced Product schema with all attributes for maximum AI engine extraction.
    
    Replaces Phase 1's basic product schema with this richer version.
    
    Usage:
        {% enhanced_product_schema product %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "description": product.description[:300] if product.description else product.name,
        "sku": getattr(product, 'sku', '') or f"HOOVALE-{product.id}",
        "mpn": getattr(product, 'sku', ''),
        "brand": {
            "@type": "Brand",
            "name": getattr(product, 'brand', 'HOOVALE')
        },
        "category": product.category.category_name if hasattr(product, 'category') and product.category else "Wall Clocks",
        "manufacturer": {
            "@type": "Organization",
            "name": "HOOVALE",
            "url": "https://hoovale.com",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Jaipur",
                "addressRegion": "Rajasthan",
                "addressCountry": "IN"
            }
        },
    }
    
    # Image
    if hasattr(product, 'image') and product.image:
        schema["image"] = f"https://hoovale.com{product.image.url}"
    
    # Pricing
    if hasattr(product, 'price') and product.price:
        schema["offers"] = {
            "@type": "Offer",
            "url": f"https://hoovale.com/product/{product.slug}/" if hasattr(product, 'slug') else "",
            "priceCurrency": "INR",
            "price": str(product.price),
            "availability": "https://schema.org/InStock" if getattr(product, 'availability', True) else "https://schema.org/OutOfStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {
                "@type": "Organization",
                "name": "HOOVALE"
            }
        }
        
        # Bulk pricing if available
        if hasattr(product, 'bulk_price') and product.bulk_price:
            schema["offers"]["priceSpecification"] = [
                {
                    "@type": "UnitPriceSpecification",
                    "name": "Retail (1-49 pieces)",
                    "price": str(product.price),
                    "priceCurrency": "INR"
                },
                {
                    "@type": "UnitPriceSpecification", 
                    "name": "Bulk (50+ pieces)",
                    "price": str(product.bulk_price),
                    "priceCurrency": "INR"
                }
            ]
    
    # Additional properties (specifications)
    if hasattr(product, 'specifications') and product.specifications:
        # Assume specifications is a dict or JSON
        try:
            specs = product.specifications if isinstance(product.specifications, dict) else json.loads(product.specifications)
            schema["additionalProperty"] = [
                {"@type": "PropertyValue", "name": k, "value": str(v)}
                for k, v in specs.items()
            ]
        except (ValueError, TypeError):
            pass
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# EVENT SCHEMA — for trade fairs and events
# ============================================================================
@register.simple_tag
def event_schema(name, start_date, end_date, location_name, location_address, description, url=None):
    """
    Event schema for trade fairs HOOVALE participates in.
    
    Usage:
        {% event_schema 
            name="Visit HOOVALE at IGFE Mumbai 2026"
            start_date="2026-08-15"
            end_date="2026-08-17"
            location_name="Bombay Exhibition Centre"
            location_address="Goregaon East, Mumbai"
            description="Visit our booth at India's largest gifting fair"
            url="https://hoovale.com/events/igfe-2026/" %}
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": name,
        "startDate": start_date,
        "endDate": end_date,
        "description": description,
        "location": {
            "@type": "Place",
            "name": location_name,
            "address": location_address
        },
        "organizer": {
            "@type": "Organization",
            "name": "HOOVALE",
            "url": "https://hoovale.com"
        },
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    }
    
    if url:
        schema["url"] = url
    
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>'
    )


# ============================================================================
# DOCUMENTATION
# ============================================================================
"""
INSTALLATION:

1. Place this file at: products/templatetags/advanced_schema.py
2. Ensure products/templatetags/__init__.py exists (Phase 1 already has this)
3. Restart Django

USAGE EXAMPLES:

In base.html (site-wide):
    {% load advanced_schema %}
    {% speakable_schema ".direct-answer,.summary,.faq-answer" %}
    {% contact_point_schema %}

In home.html:
    {% load advanced_schema %}
    {% aggregate_rating_schema avg_rating=4.7 total_reviews=150 %}
    {% person_schema name="Founder Name" job_title="Founder" organization="HOOVALE" %}

In product_detail.html:
    {% load advanced_schema %}
    {% enhanced_product_schema product %}
    {% image_schema product.image.url product.name product.description %}

In blog_detail.html:
    {% load advanced_schema %}
    {% article_schema blog %}
    {% speakable_schema ".direct-answer,.tldr" %}

In service_page.html:
    {% load advanced_schema %}
    {% service_schema service %}

In testimonials section:
    {% load advanced_schema %}
    {% for testimonial in testimonials %}
        {% review_schema testimonial %}
    {% endfor %}

IN HOWTO ARTICLES:
    {% howto_schema 
        name="How to Order Bulk Wall Clocks from HOOVALE"
        description="Step-by-step guide..."
        total_time="PT7D"
        steps=order_steps %}

VALIDATION:
After deploying, validate with:
1. Google Rich Results Test: https://search.google.com/test/rich-results
2. Schema.org Validator: https://validator.schema.org/
3. JSON-LD Playground: https://json-ld.org/playground/

EXPECTED IMPACT:
- Better AI Overview citation rates (within 3-6 months)
- Improved rich snippets in search results
- Better understanding by ChatGPT/Perplexity/Claude when they crawl
- Enhanced Knowledge Graph entries over time
- Voice search compatibility (Google Assistant, Alexa)

COMMON MISTAKES TO AVOID:
1. Fake review counts in aggregate rating (gets you penalized)
2. Inconsistent NAP across schemas
3. Schema for content that doesn't exist on page (gets flagged)
4. Multiple schemas of same type on one page
5. Outdated information (dates, prices) in schema
"""
