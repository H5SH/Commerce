# Generated by Django 4.2.1 on 2023-06-19 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_comments_alter_user_id_auction_user_auctionlist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='auction_pic',
            field=models.URLField(max_length=50, null=True),
        ),
    ]