from django.db import models
from django.utils.functional import cached_property

from .constants import PortType, Province

class Location(models.Model):
    province = models.CharField(max_length=2, choices=Province.choices, verbose_name="Provincia")
    port_type = models.CharField(max_length=2, choices=PortType.choices, verbose_name="Tipo de puerto")
    
    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ["province"]
        unique_together = ['province', 'port_type']
        
    def __str__(self) -> str:
        return f"{self.province} {self.port_type}"
    
    @cached_property
    def to_calculate(self) -> str:
        return f"{self.province} {self.port_type}"
    