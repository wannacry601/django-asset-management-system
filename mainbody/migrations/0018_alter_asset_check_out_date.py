# Generated by Django 4.1.7 on 2023-02-25 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbody', '0017_alter_asset_check_out_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='check_out_date',
            field=models.DateTimeField(null=True, verbose_name='check-out date'),
        ),
    ]
