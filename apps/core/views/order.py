from django.views.generic import CreateView
from django.urls import reverse_lazy

from ..models import Order
from ..forms import OrderForm


class OrderCreateView(CreateView):
    template_name = 'generic/create.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('core:court-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name
        return context
    

