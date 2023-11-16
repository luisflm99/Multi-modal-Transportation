from django.db import models

class Status(models.TextChoices):
    ON_HOLD = "OH", "En espera"
    IN_PROCESS = "IP", "En proceso"
    PROCESSED = "PR", "Procesada"
    
class Province(models.TextChoices):
    PINAR_DEL_RIO = "PR", "Pinar del Río"
    ARTEMISA = "AR", "Artemisa"
    LA_HABANA = "LH", "La Habana"
    MAYABEQUE = "MA", "Mayabeque"
    MATANZAS = "MT", "Matanzas"
    CIENFUEGOS = "CF", "Cienfuegos"
    VILLA_CLARA = "VC", "Villa Clara"
    SANCTI_SPIRITUS = "SS", "Sancti Spíritus"
    CIEGO_DE_AVILA = "CA", "Ciego de Ávila"
    CAMAGUEY = "CM", "Camagüey"
    LAS_TUNAS = "LT", "Las Tunas"
    HOLGUIN = "HG", "Holguín"
    GRANMA = "GR", "Granma"
    SANTIAGO_DE_CUBA = "SC", "Santiago de Cuba"
    GUANTANAMO = "GT", "Guantánamo"
    ISLA_DE_LA_JUVENTUD = "IJ", "Isla de la Juventud"

class PortType(models.TextChoices):
    AIRPORT = "AP", "Aereopuerto"
    RAILWAY_STATION = "ET", "Estación de Tren"
    WAREHOUSE = "AL", "Almacén"
    PORT = "PU", "Puerto"

class TravelMode(models.TextChoices):
    AIR = "AI", "Aéreo"
    RAIL = "RA", "Ferrocarril"
    TRUCK = "TR", "Camión"
    SEA = "SE", "Marítimo"