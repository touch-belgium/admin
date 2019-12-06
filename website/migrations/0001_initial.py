# Generated by Django 3.0 on 2019-12-06 16:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('MO', 'MO'), ('WO', 'WO'), ('XO', 'XO'), ('M27', 'M27'), ('W27', 'W27'), ('X27', 'X27'), ('M30', 'M30'), ('W30', 'W30'), ('X30', 'X30'), ('M30', 'M40'), ('W30', 'W40'), ('X40', 'X40'), ('JO', 'JO')], max_length=3)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', filebrowser.fields.FileBrowseField(default='base/team_placeholder.png', max_length=500)),
                ('founded', models.CharField(blank=True, help_text='Year in YYYY format', max_length=4)),
                ('website', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('main_belgian_club', models.BooleanField(default=False)),
                ('lat', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=16, max_digits=22, null=True)),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Venue')),
            ],
        ),
        migrations.CreateModel(
            name='TBMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('picture', filebrowser.fields.FileBrowseField(blank=True, default='base/person_placeholder.png', max_length=500)),
                ('license_number', models.CharField(blank=True, max_length=30)),
                ('committee_member', models.BooleanField()),
                ('committee_position', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('committee_text', models.TextField(blank=True, null=True)),
                ('referee', models.BooleanField(blank=True, null=True)),
                ('referee_level', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('referee_board_member', models.BooleanField(blank=True, null=True)),
                ('referee_board_position', models.CharField(blank=True, max_length=50, null=True)),
                ('referee_text', models.TextField(blank=True, null=True)),
                ('coach', models.BooleanField(blank=True, null=True)),
                ('coach_level', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('coach_position', models.CharField(blank=True, max_length=50, null=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Team')),
            ],
            options={
                'verbose_name': 'Touch Belgium member',
                'verbose_name_plural': 'Touch Belgium members',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('picture', filebrowser.fields.FileBrowseField(default='base/news_placeholder.png', max_length=500)),
                ('body', tinymce.models.HTMLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='website.Tag')),
            ],
            options={
                'ordering': ['-created_at'],
                'get_latest_by': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Do not create any pools for a league type competition', max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Category')),
                ('teams', models.ManyToManyField(to='website.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(help_text='Type the time in HH:MM format')),
                ('pitch', models.CharField(blank=True, max_length=50, null=True)),
                ('refs', models.CharField(blank=True, max_length=100, null=True)),
                ('home_touchdowns', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('away_touchdowns', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('match_type', models.CharField(blank=True, choices=[('PS', 'Pool match'), ('PO', 'Playoff'), ('QF', 'Quarter final'), ('SF', 'Semi final'), ('FF', 'Final')], help_text='Leave blank for league style competitions', max_length=2)),
                ('invitational_match', models.BooleanField(blank=True, default=False)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_team', to='website.Team')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Category')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_team', to='website.Team')),
            ],
            options={
                'verbose_name_plural': 'matches',
                'ordering': ['-when'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', filebrowser.fields.FileBrowseField(default='base/base_document.pdf', max_length=500)),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('win_value', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(0)])),
                ('defeat_value', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tie_value', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Venue')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Competition'),
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(help_text='Bonus points can be negative')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Category')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Team')),
            ],
            options={
                'verbose_name_plural': 'Bonuses',
            },
        ),
        migrations.CreateModel(
            name='BannerPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', filebrowser.fields.FileBrowseField(max_length=500)),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Tag')),
            ],
        ),
    ]
