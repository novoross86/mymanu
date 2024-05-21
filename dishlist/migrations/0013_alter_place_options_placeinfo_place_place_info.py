# Generated by Django 4.2.11 on 2024-05-21 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dishlist', '0012_remove_place_label_delete_placelabel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ['title_place'], 'verbose_name': 'Заведение', 'verbose_name_plural': 'Заведения'},
        ),
        migrations.CreateModel(
            name='PlaceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info_set', to='dishlist.place', verbose_name='Заведение')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='place_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='place_info_reverse', to='dishlist.placeinfo'),
        ),
    ]
