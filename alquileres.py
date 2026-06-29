# MODULO ALQUILERES
# Maneja todo el ciclo de alquiler:
# - Alquilar: registra socio (si es nuevo con avalador) -> selecciona pelicula -> selecciona ejemplar -> confirma
# - Mis Alquileres: consulta los alquileres activos de un socio
# - Devolver: busca los alquileres activos de un socio y permite devolverlos

import flet as ft
from conexion import con, cur
from utilidades import snackbar, volver_dueno, volver_cliente

# ═══════════════════════════════════════════════
# ALQUILAR (flujo completo: 4 pantallas)
# ═══════════════════════════════════════════════

# Pantalla 1: formulario de datos del socio
def mostrar_alquilar(page):
    page.clean()
    t_dni = ft.TextField(label="DNI")
    t_nom = ft.TextField(label="Nombre")
    t_aval = ft.TextField(label="Avalador (nuevo socio)")
    page.dni_socio = None  # Guarda el DNI en la pagina para usarlo en las siguientes pantallas
    page.add(ft.Column([ft.Text("ALQUILAR PELICULA"), ft.Text("Ingrese sus datos:"), t_dni, t_nom, t_aval, ft.ElevatedButton("Continuar", on_click=lambda e: _continuar(e, page, t_dni, t_nom, t_aval)), ft.ElevatedButton("Volver", on_click=lambda e: volver_cliente(page))]))

# Valida los datos y registra al socio si es nuevo (requiere avalador)
# SQL: busca el socio por DNI; si no existe, verifica el avalador y lo crea
def _continuar(e, page, t_dni, t_nom, t_aval):
    dni, nombre = t_dni.value.strip(), t_nom.value.strip()
    if not dni or not nombre:
        snackbar(page, "DNI y nombre obligatorios"); return
    cur.execute("SELECT nombre FROM socio WHERE dni = %s", (dni,))
    if not cur.fetchone():  # Socio no existe, hay que registrarlo
        aval = t_aval.value.strip()
        if not aval: snackbar(page, "Avalador requerido para nuevo socio"); return
        if aval == dni: snackbar(page, "Mismo DNI"); return
        cur.execute("SELECT COUNT(*) FROM socio WHERE dni = %s", (aval,))
        if cur.fetchone()[0] == 0: snackbar(page, "Avalador no existe"); return
        # SQL: inserta el nuevo socio con el avalador
        cur.execute("INSERT INTO socio (dni, nombre, avalador_dni) VALUES (%s, %s, %s)", (dni, nombre, aval))
        con.commit()
    page.dni_socio = dni  # Guarda el DNI para las siguientes pantallas
    _mostrar_disponibles(page)  # Pasa a la pantalla 2

# Pantalla 2: muestra las peliculas con ejemplares disponibles
# SQL: selecciona peliculas con al menos 1 ejemplar "Disponible" (subconsulta en HAVING)
def _mostrar_disponibles(page):
    page.clean()
    lv = ft.ListView()
    cur.execute("""SELECT p.id_pelicula, p.titulo, d.nombre, p.anio,
        (SELECT COUNT(*) FROM ejemplar e WHERE e.id_pelicula = p.id_pelicula AND e.estado = 'Disponible') AS disponibles
        FROM pelicula p LEFT JOIN director d ON p.id_director = d.id_director
        HAVING disponibles > 0 ORDER BY p.titulo""")
    for r in cur.fetchall():
        lv.controls.append(ft.Column([ft.Text(f"{r[1]}"), ft.Text(f"Director: {r[2] or 'Sin director'} | Año: {r[3]} | Disp: {r[4]}"), ft.ElevatedButton("Alquilar", on_click=lambda e, pid=r[0], tit=r[1]: _seleccionar_ejemplar(page, pid, tit)), ft.Divider()]))
    if not lv.controls:
        page.add(ft.Column([ft.Text("No hay películas disponibles"), ft.ElevatedButton("Volver", on_click=lambda e: volver_cliente(page))]))
        page.dni_socio = None; return
    page.add(ft.Column([ft.Text("SELECCIONE PELICULA"), lv, ft.ElevatedButton("Volver", on_click=lambda e: volver_cliente(page))]))

# Pantalla 3: muestra los ejemplares disponibles de la pelicula seleccionada
# SQL: busca ejemplares donde id_pelicula = X AND estado = 'Disponible'
def _seleccionar_ejemplar(page, id_peli, titulo):
    page.clean()
    lv = ft.ListView()
    cur.execute("SELECT id_ejemplar, numero_ejemplar FROM ejemplar WHERE id_pelicula = %s AND estado = 'Disponible' ORDER BY numero_ejemplar", (id_peli,))
    for e in cur.fetchall():
        lv.controls.append(ft.Row([ft.Text(f"Ejemplar N° {e[1]}"), ft.ElevatedButton("Alquilar", on_click=lambda e2, ie=e[0], num=e[1]: _confirmar_alquiler(page, ie, num, titulo))]))
    if not lv.controls:
        snackbar(page, "Ya no hay ejemplares disponibles"); _mostrar_disponibles(page); return
    page.add(ft.Column([ft.Text(f"ALQUILAR: {titulo}"), lv, ft.ElevatedButton("Volver", on_click=lambda e: _mostrar_disponibles(page))]))

# Pantalla 4: confirma el alquiler y lo guarda en la base de datos
# Verifica: que no supere los 4 alquileres activos permitidos
# SQL: INSERT en alquiler + UPDATE estado del ejemplar a 'Alquilado'
def _confirmar_alquiler(page, id_ej, num, titulo):
    dni = page.dni_socio
    if not dni: snackbar(page, "Error"); volver_cliente(page); return
    try:
        # Cuenta los alquileres activos del socio (fecha_devolucion IS NULL)
        cur.execute("SELECT COUNT(*) FROM alquiler WHERE dni_socio = %s AND fecha_devolucion IS NULL", (dni,))
        if cur.fetchone()[0] >= 4: snackbar(page, "Máximo 4 alquileres activos"); return
        # SQL: inserta el alquiler con fecha actual (CURDATE()) y sin fecha_devolucion
        cur.execute("INSERT INTO alquiler (fecha_inicio, dni_socio, id_ejemplar) VALUES (CURDATE(), %s, %s)", (dni, id_ej))
        # SQL: marca el ejemplar como alquilado
        cur.execute("UPDATE ejemplar SET estado = 'Alquilado' WHERE id_ejemplar = %s", (id_ej,))
        con.commit()
        snackbar(page, f"Alquiler exitoso: {titulo} (Ej. N°{num})")
        page.dni_socio = None; volver_cliente(page)
    except Exception as ex:
        con.rollback(); snackbar(page, f"Error: {ex}")

# ═══════════════════════════════════════════════
# MIS ALQUILERES (cliente)
# ═══════════════════════════════════════════════

# Muestra los alquileres activos de un socio (sin opcion a devolver)
# SQL: JOIN alquiler-ejemplar-pelicula, solo alquileres sin devolver
def _consultar_mis_alquileres(e, page, t_dni):
    dni = t_dni.value.strip()
    if not dni: snackbar(page, "Debe ingresar un DNI"); return
    cur.execute("SELECT nombre FROM socio WHERE dni = %s", (dni,))
    socio = cur.fetchone()
    if not socio: snackbar(page, "Socio no encontrado"); return
    page.clean()
    lv = ft.ListView()
    cur.execute("SELECT a.fecha_inicio, p.titulo, e.numero_ejemplar FROM alquiler a JOIN ejemplar e ON a.id_ejemplar = e.id_ejemplar JOIN pelicula p ON e.id_pelicula = p.id_pelicula WHERE a.dni_socio = %s AND a.fecha_devolucion IS NULL ORDER BY a.fecha_inicio DESC", (dni,))
    for a in cur.fetchall():
        lv.controls.append(ft.Column([ft.Text(f"{a[1]} - Ej. N°{a[2]}"), ft.Text(f"Alquilado: {a[0]}"), ft.Divider()]))
    if not lv.controls:
        lv.controls.append(ft.Text("No tiene alquileres activos."))
    page.add(ft.Column([ft.Text(f"ALQUILERES ({socio[0]})"), lv, ft.ElevatedButton("Volver", on_click=lambda e: volver_cliente(page))]))

def mostrar_mis_alquileres(page):
    page.clean()
    t_dni = ft.TextField(label="DNI")
    page.add(ft.Column([ft.Text("MIS ALQUILERES"), t_dni, ft.ElevatedButton("Consultar", on_click=lambda e: _consultar_mis_alquileres(e, page, t_dni)), ft.ElevatedButton("Volver", on_click=lambda e: volver_cliente(page))]))

# ═══════════════════════════════════════════════
# DEVOLVER (dueño)
# ═══════════════════════════════════════════════

# Busca los alquileres activos de un socio y permite devolverlos
# SQL: igual que mis_alquileres pero ademas trae id_alquiler e id_ejemplar para el UPDATE
def _buscar_devolver(e, page, t_dni):
    dni = t_dni.value.strip()
    if not dni: snackbar(page, "Debe ingresar un DNI"); return
    cur.execute("SELECT nombre FROM socio WHERE dni = %s", (dni,))
    socio = cur.fetchone()
    if not socio: snackbar(page, "Socio no encontrado"); return
    page.clean()
    lv = ft.ListView()
    cur.execute("SELECT a.id_alquiler, a.fecha_inicio, p.titulo, e.numero_ejemplar, e.id_ejemplar FROM alquiler a JOIN ejemplar e ON a.id_ejemplar = e.id_ejemplar JOIN pelicula p ON e.id_pelicula = p.id_pelicula WHERE a.dni_socio = %s AND a.fecha_devolucion IS NULL ORDER BY a.fecha_inicio DESC", (dni,))
    for a in cur.fetchall():
        lv.controls.append(ft.Column([ft.Text(f"{a[2]} - Ej. N°{a[3]} ({a[1]})"), ft.ElevatedButton("Devolver", on_click=lambda e, ida=a[0], ide=a[4], tit=a[2], num=a[3]: _procesar_devolver(ida, ide, tit, num, page)), ft.Divider()]))
    if not lv.controls:
        page.add(ft.Column([ft.Text(f"{socio[0]} no tiene alquileres activos."), ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))])); return
    page.add(ft.Column([ft.Text(f"DEVOLVER ({socio[0]})"), lv, ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))]))

# Procesa la devolucion: actualiza fecha_devolucion y cambia el estado del ejemplar
# SQL: UPDATE alquiler SET fecha_devolucion = CURDATE() + UPDATE ejemplar SET estado = 'Disponible'
def _procesar_devolver(id_alq, id_ej, titulo, num_ej, page):
    try:
        cur.execute("UPDATE alquiler SET fecha_devolucion = CURDATE() WHERE id_alquiler = %s", (id_alq,))
        cur.execute("UPDATE ejemplar SET estado = 'Disponible' WHERE id_ejemplar = %s", (id_ej,))
        con.commit()
        snackbar(page, f"{titulo} (Ej. N°{num_ej}) devuelta"); volver_dueno(page)
    except Exception as ex:
        con.rollback(); snackbar(page, f"Error: {ex}")

def mostrar_devolver(page):
    page.clean()
    t_dni = ft.TextField(label="DNI")
    page.add(ft.Column([ft.Text("DEVOLVER PELICULA"), t_dni, ft.ElevatedButton("Buscar", on_click=lambda e: _buscar_devolver(e, page, t_dni)), ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))]))
