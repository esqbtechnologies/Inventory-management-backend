# Generated by Django 3.2.3 on 2023-02-13 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0009_auto_20230213_1515'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='assets',
            new_name='asset',
        ),
    ]