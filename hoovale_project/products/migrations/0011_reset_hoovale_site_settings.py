"""
HOOVALE business profile cleanup.
Updates only the singleton SiteSettings record; does not delete customer,
product, enquiry, user, or unrelated business records.
"""
from django.db import migrations


def update_hoovale_site_settings(apps, schema_editor):
    SiteSettings = apps.get_model("products", "SiteSettings")

    # Set the profile values on the singleton record used by the public website.
    settings, _ = SiteSettings.objects.using(schema_editor.connection.alias).get_or_create(
        pk=1,
        defaults={
            "business_name": "HOOVALE",
            "tagline": "Wall clocks, custom gifting and wholesale supply",
        },
    )

    settings.business_name = "HOOVALE"
    settings.email = "hoovale@outlook.com"
    settings.primary_phone = "+919024132535"
    settings.whatsapp_number = "919024132535"
    settings.street_address = "20, Bal Vihar, Kalwar Road, Near KGN Hostel, Jhotwara"
    settings.locality = "Jaipur"
    settings.region = "Rajasthan"
    settings.postal_code = "302012"
    settings.country = "IN"

    # Precise street coordinates should be verified by the business owner
    # before publishing; these defaults represent Jaipur city, not an exact pin.
    settings.latitude = 26.9124
    settings.longitude = 75.7873

    settings.tagline = "Wall clocks and customized gifting solutions from Jaipur"
    settings.default_meta_title = "HOOVALE | Wall Clock Manufacturer in Jaipur"
    settings.default_meta_description = (
        "Explore HOOVALE wall clocks for homes, retailers, offices, corporate gifting "
        "and bulk enquiries. Contact our Jaipur team for product details and pricing."
    )
    settings.save(using=schema_editor.connection.alias)


def reverse_hoovale_site_settings(apps, schema_editor):
    # Do not restore unverified/wrong third-party contact details on rollback.
    # Preserve current record so the migration rollback does not reintroduce them.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_alter_blog_slug"),
    ]

    operations = [
        migrations.RunPython(
            update_hoovale_site_settings,
            reverse_hoovale_site_settings,
        ),
    ]
