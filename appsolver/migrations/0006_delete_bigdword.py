# Generated by Django 4.0.3 on 2022-03-07 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appsolver', '0005_rename_bigdictionary_bigdword_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BigDWord',
        ),
    ]