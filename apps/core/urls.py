from django.urls import path

from .views import (
    HomeView,
    AboutView,
    OrderCreateView,
    OrderListView,
    RouteCreateView,
    RouteListView
)


app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    
    # Orders
    path("order-create/", OrderCreateView.as_view(), name="order-create"),
    path("order-list/", OrderListView.as_view(), name="order-list"),
    
    # Routes
    path("route-create/", RouteCreateView.as_view(), name="route-create"),
    path("route-list/", RouteListView.as_view(), name="route-list"),
]