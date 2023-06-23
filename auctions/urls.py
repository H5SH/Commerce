from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("<str:user_id>/<int:auction_id>/entry", views.entry, name="entry"),
    path("<str:user_id>/<int:auction_id>/watchlist", views.watchlist, name="watchlist"),
    path("<str:user_id>/watchlist", views.display_watchlist, name="display_watchlist"),
    path("<str:user_id>/won", views.won, name="won"),
    path("catogeries", views.catogery, name="catogery"),
    path("<str:catogery>/same_catogery", views.same_catogery, name="same_catogery"),
    path("auction/search", views.search, name="search")
]
