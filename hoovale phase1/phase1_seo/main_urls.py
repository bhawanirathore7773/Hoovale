"""
HOOVALE Project URLs (hoovale/urls.py)
Phase 1: Adds sitemap framework
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sitemap framework — Google Search Console will crawl this
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # App URLs
    path('', include('products.urls')),
    path('', include('enquiries.urls')),
]

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'products.views.page_not_found'
handler500 = 'products.views.server_error'
