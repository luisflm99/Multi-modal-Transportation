from django.urls import path

from .views import HomeView, AboutView, OrderCreateView


app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    
    # Orders
    path("order-create/", OrderCreateView.as_view(), name="order-create"),
]