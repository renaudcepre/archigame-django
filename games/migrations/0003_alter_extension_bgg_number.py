# Generated by Django 5.0.2 on 2024-02-25 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_gameconfiguration_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extension',
            name='bgg_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
