# Generated by Django 4.2.17 on 2025-01-09 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0006_verifypush_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='iccardinfopush',
            name='ip_address',
            field=models.CharField(blank=True, default='aniqlanmagan', max_length=255, null=True),
        ),
    ]
