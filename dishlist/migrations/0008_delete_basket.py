# Generated by Django 4.2.11 on 2024-05-09 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dishlist', '0007_alter_dishes_options_category_place'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Basket',
        ),
    ]