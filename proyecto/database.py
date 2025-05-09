from src import db, app
from src.models import Puesto, Configuracion

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create initial 40 parking spots
        for i in range(1, 41):
            puesto = Puesto(numero=i)
            db.session.add(puesto)
        
        # Create initial configuration
        configuracion = Configuracion(tarifa_actual=2000)
        db.session.add(configuracion)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
