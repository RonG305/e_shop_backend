# Generated by Django 5.0.6 on 2024-08-21 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
