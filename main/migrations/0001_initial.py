# Generated by Django 5.0.6 on 2024-12-12 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('duration_minutes', models.PositiveIntegerField()),
                ('genre', models.CharField(max_length=100)),
                ('poster', models.ImageField(upload_to='posters/')),
                ('imdb_rating', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cinemas', to='main.city')),
            ],
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hall_number', models.PositiveIntegerField()),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='halls', to='main.cinema')),
            ],
            options={
                'unique_together': {('cinema', 'hall_number')},
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.PositiveIntegerField()),
                ('seat_number', models.CharField(max_length=10)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='main.hall')),
            ],
            options={
                'unique_together': {('hall', 'seat_number')},
            },
        ),
        migrations.CreateModel(
            name='ShowTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='main.hall')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtimes', to='main.movie')),
            ],
            options={
                'unique_together': {('movie', 'hall', 'start_time')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_reserved', models.BooleanField(default=False)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='main.seat')),
                ('show_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='main.showtime')),
            ],
            options={
                'unique_together': {('seat', 'show_time')},
            },
        ),
    ]
