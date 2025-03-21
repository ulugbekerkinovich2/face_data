# Generated by Django 4.2.17 on 2024-12-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heartbeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField()),
                ('ip_address', models.GenericIPAddressField()),
                ('mac_address', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ICCardInfoPush',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField()),
                ('ic_card_num', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StrangerCapture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(blank=True, null=True, upload_to='stranger_captures/')),
                ('create_time', models.DateTimeField()),
                ('device_id', models.IntegerField()),
                ('direction', models.IntegerField()),
                ('picture_type', models.IntegerField()),
                ('send_in_time', models.IntegerField()),
                ('operator', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyPush',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('similarity1', models.FloatField()),
                ('similarity2', models.FloatField()),
                ('verify_status', models.IntegerField()),
                ('verify_type', models.IntegerField()),
                ('person_type', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('gender', models.IntegerField()),
                ('nation', models.IntegerField()),
                ('card_type', models.IntegerField()),
                ('id_card', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateField()),
                ('telnum', models.CharField(blank=True, max_length=50, null=True)),
                ('native', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('mj_card_from', models.IntegerField()),
                ('mj_card_no', models.CharField(max_length=50)),
                ('rfid_card', models.CharField(max_length=50)),
                ('tempvalid', models.IntegerField()),
                ('customize_id', models.IntegerField()),
                ('person_uuid', models.CharField(blank=True, max_length=100, null=True)),
                ('valid_begin', models.DateTimeField(blank=True, null=True)),
                ('valid_end', models.DateTimeField(blank=True, null=True)),
                ('send_in_time', models.IntegerField()),
                ('direction', models.IntegerField()),
                ('sz_qr_code_data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='FaceLog',
        ),
        migrations.DeleteModel(
            name='RFLog',
        ),
    ]
