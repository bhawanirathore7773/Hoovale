from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from products.models import (
    Product, Category, Blog, CityPage, IndustryPage,
    ServicePage, FAQ, Testimonial, Banner, SiteSettings,
    PricingTierTemplate,
)
from enquiries.models import Enquiry


def dashboard_callback(request, context):
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    User = get_user_model()

    context.update({
        "dashboard": {
            "products": Product.objects.count(),
            "active_products": Product.objects.filter(is_active=True).count(),
            "categories": Category.objects.count(),
            "enquiries": Enquiry.objects.count(),
            "new_enquiries": Enquiry.objects.filter(status="new").count(),
            "published_blogs": Blog.objects.filter(is_published=True).count(),
            "city_pages": CityPage.objects.filter(is_published=True).count(),
            "industry_pages": IndustryPage.objects.filter(is_published=True).count(),
            "services": ServicePage.objects.filter(is_published=True).count(),
            "faqs": FAQ.objects.filter(is_active=True).count(),
            "testimonials": Testimonial.objects.filter(is_active=True).count(),
            "banners": Banner.objects.filter(is_active=True).count(),
            "users": User.objects.count(),
            "site_settings": SiteSettings.objects.exists(),
            "pricing_templates": PricingTierTemplate.objects.filter(is_active=True).count(),
            "monthly_enquiries": Enquiry.objects.filter(created_at__gte=month_start).count(),
        },
        "recent_enquiries": Enquiry.objects.select_related("product").order_by("-created_at")[:8],
        "recent_products": Product.objects.select_related("category").order_by("-created_at")[:6],
        "recent_blogs": Blog.objects.order_by("-created_at")[:5],
        "new_enquiries": Enquiry.objects.filter(status="new").order_by("-created_at")[:5],
    })

    return context
