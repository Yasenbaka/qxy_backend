# Generated by Django 5.0.3 on 2024-04-18 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.IntegerField()),
                ('com_name', models.CharField(max_length=50)),
                ('com_introduce', models.TextField()),
                ('com_price', models.IntegerField()),
                ('com_reserve', models.IntegerField()),
                ('com_banners', models.JSONField()),
                ('com_introduction_pictures', models.JSONField()),
                ('com_is_active', models.BooleanField(default=True)),
                ('com_is_preferential', models.BooleanField(default=True)),
                ('com_is_coupon', models.BooleanField(default=True)),
            ],
        ),
    ]