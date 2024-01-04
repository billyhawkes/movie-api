# Generated by Django 4.2.8 on 2023-12-21 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('budget', models.IntegerField()),
                ('homepage', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField()),
                ('popularity', models.FloatField()),
                ('genres', models.ManyToManyField(related_name='movies', to='base.genre')),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
