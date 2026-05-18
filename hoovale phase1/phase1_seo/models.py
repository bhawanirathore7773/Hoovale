"""
HOOVALE Wall Clock Manufacturer - SEO-Optimized Models
Phase 1: SEO Foundation
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import strip_tags


# ============================================================
# 1. CATEGORY (Existing - enhanced)
# ============================================================
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    h1_heading = models.CharField(max_length=200, blank=True, help_text="If empty, uses category name")
    seo_content = models.TextField(blank=True, help_text="800+ word SEO content for category page")

    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} Manufacturer & Supplier in Jaipur | HOOVALE"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_products', kwargs={'slug': self.slug})


# ============================================================
# 2. PRODUCT (Existing - enhanced for SEO)
# ============================================================
class Product(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    # Content
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    specifications = models.TextField(blank=True, help_text="One per line: 'Key: Value'")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bulk_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                     help_text="Discounted price for bulk orders")
    moq = models.PositiveIntegerField(default=1, help_text="Minimum Order Quantity")

    # Images
    image = models.ImageField(upload_to='products/')
    additional_images = models.JSONField(default=list, blank=True)

    # Customization
    size_options = models.JSONField(default=list, blank=True)
    material_options = models.JSONField(default=list, blank=True)
    color_options = models.JSONField(default=list, blank=True)

    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    # Open Graph
    og_title = models.CharField(max_length=100, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)

    # Schema.org product fields
    brand = models.CharField(max_length=100, default='HOOVALE')
    sku = models.CharField(max_length=50, blank=True)
    availability = models.CharField(max_length=30, default='InStock',
                                   choices=[('InStock','In Stock'),('OutOfStock','Out of Stock'),('PreOrder','Pre Order')])

    # Display flags
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} | Wholesale Wall Clock Manufacturer Jaipur"
        if not self.meta_description:
            clean = strip_tags(self.description)[:155]
            self.meta_description = f"{clean}..."
        if not self.sku:
            self.sku = f"HV-{self.id or 'NEW'}-{slugify(self.name)[:10].upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        return self.image.url if self.image else '/static/images/placeholder.jpg'


# ============================================================
# 3. CITY LANDING PAGE (NEW — Programmatic SEO)
# ============================================================
class CityPage(models.Model):
    """
    One model = unlimited city landing pages.
    URL: /wall-clock-supplier-in-{city-slug}/
    """
    city_name = models.CharField(max_length=100, unique=True, help_text="e.g., Delhi, Mumbai, Bangalore")
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated from city name")
    state = models.CharField(max_length=100, blank=True)

    # Page type (controls URL pattern + content tone)
    PAGE_TYPE_CHOICES = [
        ('manufacturer', 'Manufacturer in [City]'),
        ('supplier', 'Supplier in [City]'),
        ('wholesaler', 'Wholesaler in [City]'),
    ]
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='supplier')

    # Hero section
    h1_heading = models.CharField(max_length=200, help_text="e.g., 'Wall Clock Supplier in Delhi'")
    hero_subheading = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='city_pages/', blank=True, null=True)

    # Content (each section ~150-300 words for ~1500 word total page)
    intro_content = models.TextField(help_text="Opening section: who you serve in this city")
    why_choose_content = models.TextField(blank=True, help_text="Why choose HOOVALE for this city")
    services_content = models.TextField(blank=True, help_text="Services offered to this city")
    delivery_content = models.TextField(blank=True, help_text="Delivery info to this city")
    industries_content = models.TextField(blank=True, help_text="Industries served in this city")
    closing_content = models.TextField(blank=True, help_text="Final CTA paragraph")

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=400, blank=True,
                                    help_text="Comma-separated, e.g., 'wall clock supplier delhi, ...'")

    # Local relevance
    nearby_areas = models.TextField(blank=True, help_text="Comma-separated nearby areas/pincodes")
    delivery_time = models.CharField(max_length=50, blank=True, default='3-5 business days')

    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'city_name']
        verbose_name = 'City Landing Page'
        verbose_name_plural = 'City Landing Pages (SEO)'

    def __str__(self):
        return f"Wall Clock {self.get_page_type_display()} {self.city_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.city_name)
        if not self.meta_title:
            self.meta_title = f"Wall Clock {self.get_page_type_display().split(' in')[0]} in {self.city_name} | HOOVALE Jaipur"
        if not self.meta_description:
            self.meta_description = (
                f"Top wall clock {self.page_type} in {self.city_name}. "
                f"Bulk orders, custom logo printing, fast delivery from Jaipur. "
                f"Call/WhatsApp for wholesale prices."
            )[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('city_landing', kwargs={'slug': self.slug})


# ============================================================
# 4. INDUSTRY PAGE (NEW — Vertical SEO)
# ============================================================
class IndustryPage(models.Model):
    """
    Industry-specific landing pages.
    URL: /wall-clocks-for-{industry-slug}/
    Examples: corporate offices, hotels, hospitals, schools, retail
    """
    industry_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="FontAwesome class, e.g., 'fa-building'")

    # Hero
    h1_heading = models.CharField(max_length=200)
    hero_subheading = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='industries/', blank=True, null=True)

    # Content
    intro_content = models.TextField()
    benefits_content = models.TextField(blank=True)
    customization_content = models.TextField(blank=True)
    case_study_content = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=400, blank=True)

    # Recommended products (M2M to Product)
    featured_products = models.ManyToManyField(Product, blank=True, related_name='industries')

    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'industry_name']
        verbose_name_plural = 'Industry Pages (SEO)'

    def __str__(self):
        return self.industry_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.industry_name)
        if not self.meta_title:
            self.meta_title = f"Wall Clocks for {self.industry_name} | Bulk Supplier | HOOVALE"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('industry_page', kwargs={'slug': self.slug})


# ============================================================
# 5. FAQ (NEW — for FAQ schema markup)
# ============================================================
class FAQ(models.Model):
    """
    Site-wide and page-specific FAQs.
    Renders as schema.org FAQPage markup → rich snippets in Google.
    """
    question = models.CharField(max_length=300)
    answer = models.TextField()

    # Where to display
    SCOPE_CHOICES = [
        ('global', 'Global (All Pages)'),
        ('home', 'Homepage Only'),
        ('product', 'Product Pages'),
        ('city', 'City Pages'),
        ('industry', 'Industry Pages'),
        ('contact', 'Contact Page'),
        ('about', 'About Page'),
    ]
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='global')

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scope', 'display_order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


# ============================================================
# 6. TESTIMONIAL (NEW — for Review schema)
# ============================================================
class Testimonial(models.Model):
    """Customer testimonials. Renders as schema.org Review markup."""
    customer_name = models.CharField(max_length=200)
    customer_designation = models.CharField(max_length=200, blank=True,
                                          help_text="e.g., 'Purchase Manager, ABC Hotels'")
    customer_city = models.CharField(max_length=100, blank=True)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    rating = models.PositiveSmallIntegerField(default=5,
                                            choices=[(i, str(i)) for i in range(1, 6)])
    review_title = models.CharField(max_length=200, blank=True)
    review_content = models.TextField()

    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'display_order', '-created_at']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


# ============================================================
# 7. SERVICE PAGE (NEW — OEM, Bulk, Customization etc.)
# ============================================================
class ServicePage(models.Model):
    """
    Service-specific landing pages.
    URL: /services/{slug}/
    Examples: OEM Manufacturing, Bulk Orders, Custom Logo Printing
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True)

    h1_heading = models.CharField(max_length=200)
    hero_subheading = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='services/', blank=True, null=True)

    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    process_content = models.TextField(blank=True, help_text="How the service works")
    benefits_content = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=400, blank=True)

    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Service Pages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} | Wall Clock Manufacturer Jaipur | HOOVALE"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_page', kwargs={'slug': self.slug})


# ============================================================
# 8. BANNER (NEW — Homepage carousel)
# ============================================================
class Banner(models.Model):
    """Homepage banner carousel. Separate desktop + mobile banners."""
    BANNER_TYPE_CHOICES = [
        ('website', '💻 Desktop / Website Banner'),
        ('mobile', '📱 Mobile Banner'),
    ]

    title = models.CharField(max_length=200, help_text="For admin reference")
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPE_CHOICES, default='website')
    image = models.ImageField(upload_to='banners/', help_text="Desktop: 1920×600px • Mobile: 600×800px")

    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=400, blank=True)
    cta_text = models.CharField(max_length=100, blank=True, default='Shop Now')
    cta_url = models.CharField(max_length=500, blank=True, default='/products/')

    text_color = models.CharField(max_length=7, default='#FFFFFF')
    text_position = models.CharField(max_length=20, default='center-center', choices=[
        ('top-left','Top Left'),('top-center','Top Center'),('top-right','Top Right'),
        ('center-left','Center Left'),('center-center','Center'),('center-right','Center Right'),
        ('bottom-left','Bottom Left'),('bottom-center','Bottom Center'),('bottom-right','Bottom Right'),
    ])
    overlay_opacity = models.FloatField(default=0.4, help_text="0.0 (clear) to 1.0 (black)")

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['banner_type', 'order']
        verbose_name_plural = 'Homepage Banners'

    def __str__(self):
        return f"{self.get_banner_type_display()} — {self.title}"


# ============================================================
# 9. SITE SETTINGS (NEW — Centralized config)
# ============================================================
class SiteSettings(models.Model):
    """
    Singleton model for site-wide settings.
    Phone number, WhatsApp number, address, etc. all editable from admin.
    """
    # Business identity
    business_name = models.CharField(max_length=200, default='HOOVALE')
    tagline = models.CharField(max_length=300, default='Premium Wall Clock Manufacturer in Jaipur')

    # Contact
    primary_phone = models.CharField(max_length=20, default='+919462207356')
    whatsapp_number = models.CharField(max_length=20, default='919462207356',
                                      help_text="Format: 91XXXXXXXXXX (no + or -)")
    email = models.EmailField(default='info@hoovale.com')

    # Address (for LocalBusiness schema)
    street_address = models.CharField(max_length=300, default='Jaipur, Rajasthan, India')
    locality = models.CharField(max_length=100, default='Jaipur')
    region = models.CharField(max_length=100, default='Rajasthan')
    postal_code = models.CharField(max_length=10, default='302001')
    country = models.CharField(max_length=10, default='IN')

    # Geo coordinates for LocalBusiness schema
    latitude = models.FloatField(default=26.9124)
    longitude = models.FloatField(default=75.7873)

    # Business credentials (EEAT signals)
    gst_number = models.CharField(max_length=20, blank=True, help_text="GST Number for trust")
    establishment_year = models.PositiveIntegerField(default=2010)
    employee_count = models.CharField(max_length=20, blank=True, default='10-50')

    # Social
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # SEO defaults
    default_meta_title = models.CharField(max_length=70,
        default='HOOVALE — Wall Clock Manufacturer & Supplier in Jaipur')
    default_meta_description = models.CharField(max_length=160,
        default='Leading wall clock manufacturer in Jaipur. Bulk orders, custom logo printing, OEM supply across India. Call for wholesale prices.')

    # Verification
    google_verification = models.CharField(max_length=200, blank=True)
    bing_verification = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ============================================================
# 10. BLOG (Existing — kept compatible)
# ============================================================
class Blog(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100, default='Wall Clocks')
    featured_image = models.ImageField(upload_to='blog/%Y/%m/')
    description = models.TextField(help_text="SEO optimized content")

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
