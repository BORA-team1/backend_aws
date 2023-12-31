# Generated by Django 3.0.8 on 2023-08-14 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('audio_id', models.AutoField(primary_key=True, serialize=False)),
                ('long', models.IntegerField()),
                ('audiofile', models.TextField(blank=True, null=True)),
                ('audio_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audio_post', to='post.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('playlist_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('des', models.CharField(blank=True, max_length=400, null=True)),
                ('is_base', models.BooleanField(default=False)),
                ('first_audio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_audio', to='audio.Audio')),
                ('hashtag', models.ManyToManyField(to='account.Hashtag')),
                ('mypli_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mypli_user', to=settings.AUTH_USER_MODEL)),
                ('playlist_audio', models.ManyToManyField(related_name='playlist_audio', to='audio.Audio')),
            ],
        ),
    ]
