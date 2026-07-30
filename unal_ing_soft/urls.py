"""
URL configuration for unal_ing_soft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from accounts.views import AccountLoginView, home, logout_view, profile_view
from sells import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Cuentas
    path('profile/', profile_view, name='profile'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # Menú y pedidos
    path('menu/', views.menu, name='menu'),

    # Panel de personal
    path('panel/', views.panel, name='panel'),

    # Cocina
    path('cocina/', views.cocina_ordenes, name='cocina_ordenes'),
    path('cocina/orden/<int:order_id>/estado/', views.actualizar_estado_orden, name='actualizar_estado_orden'),

    # Cuenta / facturación
    path('cuentas/', views.cuentas, name='cuentas'),
    path('cuentas/<int:order_id>/', views.ver_cuenta, name='ver_cuenta'),

    # Domiciliarios (personal de logística)
    path('domiciliarios/disponibilidad/', views.disponibilidad_domiciliarios, name='disponibilidad_domiciliarios'),
    path('domicilios/asignar/', views.asignar_domicilios, name='asignar_domicilios'),

    # Panel del domiciliario
    path('mis-domicilios/', views.mis_domicilios, name='mis_domicilios'),
    path('mis-domicilios/disponibilidad/', views.toggle_disponibilidad, name='toggle_disponibilidad'),
    path('mis-domicilios/<int:domicilio_id>/entregado/', views.marcar_entregado, name='marcar_entregado'),
]
