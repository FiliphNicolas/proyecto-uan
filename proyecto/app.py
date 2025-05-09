from datetime import datetime
from factory import app, db
from models import Puesto, Carro, RegistroMovimiento, Configuracion
import routes

# Register routes
app.add_url_rule('/', view_func=routes.index)
app.add_url_rule('/ingresar', view_func=routes.ingresar_carro, methods=['POST'])
app.add_url_rule('/salir', view_func=routes.salir_carro, methods=['POST'])
app.add_url_rule('/configuracion', view_func=routes.configuracion)
app.add_url_rule('/actualizar_configuracion', view_func=routes.actualizar_configuracion, methods=['POST'])
app.add_url_rule('/avanzar_tiempo', view_func=routes.avanzar_tiempo, methods=['POST'])

# Initialize database
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create initial parking spots
        for i in range(1, 41):
            puesto = Puesto(numero=i, estado='libre')
            db.session.add(puesto)
        # Create default configuration with current time
        config = Configuracion(tarifa_actual=5000, hora_simulada=datetime.now())
        db.session.add(config)
        db.session.commit()

def init_db():
    with app.app_context():
        db.create_all()
        # Create initial parking spots if they don't exist
        if Puesto.query.count() == 0:
            for i in range(1, 41):
                puesto = Puesto(numero=i, estado='libre')
                db.session.add(puesto)
            # Create default configuration with current time
            config = Configuracion(tarifa_actual=5000, hora_simulada=datetime.now())
            db.session.add(config)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
