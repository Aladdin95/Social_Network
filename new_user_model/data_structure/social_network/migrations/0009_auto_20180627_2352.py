# Generated by Django 2.0.4 on 2018-06-27 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0008_auto_20180507_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('users', models.ManyToManyField(related_name='my_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mypost',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='social_network.Group'),
        ),
    ]
