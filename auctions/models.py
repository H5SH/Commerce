from django.contrib.auth.models import AbstractUser
from django.db import models
    

# bids of the auctions
class Bids(models.Model):
    bider_id = models.IntegerField()
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bider_id}: {self.bid}"


# comments on an auction
class Comments(models.Model):
    commenter = models.CharField(max_length=150)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.commenter} : {self.comment}"


# Auction stores name link of the pic and price
class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    auction_active = models.BooleanField(default=True)
    auction_name = models.CharField(max_length=64)
    auction_type = models.CharField(max_length=15, blank=True)
    auction_discription = models.CharField(max_length=640)
    starting_price = models.FloatField(default=0)
    auction_pic= models.URLField(default=None)
    auction_comment = models.ManyToManyField(Comments, blank=True, related_name="chat")
    auction_bid = models.ForeignKey(Bids, on_delete=models.CASCADE, null=True, blank=True, related_name="value")


    def __str__(self):
        return f"{self.auction_name}: {self.auction_bid}; {self.auction_discription}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction, blank=True, related_name="liked")
    auctionlist = models.ManyToManyField(Auction, blank=True, related_name="myentry")
    auctions_won = models.ManyToManyField(Auction, blank=True,related_name="won")

