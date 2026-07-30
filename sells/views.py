import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import domiciliario_required, staff_required
from sells.models import Domicilio, Order, OrderItem, Product, Venta


IMPUESTO = 0.08  # 8% — debe coincidir con el porcentaje mostrado en menu.html


def menu(request):
    context = {
        'productos': Product.objects.all(),
        'categorias': Product.Category.choices,
    }
    if request.method == 'POST' and 'finalizar_pedido' in request.POST:
        carrito_json = request.POST.get('carrito_data')
        es_domicilio = request.POST.get('es_domicilio') == 'on'
        try:
            carrito = json.loads(carrito_json) if carrito_json else []
            if not carrito:
                messages.error(request, "Tu carrito está vacío. Añade productos antes de finalizar el pedido.")
            else:
                # Calcular el total primero
                total_subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
                total_con_impuestos = total_subtotal * (1 + IMPUESTO)

                # Crear la orden
                nueva_orden = Order.objects.create(total=total_con_impuestos)

                # Registrar el pedido a domicilio si el cliente lo solicitó explícitamente
                if es_domicilio and request.user.is_authenticated:
                    Domicilio.objects.create(
                        user=request.user,
                        order=nueva_orden,
                        total=total_con_impuestos,
                        address=request.user.address if hasattr(request.user, 'address') else "No especificada"
                    )

                # Crear los items de la orden y preparar descripción para Venta
                detalles_productos = []
                for item in carrito:
                    producto = Product.objects.get(product_id=item['id'])
                    OrderItem.objects.create(
                        order=nueva_orden,
                        product=producto,
                        quantity=item['cantidad'],
                        price=item['precio']
                    )
                    detalles_productos.append(f"{item['cantidad']} x {producto.product} (${item['precio']})")

                # Registrar la venta
                Venta.objects.create(
                    total=total_con_impuestos,
                    productos_vendidos=", ".join(detalles_productos),
                    orden=nueva_orden
                )

                messages.success(request, f"¡Pedido #{nueva_orden.order_id} registrado con éxito!")
                return redirect('menu')
        except (json.JSONDecodeError, KeyError, Product.DoesNotExist):
            messages.error(request, "No pudimos procesar tu pedido. Intenta de nuevo.")

    return render(request, "menu.html", context)


@staff_required
def panel(request):
    context = {
        'ordenes_activas': Order.objects.exclude(status=Order.Status.ENTREGADO).count(),
        'domicilios_pendientes': Domicilio.objects.filter(domiciliario__isnull=True).count(),
        'domiciliarios_disponibles': get_user_model().objects.filter(
            role=get_user_model().Role.DOMICILIARIO, is_available=True
        ).count(),
    }
    return render(request, "panel.html", context)


# ===================== Cocina =====================

@staff_required
def cocina_ordenes(request):
    ordenes = (
        Order.objects
        .exclude(status=Order.Status.ENTREGADO)
        .prefetch_related('items__product')
        .order_by('created_at')
    )
    return render(request, "cocina.html", {
        'ordenes': ordenes,
        'estados': Order.Status.choices,
    })


@staff_required
@require_POST
def actualizar_estado_orden(request, order_id):
    orden = get_object_or_404(Order, pk=order_id)
    nuevo_estado = request.POST.get('status')
    if nuevo_estado in Order.Status.values:
        orden.status = nuevo_estado
        orden.save(update_fields=['status'])
        messages.success(request, f"Orden #{orden.order_id} actualizada a «{orden.get_status_display()}».")
    else:
        messages.error(request, "Estado no válido.")
    return redirect('cocina_ordenes')


# ===================== Cuenta =====================

@staff_required
def cuentas(request):
    ordenes = Order.objects.order_by('-created_at')
    return render(request, "cuentas.html", {'ordenes': ordenes})


@staff_required
def ver_cuenta(request, order_id):
    orden = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=order_id)
    domicilio = getattr(orden, 'domicilio', None)
    subtotal = sum(item.price * item.quantity for item in orden.items.all())
    return render(request, "cuenta_detalle.html", {
        'orden': orden,
        'domicilio': domicilio,
        'subtotal': subtotal,
    })


# ===================== Domiciliarios =====================

@staff_required
def disponibilidad_domiciliarios(request):
    Account = get_user_model()
    domiciliarios = Account.objects.filter(role=Account.Role.DOMICILIARIO).order_by('-is_available', 'username')
    return render(request, "domiciliarios_disponibilidad.html", {'domiciliarios': domiciliarios})


@staff_required
def asignar_domicilios(request):
    Account = get_user_model()
    if request.method == 'POST':
        domicilio = get_object_or_404(Domicilio, pk=request.POST.get('domicilio_id'))
        domiciliario_id = request.POST.get('domiciliario_id')
        domiciliario = get_object_or_404(
            Account, pk=domiciliario_id, role=Account.Role.DOMICILIARIO, is_available=True
        )
        domicilio.domiciliario = domiciliario
        domicilio.save(update_fields=['domiciliario'])
        messages.success(request, f"Domicilio #{domicilio.domicilio_id} asignado a {domiciliario.username}.")
        return redirect('asignar_domicilios')

    domicilios_pendientes = Domicilio.objects.filter(domiciliario__isnull=True).order_by('created_at')
    domiciliarios_disponibles = Account.objects.filter(role=Account.Role.DOMICILIARIO, is_available=True)
    return render(request, "asignar_domicilios.html", {
        'domicilios_pendientes': domicilios_pendientes,
        'domiciliarios_disponibles': domiciliarios_disponibles,
    })


# ===================== Panel del domiciliario =====================

@domiciliario_required
def mis_domicilios(request):
    domicilios = request.user.domicilios_asignados.order_by('-created_at')
    return render(request, "mis_domicilios.html", {'domicilios': domicilios})


@domiciliario_required
@require_POST
def toggle_disponibilidad(request):
    request.user.is_available = not request.user.is_available
    request.user.save(update_fields=['is_available'])
    estado = "disponible" if request.user.is_available else "no disponible"
    messages.success(request, f"Ahora estás marcado como {estado}.")
    return redirect('mis_domicilios')
