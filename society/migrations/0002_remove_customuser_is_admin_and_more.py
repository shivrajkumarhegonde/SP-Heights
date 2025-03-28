# Generated by Django 5.1.5 on 2025-02-01 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_flat_owner',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_tenant',
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('flat_owner', 'Flat Owner'), ('tenant', 'Tenant')], default='flat_owner', max_length=20),
        ),
    ]
