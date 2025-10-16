# presenters/donante_presenter.py
from models.donante_model import DonanteModel

class DonantePresenter:
    def __init__(self):
        self.donante_model = DonanteModel()

    def get_all(self):
        return self.donante_model.get_all()

    def get(self, id):
        return self.donante_model.get_by_id(id)

    def create(self, nombre, correo=None, telefono=None, direccion=None, cedula=None):
        donante_id = self.donante_model.create(nombre, correo, telefono, direccion, cedula)
        return self.get(donante_id)

    def update(self, id, **kwargs):
        donante = self.get(id)
        if not donante:
            return None
        success = self.donante_model.update(id,
                                            nombre=kwargs.get('nombre', donante['nombre']),
                                            correo=kwargs.get('correo', donante['correo']),
                                            telefono=kwargs.get('telefono', donante['telefono']),
                                            direccion=kwargs.get('direccion', donante['direccion']),
                                            cedula=kwargs.get('cedula', donante['cedula']))
        if success:
            return self.get(id)
        return None

    def toggle_estado(self, id, estado):
        donante = self.get(id)
        if not donante:
            return None
        success = self.donante_model.toggle_estado(id, estado)
        if success:
            return self.get(id)
        return None