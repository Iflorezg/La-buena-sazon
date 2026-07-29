from django.contrib.auth.decorators import login_required, user_passes_test


def staff_required(view_func):
    """Restringe la vista al personal interno (cocina, caja, logística)."""
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))


def domiciliario_required(view_func):
    """Restringe la vista a cuentas con rol de domiciliario."""
    return login_required(user_passes_test(lambda u: u.role == u.Role.DOMICILIARIO)(view_func))
