# presenters/beneficiario_presenter.py
from models.beneficiario_model import BeneficiarioModel

class BeneficiarioPresenter:
    def __init__(self):
        self.beneficiario_model = BeneficiarioModel()

    def get_all(self):
        return self.beneficiario_model.get_all()

    def get(self, id):
        return self.beneficiario_model.get_by_id(id)

    def create(self, nombre, nit=None, telefono=None, correo=None, direccion=None, observaciones=None):
        beneficiario_id = self.beneficiario_model.create(nombre, nit, telefono, correo, direccion, observaciones)
        return self.get(beneficiario_id)

    def update(self, id, **kwargs):
        beneficiario = self.get(id)
        if not beneficiario:
            return None
        success = self.beneficiario_model.update(id,
                                                nombre=kwargs.get('nombre', beneficiario['nombre']),
                                                nit=kwargs.get('nit', beneficiario['nit']),
                                                telefono=kwargs.get('telefono', beneficiario['telefono']),
                                                correo=kwargs.get('correo', beneficiario['correo']),
                                                direccion=kwargs.get('direccion', beneficiario['direccion']),
                                                observaciones=kwargs.get('observaciones', beneficiario['observaciones']))
        if success:
            return self.get(id)
        return None

    def toggle_activo(self, id, activo):
        beneficiario = self.get(id)
        if not beneficiario:
            return None
        success = self.beneficiario_model.toggle_activo(id, activo)
        if success:
            return self.get(id)
        return None