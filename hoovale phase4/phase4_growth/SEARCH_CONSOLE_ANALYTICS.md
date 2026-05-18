# 📊 GOOGLE SEARCH CONSOLE + ANALYTICS SETUP

> **Why this matters:** Without these tools, you're flying blind. Search Console tells you which keywords drive traffic. Analytics tells you what visitors do. Together they reveal exactly what's working and what isn't.

---

## 🔍 PART 1: GOOGLE SEARCH CONSOLE

Search Console is Google's free tool showing how your site performs in search results.

### Setup (15 minutes)

#### Step 1: Visit `search.google.com/search-console`
Sign in with the Gmail account you'll use long-term for SEO management.

#### Step 2: Add Property

Choose **"Domain"** property type (preferred — covers all subdomains and protocols):
- Enter: `hoovale.com`
- Verify via DNS TXT record (Google shows you the exact record to add)
- Add the TXT record in your domain registrar (GoDaddy, Namecheap, etc.)
- Wait 5-30 minutes, then click "Verify" in Search Console

Alternative: **"URL prefix"** property (only covers `https://hoovale.com`):
- Easier verification options (HTML file upload, meta tag, Google Analytics)
- Less comprehensive than Domain property

#### Step 3: Submit Sitemap

After verification:
1. Left menu → "Sitemaps"
2. Enter: `sitemap.xml` (your sitemap from Phase 1)
3. Click "Submit"
4. Wait 24-48 hours — Google starts crawling all URLs

If status shows "Couldn't fetch" — double-check `https://hoovale.com/sitemap.xml` is publicly accessible.

#### Step 4: Submit Robots.txt

1. Visit `https://hoovale.com/robots.txt` to verify it's accessible
2. Search Console → Settings → robots.txt → check if Google sees it correctly

---

### Search Console — What to Monitor Weekly

#### Performance Report (most important)

**Total clicks**: Visitors from Google search → your site
**Total impressions**: How many times your pages appeared in search results
**Average CTR**: clicks ÷ impressions (industry average 1-3%)
**Average position**: Where your pages typically rank

#### Filter by Query (keywords)

Shows exactly which keywords drive your traffic:

- **High impressions, low CTR**: pages appearing in search but not getting clicks → improve title and meta description
- **Low impressions, high position**: ranking well but few searches → keyword has low volume; consider broader terms
- **High clicks**: working well, do more of this content type
- **Position 5-15**: opportunities to push to top 3 with content updates

#### Filter by Page

Identifies which of your pages get traffic:

- City landing pages should show impressions for "wall clock supplier in [city]" queries
- Product pages should show product-specific searches
- Blog posts should show informational queries

#### Index Coverage Report

Left menu → "Pages"

**Indexed pages**: should grow to 30-50+ within 2 weeks of submitting sitemap
**Excluded pages**: review reasons — common issues:
- "Crawled but not indexed" → low quality content, needs improvement
- "Discovered, not indexed" → Google hasn't crawled yet, wait
- "Blocked by robots.txt" → check robots.txt isn't blocking important pages

#### Mobile Usability

Reports any mobile issues. Should be 0 errors after Phase 3 mobile-first overhaul.

#### Core Web Vitals

Reports LCP, FID, CLS metrics. After Phase 3 performance optimization, all should be "Good."

---

### Search Console — Power Tips

**1. Identify "almost ranking" keywords**

In Performance report, filter by Average Position 8-20. These are pages just outside top results. Update content for these keywords (improve title, add more depth, build internal links to them) and they often jump to top 3.

**2. Find "missing" keywords**

If you target "wall clock manufacturer in jaipur" but Search Console shows 0 impressions — your page isn't ranking for it. Either:
- Page isn't indexed yet (check Index Coverage)
- Content doesn't match query intent (rewrite)
- Site has no authority for it (need backlinks)

**3. Disavow toxic backlinks**

Left menu → Links → External Links. If you see spammy sites linking to you (gambling, adult content, etc.), use Disavow Tool. Most clean sites won't need this.

**4. Submit individual URLs for indexing**

For new important pages, use URL Inspection tool → "Request Indexing." Faster than waiting for natural crawl.

---

## 📈 PART 2: GOOGLE ANALYTICS 4 (GA4)

Analytics tells you what visitors do AFTER they reach your site.

### Setup (10 minutes)

#### Step 1: Create GA4 Property

1. Visit `analytics.google.com`
2. Click "Admin" (bottom left) → "Create Property"
3. Property name: HOOVALE
4. Reporting time zone: India Standard Time
5. Currency: INR
6. Industry: Manufacturing
7. Business size: choose appropriate
8. Click "Next" → "Create"

#### Step 2: Set Up Data Stream

1. Choose "Web"
2. Website URL: `https://hoovale.com`
3. Stream name: HOOVALE Website
4. Click "Create stream"
5. Copy the **Measurement ID** (looks like `G-XXXXXXXXXX`)

#### Step 3: Add GA4 to Website

In your `templates/base.html`, find the analytics block (commented out from Phase 1) and replace `G-XXXXXXX` with your actual ID, then uncomment:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-YOUR-ID');
</script>
```

Deploy. Within 1-2 hours, GA4 will start showing real-time data.

#### Step 4: Link GA4 to Search Console

In GA4 → Admin → Property settings → "Search Console links" → Link your Search Console property.

This unifies SEO data (impressions, clicks, queries) with on-site behavior (sessions, conversions).

---

### Set Up Conversions (Critical)

Track what matters for HOOVALE:

#### Conversion 1: WhatsApp Click

In your sticky_ctas.html and other WhatsApp links, add tracking:

```html
<a href="https://wa.me/919462207356?text=..."
   onclick="gtag('event', 'whatsapp_click', {'source': 'sticky_button'});">
   WhatsApp
</a>
```

#### Conversion 2: Phone Call

```html
<a href="tel:+919462207356"
   onclick="gtag('event', 'phone_call', {'source': 'sticky_button'});">
   Call Now
</a>
```

#### Conversion 3: Form Submission

In your contact form / bulk inquiry form JavaScript, after successful submission:

```javascript
gtag('event', 'form_submit', {
    'form_type': 'bulk_inquiry',  // or 'contact', 'catalogue_download'
    'source': window.location.pathname
});
```

#### Conversion 4: Catalogue Download

```javascript
// On exit popup or catalogue download form success:
gtag('event', 'catalogue_request', {
    'source': 'exit_popup'  // or 'inline_form'
});
```

#### Mark Events as Conversions

In GA4 → Admin → Events → toggle "Mark as conversion" for each:
- whatsapp_click
- phone_call
- form_submit
- catalogue_request

These now appear in conversion reports.

---

### What to Monitor in GA4

#### Daily (5 min)

- **Real-time report**: see live visitors
- **Today's sessions** vs yesterday: spot anomalies

#### Weekly (15 min)

- **Acquisition → Traffic Sources**: where visitors come from (Organic Search, Direct, Referral, Social)
- **Engagement → Pages and Screens**: most-visited pages, average engagement time
- **Conversions**: how many WhatsApp clicks, calls, form submits this week

#### Monthly (30 min)

- **Audience demographics**: where visitors come from (cities, devices)
- **User journey**: how visitors move through site before converting
- **Conversion paths**: which sources/pages drive most leads

---

### Key Metrics to Track

For HOOVALE B2B SEO:

| Metric | Target (3 months) | Target (12 months) |
|--------|------------------|-------------------|
| Monthly organic visitors | 500+ | 5000+ |
| WhatsApp clicks per month | 30+ | 200+ |
| Phone calls per month | 10+ | 80+ |
| Form submissions per month | 5+ | 50+ |
| Avg engagement time | 1 min+ | 2 min+ |
| Bounce rate | <60% | <50% |

---

## 🎯 SEARCH CONSOLE + ANALYTICS WORKFLOWS

### Workflow 1: Identify Underperforming Pages

1. Search Console → Performance → filter pages with 100+ impressions but <2% CTR
2. Open each page in browser
3. Improve title (more compelling, includes keyword)
4. Improve meta description (clearer value prop)
5. Re-submit URL for indexing
6. Check CTR improvement in 7-14 days

### Workflow 2: Find Content Gaps

1. Search Console → Queries report
2. Sort by impressions descending
3. Identify queries you're getting impressions for but not ranking top 3
4. Create dedicated content for those queries
5. Build internal links from existing pages

### Workflow 3: Identify Top Conversion Pages

1. GA4 → Reports → Engagement → Pages and Screens
2. Add secondary dimension: Event count for whatsapp_click
3. Identify pages driving most WhatsApp clicks
4. Optimise those pages further (clearer CTAs, more product info)
5. Build internal links to them from other pages

---

## 🚨 COMMON MISTAKES

1. **Not verifying Search Console** for full domain — only one subdomain coverage misses data
2. **Not submitting sitemap** — Google relies on natural crawl, much slower
3. **Not setting up conversions** in GA4 — can't measure what matters
4. **Looking at vanity metrics** (page views) instead of actions (calls, WhatsApp, forms)
5. **Not linking GA4 + Search Console** — missing unified view of SEO performance
6. **Reviewing data daily but never acting on it** — analytics without action is wasted

---

## ✅ SETUP CHECKLIST

- [ ] Search Console verified for hoovale.com (Domain property)
- [ ] Sitemap submitted to Search Console
- [ ] Robots.txt verified accessible
- [ ] GA4 property created with India timezone, INR currency
- [ ] GA4 tag added to base.html and deployed
- [ ] Real-time data showing in GA4
- [ ] WhatsApp click event configured + marked as conversion
- [ ] Phone call event configured + marked as conversion
- [ ] Form submit event configured + marked as conversion
- [ ] Catalogue download event configured + marked as conversion
- [ ] GA4 linked to Search Console
- [ ] Weekly review schedule set in calendar (15 min/week)

Once setup, the data tells you exactly what's working — let it guide your monthly SEO priorities.
