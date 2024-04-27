# Generated by Django 5.0.4 on 2024-04-27 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_commodity_com_name_alter_commodity_com_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=255, unique=True)),
                ('ongoing_order', models.JSONField()),
                ('service_order', models.JSONField()),
                ('closed_order', models.JSONField()),
            ],
        ),
    ]
