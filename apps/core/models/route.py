import pandas as pd
from django.db import models
from django.utils.functional import cached_property

from .location import Location
from .constants import TravelMode
from ..managers import RouteManager


class Route(models.Model):
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="source_routes", verbose_name="Lugar de origen")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destination_routes", verbose_name="Lugar de destino")
    container_size = models.IntegerField(verbose_name="Tamaño del Contenedor", default=100)
    carrier = models.CharField(max_length=255, verbose_name="Transportista")
    travel_mode = models.CharField(max_length=2, choices=TravelMode.choices, verbose_name="Modo de Viaje")
    fixed_freight_cost = models.IntegerField(verbose_name="Costo Fijo de Flete", default=0)
    handling_cost = models.IntegerField(verbose_name="Costo de Manejo de Puerto/Aeropuerto/Estación de Tren", default=0)
    bunker_fuel_cost = models.IntegerField(verbose_name="Costo de Bunker/Combustible", default=0)
    documentation_cost = models.IntegerField(verbose_name="Costo de Documentación", default=0)
    equipment_cost = models.IntegerField(verbose_name="Costo de Equipamiento", default=0)
    extra_cost = models.IntegerField(verbose_name="Costo Extra", default=0)
    warehouse_cost = models.IntegerField(verbose_name="Costo de Almacén", default=0)
    transit_duty = models.FloatField(verbose_name="Derecho de Tránsito", default=0)
    custom_clearance_time = models.IntegerField(verbose_name="Tiempo de Despacho Aduanero")
    handling_time = models.IntegerField(verbose_name="Tiempo de Manejo de Puerto/Aeropuerto/Estación de Tren")
    extra_time = models.IntegerField(verbose_name="Tiempo Extra")
    transit_time = models.IntegerField(verbose_name="Tiempo de Tránsito")
    monday = models.BooleanField(verbose_name="Lunes", default=True)
    tuesday = models.BooleanField(verbose_name="Martes", default=True)
    wednesday = models.BooleanField(verbose_name="Miércoles", default=True)
    thursday = models.BooleanField(verbose_name="Jueves", default=True)
    friday = models.BooleanField(verbose_name="Viernes", default=True)
    saturday = models.BooleanField(verbose_name="Sábado", default=True)
    sunday = models.BooleanField(verbose_name="Domingo", default=True)
    
    objects = RouteManager()

    class Meta:
        verbose_name = "Ruta"
        unique_together = ['source', 'destination']
        ordering = ["source"]
        
    def __str__(self) -> str:
        return f"{self.source} --> {self.destination} - {self.warehouse_cost}"
    
    @cached_property
    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "Route Number": [self.pk],
            "Source": [self.source.to_calculate],
            "Destination": [self.destination.to_calculate],
            "Container Size": [self.container_size],
            "Carrier": [self.carrier],
            "Travel Mode": [self.travel_mode],
            "Fixed Freight Cost": [self.fixed_freight_cost],
            "Port/Airport/Rail Handling Cost": [self.handling_cost],
            "Bunker/Fuel Cost": [self.bunker_fuel_cost],
            "Documentation Cost": [self.documentation_cost],
            "Equipment Cost": [self.equipment_cost],
            "Extra Cost": [self.extra_cost],
            "Warehouse Cost": [self.warehouse_cost],
            "Transit Duty": [self.transit_duty],
            "Custom Clearance Time (hours)": [self.custom_clearance_time],
            "Port/Airport/Rail Handling Time (hours)": [self.handling_time],
            "Extra Time": [self.extra_time],
            "Transit Time (hours)": [self.transit_time],
            "Monday": [int(self.monday)],
            "Tuesday": [int(self.tuesday)],
            "Wednesday": [int(self.wednesday)],
            "Thursday": [int(self.thursday)],
            "Friday": [int(self.friday)],
            "Saturday": [int(self.saturday)],
            "Sunday": [int(self.sunday)],
        })
