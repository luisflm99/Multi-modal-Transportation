from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from ..models import Route
from ..forms import RouteForm


class RouteCreateView(CreateView):
    template_name = 'generic/create.html'
    model = Route
    form_class = RouteForm
    success_url = reverse_lazy('core:route-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name
        return context

   
class RouteListView(ListView):
    model = Route
    template_name = 'routes/list.html'
    context_object_name = 'routes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model._meta.verbose_name_plural
        return context