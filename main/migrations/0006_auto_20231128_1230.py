# Generated by Django 3.2.21 on 2023-11-28 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20231128_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hero',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hero',
            name='subtitle',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hero',
            name='tile',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
