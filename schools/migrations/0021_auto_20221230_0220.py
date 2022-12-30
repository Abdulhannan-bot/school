# Generated by Django 3.2.16 on 2022-12-30 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('schools', '0020_auto_20221229_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonstaff',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.school'),
        ),
        migrations.AlterField(
            model_name='school',
            name='profile_pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to='media/'),
        ),
        migrations.CreateModel(
            name='Remarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks_on', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.student')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]