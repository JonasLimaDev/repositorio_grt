from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Autor)
admin.site.register(Categoria)

admin.site.register(NivelEnsino)

admin.site.register(Subcategoria)

admin.site.register(Item)
