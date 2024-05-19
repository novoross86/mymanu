# Generated by Django 4.2.11 on 2024-04-26 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dishlist', '0003_place_alter_dishes_category_alter_dishes_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('content', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, verbose_name='Цена')),
                ('is_public', models.BooleanField(default=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dishlist.category', verbose_name='Категория')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dishlist.place', verbose_name='Заведение')),
            ],
        ),
    ]
