# Generated by Django 4.2.7 on 2024-09-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_terms_alter_tacagree_is_consent_userterms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('W', 'WOMAN'), ('M', 'MAN')], max_length=1, verbose_name='gender'),
        ),
    ]
