# Generated by Django 2.2.3 on 2019-07-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PageScrape', '0037_remove_snapdeal_prod_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapdeal',
            name='prod_reviews',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]
