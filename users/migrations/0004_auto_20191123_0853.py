# Generated by Django 2.2.4 on 2019-11-23 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_organizationrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('request_type', models.IntegerField(blank=True, choices=[(1, 'apply for organization'), (2, 'upgrade to manager')], default=1, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='users.Organization')),
            ],
            options={
                'verbose_name': 'Organization Request',
                'verbose_name_plural': 'Organization Requests',
            },
        ),
        migrations.DeleteModel(
            name='OrganizationRequest',
        ),
    ]