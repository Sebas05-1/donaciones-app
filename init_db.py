# init_db.py
from models.role_model import RoleModel
from models.usuario_model import UsuarioModel
from models.donante_model import DonanteModel
from models.tipo_donacion_model import TipoDonacionModel
from models.donacion_model import DonacionModel
from models.beneficiario_model import BeneficiarioModel
from models.asignacion_model import AsignacionModel

def init_db():
    RoleModel.create_table()
    UsuarioModel.create_table()
    DonanteModel.create_table()
    TipoDonacionModel.create_table()
    DonacionModel.create_table()
    BeneficiarioModel.create_table()
    AsignacionModel.create_table()
    print("Tablas creadas")

if __name__ == '__main__':
    init_db()