from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("clear/", views.clear, name="clear"),
    path("validate/", views.validate, name="validate"),
    path("guess/", views.guess, name="guess")
]