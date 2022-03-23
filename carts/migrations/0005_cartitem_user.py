# Generated by Django 4.0 on 2022-03-05 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_id'),
        ('carts', '0004_alter_cart_id_alter_cartitem_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
    ]
