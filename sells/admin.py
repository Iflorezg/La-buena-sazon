from django.contrib import admin

from sells.models import Product, Order, OrderItem, Domicilio, Venta

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('venta_id', 'fecha', 'total')
    readonly_fields = ('fecha',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'created_at', 'status', 'total')
    list_filter = ('status',)
    inlines = [OrderItemInline]

admin.site.register(Product)

@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('domicilio_id', 'user', 'order', 'domiciliario', 'total', 'created_at')
    list_filter = ('domiciliario',)
    search_fields = ('user__username', 'address')