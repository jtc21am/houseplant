# Generated by Django 4.2.1 on 2023-06-09 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_alter_plant_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='grown_from',
            field=models.CharField(choices=[('SEED', 'Seed'), ('SEEDLING', 'Seedling'), ('CUTTING', 'Cutting'), ('FULLSIZE', 'Full Size'), ('BULB', 'Bulb')], default='Full Size', max_length=100),
        ),
        migrations.AlterField(
            model_name='plant',
            name='location',
            field=models.CharField(choices=[('KITCHEN', 'Kitchen'), ('LIVING RM', 'Living Room'), ('MUDROOM', 'Mud Room'), ('FR STEPS', 'Front Steps'), ('BK DECK', 'Back Deck'), ('BK GARDEN', 'Back Garden'), ('FR GARDEN', 'Front Garden')], default='Mud Room', max_length=100),
        ),
    ]
