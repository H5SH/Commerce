from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser

from auctions.models import *
from django import forms

itemtypes = [
    "none",
    "Fashion",
    "Toys",
    "Electronics",
    "Home"
]

# form for comment and bid
class CommentBidForm(forms.Form):
    comment = forms.CharField(required=False)
    bid = forms.FloatField(required=False)


class NewEntryForm(forms.Form):
    title = forms.CharField(label='title', 
                    widget=forms.TextInput(attrs={'placeholder': 'title'}))
    pic = forms.URLField(label="Optional", required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'pic'}))
    price = forms.FloatField(label="Starting Price", widget=forms.TextInput(attrs={'placeholder': 'price'}))
    discription = forms.CharField(widget=forms.Textarea(attrs={"name": "discription", "cols": "100", "rows":"15"}))


def index(request):
    f = Auction.objects.all()
    return render(request, "auctions/index.html",{
        "heading": "Active listings",
        "entries": f.exclude(auction_active=False),
    })

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        try:
            entry = Auction.objects.filter(auction_name__icontains=title).all()
        except Auction.DoesNotExist:
            entry = 'none'

        return render(request, "auctions/index.html", {
            "heading": title,
            "entries": entry
        })


        # else:
        #     entries = util.list_entries()
        #     related = []
        #     for entry in entries:
        #         if title.lower() in entry.lower():
        #             related.append(entry)

        #     if len(related) is 0:
        #         return render(request, "encyclopedia/apology.html",{
        #             "title": "Apology",
        #             "messege": "No data found"
        #         })

        #     else:
        #         return render(request, "encyclopedia/recomended.html", {
        #              "messege": "You mean",
        #              "entry": related
        #         })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # to make sure that the price is float input
            try:
                price = float(form.cleaned_data["price"])
            except ValueError:
                return Error(request, "Price was not in numbers", "Invalid price input")
        

            # catogary = form.cleaned_data["type"]
            # check that title and discription are not null
            if form.cleaned_data["title"] and form.cleaned_data["discription"]:
                title = form.cleaned_data["title"]
                discription = form.cleaned_data["discription"]
                # to get the user from hidden input field
                user_id = request.POST["user_id"]
                p = Bids(bider_id=user_id, bid=price)
                p.save()
                catogery = request.POST["catogery"]
                # save the picture
                if form.cleaned_data["pic"]:
                    pic = form.cleaned_data["pic"]
                    f = Auction(auction_name = title, auction_bid=p, starting_price=price, auction_discription=discription, auction_pic=pic,auction_type=catogery, auction_active=True)
                    f.save()
                else:
                    f = Auction(auction_name = title, auction_bid=p, auction_discription=discription, starting_price=price, auction_type=catogery,auction_active=True)
                    f.save()
                   
                # saves the auction the current user 
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Error(request, "User does not exist", "Error")

                user.auctionlist.add(f)
                f = Auction.objects.all()
                return HttpResponseRedirect(reverse("index"))
                # return render(request, "auctions/index.html",{
                #     "heading": "Active listings",
                #     "entries": f
                # })
                
            else:
                return Error(request, "Title or discription was not mentioned" , "Invalid input")

        else:
            return Error(request, form.errors, "Error")
        
    else:
        return render(request, "auctions/new.html",{
            "form": NewEntryForm(),
            "catogeries": itemtypes
        })


# entry details
def entry(request, auction_id, user_id):
    # Post will be used when a comment is added 
    if request.method == "POST":
        try:
            u = User.objects.get(id=user_id)
            f = Auction.objects.get(id=auction_id)
        except User.DoesNotExist or Auction.DoesNotExist:
            return Error(request, "user or auction does not exist", "Error")
    
        form = CommentBidForm(request.POST)
        if form.is_valid() and (form.cleaned_data["comment"] or form.cleaned_data["bid"]):

            # if user has commented
            if form.cleaned_data["comment"]:
                # saves the comment
                com = form.cleaned_data["comment"]
                com = Comment(com, auction_id, u.username)
                """
                Comment returns false when auctions id is incorrent
                """
                if com is False:
                    return Error(request, "Auction Id is incorrect", "Error")
            
            # if user has added a bid 
            if form.cleaned_data["bid"]:
                # saves the bid
                """
                returns false when the bid is smaller or equal
                       to the previous bid
                """
                bid = form.cleaned_data["bid"]
                bid = biding(bid, auction_id, user_id)
                if bid == False:
                    return Error(request, "Bid must be bigger then previous bids","Error")

            
            # getting data for display
            f = Auction.objects.get(id=auction_id)
            return render(request, "auctions/Entry.html",{
                "entry": f,
                "watchlist": u.watchlist.all,
                "auction_list": u.auctionlist.all(),
                "form": CommentBidForm(),
                "comments": f.auction_comment.all()
            })
        
        # else runs when user has has neither commented nor bid
        # user has used the 3rd and only option that is to CLOSE auction
        else:
            try:
                f = Auction.objects.get(id=auction_id)
                 # person who won the auction
                winner = f.auction_bid.bider_id 
                user = User.objects.get(id=winner)
            except Auction.DoesNotExist or User.DoesNotExist:
                return Error(request, "Invalid Auction Id or User Id", "Error")
            
            user.auctions_won.add(f)
            f.auction_active = False
            f.save()

            return render(request, "auctions/entry.html",{
                "entry": f,
                "winner": user.username,
                "comments": f.auction_comment.all()
            })
                    
            
    # simple display for entry by get
    else:
        try:
            f = Auction.objects.get(id=auction_id)
        except Auction.DoesNotExist:
            return Error(request, "auction does not exist", "Error")

        if int(user_id) != 0:
            try:
                s = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Error(request, "user id incorrect", "Error")
        
            return render(request, "auctions/entry.html",{
            "entry": f,
            "watchlist": s.watchlist.all(),
            "auction_list": s.auctionlist.all(),
            "form": CommentBidForm(),
            "comments": f.auction_comment.all()
        })

        # else will be used when the NO user is loged in and the user id is 0
        # guest will not be allowed to comment or add to watchlist
        else:
            return render(request, "auctions/entry.html",{
                "entry": f,
                "comments": f.auction_comment.all()
            })

        



@login_required
def display_watchlist(request, user_id):
    try:
        w = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Error(request, "User id incorrect", "Error")

    return render(request, "auctions/index.html",{
        "heading": "Watchlist",
        "entries": w.watchlist.all()
    })



# Auction added to the watchlist
@login_required
def watchlist(request, user_id, auction_id):
    try:
        s = User.objects.get(id=user_id)
        f = Auction.objects.get(id=auction_id)
    except User.DoesNotExist or Auction.DoesNotExist:
        return Error(request, "User or Auction id invalid", "Error")

    if request.method == "POST":
        
        s.watchlist.add(f)

        return render(request, "auctions/index.html",{
            "heading": "Watchlist",
            "entries": s.watchlist.all(),
        })
    # else is used to remove certain entry from watchlist
    else:
        s.watchlist.remove(f)

        return render(request, "auctions/index.html",{
            "heading": "Watchlist",
            "entries": s.watchlist.all()
        })
    
       
        # try:
        #     f = Auction.objects.get(id=s)
        # except Auction.DoesNotExist:
        #     f = None
    
        # # if image does not exits then g is none
        # try:
        #     g = Image.objects.filter(caption=f.auction_name)
        # except Image.DoesNotExist:
        #     g = None

        # return render(request, "auctions/index.html",{
        #        "heading": "Watchlist",
        #        "entry": f,
        #        "image": g
        # })


def biding(bid, auction_id, user_id):
    # to get the previous bid of auction
    price = Auction.objects.get(id=auction_id)

    # if the entered is low
    if bid <= price.auction_bid.bid:
        return False

    else:
        s = Bids(bider_id=user_id, bid=bid)
        s.save()
        f = Auction.objects.get(id=auction_id)
        f.auction_bid = s
        f.save()
        
        return True



# adds comment
def Comment(comment, auction_id, username):
    c = Comments(commenter=username, comment=comment)
    c.save()
    try:
        f = Auction.objects.get(id=auction_id)
    except Auction.DoesNotExist:
        return False
    f.auction_comment.add(c)
    
    return True
    # return render(request, "auctions/entry.html",{
    #         "entry": f,
    #         "form": CommentBidForm(),
    #         # to check whether the auction is the watchlist or not
    #         "watchlist": u.watchlist.all(),
    #         "comments": f.auction_comment.all()
    #     })


def Error(request, massege, title):
    return render(request, "auctions/Error.html",{
        "massege": massege,
        "title": title
    })


def won(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Error(request, "User does not exist", "Error")

    if user.auctions_won is not None:
        return render(request, "auctions/won.html",{
            "entries": user.auctions_won.all(),
            "heading": "Auctions won"
        })
    else:
        return render(request,"auctions/won.html",{
            "heading": "No auctions won so far :("
        })

def catogery(request):
    return render(request, "auctions/catogery.html",{
        "catogeries": itemtypes
    })

def same_catogery(request, catogery):
    f = Auction.objects.filter(auction_type=catogery).all()
    return render(request, "auctions/index.html",{
        "entries": f
    })
    pass