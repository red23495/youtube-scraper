# Generated by Django 4.0.6 on 2022-07-30 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('channel_id', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=256)),
                ('fhv', models.IntegerField(default=0, help_text='first hour view')),
                ('fhv_rating', models.DecimalField(decimal_places=6, default=0, help_text='first hour view rating on channel', max_digits=30)),
            ],
            options={
                'db_table': 'videos',
                'ordering': ('-fhv_rating',),
            },
        ),
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(db_column='tag_id', on_delete=django.db.models.deletion.CASCADE, related_name='video_tags', related_query_name='video_tag', to='video.tag')),
                ('video', models.ForeignKey(db_column='video_id', on_delete=django.db.models.deletion.CASCADE, related_name='video_tags', related_query_name='video_tag', to='video.video')),
            ],
            options={
                'db_table': 'video_tags',
            },
        ),
    ]
