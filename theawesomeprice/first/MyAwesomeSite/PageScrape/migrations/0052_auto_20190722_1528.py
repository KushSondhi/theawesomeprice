# Generated by Django 2.2.3 on 2019-07-22 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PageScrape', '0051_shopclues_prod_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopclues',
            old_name='prod_image_url',
            new_name='prod_image_URL',
        ),
    ]
