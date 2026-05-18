"""
HOOVALE Admin Configuration
Phase 1: All SEO models registered with rich admin interfaces
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, Blog, CityPage, IndustryPage,
    ServicePage, FAQ, Testimonial, Banner, SiteSettings
)


# ============================================================
# CATEGORY
# ============================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'is_featured', 'display_order']
    list_filter = ['is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'display_order']
    fieldsets = (
        ('Basic', {'fields': ('name', 'slug', 'description', 'image')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords', 'h1_heading', 'seo_content'),
                 'classes': ('collapse',)}),
        ('Display', {'fields': ('is_featured', 'display_order')}),
    )

    def product_count(self, obj):
        return format_html('<strong style="color:#0051A3;">{} products</strong>', obj.products.count())
    product_count.short_description = 'Products'


# ============================================================
# PRODUCT
# ============================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'moq', 'badges', 'is_active']
    list_filter = ['category', 'is_featured', 'is_bestseller', 'is_new_arrival', 'is_active']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    fieldsets = (
        ('Basic', {'fields': ('name', 'slug', 'category', 'short_description', 'description', 'specifications')}),
        ('Pricing', {'fields': ('price', 'bulk_price', 'moq')}),
        ('Images', {'fields': ('image', 'additional_images')}),
        ('Customization', {'fields': ('size_options', 'material_options', 'color_options'),
                          'classes': ('collapse',)}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords', 'sku', 'brand', 'availability'),
                 'classes': ('collapse',)}),
        ('Open Graph', {'fields': ('og_title', 'og_description', 'og_image'),
                       'classes': ('collapse',)}),
        ('Display Flags', {'fields': ('is_featured', 'is_bestseller', 'is_new_arrival', 'is_active')}),
    )

    def badges(self, obj):
        b = []
        if obj.is_featured: b.append('<span style="background:#FFA500;color:white;padding:2px 6px;border-radius:3px;font-size:0.7rem;">⭐ FEATURED</span>')
        if obj.is_bestseller: b.append('<span style="background:#10b981;color:white;padding:2px 6px;border-radius:3px;font-size:0.7rem;">🔥 BESTSELLER</span>')
        if obj.is_new_arrival: b.append('<span style="background:#3b82f6;color:white;padding:2px 6px;border-radius:3px;font-size:0.7rem;">🆕 NEW</span>')
        return format_html(' '.join(b)) if b else '-'


# ============================================================
# CITY LANDING PAGE
# ============================================================
@admin.register(CityPage)
class CityPageAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'page_type', 'is_published', 'display_order']
    list_filter = ['page_type', 'is_published']
    search_fields = ['city_name', 'state', 'h1_heading']
    prepopulated_fields = {'slug': ('city_name',)}
    list_editable = ['is_published', 'display_order']
    fieldsets = (
        ('🏙️ City Identity', {
            'fields': ('city_name', 'slug', 'state', 'page_type'),
            'description': 'Each city = 1 SEO landing page. Add 8+ cities for maximum coverage.',
        }),
        ('🎯 Hero Section', {
            'fields': ('h1_heading', 'hero_subheading', 'hero_image'),
        }),
        ('📝 Content Sections (Total ~1500 words for ranking)', {
            'fields': ('intro_content', 'why_choose_content', 'services_content',
                      'delivery_content', 'industries_content', 'closing_content'),
            'description': 'Each section ~150-300 words. Use natural, helpful language with city name.',
        }),
        ('🔍 SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'nearby_areas', 'delivery_time'),
        }),
        ('⚙️ Display', {
            'fields': ('is_published', 'display_order'),
        }),
    )


# ============================================================
# INDUSTRY PAGE
# ============================================================
@admin.register(IndustryPage)
class IndustryPageAdmin(admin.ModelAdmin):
    list_display = ['industry_name', 'is_published', 'display_order']
    list_filter = ['is_published']
    search_fields = ['industry_name', 'h1_heading']
    prepopulated_fields = {'slug': ('industry_name',)}
    list_editable = ['is_published', 'display_order']
    filter_horizontal = ['featured_products']


# ============================================================
# SERVICE PAGE
# ============================================================
@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published', 'display_order']
    list_filter = ['is_published']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_published', 'display_order']


# ============================================================
# FAQ
# ============================================================
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'scope', 'display_order', 'is_active']
    list_filter = ['scope', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['scope', 'display_order', 'is_active']

    def question_short(self, obj):
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
    question_short.short_description = 'Question'


# ============================================================
# TESTIMONIAL
# ============================================================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_designation', 'stars', 'is_featured', 'is_active']
    list_filter = ['rating', 'is_featured', 'is_active']
    search_fields = ['customer_name', 'review_content']
    list_editable = ['is_featured', 'is_active']

    def stars(self, obj):
        return format_html('<span style="color:#FFA500;">{}</span>', '★' * obj.rating)


# ============================================================
# BANNER (Homepage Carousel)
# ============================================================
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type_icon', 'order', 'is_active', 'preview']
    list_filter = ['banner_type', 'is_active']
    list_editable = ['order', 'is_active']

    def banner_type_icon(self, obj):
        icon = '💻' if obj.banner_type == 'website' else '📱'
        return f"{icon} {obj.get_banner_type_display()}"
    banner_type_icon.short_description = 'Type'

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:120px; border-radius:4px;">', obj.image.url)
        return '-'


# ============================================================
# SITE SETTINGS (Singleton — only 1 record)
# ============================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Business Identity', {
            'fields': ('business_name', 'tagline', 'establishment_year', 'employee_count', 'gst_number'),
        }),
        ('Contact (CRITICAL — appears everywhere)', {
            'fields': ('primary_phone', 'whatsapp_number', 'email'),
            'description': 'These are used in sticky CTAs, footer, schema markup. WhatsApp format: 91XXXXXXXXXX',
        }),
        ('Address (LocalBusiness Schema)', {
            'fields': ('street_address', 'locality', 'region', 'postal_code', 'country', 'latitude', 'longitude'),
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'linkedin_url'),
            'classes': ('collapse',),
        }),
        ('Default SEO', {
            'fields': ('default_meta_title', 'default_meta_description'),
        }),
        ('Search Engine Verification', {
            'fields': ('google_verification', 'bing_verification'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        # Singleton — prevent adding more than 1
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================
# BLOG
# ============================================================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'created_at']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']


# ============================================================
# Customize admin site
# ============================================================
admin.site.site_header = "🕐 HOOVALE Admin"
admin.site.site_title = "HOOVALE - Wall Clock Manufacturer"
admin.site.index_title = "SEO + Content Management"
