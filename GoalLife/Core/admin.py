from django.contrib import admin
from .models import Categoria, Consejo, Meta, Ingreso, Gasto, Obligacion

# Register your models here.
# Registro básico para ver las tablas en el panel
admin.site.register(Categoria)
admin.site.register(Consejo)
admin.site.register(Meta)
admin.site.register(Ingreso)
admin.site.register(Gasto)
admin.site.register(Obligacion)
