# Generated by Django 3.2.3 on 2023-02-13 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0008_rename_item_assets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='Qr_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='Qr',
        ),
    ]