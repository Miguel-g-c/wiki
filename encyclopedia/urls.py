from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("error/<str:message>", views.error, name="error"),
    path("search/<str:query>", views.search, name="search"),
    path("new-page", views.create, name="create"),
    path("edit-page/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")
]
