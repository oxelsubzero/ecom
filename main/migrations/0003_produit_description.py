# Generated by Django 3.2.21 on 2023-11-20 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20231120_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='description',
            field=models.TextField(null=True),
        ),
    ]