# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from presenters.auth_presenter import AuthPresenter
from presenters.user_presenter import UserPresenter
from presenters.donante_presenter import DonantePresenter
from presenters.donacion_presenter import DonacionPresenter
from presenters.beneficiario_presenter import BeneficiarioPresenter
from presenters.asignacion_presenter import AsignacionPresenter
from models.role_model import RoleModel
from models.donante_model import DonanteModel
from models.tipo_donacion_model import TipoDonacionModel
from models.donacion_model import DonacionModel
from models.beneficiario_model import BeneficiarioModel
from models.asignacion_model import AsignacionModel

bp = Blueprint('main', __name__)
auth_presenter = AuthPresenter()
user_presenter = UserPresenter()
donante_presenter = DonantePresenter()
donacion_presenter = DonacionPresenter()
beneficiario_presenter = BeneficiarioPresenter()
asignacion_presenter = AsignacionPresenter()

# helpers
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para continuar', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return wrapper

def role_required(roles_allowed):
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Por favor inicia sesión para continuar', 'warning')
                return redirect(url_for('main.login'))
            if not session.get('role'):
                flash("No tienes un rol asignado. Contacta al administrador", "warning")
                return redirect(url_for('main.dashboard'))
            if session.get('role') not in roles_allowed:
                flash("No tienes permiso para ver esa página", "danger")
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')
        ok, result = auth_presenter.validate_login(identifier, password)
        if ok:
            user = result
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role_nombre'] if user['role_nombre'] else None
            return redirect(url_for('main.dashboard'))
        else:
            flash(result, 'danger')
    return render_template('login.html')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        telefono = request.form.get('telefono')
        cedula = request.form.get('cedula')
        ok, res = auth_presenter.register_user(username, email, password, telefono, cedula)
        if ok:
            flash("Registrado correctamente. Espera a que el superAdmin asigne rol.", "success")
            return redirect(url_for('main.login'))
        else:
            flash(res, "danger")
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    return render_template('dashboard.html', role=role)

# USUARIOS - solo superAdmin
@bp.route('/usuarios')
@login_required
@role_required(['superAdmin'])
def usuarios():
    users = user_presenter.get_all_users()
    roles = RoleModel.get_all_roles(exclude_superadmin=True)
    return render_template('usuarios/users.html', users=users, roles=roles)

@bp.route('/usuarios/editar/<int:user_id>', methods=['GET','POST'])
@login_required
@role_required(['superAdmin'])
def editar_usuario(user_id):
    user = user_presenter.get_user(user_id)
    roles = RoleModel.get_all_roles(exclude_superadmin=True)
    if request.method == 'POST':
        new_role = request.form.get('role_id')
        new_role_id = int(new_role) if new_role else None
        ok, res = user_presenter.update_user_role(user_id, new_role_id)
        if ok:
            flash("Usuario actualizado.", "success")
            return redirect(url_for('main.usuarios'))
        else:
            flash(res, "danger")
    return render_template('usuarios/user_edit.html', user=user, roles=roles)

@bp.route('/usuarios/desactivar/<int:user_id>')
@login_required
@role_required(['superAdmin'])
def desactivar_usuario(user_id):
    ok, res = user_presenter.deactivate_user(user_id)
    if ok:
        flash("Usuario desactivado.", "success")
    else:
        flash(res, "danger")
    return redirect(url_for('main.usuarios'))

# Accesos - admin y superAdmin
# DONANTES
@bp.route('/donantes/nuevo', methods=['GET','POST'])
@login_required
@role_required(['superAdmin','administrador'])
def donantes_nuevo():
    if request.method=='POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        cedula = request.form.get('cedula')
        donante_presenter.create(nombre, correo, telefono, direccion, cedula)
        flash("Donante creado", "success")
        return redirect(url_for('main.donantes'))
    return render_template('donantes/donante_form.html')

@bp.route('/donantes/editar/<int:id>', methods=['GET','POST'])
@login_required
@role_required(['superAdmin','administrador'])
def donantes_editar(id):
    d = donante_presenter.get(id)
    if request.method=='POST':
        donante_presenter.update(id,
            nombre=request.form.get('nombre'),
            correo=request.form.get('correo'),
            telefono=request.form.get('telefono'),
            direccion=request.form.get('direccion'),
            cedula=request.form.get('cedula'))
        flash("Donante actualizado", "success")
        return redirect(url_for('main.donantes'))
    return render_template('donantes/donante_form.html', donante=d)

@bp.route('/donantes/toggle/<int:id>')
@login_required
@role_required(['superAdmin','administrador'])
def donantes_toggle(id):
    d = donante_presenter.get(id)
    new = not d['estado']
    donante_presenter.toggle_estado(id, new)
    flash("Estado cambiado", "success")
    return redirect(url_for('main.donantes'))

# DONACIONES
@bp.route('/donaciones/nuevo', methods=['GET','POST'])
@login_required
@role_required(['superAdmin','administrador'])
def donaciones_nuevo():
    tipos = TipoDonacionModel.get_all()
    donantes = DonanteModel.get_all(only_active=True)
    if request.method=='POST':
        nombre = request.form.get('nombre')
        tipo_id = int(request.form.get('tipo_id'))
        donante_id = request.form.get('donante_id') or None
        donante_id = int(donante_id) if donante_id else None
        monto = request.form.get('monto') or None
        cantidad = request.form.get('cantidad') or None
        descripcion = request.form.get('descripcion')
        monto_val = float(monto) if monto else None
        cantidad_val = int(cantidad) if cantidad else None
        donacion_presenter.create(nombre, tipo_id, donante_id, monto_val, cantidad_val, descripcion)
        flash("Donación creada", "success")
        return redirect(url_for('main.donaciones'))
    return render_template('donaciones/donacion_form.html', tipos=tipos, donantes=donantes)

@bp.route('/donaciones/editar/<int:id>', methods=['GET','POST'])
@login_required
@role_required(['superAdmin','administrador'])
def donaciones_editar(id):
    d = donacion_presenter.get(id)
    tipos = TipoDonacionModel.get_all()
    donantes = DonanteModel.get_all(only_active=True)
    if request.method=='POST':
        donacion_presenter.update(id,
            nombre=request.form.get('nombre'),
            tipo_id=int(request.form.get('tipo_id')),
            donante_id=int(request.form.get('donante_id')) if request.form.get('donante_id') else None,
            monto=float(request.form.get('monto')) if request.form.get('monto') else None,
            cantidad=int(request.form.get('cantidad')) if request.form.get('cantidad') else None,
            descripcion=request.form.get('descripcion'))
        flash("Donación actualizada", "success")
        return redirect(url_for('main.donaciones'))
    return render_template('donaciones/donacion_form.html', donacion=d, tipos=tipos, donantes=donantes)

@bp.route('/donaciones/desactivar/<int:id>')
@login_required
@role_required(['superAdmin','administrador'])
def donaciones_desactivar(id):
    donacion_presenter.deactivate(id)
    flash("Donación desactivada", "success")
    return redirect(url_for('main.donaciones'))

# BENEFICIARIOS
@bp.route('/beneficiarios_nuevo', methods=['GET','POST'])
@login_required
@role_required(['superAdmin','administrador'])
def beneficiarios_nuevo():
    if request.method=='POST':
        beneficiario_presenter.create(
            nombre=request.form.get('nombre'),
            nit=request.form.get('nit'),
            telefono=request.form.get('telefono'),
            correo=request.form.get('correo'),
            direccion=request.form.get('direccion'),
            observaciones=request.form.get('observaciones')
        )
        flash("Beneficiario creado", "success")
        return redirect(url_for('main.beneficiarios'))
    return render_template('beneficiarios/beneficiario_form.html')

@bp.route('/beneficiarios/editar/<int:id>', methods=['GET','POST'])
@login_required
@role_required(['superAdmin','administrador'])
def beneficiarios_editar(id):
    b = beneficiario_presenter.get(id)
    if request.method=='POST':
        beneficiario_presenter.update(id,
            nombre=request.form.get('nombre'),
            nit=request.form.get('nit'),
            telefono=request.form.get('telefono'),
            correo=request.form.get('correo'),
            direccion=request.form.get('direccion'),
            observaciones=request.form.get('observaciones')
        )
        flash("Beneficiario actualizado", "success")
        return redirect(url_for('main.beneficiarios'))
    return render_template('beneficiarios/beneficiario_form.html', beneficiario=b)

@bp.route('/beneficiarios/toggle/<int:id>')
@login_required
@role_required(['superAdmin','administrador'])
def beneficiarios_toggle(id):
    b = beneficiario_presenter.get(id)
    new = not b['activo']
    beneficiario_presenter.toggle_activo(id, new)
    flash("Estado cambiado", "success")
    return redirect(url_for('main.beneficiarios'))

# ASIGNACIONES
@bp.route('/asignaciones/nuevo', methods=['GET', 'POST'])
@login_required
@role_required(['superAdmin', 'administrador'])
def asignaciones_nuevo():
    donaciones = DonacionModel.get_all(only_active=True)
    beneficiarios = BeneficiarioModel.get_all(only_active=True)
    tipos_donacion = TipoDonacionModel.get_all()

    if request.method == 'POST':
        donacion_id = int(request.form.get('donacion_id'))
        beneficiario_id = int(request.form.get('beneficiario_id'))
        tipo_id = int(request.form.get('tipo_id'))
        cantidad = request.form.get('cantidad') or None
        monto = request.form.get('monto') or None
        cantidad_val = int(cantidad) if cantidad else None
        monto_val = float(monto) if monto else None

        # Validar que tipo_id coincide con la donación
        donacion = DonacionModel.get_by_id(donacion_id)
        if donacion and donacion['tipo_id'] != tipo_id:
            flash("El tipo de donación seleccionado no coincide con la donación.", "danger")
            return render_template('asignaciones/asignacion_form.html', 
                                 donaciones=donaciones, 
                                 beneficiarios=beneficiarios, 
                                 tipos_donacion=tipos_donacion)

        ok, res = asignacion_presenter.create(donacion_id, beneficiario_id, tipo_id, cantidad_val, monto_val)
        if ok:
            flash("Asignación creada", "success")
            return redirect(url_for('main.asignaciones'))
        else:
            flash(res, 'danger')

    return render_template('asignaciones/asignacion_form.html', 
                         donaciones=donaciones, 
                         beneficiarios=beneficiarios, 
                         tipos_donacion=tipos_donacion, 
                         asignacion=None)

@bp.route('/asignaciones/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(['superAdmin', 'administrador'])
def asignaciones_editar(id):
    asignacion = AsignacionModel.get_by_id(id)
    if not asignacion:
        flash("Asignación no encontrada", "danger")
        return redirect(url_for('main.asignaciones'))
    donaciones = DonacionModel.get_all(only_active=True)
    beneficiarios = BeneficiarioModel.get_all(only_active=True)
    tipos_donacion = TipoDonacionModel.get_all()

    if request.method == 'POST':
        donacion_id = int(request.form.get('donacion_id'))
        beneficiario_id = int(request.form.get('beneficiario_id'))
        tipo_id = int(request.form.get('tipo_id'))
        cantidad = request.form.get('cantidad') or None
        monto = request.form.get('monto') or None
        cantidad_val = int(cantidad) if cantidad else None
        monto_val = float(monto) if monto else None

        # Validar que tipo_id coincide con la donación
        donacion = DonacionModel.get_by_id(donacion_id)
        if donacion and donacion['tipo_id'] != tipo_id:
            flash("El tipo de donación seleccionado no coincide con la donación.", "danger")
            return render_template('asignaciones/asignacion_form.html', 
                                 donaciones=donaciones, 
                                 beneficiarios=beneficiarios, 
                                 tipos_donacion=tipos_donacion, 
                                 asignacion=asignacion)

        # Eliminar y crear nueva asignación
        ok, msg = asignacion_presenter.delete(id)
        if ok:
            ok, res = asignacion_presenter.create(donacion_id, beneficiario_id, tipo_id, cantidad_val, monto_val)
            if ok:
                flash("Asignación actualizada", "success")
                return redirect(url_for('main.asignaciones'))
            else:
                flash(res, 'danger')
        else:
            flash(msg, 'danger')

    return render_template('asignaciones/asignacion_form.html', 
                         donaciones=donaciones, 
                         beneficiarios=beneficiarios, 
                         tipos_donacion=tipos_donacion, 
                         asignacion=asignacion)

@bp.route('/asignaciones/eliminar/<int:id>')
@login_required
@role_required(['superAdmin', 'administrador'])
def asignaciones_eliminar(id):
    ok, msg = asignacion_presenter.delete(id)
    flash(msg if ok else msg, 'success' if ok else 'danger')
    return redirect(url_for('main.asignaciones'))

# Accesos - admin, auditor y superAdmin
@bp.route('/lista')
@login_required
@role_required(['superAdmin', 'administrador', 'auditor'])
def lista():
    return render_template('lista.html')

@bp.route('/donantes')
@login_required
@role_required(['superAdmin','administrador','auditor'])
def donantes():
    all = donante_presenter.get_all()
    return render_template('donantes/donantes.html', donantes=all)

@bp.route('/donaciones')
@login_required
@role_required(['superAdmin','administrador','auditor'])
def donaciones():
    all = donacion_presenter.get_all()
    tipos = TipoDonacionModel.get_all()
    return render_template('donaciones/donaciones.html', donaciones=all, tipos=tipos)

@bp.route('/inventario/material')
@login_required
@role_required(['superAdmin','administrador','auditor'])
def inventario_material():
    data = donacion_presenter.inventario_material()
    return render_template('donaciones/inventario_material.html', data=data)

@bp.route('/inventario/economico')
@login_required
@role_required(['superAdmin','administrador','auditor'])
def inventario_economico():
    data = donacion_presenter.inventario_economico()
    return render_template('donaciones/inventario_economico.html', data=data)

@bp.route('/beneficiarios')
@login_required
@role_required(['superAdmin','administrador','auditor'])
def beneficiarios():
    all = beneficiario_presenter.get_all()
    return render_template('beneficiarios/beneficiarios.html', beneficiarios=all)

@bp.route('/asignaciones')
@login_required
@role_required(['superAdmin','administrador','auditor'])
def asignaciones():
    all = asignacion_presenter.get_all()
    return render_template('asignaciones/asignaciones.html', asignaciones=all)