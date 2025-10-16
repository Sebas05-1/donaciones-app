# presenters/auth_presenter.py
from models.usuario_model import UsuarioModel
from models.role_model import RoleModel
from app import bcrypt

class AuthPresenter:
    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.role_model = RoleModel()

    def register_user(self, username, email, password, telefono='', cedula=''):
        # Validación básica
        if not username or not email or not password:
            return False, "Todos los campos marcados son obligatorios"
            
        # Verificar existencia
        existing_user = self.usuario_model.get_user_by_username_or_email(username)
        if existing_user:
            if existing_user['username'] == username:
                return False, "El nombre de usuario ya existe"
            if existing_user['email'] == email:
                return False, "El email ya está registrado"
                
        # Validar formato de email básico
        if '@' not in email or '.' not in email:
            return False, "El formato del email no es válido"
            
        # Validar longitud de contraseña
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
            
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = self.usuario_model.create_user(username, email, pw_hash, telefono, cedula, role_id=None, activo=True)
        return True, {'id': user_id, 'username': username, 'email': email}

    def validate_login(self, username_or_email, password):
        user = self.usuario_model.get_user_by_username_or_email(username_or_email)
        if user is None:
            return False, "Credenciales inválidas"
        if not user['activo']:
            return False, "Usuario inactivo. Contacte al administrador."
        if bcrypt.check_password_hash(user['password'], password):
            return True, user
        return False, "Credenciales inválidas"