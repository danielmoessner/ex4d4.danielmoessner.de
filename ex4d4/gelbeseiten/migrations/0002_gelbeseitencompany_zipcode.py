# Generated by Django 2.2.5 on 2020-02-05 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gelbeseiten', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gelbeseitencompany',
            name='zipcode',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
