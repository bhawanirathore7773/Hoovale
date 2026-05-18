"""
HOOVALE Performance Settings
============================
Add these to your settings.py for major Core Web Vitals improvements.

Estimated impact:
- PageSpeed Mobile: 60-70 → 85-95
- LCP (Largest Contentful Paint): 4-6s → 1.5-2.5s
- TBT (Total Blocking Time): 800ms → <200ms
"""

# ============================================================
# 1. WHITENOISE — Compressed static files (HUGE speed boost)
# ============================================================
"""
Install:
    pip install whitenoise

Then in settings.py:
"""

# Add to MIDDLEWARE (right after SecurityMiddleware):
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← ADD THIS
    # ... rest of your middleware
]

# Add at bottom of settings.py:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# This automatically:
# - Gzips/Brotli compresses static files
# - Adds far-future cache headers
# - Hashes filenames for cache busting


# ============================================================
# 2. CACHING — Database query caching
# ============================================================
"""
Install:
    pip install django-redis  (or use local memory for testing)
"""

# For production (Redis):
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 60 * 15,  # 15 minutes default
    }
}

# For development / small sites (in-memory):
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'hoovale-cache',
        'TIMEOUT': 60 * 15,
    }
}

# Cache key prefix to avoid collisions across deployments
CACHE_MIDDLEWARE_KEY_PREFIX = 'hoovale'
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # Cache pages 15 minutes


# ============================================================
# 3. SESSION OPTIMIZATION
# ============================================================
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days


# ============================================================
# 4. SECURITY HEADERS (also helps SEO trust)
# ============================================================
SECURE_SSL_REDIRECT = True  # Force HTTPS in production
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'same-origin'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# ============================================================
# 5. DATABASE OPTIMIZATION
# ============================================================
# Persistent connections (avoid connection overhead)
DATABASES = {
    'default': {
        # ... your existing config ...
        'CONN_MAX_AGE': 600,  # 10 minutes
        'CONN_HEALTH_CHECKS': True,
    }
}


# ============================================================
# 6. STATIC + MEDIA FILES
# ============================================================
import os
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For collectstatic
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise serves static files in production - no separate config needed
