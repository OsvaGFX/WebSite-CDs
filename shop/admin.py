from django.contrib import admin
from .models import Category, Product, Comment  # Asegúrate de importar Comment

# Registro de modelos en el admin
admin.site.register(Category)
admin.site.register(Product)

# Registrando el modelo Comment
@admin.register(Comment)  # Puedes usar el decorador @admin.register para registrar el modelo
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'content', 'created_at')  # Campos a mostrar en la lista
    search_fields = ('user__username', 'product__title', 'content')  # Permite la búsqueda por estos campos
    list_filter = ('created_at',)  # Filtro por fecha de creación