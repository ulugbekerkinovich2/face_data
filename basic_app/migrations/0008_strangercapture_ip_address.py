# Generated by Django 4.2.17 on 2025-01-10 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0007_iccardinfopush_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='strangercapture',
            name='ip_address',
            field=models.CharField(blank=True, default='aniqlanmagan', max_length=255, null=True),
        ),
    ]
