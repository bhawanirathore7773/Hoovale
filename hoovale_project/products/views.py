"""
HOOVALE Views - Phase 1 SEO Foundation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import (
    Product, Category, Blog, CityPage, IndustryPage,
    ServicePage, FAQ, Testimonial, Banner, SiteSettings
)


# ============================================================
# HOMEPAGE
# ============================================================
def home(request):
    site = SiteSettings.load()
    website_banners = Banner.objects.filter(is_active=True, banner_type='website').order_by('order')
    mobile_banners = Banner.objects.filter(is_active=True, banner_type='mobile').order_by('order')
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = Category.objects.filter(is_featured=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:6]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'home'])[:8]
    industries = IndustryPage.objects.filter(is_published=True)[:6]
    cities = CityPage.objects.filter(is_published=True)[:8]
    latest_blogs = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]

    context = {
        'site': site,
        'website_banners': website_banners,
        'mobile_banners': mobile_banners,
        'featured_products': featured_products,
        'categories': categories,
        'testimonials': testimonials,
        'faqs': faqs,
        'industries': industries,
        'cities': cities,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'products/home.html', context)


# ============================================================
# PRODUCTS
# ============================================================
def products_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    selected_category = request.GET.get('category', '')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)

    context = {
        'products': products_page,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'current_page': int(page_number) if str(page_number).isdigit() else 1,
        'total_pages': paginator.num_pages,
    }
    return render(request, 'products/products_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'product'])[:6]
  

    specifications = []

    if product.specifications:
        for line in product.specifications.splitlines():

            if ":" in line:
                key, value = line.split(":", 1)

                specifications.append({
                    "key": key.strip(),
                    "value": value.strip()
                })


    context = {
        'product': product,
        'related_products': related_products,
        "specifications": specifications,
        'faqs': faqs,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Products', '/products/'),
            (product.category.name, product.category.get_absolute_url()),
            (product.name, None),
        ],
    }
    return render(request, 'products/product_detail.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': products_page,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Products', '/products/'),
            (category.name, None),
        ],
    }
    return render(request, 'products/category_detail.html', context)


# ============================================================
# CITY LANDING PAGES (Programmatic SEO)
# ============================================================
def city_landing(request, slug):
    city = get_object_or_404(CityPage, slug=slug, is_published=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'city'])[:6]

    # Static benefits for the cards section
    benefits = [
        {'icon': 'fas fa-industry', 'title': 'Direct Factory', 'desc': 'No middlemen — best wholesale prices'},
        {'icon': 'fas fa-truck-fast', 'title': 'Fast Delivery', 'desc': f'{city.delivery_time} to {city.city_name}'},
        {'icon': 'fas fa-paint-brush', 'title': 'Custom Logo', 'desc': 'Branded clocks with your logo'},
        {'icon': 'fas fa-shield-alt', 'title': 'Quality Assured', 'desc': '1 year warranty on all products'},
    ]

    context = {
        'city': city,
        'featured_products': featured_products,
        'faqs': faqs,
        'benefits': benefits,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Locations', '/locations/'),
            (city.h1_heading, None),
        ],
    }
    return render(request, 'products/city_landing.html', context)


def cities_index(request):
    """Index page listing all city landing pages."""
    cities = CityPage.objects.filter(is_published=True).order_by('display_order', 'city_name')
    return render(request, 'products/cities_index.html', {'cities': cities})


# ============================================================
# INDUSTRY PAGES
# ============================================================
def industry_page(request, slug):
    industry = get_object_or_404(IndustryPage, slug=slug, is_published=True)
    products = industry.featured_products.filter(is_active=True)[:8]
    if not products.exists():
        products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'industry'])[:6]

    context = {
        'industry': industry,
        'products': products,
        'faqs': faqs,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Industries', '/industries/'),
            (industry.industry_name, None),
        ],
    }
    return render(request, 'products/industry_page.html', context)


def industries_index(request):
    industries = IndustryPage.objects.filter(is_published=True).order_by('display_order', 'industry_name')
    return render(request, 'products/industries_index.html', {'industries': industries})


# ============================================================
# SERVICE PAGES
# ============================================================
def service_page(request, slug):
    service = get_object_or_404(ServicePage, slug=slug, is_published=True)
    related_services = ServicePage.objects.filter(is_published=True).exclude(id=service.id)[:4]

    context = {
        'service': service,
        'related_services': related_services,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Services', '/services/'),
            (service.name, None),
        ],
    }
    return render(request, 'products/service_page.html', context)


def services_index(request):
    services = ServicePage.objects.filter(is_published=True).order_by('display_order', 'name')
    return render(request, 'products/services_index.html', {'services': services})


# ============================================================
# BLOG
# ============================================================
def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page_number)
    return render(request, 'products/blog_list.html', {
        'blogs': blogs_page,
        'current_page': int(page_number) if str(page_number).isdigit() else 1,
        'total_pages': paginator.num_pages,
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    related_blogs = Blog.objects.filter(is_published=True).exclude(id=blog.id)[:3]
    return render(request, 'products/blog_detail.html', {
        'blog': blog, 'related_blogs': related_blogs,
    })


# ============================================================
# STATIC PAGES
# ============================================================
def about(request):
    site = SiteSettings.load()
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    return render(request, 'products/about.html', {'site': site, 'testimonials': testimonials})


def contact(request):
    site = SiteSettings.load()
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'contact'])[:6]
    return render(request, 'products/contact.html', {'site': site, 'faqs': faqs})


# ============================================================
# ROBOTS.TXT
# ============================================================
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "",
        "Sitemap: https://hoovale.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ============================================================
# ENQUIRY (Existing — kept compatible)
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def submit_enquiry(request):
    try:
        from enquiries.models import Enquiry
        product_id = request.POST.get('product_id')
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, phone, city, message]):
            return JsonResponse({'success': False, 'error': 'Please fill all required fields'}, status=400)

        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

        enquiry = Enquiry.objects.create(
            product=product, name=name, phone=phone, email=email,
            city=city, message=message, status='new'
        )
        return JsonResponse({'success': True, 'message': 'Enquiry submitted!', 'enquiry_id': enquiry.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# ERROR HANDLERS
# ============================================================
def page_not_found(request, exception):
    return render(request, 'products/404.html', status=404)


def server_error(request):
    return render(request, 'products/500.html', status=500)
