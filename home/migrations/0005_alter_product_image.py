# Generated by Django 5.1.1 on 2024-12-05 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_avaible_product_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='products/%y/%m/%d/'),
        ),
    ]
