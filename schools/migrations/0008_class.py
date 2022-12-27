# Generated by Django 3.2.16 on 2022-12-26 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0007_remarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ManyToManyField(to='schools.Student')),
                ('teachers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.teacher')),
            ],
        ),
    ]