# Generated by Django 3.2.16 on 2022-12-26 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0009_remarks_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='teachers',
            new_name='teacher',
        ),
    ]