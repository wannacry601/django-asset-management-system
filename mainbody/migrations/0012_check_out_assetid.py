# Generated by Django 4.1.7 on 2023-02-23 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainbody', '0011_check_out_asset_check_out_checkdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='check_out',
            name='assetID',
            field=models.ForeignKey(default='0000000000000', on_delete=django.db.models.deletion.CASCADE, to='mainbody.asset'),
        ),
    ]
