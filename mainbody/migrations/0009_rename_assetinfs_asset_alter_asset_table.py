# Generated by Django 4.1.7 on 2023-02-21 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainbody', '0008_alter_assetinfs_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='assetinfs',
            new_name='asset',
        ),
        migrations.AlterModelTable(
            name='asset',
            table='Assets',
        ),
    ]
