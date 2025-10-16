from models.asignacion_model import AsignacionModel
from models.donacion_model import DonacionModel
from models.tipo_donacion_model import TipoDonacionModel
from app import get_db_connection
import pymysql

class AsignacionPresenter:
    def __init__(self):
        self.asignacion_model = AsignacionModel()
        self.donacion_model = DonacionModel()
        self.tipo_donacion_model = TipoDonacionModel()

    def get_all(self):
        return self.asignacion_model.get_all()

    def get_active_donations_with_available(self):
        donations = self.donacion_model.get_all(only_active=True)
        result = []
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                for don in donations:
                    tipo = self.tipo_donacion_model.get_by_id(don['tipo_id'])
                    if not tipo:
                        continue
                    if tipo['nombre'] == 'material':
                        cursor.execute("""
                            SELECT COALESCE(SUM(cantidad), 0) as asignado
                            FROM asignaciones
                            WHERE donacion_id = %s
                        """, (don['id'],))
                        asignado = cursor.fetchone()['asignado'] or 0
                        total = don['cantidad'] or 0
                        available = total - asignado
                        result.append({
                            'id': don['id'],
                            'nombre': don['nombre'],
                            'tipo': tipo['nombre'],
                            'available': available,
                            'unit': 'unidades'
                        })
                    elif tipo['nombre'] == 'economico':
                        cursor.execute("""
                            SELECT COALESCE(SUM(monto), 0) as asignado
                            FROM asignaciones
                            WHERE donacion_id = %s
                        """, (don['id'],))
                        asignado = cursor.fetchone()['asignado'] or 0.0
                        total = float(don['monto'] or 0.0)
                        available = total - asignado
                        result.append({
                            'id': don['id'],
                            'nombre': don['nombre'],
                            'tipo': tipo['nombre'],
                            'available': available,
                            'unit': 'USD'
                        })
                    else:
                        result.append({
                            'id': don['id'],
                            'nombre': don['nombre'],
                            'tipo': tipo['nombre'],
                            'available': None,
                            'unit': None
                        })
                return result
        finally:
            conn.close()

    def get_global_totals(self):
        total_monto = 0.0
        total_cantidad = 0
        donations = self.donacion_model.get_all(only_active=True)
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                for don in donations:
                    tipo = self.tipo_donacion_model.get_by_id(don['tipo_id'])
                    if not tipo:
                        continue
                    if tipo['nombre'] == 'material':
                        cursor.execute("""
                            SELECT COALESCE(SUM(cantidad), 0) as asignado
                            FROM asignaciones
                            WHERE donacion_id = %s
                        """, (don['id'],))
                        asignado = cursor.fetchone()['asignado'] or 0
                        total = don['cantidad'] or 0
                        total_cantidad += total - asignado
                    elif tipo['nombre'] == 'economico':
                        cursor.execute("""
                            SELECT COALESCE(SUM(monto), 0) as asignado
                            FROM asignaciones
                            WHERE donacion_id = %s
                        """, (don['id'],))
                        asignado = cursor.fetchone()['asignado'] or 0.0
                        total = float(don['monto'] or 0.0)
                        total_monto += total - asignado
                return {'total_monto': total_monto, 'total_cantidad': total_cantidad}
        finally:
            conn.close()

    def create(self, donacion_id, beneficiario_id, tipo_id, cantidad=None, monto=None):
        don = self.donacion_model.get_by_id(donacion_id)
        tipo = self.tipo_donacion_model.get_by_id(tipo_id)
        if not don or not tipo:
            return False, "Donación o tipo no encontrado"

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if tipo['nombre'] == 'material':
                    total = don['cantidad'] or 0
                    cursor.execute("""
                        SELECT COALESCE(SUM(cantidad), 0) as asignado
                        FROM asignaciones
                        WHERE donacion_id = %s
                    """, (donacion_id,))
                    asignado = cursor.fetchone()['asignado'] or 0
                    if cantidad is None or int(cantidad) <= 0:
                        return False, "Cantidad inválida"
                    if asignado + int(cantidad) > int(total):
                        return False, f"No hay suficiente cantidad disponible (disponible: {total - asignado})"
                elif tipo['nombre'] == 'economico':
                    total = float(don['monto'] or 0.0)
                    cursor.execute("""
                        SELECT COALESCE(SUM(monto), 0) as asignado
                        FROM asignaciones
                        WHERE donacion_id = %s
                    """, (donacion_id,))
                    asignado = cursor.fetchone()['asignado'] or 0.0
                    if monto is None or float(monto) <= 0:
                        return False, "Monto inválido"
                    if float(asignado) + float(monto) > float(total):
                        return False, f"No hay suficiente dinero disponible (disponible: {total - asignado})"
                asignacion_id = self.asignacion_model.create(donacion_id, beneficiario_id, tipo_id, cantidad, monto)
                return True, self.asignacion_model.get_by_id(asignacion_id)
        finally:
            conn.close()

    def delete(self, id):
        asignacion = self.asignacion_model.get_by_id(id)
        if not asignacion:
            return False, "Asignación no encontrada"
        success = self.asignacion_model.delete(id)
        if success:
            return True, "Eliminada"
        return False, "Error al eliminar"