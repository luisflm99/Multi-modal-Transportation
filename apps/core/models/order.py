import pandas as pd

from django.db import models
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError

from .cvxpy import CVXPY
from .constants import Status
from .location import Location
from .route import Route
from .error import NotSolvable


def validate_max_value(value) -> None:
   if value > 100:
       raise ValidationError(
           "%(value)s es mayor que el valor máximo permitido 100",
           params={"value": value},
       )


class Order(models.Model):
    ship_from = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Lugar de origen", related_name="orders_from")
    ship_to = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Lugar de destino", related_name="orders_to")
    commodity = models.CharField(max_length=255, verbose_name="Mercancía")
    value = models.IntegerField(verbose_name="Valor")
    volume = models.IntegerField(verbose_name="Volumen", default=0, validators=[validate_max_value])
    date = models.DateField(verbose_name="Fecha", auto_now_add=True)
    required_delivery_date = models.DateField(verbose_name="Fecha de entrega requerida")
    tax_percentage = models.FloatField(verbose_name="Porcentaje de impuesto", default=0)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ON_HOLD, verbose_name="Estado")
    
    class Meta:
        verbose_name = "Órden"
        verbose_name_plural = "Órdenes"

    def __str__(self) -> str:
        return f"{self.commodity} - {self.ship_from} to {self.ship_to}"

    @cached_property
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "Order Number": [self.pk],
            "Ship From": [self.ship_from.to_calculate],
            "Ship To": [self.ship_to.to_calculate],
            "Commodity": [self.commodity],
            "Order Value": [self.value],
            "Volume": [self.volume],
            "Order Date": [pd.to_datetime(self.date, format="%d/%m/%Y")],
            "Required Delivery Date": [pd.to_datetime(self.required_delivery_date, format="%d/%m/%Y")],
            "Tax Percentage": [self.tax_percentage]
        })
    
    def optimize_route(self) -> str:
        order = self.to_dataframe
        routes = Route.objects.routes_dataframe()
        m = CVXPY()
        m.set_param(routes, order)
        m.build_model()
        m.solve_model()
        
        try:
            t = m.solution_txt(order)
            print(t)
            return t
        except NotSolvable as error:
            return error.args[0]
        
        
class OrderOptimized(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Órden", related_name="optimizeds")
    
