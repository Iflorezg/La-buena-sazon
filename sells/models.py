from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.CharField(max_length=500, default='')
    def __str__(self):
        return self.product
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0.0)

    def __str__(self):
        return f"Orden {self.order_id} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField() # Price at the time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.product}"
class Domicilio(models.Model):
    domicilio_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='domicilio')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0.0)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"Domicilio {self.domicilio_id} - {self.user.username if self.user else 'Anónimo'}"

class Venta(models.Model):
    venta_id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    productos_vendidos = models.TextField() # Descripción de los productos y cantidades
    total = models.FloatField()
    orden = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.venta_id} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"