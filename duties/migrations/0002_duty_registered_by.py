# Generated by Django 2.2.4 on 2019-11-23 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('duties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='duty',
            name='registered_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.expressions.Case, related_name='registered_duties', to=settings.AUTH_USER_MODEL),
        ),
    ]
