# Generated by Django 5.1.4 on 2025-03-24 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_config_scan_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.PositiveIntegerField(default=1)),
            ],
        ),
    ]
