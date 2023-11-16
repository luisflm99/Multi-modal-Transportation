from django.views.generic import TemplateView
from django.contrib.auth.models import User

from ..models import Order, Route


class HomeView(TemplateView):
    template_name = "home/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.all().count()
        context['routes_count'] = Route.objects.all().count()
        context['orders_count'] = Order.objects.filter().count()
        context['processed_orders_count'] = Order.objects.filter().count()
        return context


class AboutView(TemplateView):
    template_name = "home/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.all().count()
        context['routes_count'] = Route.objects.all().count()
        context['orders_count'] = Order.objects.filter().count()
        context['processed_orders_count'] = Order.objects.filter().count()
        return context
