# Generated by Django 3.2.15 on 2024-07-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flash', '0007_auto_20240701_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='type',
            field=models.CharField(choices=[('folder', 'Folder'), ('subfolder', 'Subfolder')], default='folder', max_length=10),
        ),
    ]