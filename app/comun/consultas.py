# app/comun/consultas.py    Consultas de LECTURA que usan varios equipos.
# Si tu equipo necesita una consulta compartida nueva, pídela con un Issue.
from app import db

# CONTRATO: valores exactos de registro_asistencia.estatus y notificacion.tipo
ESTATUS = ("Puntual", "Retardo", "Falta", "Falta justificada", "Salida anticipada")

# Clase CSS de la insignia de cada estatus (ver Guía de estilos)
INSIGNIA = {
    "Puntual": "insignia-puntual",
    "Retardo": "insignia-retardo",
    "Falta": "insignia-falta",
    "Falta justificada": "insignia-justificada",
    "Salida anticipada": "insignia-salida",
}


def alumno_por_uid(uid):
    """Busca al dueño de una credencial ACTIVA. Devuelve None si no existe."""
    return db.consultar_uno(
        """SELECT a.alumno_id, a.matricula, a.nombre, a.apellidos, a.grupo_id
           FROM credencial c
           JOIN alumno a ON a.alumno_id = c.alumno_id
           WHERE c.uid_rfid = %s AND c.estatus = 'Activa' AND a.estado = 'Activo'""",
        (uid,),
    )


def horario_del_dia(grupo_id, dia_semana):
    """Horario de un grupo para un día (1 = lunes ... 5 = viernes)."""
    return db.consultar_uno(
        "SELECT * FROM horario WHERE grupo_id = %s AND dia_semana = %s",
        (grupo_id, dia_semana),
    )


def grupos_con_carrera():
    """Lista de grupos con el nombre de su carrera (para filtros y menús)."""
    return db.consultar(
        """SELECT g.grupo_id, g.clave, g.turno, g.semestre, c.nombre AS carrera
           FROM grupo g JOIN carrera c ON c.carrera_id = g.carrera_id
           ORDER BY c.nombre, g.clave"""
    )
