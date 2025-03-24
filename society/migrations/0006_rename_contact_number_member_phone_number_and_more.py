# Generated by Django 5.1.5 on 2025-02-17 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0005_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='contact_number',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='member',
            name='flat_number',
            field=models.CharField(default='Not Assigned', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('tenant', 'Tenant'), ('flat_owner', 'Flat Owner')], default='Tenant', max_length=50),
            preserve_default=False,
        ),
    ]
