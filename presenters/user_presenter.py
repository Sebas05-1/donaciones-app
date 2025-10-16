# presenters/user_presenter.py
from models.usuario_model import UsuarioModel
from models.role_model import RoleModel

class UserPresenter:
    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.role_model = RoleModel()

    def get_all_users(self):
        return self.usuario_model.get_all_users()

    def get_user(self, user_id):
        return self.usuario_model.get_user_by_id(user_id)

    def update_user_role(self, user_id, new_role_id):
        user = self.get_user(user_id)
        if not user:
            return False, "Usuario no encontrado"
        # Evitar asignar superAdmin desde UI
        role = self.role_model.get_role_by_id(new_role_id)
        if role and role['nombre'] == 'superAdmin':
            return False, "No permitido asignar rol superAdmin desde la aplicación"
        success = self.usuario_model.update_user_role(user_id, new_role_id)
        if success:
            return True, self.get_user(user_id)
        return False, "Error al actualizar el rol"

    def deactivate_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False, "Usuario no encontrado"
        success = self.usuario_model.deactivate_user(user_id)
        if success:
            return True, self.get_user(user_id)
        return False, "Error al desactivar el usuario"

    def activate_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False, "Usuario no encontrado"
        success = self.usuario_model.update_user_role(user_id, True)  # Reusamos update para activo
        if success:
            return True, self.get_user(user_id)
        return False, "Error al activar el usuario"