# Generated by Django 4.2.17 on 2025-03-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0025_alter_userrole_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='full_name',
            field=models.CharField(max_length=256),
        ),
    ]
