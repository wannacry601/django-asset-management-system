# Generated by Django 4.1.7 on 2023-02-23 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainbody', '0014_alter_check_out_assetid'),
    ]

    operations = [
        migrations.AddField(
            model_name='check_out',
            name='userID',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='check_out',
            name='assetID',
            field=models.ForeignKey(default='1145141145142', on_delete=django.db.models.deletion.CASCADE, to='mainbody.asset'),
        ),
    ]