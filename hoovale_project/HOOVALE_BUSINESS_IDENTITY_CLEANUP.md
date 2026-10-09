# HOOVALE — Business Identity Cleanup

This migration updates the singleton website settings record only. It does not delete product listings, enquiries, customer/user accounts, testimonials, blog posts, or other database records.

## Updated official profile
- Business name: HOOVALE
- Email: hoovale@outlook.com
- Phone/WhatsApp: +91 90241 32535
- Address: 20, Bal Vihar, Kalwar Road, Near KGN Hostel, Jhotwara, Jaipur, Rajasthan 302012, India

## Deploying the changes
The migration `products.0011_reset_hoovale_site_settings` runs during the normal Django migration process. On your hosting platform, deploy the new commit and run:

```bash
python manage.py migrate
```

If your deployment pipeline already runs migrations automatically, no separate command may be needed.

## Important notes
The website database is not hosted in GitHub. The migration will update the live database only when the new code is deployed and migrations are run against that database.

The About page has also been rewritten to remove unverified numerical and operational claims (such as establishment year, customer counts, city counts, factory-scale claims, warranty, GST registration and production process statements) and replace them with business information that does not make unsupported claims.

The address-specific latitude/longitude has not been guessed. The current Jaipur city coordinates remain placeholders and should be replaced after confirming the exact location on a map. Please add only verified GST, years of operation, manufacturing capability, product count, warranty, delivery timelines, social profiles, and testimonials through the admin panel.

This cleanup intentionally preserves existing product/catalogue content and customer records, because deleting these would be destructive and those records cannot reliably be identified as belonging to another business without inspecting the live database.
