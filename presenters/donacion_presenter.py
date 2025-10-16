# presenters/donacion_presenter.py
from models.donacion_model import DonacionModel
from models.tipo_donacion_model import TipoDonacionModel
from app import get_db_connection
import pymysql

class DonacionPresenter:
    def __init__(self):
        self.donacion_model = DonacionModel()
        self.tipo_donacion_model = TipoDonacionModel()

    def get_all(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.*, t.nombre as tipo_nombre, IFNULL(dn.nombre, '') as donante_nombre
                    FROM donaciones d
                    LEFT JOIN tipo_donacion t ON d.tipo_id = t.id
                    LEFT JOIN donantes dn ON d.donante_id = dn.id
                    ORDER BY d.id DESC
                """)
                return cursor.fetchall()
        finally:
            conn.close()

    def get(self, id):
        return self.donacion_model.get_by_id(id)

    def create(self, nombre, tipo_id, donante_id=None, monto=None, cantidad=None, descripcion=None):
        donacion_id = self.donacion_model.create(nombre, tipo_id, donante_id, monto, cantidad, descripcion)
        return self.get(donacion_id)

    def update(self, id, **kwargs):
        donacion = self.get(id)
        if not donacion:
            return None
        success = self.donacion_model.update(id,
                                            nombre=kwargs.get('nombre', donacion['nombre']),
                                            tipo_id=kwargs.get('tipo_id', donacion['tipo_id']),
                                            donante_id=kwargs.get('donante_id', donacion['donante_id']),
                                            monto=kwargs.get('monto', donacion['monto']),
                                            cantidad=kwargs.get('cantidad', donacion['cantidad']),
                                            descripcion=kwargs.get('descripcion', donacion['descripcion']))
        if success:
            return self.get(id)
        return None

    def deactivate(self, id):
        donacion = self.get(id)
        if not donacion:
            return None
        success = self.donacion_model.deactivate(id)
        if success:
            return self.get(id)
        return None

    def inventario_material(self):
        tipo = self.tipo_donacion_model.get_by_name('material')
        if not tipo:
            return []
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, COALESCE(d.cantidad, 0) as total_cantidad,
                           COALESCE(SUM(a.cantidad), 0) as asignado
                    FROM donaciones d
                    LEFT JOIN asignaciones a ON a.donacion_id = d.id
                    WHERE d.tipo_id = %s AND d.estado = TRUE
                    GROUP BY d.id, d.nombre, d.cantidad
                """, (tipo['id'],))
                totals = cursor.fetchall()
                result = []
                for row in totals:
                    disponible = int(row['total_cantidad']) - int(row['asignado'])
                    result.append({
                        'donacion_id': row['id'],
                        'nombre': row['nombre'],
                        'total': int(row['total_cantidad']),
                        'asignado': int(row['asignado']),
                        'disponible': disponible
                    })
                return result
        finally:
            conn.close()

    def inventario_economico(self):
        tipo = self.tipo_donacion_model.get_by_name('economico')
        if not tipo:
            return []
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT d.id, d.nombre, COALESCE(d.monto, 0) as total_monto,
                           COALESCE(SUM(a.monto), 0) as asignado
                    FROM donaciones d
                    LEFT JOIN asignaciones a ON a.donacion_id = d.id
                    WHERE d.tipo_id = %s AND d.estado = TRUE
                    GROUP BY d.id, d.nombre, d.monto
                """, (tipo['id'],))
                totals = cursor.fetchall()
                result = []
                for row in totals:
                    disponible = float(row['total_monto']) - float(row['asignado'])
                    result.append({
                        'donacion_id': row['id'],
                        'nombre': row['nombre'],
                        'total': float(row['total_monto']),
                        'asignado': float(row['asignado']),
                        'disponible': disponible
                    })
                return result
        finally:
            conn.close()