# 🚀 PHASE 1 INSTALLATION GUIDE

## 📋 PRE-INSTALL CHECK

Before starting:
- ✅ You have your existing `hoovale_project` Django code working
- ✅ You can run `python manage.py runserver` and see the site
- ✅ You have admin credentials

---

## 📂 FILE-BY-FILE INSTALLATION

### **Step 1: Update `products/models.py`**
**Action:** Replace your current file completely

```bash
# Backup first
cp products/models.py products/models.py.backup

# Replace
cp /downloads/models.py products/models.py
```

This adds: `CityPage`, `IndustryPage`, `ServicePage`, `FAQ`, `Testimonial`, `Banner`, `SiteSettings` models.

---

### **Step 2: Create `products/templatetags/seo_tags.py`**

```bash
# Create folder if missing
mkdir -p products/templatetags
touch products/templatetags/__init__.py

# Add the file
cp /downloads/seo_tags.py products/templatetags/seo_tags.py
```

This is the **biggest SEO win** — generates all schema markup.

---

### **Step 3: Add `products/sitemaps.py`**

```bash
cp /downloads/sitemaps.py products/sitemaps.py
```

Generates dynamic XML sitemap automatically.

---

### **Step 4: Replace `products/admin.py`**

```bash
cp products/admin.py products/admin.py.backup
cp /downloads/admin.py products/admin.py
```

Rich admin interface for all new models.

---

### **Step 5: Replace `products/views.py`**

```bash
cp products/views.py products/views.py.backup
cp /downloads/views.py products/views.py
```

---

### **Step 6: Replace `products/urls.py`**

```bash
cp products/urls.py products/urls.py.backup
cp /downloads/urls.py products/urls.py
```

Adds URL patterns for cities, industries, services.

---

### **Step 7: Update main `hoovale/urls.py`**

```bash
cp hoovale/urls.py hoovale/urls.py.backup
cp /downloads/main_urls.py hoovale/urls.py
```

Registers Django's sitemap framework.

---

### **Step 8: Replace `templates/base.html`**

```bash
cp templates/base.html templates/base.html.backup
cp /downloads/base.html templates/base.html
```

Complete SEO meta-tag system + sticky CTAs included.

---

### **Step 9: Add `templates/components/sticky_ctas.html`**

```bash
mkdir -p templates/components
cp /downloads/sticky_ctas.html templates/components/sticky_ctas.html
```

---

### **Step 10: Add `templates/products/city_landing.html`**

```bash
cp /downloads/city_landing.html templates/products/city_landing.html
```

---

### **Step 11: Replace `templates/products/home.html`**

```bash
cp templates/products/home.html templates/products/home.html.backup
cp /downloads/home.html templates/products/home.html
```

---

## 🗄️ DATABASE MIGRATION

```bash
# Create migration for new models
python manage.py makemigrations

# You should see:
# - Create model SiteSettings
# - Create model CityPage
# - Create model IndustryPage
# - Create model ServicePage
# - Create model FAQ
# - Create model Testimonial
# - Create model Banner
# - Add fields to Product, Category

# Apply migrations
python manage.py migrate
```

---

## ⚙️ INITIAL SETUP (5 minutes)

### **Step A: Configure Site Settings**

1. Run: `python manage.py runserver`
2. Visit: `http://localhost:8000/admin/`
3. Click: **Site Settings → Add Site Settings**
4. Fill in:
   - Business name: `HOOVALE`
   - Phone: `+919462207356`
   - WhatsApp: `919462207356` (no + or -)
   - Email: your email
   - Street address: full address
   - GST number: your GST
   - Latitude/Longitude: your factory coords (Google "Jaipur lat lng")
5. Save

### **Step B: Add 1 Test City Page**

1. Admin → **City Landing Pages → Add City**
2. Fill in:
   - City name: `Delhi`
   - Page type: `Supplier`
   - H1 heading: `Wall Clock Supplier in Delhi`
   - Hero subheading: `Direct factory pricing for Delhi-based retailers, distributors and corporate buyers.`
   - Intro content: 200 words about supplying Delhi
   - Why choose content: 200 words
   - Services content: 200 words
   - Delivery content: 100 words
   - Industries content: 200 words
   - Closing content: 50 words
3. Save

### **Step C: Add 1 Industry Page**

1. Admin → **Industry Pages → Add**
2. Fill in: `Corporate Offices`, content, etc.

### **Step D: Add 5 FAQs**

1. Admin → **FAQs → Add**
2. Examples:
   - "What is your minimum order quantity?" / "Our MOQ is 5 pieces..."
   - "Do you offer custom logo printing?" / "Yes, free on bulk orders..."
   - "How long does delivery take?" / "3-7 business days across India..."
   - Set scope to `global`

### **Step E: Add 3 Testimonials**

1. Admin → **Testimonials → Add**
2. Real or representative reviews

### **Step F: Add 1 Banner (Optional)**

If you want a hero banner instead of the default gradient:
1. Admin → **Homepage Banners → Add**
2. Upload 1920×600 image, fill content

---

## ✅ TESTING

### Test 1: Homepage
Visit `http://localhost:8000/` — should see:
- Premium hero section
- Trust strip
- Categories
- Featured products
- Industries served (if you added them)
- Cities (if you added them)
- Testimonials
- FAQ
- Sticky WhatsApp + Call buttons (bottom right)

### Test 2: City Page
Visit `http://localhost:8000/wall-clock-supplier-in-delhi/`

### Test 3: Sitemap
Visit `http://localhost:8000/sitemap.xml`
- Should show all your URLs in XML

### Test 4: Robots.txt
Visit `http://localhost:8000/robots.txt`

### Test 5: Schema Markup
1. Right-click homepage → View Source
2. Search for `application/ld+json`
3. Should see multiple schema blocks (Organization, LocalBusiness, FAQPage, etc.)
4. Test at: https://search.google.com/test/rich-results

### Test 6: Mobile View
Resize browser to <768px:
- Sticky CTAs become bottom bar (Call + WhatsApp)
- Layout stays clean

---

## 🚨 TROUBLESHOOTING

### "Template tag library 'seo_tags' not found"
- Verify file is at: `products/templatetags/seo_tags.py`
- Verify `products/templatetags/__init__.py` exists (empty file)
- Restart server

### "SiteSettings does not exist"
- Visit `/admin/` and add a SiteSettings record
- Or run: `python manage.py shell` → `from products.models import SiteSettings; SiteSettings.load()`

### "Sticky CTA not appearing"
- Check `templates/components/sticky_ctas.html` exists
- Hard refresh browser (Ctrl+Shift+R)

### Migrations failing
```bash
# If you get conflicts:
python manage.py migrate --run-syncdb
```

### Sitemap empty
- Add at least 1 product, 1 category, 1 city page
- Visit `/sitemap.xml` again

---

## 📊 WHAT YOU'VE GAINED

After Phase 1 installation:

| Feature | Status |
|---------|--------|
| LocalBusiness schema | ✅ Live on every page |
| Organization schema | ✅ Live |
| Product schema (rich snippets) | ✅ Ready (renders on product pages) |
| FAQ schema | ✅ Live wherever FAQs render |
| Aggregate Rating schema | ✅ Live (homepage from testimonials) |
| Breadcrumb schema | ✅ Ready |
| Dynamic XML sitemap | ✅ /sitemap.xml |
| Robots.txt | ✅ /robots.txt |
| Open Graph tags | ✅ All pages |
| Twitter cards | ✅ All pages |
| Canonical URLs | ✅ All pages |
| Geo meta tags | ✅ All pages |
| Sticky WhatsApp button | ✅ All pages |
| Sticky Call button | ✅ All pages |
| Mobile bottom CTA bar | ✅ Mobile-only |
| City landing page system | ✅ Add unlimited cities from admin |
| Industry page system | ✅ Add unlimited from admin |
| Service page system | ✅ Add unlimited from admin |
| Testimonial system | ✅ With auto rating schema |
| FAQ system | ✅ With auto FAQ schema |
| Site Settings (centralized) | ✅ All contact info from one place |

---

## ➡️ NEXT: REQUEST PHASE 2

Once everything works, reply:

```
Continue Phase 2: Content Pages
```

I'll then build:
- 14 product category pages with unique content
- 8 city landing pages with full 1500+ word SEO content (Delhi, Mumbai, Bangalore, Chennai, Hyderabad, Pune, Ahmedabad, Kolkata)
- 6 industry pages (Corporate, Hotels, Schools, Hospitals, Retail, Offices)
- 5 service pages (OEM, Bulk, Customization, Promotional, Distributor)
- About Us page with EEAT signals
- Contact page with map embed
- FAQ page (full 20+ questions)
- Quick Quote / Bulk Inquiry forms

---

## 💡 PRO TIPS

1. **Submit sitemap to Google immediately** — Search Console → Sitemaps → add `https://yourdomain.com/sitemap.xml`
2. **Set up Google Business Profile** for Jaipur — boosts local SEO 10x
3. **Add real testimonials with names/companies** — Google trusts real reviews
4. **Don't keyword stuff** — write naturally; the schema does the SEO heavy lifting
5. **Update Site Settings GST + address** — appears in LocalBusiness schema = trust signal

---

**Phase 1 done. Foundation laid. Ready for Phase 2 when you are.** 🚀
