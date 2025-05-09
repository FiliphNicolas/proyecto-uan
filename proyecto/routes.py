from flask import render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from factory import db
from models import Puesto, Carro, RegistroMovimiento, Configuracion

def index():
    puestos = Puesto.query.all()
    configuracion = Configuracion.query.first()
    hora_actual = configuracion.hora_simulada
    
    # Calculate daily revenue
    inicio_dia = hora_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = hora_actual.replace(hour=23, minute=59, second=59, microsecond=999999)
    ingresos_dia = db.session.query(db.func.sum(RegistroMovimiento.valor_pagado)).\
        filter(RegistroMovimiento.hora_salida.between(inicio_dia, fin_dia)).scalar() or 0
    
    # Calculate total revenue
    ingresos_totales = db.session.query(db.func.sum(RegistroMovimiento.valor_pagado)).scalar() or 0
    
    # Get recent transactions
    ultimas_transacciones = RegistroMovimiento.query.\
        order_by(RegistroMovimiento.hora_salida.desc()).\
        limit(5).all()
    
    return render_template('index.html', 
                         puestos=puestos,
                         hora_actual=hora_actual.strftime('%Y-%m-%d %H:%M'),
                         ingresos_dia=ingresos_dia,
                         ingresos_totales=ingresos_totales,
                         ultimas_transacciones=ultimas_transacciones)

def ingresar_carro():
    placa = request.form['placa']
    hora_entrada = request.form['hora_entrada']
    
    # Check if car already exists and is active
    carro_existente = Carro.query.filter_by(placa=placa, estado='activo').first()
    if carro_existente:
        flash('El carro ya está en el parqueadero', 'error')
        return redirect('/')
    
    # Find available spot
    puesto = Puesto.query.filter_by(estado='libre').first()
    if not puesto:
        flash('No hay puestos disponibles', 'error')
        return redirect('/')
    
    # Get current simulated time
    configuracion = Configuracion.query.first()
    hora_actual = configuracion.hora_simulada
    
    # Parse the input time
    try:
        hora_minuto = datetime.strptime(hora_entrada, '%H:%M').time()
        # Combine the simulated date with the input time
        hora_entrada_completa = datetime.combine(hora_actual.date(), hora_minuto)
    except ValueError:
        flash('Formato de hora inválido', 'error')
        return redirect('/')
    
    # Create new car entry
    carro = Carro(
        placa=placa,
        hora_entrada=hora_entrada_completa,
        puesto_id=puesto.id,
        estado='activo'
    )
    
    try:
        # Update spot status
        puesto.estado = 'ocupado'
        db.session.add(carro)
        db.session.commit()
        
        flash('Carro ingresado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al registrar el carro', 'error')
        
    return redirect('/')


def salir_carro():
    placa = request.form['placa']
    carro = Carro.query.filter_by(placa=placa, estado='activo').first()
    
    if not carro:
        flash('No se encontró el carro', 'error')
        return redirect('/')
    
    # Get current simulated time
    configuracion = Configuracion.query.first()
    hora_actual = configuracion.hora_simulada
    
    # Calculate payment
    tiempo = (hora_actual - carro.hora_entrada).total_seconds() / 3600
    valor = configuracion.tarifa_actual * (tiempo + 1)  # Round up to next hour
    
    # Create movement record
    registro = RegistroMovimiento(
        placa=placa,
        hora_entrada=carro.hora_entrada,
        hora_salida=hora_actual,
        valor_pagado=valor
    )
    
    # Update car and spot
    carro.estado = 'inactivo'
    carro.puesto.estado = 'libre'
    carro.puesto.carro_id = None
    
    db.session.add(registro)
    db.session.commit()
    flash(f'Carro salido exitosamente. Valor a pagar: ${valor:.2f}', 'success')
    return redirect('/')

def configuracion():
    configuracion = Configuracion.query.first()
    return render_template('configuracion.html', configuracion=configuracion)

def actualizar_configuracion():
    tarifa = float(request.form['tarifa'])
    configuracion = Configuracion.query.first()
    configuracion.tarifa_actual = tarifa
    db.session.commit()
    flash('Configuración actualizada exitosamente', 'success')
    return redirect('/configuracion')

def avanzar_tiempo():
    horas = int(request.form['horas'])
    configuracion = Configuracion.query.first()
    configuracion.hora_simulada += timedelta(hours=horas)
    db.session.commit()
    flash('Hora avanzada exitosamente', 'success')
    return redirect('/')
