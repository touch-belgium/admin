# Generated by Django 3.1.1 on 2020-09-21 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20200919_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='BelgianClub',
            fields=[
                ('club_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='website.club')),
            ],
            bases=('website.club',),
        ),
    ]
