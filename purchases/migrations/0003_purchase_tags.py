# Generated by Django 3.0.5 on 2020-04-22 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0001_initial"),
        ("purchases", "0002_purchase_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="tags",
            field=models.ManyToManyField(to="tags.Tag"),
        ),
    ]
