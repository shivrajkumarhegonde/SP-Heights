# Generated by Django 5.1.5 on 2025-03-13 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0010_remove_complaint_created_at_alter_complaint_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='flat_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
