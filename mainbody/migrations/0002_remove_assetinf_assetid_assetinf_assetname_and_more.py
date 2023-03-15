# Generated by Django 4.1.7 on 2023-02-21 14:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainbody', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetinf',
            name='assetid',
        ),
        migrations.AddField(
            model_name='assetinf',
            name='assetname',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='Book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assetinf',
            name='user',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='Shawn'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assetinf',
            name='id',
            field=models.CharField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
