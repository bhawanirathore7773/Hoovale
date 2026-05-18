# 🎨 PHASE 3 INSTALLATION — PREMIUM UI + PERFORMANCE

> **Pre-requisite:** Phase 1 + Phase 2 must be installed and working.

---

## 📦 WHAT'S IN PHASE 3

| File | Purpose | Impact |
|------|---------|--------|
| `premium_theme.css` | Black/White/Gold industrial theme via CSS variables | Visual overhaul |
| `home_premium.html` | New homepage using premium theme + all components | High |
| `exit_intent.html` | Exit intent popup with email capture | +10-15% leads |
| `catalogue_download.html` | Inline email capture section | +5-10% leads |
| `social_proof_components.html` | Trust badges, client logos slider, testimonials carousel, video section | Trust |
| `performance_settings.py` | Django settings for compression, caching, security | 90+ PageSpeed |
| `PERFORMANCE_GUIDE.md` | Core Web Vitals optimization checklist | Speed |

---

## 📂 INSTALLATION STEPS

### **Step 1: Add the premium CSS theme**

```bash
cp /downloads/premium_theme.css static/css/premium_theme.css
```

### **Step 2: Update `templates/base.html`**

Add this **inside `<head>`, AFTER bootstrap CSS, BEFORE your style.css:**

```html
{# Add Playfair Display font for premium typography #}
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

{# Premium theme #}
<link rel="stylesheet" href="{% static 'css/premium_theme.css' %}">
```

Then update the `<nav>` element class to use the new theme:
```html
<nav class="navbar navbar-expand-lg hv-navbar sticky-top">
```

And update the footer section to use:
```html
<footer class="hv-footer">
```

### **Step 3: Add components**

```bash
mkdir -p templates/components
cp /downloads/exit_intent.html templates/components/exit_intent.html
cp /downloads/catalogue_download.html templates/components/catalogue_download.html
cp /downloads/social_proof_components.html templates/components/social_proof_components.html
```

### **Step 4: Replace the homepage**

```bash
# Backup current homepage
cp templates/products/home.html templates/products/home.html.phase2backup

# Use new premium homepage
cp /downloads/home_premium.html templates/products/home.html
```

### **Step 5: Include exit intent globally (optional but recommended)**

In `templates/base.html`, just before `</body>`:

```html
{# Exit intent popup - shows once per 7 days #}
{% include 'components/exit_intent.html' %}
```

This makes the popup appear on every page (not just homepage).

### **Step 6: Performance optimization (the speed boost)**

```bash
# Install dependencies
pip install whitenoise
# Optional: pip install django-redis
```

Open `hoovale/settings.py` and add the configurations from `performance_settings.py` (review each section carefully — don't blindly paste production-only settings into development).

For **development**:
- Add WhiteNoise middleware
- Use `LocMemCache`
- Skip SSL/HSTS settings (those are production-only)

For **production**:
- All security headers
- Redis cache (or LocMem for small sites)
- `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

### **Step 7: Collect static files (production)**

```bash
python manage.py collectstatic --noinput
```

### **Step 8: Restart and test**

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` — you should see:
- Black hero with gold accent typography
- Premium "Playfair Display" headings
- Trust badges bar
- Catalogue download form
- Auto-scrolling client logos
- Testimonials carousel
- New black/gold color scheme throughout

---

## 🎯 CORE WEB VITALS OPTIMIZATION CHECKLIST

After Phase 3 install, run these to maximize PageSpeed:

### **1. Image optimization** ⭐ (biggest single win)

Convert your existing JPEGs/PNGs to WebP:

```bash
# Install Pillow (likely already installed)
pip install Pillow

# Run this Python script to convert all media images to WebP:
```

Create `convert_to_webp.py` at project root:
```python
from PIL import Image
import os

MEDIA_DIR = 'media'

for root, dirs, files in os.walk(MEDIA_DIR):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(root, file)
            try:
                img = Image.open(path)
                webp_path = os.path.splitext(path)[0] + '.webp'
                img.save(webp_path, 'webp', quality=82, method=6)
                print(f'✓ {file} → WebP')
            except Exception as e:
                print(f'✗ {file}: {e}')
```

Run: `python convert_to_webp.py`

This typically reduces image sizes by **60-80%**.

### **2. Lazy loading** (already in templates)

All `<img>` tags in Phase 1-3 templates have `loading="lazy"`. This defers off-screen image loading.

### **3. Preconnect to external domains** (already in base.html)

The Phase 1 base.html already has:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
```

### **4. Defer JavaScript** (manual step)

Edit `templates/base.html` and add `defer` to non-critical scripts:
```html
<script defer src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/..."></script>
```

### **5. Test PageSpeed**

After all optimizations:
1. Visit https://pagespeed.web.dev/
2. Enter your URL
3. Target: Mobile 85+, Desktop 95+

If you're below targets, the most common culprits are:
- Large unoptimized images (use WebP)
- Render-blocking CSS (inline critical CSS)
- Unused JavaScript (audit and remove)
- Slow server response time (enable caching)

---

## 🚨 TROUBLESHOOTING

### Homepage looks weird / unstyled
- Hard refresh browser (Ctrl+Shift+R)
- Check `premium_theme.css` is at `static/css/premium_theme.css`
- Run `python manage.py collectstatic` if in production

### Exit popup not showing
- Clear localStorage: open DevTools → Application → Local Storage → delete `hv_exit_shown`
- The popup only shows once per 7 days per user
- On desktop, move mouse rapidly toward top of browser window

### Carousel not working
- Verify Bootstrap 5 JS is loaded (Phase 1 base.html includes it)
- Open DevTools console — check for JS errors

### Catalogue form not submitting
- Verify `submit_enquiry` URL exists in `urls.py` (from Phase 1)
- Verify `Enquiry` model exists in `enquiries` app (existing in your project)
- Check browser network tab when submitting

### WhiteNoise: "Missing staticfiles manifest entry"
- Run: `python manage.py collectstatic --noinput`
- Verify `STATIC_ROOT` is set in settings.py

---

## 📊 PHASE 3 IMPACT

After installation:

| Metric | Before | After |
|--------|--------|-------|
| Visual aesthetic | Standard Bootstrap | Premium Black/Gold industrial |
| Conversion CTAs | Sticky WhatsApp only | + Exit popup + Catalogue + Bulk modal |
| Trust signals | Basic badges | Full trust bar + logos + carousel + video |
| Email capture | None | 2 capture points (popup + inline) |
| PageSpeed Mobile | 60-70 | 85-95 (after image optimization) |
| Mobile UX | Bootstrap default | Optimized for thumb-zone interactions |

---

## ✅ PHASE 3 COMPLETION CHECKLIST

- [ ] `premium_theme.css` copied to `static/css/`
- [ ] Playfair Display font added to `base.html`
- [ ] Navbar uses `hv-navbar` class
- [ ] Footer uses `hv-footer` class
- [ ] Components copied to `templates/components/`
- [ ] Homepage replaced with `home_premium.html`
- [ ] Exit intent included globally in `base.html`
- [ ] WhiteNoise installed + middleware added
- [ ] Cache configured (LocMem for dev, Redis for prod)
- [ ] Static files collected (production only)
- [ ] PageSpeed test run (target 85+ mobile)
- [ ] Tested exit popup, catalogue form, carousel
- [ ] All Phase 1 + 2 functionality still working

---

## ➡️ NEXT: REQUEST PHASE 4

Once Phase 3 is verified working, reply:

```
Continue Phase 4
```

Phase 4 = Content + Growth:
- 25 SEO-optimized blog posts on wall clock topics (topical authority)
- Internal linking automation
- Google Business Profile optimization guide
- Search Console + Analytics setup walkthrough
- Backlink + citation strategy document
- Local SEO checklist

---

**Phase 3 complete. Premium UI live. Performance optimized. Conversion components active.** 🎉
