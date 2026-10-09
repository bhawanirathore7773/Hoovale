"""
Correct HOOVALE's public address to the business listing near KGN Hostel.
Only the SiteSettings profile is updated; business/customer/product records remain untouched.
"""
from django.db import migrations


def update_hoovale_address(apps, schema_editor):
    SiteSettings = apps.get_model("products", "SiteSettings")
    alias = schema_editor.connection.alias
    settings = SiteSettings.objects.using(alias).filter(pk=1).first()
    if settings is None:
        settings = SiteSettings.objects.using(alias).order_by("pk").first()
    if settings is None:
        return

    settings.business_name = "HOOVALE Ventures"
    settings.email = "hoovale@outlook.com"
    settings.primary_phone = "+919024132535"
    settings.whatsapp_number = "919024132535"
    settings.street_address = "Shop No. 2, Near KGN Hostel, Jhotwara"
    settings.locality = "Jaipur"
    settings.region = "Rajasthan"
    settings.postal_code = "302012"
    settings.country = "IN"
    settings.default_meta_title = "HOOVALE Ventures | Wall Clock Manufacturer in Jaipur"
    settings.default_meta_description = (
        "Contact HOOVALE Ventures near KGN Hostel, Jhotwara, Jaipur 302012 "
        "for wall-clock products, bulk orders and customized enquiries."
    )
    # Do not overwrite latitude/longitude with guessed coordinates. The contact
    # page now embeds a map search for the business name and verified locality.
    settings.save(using=alias)


def reverse_hoovale_address(apps, schema_editor):
    # Do not restore the previously incorrect address.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0011_reset_hoovale_site_settings"),
    ]

    operations = [
        migrations.RunPython(update_hoovale_address, reverse_hoovale_address),
    ]
