import json
from django.shortcuts import render, redirect
from sells.models import Product, Order, OrderItem, Domicilio, Venta

def menu(request):
    context = {'productos': Product.objects.all()}
    if request.method == 'POST' and 'finalizar_pedido' in request.POST:
        carrito_json = request.POST.get('carrito_data')
        if carrito_json:
            try:
                carrito = json.loads(carrito_json)
                if carrito:
                    # Calcular el total primero
                    total_subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
                    total_con_impuestos = total_subtotal * 1.08
                    
                    # Crear la orden
                    nueva_orden = Order.objects.create(total=total_con_impuestos)
                    
                    # Registrar el domicilio si el usuario está autenticado
                    if request.user.is_authenticated:
                        nuevo_domicilio = Domicilio.objects.create(
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
                    
                    return redirect('menu') 
            except Exception as e:
                print(f"Error procesando pedido: {e}")
                
    return render(request, "menu.html", context)

def agregar_al_carrito(request):
    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')
        # buscar el platillo y agregarlo al carrito (sesión, BD, etc.)
    return redirect('menu')  # vuelve a la página del menú

def sumar_cantidad(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
    return redirect('menu')

def restar_cantidad(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
    return redirect('menu')

def finalizar_pedido(request):
    if request.method == 'POST':
        # crear la orden, limpiar carrito, etc.
        pass
    return redirect('confirmacion_pedido')

def imprimir_pre_cuenta(request):
    if request.method == 'POST':
        # generar PDF o vista imprimible
        pass
    return redirect('pre_cuenta')
