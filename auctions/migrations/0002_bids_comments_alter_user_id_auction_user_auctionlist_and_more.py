# Generated by Django 4.2.1 on 2023-06-19 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bider_id', models.IntegerField()),
                ('bid', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commenter', models.CharField(max_length=150)),
                ('comment', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('auction_active', models.BooleanField(default=True)),
                ('auction_name', models.CharField(max_length=64)),
                ('auction_type', models.CharField(blank=True, max_length=15)),
                ('auction_discription', models.CharField(max_length=640)),
                ('starting_price', models.FloatField(default=0)),
                ('auction_pic', models.CharField(max_length=50, null=True)),
                ('auction_bid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='value', to='auctions.bids')),
                ('auction_comment', models.ManyToManyField(blank=True, related_name='chat', to='auctions.comments')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='auctionlist',
            field=models.ManyToManyField(blank=True, related_name='myentry', to='auctions.auction'),
        ),
        migrations.AddField(
            model_name='user',
            name='auctions_won',
            field=models.ManyToManyField(blank=True, related_name='won', to='auctions.auction'),
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='liked', to='auctions.auction'),
        ),
    ]
