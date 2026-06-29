# MODULO PELICULAS
# Contiene TODO lo relacionado con peliculas:
# - Buscar (dueño y cliente)
# - Registrar (formulario completo con director, actores, ejemplares)
# - Modificar (buscar, seleccionar, editar)
# - Eliminar (buscar, seleccionar, confirmar, borrar)

import flet as ft
from conexion import con, cur
from utilidades import snackbar, volver_dueno, volver_cliente

# ─────────────────────────────────────────────
# FUNCIONES DE CONSULTA (COMPARTIDAS)
# ─────────────────────────────────────────────

# Busca peliculas cuyo titulo contenga el texto ingresado.
# SQL: JOIN con director para mostrar el nombre del director.
# Si texto esta vacio, devuelve TODAS las peliculas.
def _buscar(texto):
    sql = "SELECT p.id_pelicula, p.titulo, p.nacionalidad, p.productora, p.anio, d.nombre FROM pelicula p LEFT JOIN director d ON p.id_director = d.id_director"
    if texto:
        sql += " WHERE p.titulo LIKE %s"  # Busqueda parcial con %
    cur.execute(sql + " ORDER BY p.titulo", (f"%{texto}%",) if texto else ())
    return cur.fetchall()

# Igual que _buscar pero agrega una columna extra:
# "disponibles" = cantidad de ejemplares con estado 'Disponible'.
# Solo muestra peliculas que tengan al menos 1 disponible (HAVING).
# Se usa en el panel del cliente ("Ver Peliculas").
def _buscar_con_disponibles(texto):
    sql = "SELECT p.id_pelicula, p.titulo, p.nacionalidad, p.productora, p.anio, d.nombre, (SELECT COUNT(*) FROM ejemplar e WHERE e.id_pelicula = p.id_pelicula AND e.estado = 'Disponible') AS disponibles FROM pelicula p LEFT JOIN director d ON p.id_director = d.id_director"
    if texto:
        sql += " WHERE p.titulo LIKE %s"
    cur.execute(sql + " HAVING disponibles > 0 ORDER BY p.titulo", (f"%{texto}%",) if texto else ())
    return cur.fetchall()

# ─────────────────────────────────────────────
# PANTALLA DE BUSQUEDA (REUTILIZABLE)
# ─────────────────────────────────────────────

# Esta funcion se ejecuta cada vez que el usuario escribe en el campo de busqueda
# o cuando se carga la pantalla por primera vez (mostrar_todos=True).
# Recibe la funcion de consulta (query_fn) y opcionalmente un boton con su accion.
def _act_buscar(lv, txt, page, query_fn, btn_texto=None, al_clickear=None, mostrar_todos=True):
    lv.controls.clear()
    # mostrar_todos=False se usa en modificar/eliminar (solo busca si hay texto)
    if mostrar_todos or txt.value:
        for r in query_fn(txt.value):
            # r[1]=titulo, r[5]=director, r[4]=año, r[3]=productora, r[2]=nacionalidad
            c = [ft.Text(f"{r[1]} - {r[5] or 'Sin director'} ({r[4]})"), ft.Text(f"{r[3]} | {r[2]}")]
            # Si la consulta trajo la columna "disponibles" (solo cliente), la muestra
            if len(r) > 6:
                c.append(ft.Text(f"Disp: {r[6]}"))
            # Si hay un boton (Modificar/Eliminar), lo agrega con su accion
            # Usa lambda con pid=r[0] para capturar el id de cada pelicula
            if btn_texto and al_clickear:
                c.append(ft.ElevatedButton(btn_texto, on_click=lambda e, pid=r[0]: al_clickear(pid)))
            c.append(ft.Divider())
            lv.controls.append(ft.Column(c))
    page.update()

# Crea la pantalla completa: titulo, campo de busqueda, lista y boton Volver.
# Es reutilizada por: mostrar_buscar, mostrar_ver_peliculas, mostrar_modificar, mostrar_eliminar
def _buscar_pelis(page, titulo, query_fn, volver_fn, btn_texto=None, al_clickear=None, mostrar_todos=True):
    page.clean()
    lv = ft.ListView()
    txt = ft.TextField(label="Buscar", on_change=lambda e: _act_buscar(lv, txt, page, query_fn, btn_texto, al_clickear, mostrar_todos))
    page.add(ft.Column([ft.Text(titulo), txt, lv, ft.ElevatedButton("Volver", on_click=lambda e: volver_fn(page))]))
    # Si mostrar_todos=True, carga la lista inmediatamente (buscar/ver peliculas)
    if mostrar_todos:
        _act_buscar(lv, txt, page, query_fn, btn_texto, al_clickear, mostrar_todos)

# ─────────────────────────────────────────────
# WRAPPERS (cada funcion publica llama a _buscar_pelis con sus parametros)
# ─────────────────────────────────────────────

# Dueño: busca peliculas (solo lectura, sin botones)
def mostrar_buscar(page):
    _buscar_pelis(page, "BUSCAR PELICULA", _buscar, volver_dueno)

# Cliente: busca peliculas con ejemplares disponibles
def mostrar_ver_peliculas(page):
    _buscar_pelis(page, "PELICULAS", _buscar_con_disponibles, volver_cliente)

# Dueño: busca y selecciona una pelicula para modificarla
def mostrar_modificar(page):
    _buscar_pelis(page, "MODIFICAR PELICULA", _buscar, volver_dueno, "Modificar", lambda pid: _form_modificar(page, pid), False)

# Dueño: busca y selecciona una pelicula para eliminarla
def mostrar_eliminar(page):
    _buscar_pelis(page, "ELIMINAR PELICULA", _buscar, volver_dueno, "Eliminar", lambda pid: _confirmar_eliminar(page, pid), False)

# ─────────────────────────────────────────────
# MODIFICAR
# ─────────────────────────────────────────────

# Muestra el formulario con los datos actuales de la pelicula para editarlos
def _form_modificar(page, id_peli):
    # SQL: trae todos los campos de la pelicula por su ID
    cur.execute("SELECT * FROM pelicula WHERE id_pelicula = %s", (id_peli,))
    peli = cur.fetchone()
    if not peli:
        snackbar(page, "Película no existe"); volver_dueno(page); return
    page.clean()
    # Crea los campos con los valores actuales precargados
    t_tit = ft.TextField(label="Título", value=peli[1])
    t_nac = ft.TextField(label="Nacionalidad", value=peli[2])
    t_prod = ft.TextField(label="Productora", value=peli[3])
    t_anio = ft.TextField(label="Año", value=str(peli[4]))
    t_dir = ft.TextField(label="ID del director", value=str(peli[5]))
    page.add(ft.Column([ft.Text("MODIFICAR PELICULA"), t_tit, t_nac, t_prod, t_anio, t_dir, ft.ElevatedButton("Guardar", on_click=lambda e: _guardar_modificar(page, t_tit, t_nac, t_prod, t_anio, t_dir, id_peli)), ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))]))

# Ejecuta el UPDATE en la base de datos con los nuevos valores
def _guardar_modificar(page, t_tit, t_nac, t_prod, t_anio, t_dir, id_peli):
    if not all([t_tit.value, t_nac.value, t_prod.value, t_anio.value, t_dir.value]):
        snackbar(page, "Todos los campos son obligatorios"); return
    try:
        # SQL: actualiza los campos de la pelicula
        cur.execute("UPDATE pelicula SET titulo=%s, nacionalidad=%s, productora=%s, anio=%s, id_director=%s WHERE id_pelicula=%s", (t_tit.value, t_nac.value, t_prod.value, int(t_anio.value), int(t_dir.value), id_peli))
        con.commit()
        snackbar(page, "Película modificada"); volver_dueno(page)
    except Exception as ex:
        con.rollback(); snackbar(page, f"Error: {ex}")

# ─────────────────────────────────────────────
# ELIMINAR
# ─────────────────────────────────────────────

# Pantalla de confirmacion antes de borrar
def _confirmar_eliminar(page, id_peli):
    # SQL: trae el titulo para mostrarlo en la confirmacion
    cur.execute("SELECT titulo FROM pelicula WHERE id_pelicula = %s", (id_peli,))
    titulo = cur.fetchone()[0]
    page.clean()
    page.add(ft.Column([ft.Text(f"¿Eliminar {titulo}?"), ft.Text("Se borrarán ejemplares y alquileres relacionados."), ft.ElevatedButton("Sí, eliminar", on_click=lambda e: _eliminar_peli(page, id_peli)), ft.ElevatedButton("No", on_click=lambda e: mostrar_eliminar(page))]))

# Ejecuta la eliminacion en cascada:
# 1. Borra los alquileres de los ejemplares de esta pelicula
# 2. Borra los ejemplares
# 3. Borra las relaciones pelicula-actor
# 4. Borra la pelicula
def _eliminar_peli(page, id_peli):
    try:
        cur.execute("DELETE FROM alquiler WHERE id_ejemplar IN (SELECT id_ejemplar FROM ejemplar WHERE id_pelicula = %s)", (id_peli,))
        cur.execute("DELETE FROM ejemplar WHERE id_pelicula = %s", (id_peli,))
        cur.execute("DELETE FROM pelicula_actor WHERE id_pelicula = %s", (id_peli,))
        cur.execute("DELETE FROM pelicula WHERE id_pelicula = %s", (id_peli,))
        con.commit()
        snackbar(page, "Película eliminada"); volver_dueno(page)
    except Exception as ex:
        con.rollback(); snackbar(page, f"Error: {ex}")

# ─────────────────────────────────────────────
# REGISTRAR
# ─────────────────────────────────────────────

# Cuando el usuario cambia la "Cantidad de actores", esta funcion genera
# esa cantidad de formularios (Nombre, Nacionalidad, Sexo) dinamicamente.
def _cambiar_act(e, t_cant_act, cont_act, ult_cant, page):
    try:
        cant = int(t_cant_act.value) if t_cant_act.value else 0
    except:
        cant = 0
    if cant == ult_cant[0]:  # Si no cambio la cantidad, no hace nada
        return
    ult_cant[0] = cant
    cont_act.controls.clear()
    for i in range(cant):
        cont_act.controls.append(ft.Column([ft.Text(f"Actor {i+1}"), ft.TextField(label="Nombre"), ft.TextField(label="Nacionalidad"), ft.TextField(label="Sexo"), ft.Divider()]))
    page.update()

# Guarda la pelicula completa en una sola transaccion:
# 1. Busca o crea el director
# 2. Inserta la pelicula
# 3. Inserta cada actor y su relacion con la pelicula
# 4. Crea los ejemplares con estado "Disponible"
# Si algo falla, se hace rollback de todo.
def _guardar_peli(page, t_tit, t_nac, t_prod, t_anio, t_dir_nom, t_dir_nac, t_cant_act, t_cant_ej, cont_act):
    if not all([t_tit.value, t_nac.value, t_prod.value, t_anio.value, t_dir_nom.value, t_dir_nac.value, t_cant_act.value, t_cant_ej.value]):
        snackbar(page, "Todos los campos son obligatorios"); return
    try:
        int(t_anio.value); int(t_cant_act.value); cant_ej = int(t_cant_ej.value)
    except:
        snackbar(page, "Año, actores y ejemplares deben ser números"); return
    # Recolecta los datos de los actores desde los formularios dinámicos
    actores = []
    for col in cont_act.controls:
        v = [col.controls[1].value, col.controls[2].value, col.controls[3].value]
        if not all(v):
            snackbar(page, "Todos los campos de actores son obligatorios"); return
        actores.append(v)
    try:
        # 1. Buscar si el director ya existe (por nombre), si no, crearlo
        cur.execute("SELECT id_director FROM director WHERE nombre = %s", (t_dir_nom.value,))
        r = cur.fetchone()
        id_dir = r[0] if r else None
        if not id_dir:
            cur.execute("INSERT INTO director (nombre, nacionalidad) VALUES (%s, %s)", (t_dir_nom.value, t_dir_nac.value))
            id_dir = cur.lastrowid  # Obtiene el ID autoincremental generado
        # 2. Insertar la pelicula
        cur.execute("INSERT INTO pelicula (titulo, nacionalidad, productora, anio, id_director) VALUES (%s, %s, %s, %s, %s)", (t_tit.value, t_nac.value, t_prod.value, int(t_anio.value), id_dir))
        id_peli = cur.lastrowid
        # 3. Insertar cada actor y la relacion pelicula-actor
        for nom, nac, sex in actores:
            cur.execute("INSERT INTO actor (nombre, nacionalidad, sexo) VALUES (%s, %s, %s)", (nom, nac, sex))
            cur.execute("INSERT INTO pelicula_actor (id_pelicula, id_actor) VALUES (%s, %s)", (id_peli, cur.lastrowid))
        # 4. Crear los ejemplares (todos "Disponible")
        for i in range(cant_ej):
            cur.execute("INSERT INTO ejemplar (numero_ejemplar, estado, id_pelicula) VALUES (%s, 'Disponible', %s)", (i+1, id_peli))
        con.commit()
        snackbar(page, f"Película registrada con {cant_ej} ejemplares")
        volver_dueno(page)
    except Exception as ex:
        con.rollback(); snackbar(page, f"Error: {ex}")

# Muestra el formulario completo para registrar una nueva pelicula
def mostrar_registrar(page):
    page.clean()
    # Todos los campos del formulario
    t_tit = ft.TextField(label="Titulo")
    t_nac = ft.TextField(label="Nacionalidad")
    t_prod = ft.TextField(label="Productora")
    t_anio = ft.TextField(label="Año")
    t_dir_nom = ft.TextField(label="Nombre del director")
    t_dir_nac = ft.TextField(label="Nacionalidad del director")
    t_cant_act = ft.TextField(label="Cantidad de actores")
    t_cant_ej = ft.TextField(label="Cantidad de ejemplares")
    cont_act = ft.Column()        # Contenedor para los formularios de actores
    ult_cant = [0]                # Lista mutable para recordar la ultima cantidad
    # Cuando cambia "Cantidad de actores", se generan los campos dinamicamente
    t_cant_act.on_change = lambda e: _cambiar_act(e, t_cant_act, cont_act, ult_cant, page)
    page.add(ft.Column([ft.Text("REGISTRAR PELICULA"), t_tit, t_nac, t_prod, t_anio, ft.Text("DIRECTOR"), t_dir_nom, t_dir_nac, ft.Text("ACTORES"), t_cant_act, cont_act, t_cant_ej, ft.ElevatedButton("Guardar", on_click=lambda e: _guardar_peli(page, t_tit, t_nac, t_prod, t_anio, t_dir_nom, t_dir_nac, t_cant_act, t_cant_ej, cont_act)), ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))], scroll=ft.ScrollMode.AUTO))
