# Generated by Django 5.1.1 on 2024-11-24 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',)},
        ),
    ]
