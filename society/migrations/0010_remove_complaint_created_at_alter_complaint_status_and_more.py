# Generated by Django 5.1.5 on 2025-03-06 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0009_alter_member_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('chairman', 'Chairman'), ('treasurer', 'Treasurer'), ('admin', 'admin'), ('tenant', 'Tenant'), ('flat_owner', 'Flat Owner'), ('secretary', 'Secretary')], max_length=50),
        ),
    ]
