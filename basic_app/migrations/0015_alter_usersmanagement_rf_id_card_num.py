# Generated by Django 4.2.17 on 2025-01-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0014_controllog_face_id_strangercapturelog_face_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersmanagement',
            name='rf_id_card_num',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
