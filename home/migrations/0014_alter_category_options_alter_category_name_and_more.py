# Generated by Django 5.1.1 on 2025-03-09 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_remove_category_sub_category_category_sub_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.RemoveField(
            model_name='category',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scategory', to='home.category'),
        ),
    ]
