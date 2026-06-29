import flet as ft
from conexion import con, cur
from utilidades import snackbar, volver_dueno

def mostrar_socios(page):
    page.clean()
    cur.execute("""SELECT s.dni, s.nombre, p.titulo, e.numero_ejemplar
        FROM socio s
        LEFT JOIN alquiler a ON s.dni = a.dni_socio AND a.fecha_devolucion IS NULL
        LEFT JOIN ejemplar e ON a.id_ejemplar = e.id_ejemplar
        LEFT JOIN pelicula p ON e.id_pelicula = p.id_pelicula
        ORDER BY s.nombre, p.titulo""")
    datos = cur.fetchall()
    socios = {}
    for d in datos:
        if d[0] not in socios:
            socios[d[0]] = {"nombre": d[1], "pelis": []}
        if d[2]:
            socios[d[0]]["pelis"].append(f"{d[2]} (Ej. N°{d[3]})")
    if not socios:
        page.add(ft.Column([ft.Text("No hay socios"), ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))]))
        return
    lv = ft.ListView()
    for dni, data in sorted(socios.items(), key=lambda x: x[1]["nombre"]):
        c = [ft.Row([ft.Text(f"{data['nombre']} (DNI: {dni})"), ft.ElevatedButton("Eliminar", on_click=lambda e, d=dni: _confirmar(page, d))])]
        if data["pelis"]:
            for p in data["pelis"]:
                c.append(ft.Text(f"  - {p}"))
        else:
            c.append(ft.Text("  Sin alquileres activos"))
        c.append(ft.Divider())
        lv.controls.append(ft.Column(c))
    page.add(ft.Column([ft.Text("SOCIOS"), lv, ft.ElevatedButton("Volver", on_click=lambda e: volver_dueno(page))]))

def _confirmar(page, dni):
    page.clean()
    page.add(ft.Column([ft.Text("¿Eliminar socio?"), ft.Text("Se eliminarán también sus alquileres."), ft.ElevatedButton("Sí, eliminar", on_click=lambda e: _eliminar(page, dni)), ft.ElevatedButton("No", on_click=lambda e: mostrar_socios(page))]))

def _eliminar(page, dni):
    try:
        cur.execute("UPDATE socio SET avalador_dni = NULL WHERE avalador_dni = %s", (dni,))
        cur.execute("DELETE FROM alquiler WHERE dni_socio = %s", (dni,))
        cur.execute("DELETE FROM socio WHERE dni = %s", (dni,))
        con.commit()
        snackbar(page, "Socio eliminado"); mostrar_socios(page)
    except Exception as ex:
        con.rollback(); snackbar(page, f"Error: {ex}")
