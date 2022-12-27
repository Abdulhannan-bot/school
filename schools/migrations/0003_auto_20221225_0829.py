# Generated by Django 3.2.16 on 2022-12-25 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_auto_20221225_0506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.AddField(
            model_name='nonstaff',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='nonstaff',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='nonstaff',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='nonstaff',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
    ]
