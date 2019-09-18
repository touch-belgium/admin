# Generated by Django 2.2.5 on 2019-09-18 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20190915_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='website.Tag')),
            ],
        ),
    ]