# Generated by Django 3.2.16 on 2022-12-30 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0022_alter_school_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
