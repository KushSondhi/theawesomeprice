# Generated by Django 2.2b1 on 2019-06-10 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PageScrape', '0002_auto_20190610_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopclues',
            name='prod_mrp',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='shopclues',
            name='prod_price',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='snapdeal',
            name='prod_mrp',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='snapdeal',
            name='prod_price',
            field=models.CharField(max_length=10),
        ),
    ]
