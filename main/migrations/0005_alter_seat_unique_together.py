# Generated by Django 5.0.6 on 2024-12-22 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_ticket_is_locked'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together=set(),
        ),
    ]
