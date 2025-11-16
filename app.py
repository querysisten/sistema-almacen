from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'almacen'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


#menu
@app.route('/menu.html')
def menu():
    return render_template('menu.html')

    #menu
@app.route('/menu_oficina.html')
def menu_oficina():
    return render_template('menu_oficina.html')

@app.route('/destalle_inventario.html')
def destalle_inventario():
    return render_template('destalle_inventario.html')



@app.route('/marcas.html')
def marcas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_marcas")
    data = cur.fetchall()
    return render_template('marcas.html', dato=data)


@app.route('/insertar_marca_ajax', methods=['POST'])
def insertar_marca_ajax():
    marca = request.form['marca']
    modelo = request.form['modelo']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tb_marcas (marca, modelo) VALUES (%s, %s)", (marca, modelo))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True)

@app.route('/get_marca/<int:id>')
def get_marca(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_marcas WHERE id=%s", (id,))
    data = cur.fetchone()
    return jsonify(data)

@app.route('/editar_marca_ajax', methods=['POST'])
def editar_marca_ajax():
    id = request.form['id']
    marca = request.form['marca']
    modelo = request.form['modelo']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tb_marcas SET marca=%s, modelo=%s WHERE id=%s", (marca, modelo, id))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_marcas WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('marcas'))


@app.route('/buscar_marca_ajax', methods=['GET'])
def buscar_marca_ajax():
    termino = request.args.get('q', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_marcas WHERE marca LIKE %s", ('%' + termino + '%',))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)






















#REGISTRO DE CLIENTE

@app.route('/cliente.html')
def cliente():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_clientes")
    data = cur.fetchall()
    cur.close()
    return render_template('cliente.html', dato=data)

@app.route('/insertar_cliente', methods=['POST'])
def insertar_cliente():
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']
    fecha = request.form['fecha']
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO tb_clientes (nombres, apellidos, telefono, correo, direccion, fecha) "
        "VALUES (%s,%s,%s,%s,%s,%s)",
        (nombres, apellidos, telefono, correo, direccion, fecha)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cliente'))

@app.route('/editar_cliente', methods=['POST'])
def editar_cliente():
    id = request.form['id']
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']
    fecha = request.form['fecha']
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE tb_clientes SET nombres=%s, apellidos=%s, telefono=%s, correo=%s, direccion=%s, fecha=%s WHERE id=%s",
        (nombres, apellidos, telefono, correo, direccion, fecha, id)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cliente'))

@app.route('/get_cliente/<int:id>')
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_clientes WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)

@app.route('/eliminar_cliente/<int:id>')
def eliminar_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_clientes WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('cliente'))

@app.route('/buscar_cliente_ajax', methods=['GET'])
def buscar_cliente_ajax():
    termino = request.args.get('q', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM tb_clientes
        WHERE CAST(id AS CHAR) LIKE %s
           OR nombres LIKE %s
           OR apellidos LIKE %s
    """, ('%' + termino + '%', '%' + termino + '%', '%' + termino + '%'))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)





















#FORMULARIO EMPLEADOS.HTML 


@app.route('/empleados.html')
def empleados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_empleados")
    data = cur.fetchall()
    cur.close()
    return render_template('empleados.html', dato=data)



@app.route('/insertar_empleados', methods=['POST'])
def insertar_empleados():
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']
    cargo = request.form['cargo']
    estatus = request.form['estatus']
    fecha_registro = request.form['fecha_registro']

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO tb_empleados 
        (nombres, apellidos, cedula, telefono, correo, direccion, cargo, estatus, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nombres, apellidos, cedula, telefono, correo, direccion, cargo, estatus, fecha_registro)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('empleados'))




@app.route('/editar_empleados', methods=['POST'])
def editar_empleados():
    id = request.form['id']
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    correo = request.form['correo']
    direccion = request.form['direccion']
    cargo = request.form['cargo']
    estatus = request.form['estatus']
    fecha_registro = request.form['fecha_registro']
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE tb_empleados SET nombres=%s, apellidos=%s, cedula=%s, telefono=%s, correo=%s, direccion=%s,cargo=%s,estatus=%s, fecha_registro=%s WHERE id=%s",
        (nombres, apellidos,cedula ,telefono, correo, direccion,cargo,estatus, fecha_registro, id)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('empleados'))



@app.route('/get_empleados/<int:id>')
def get_empledos(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_empleados WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)



@app.route('/eliminar_empleados/<int:id>')
def eliminar_empleados(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_empleados WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('empleados'))

@app.route('/buscar_empleados_ajax', methods=['GET'])
def buscar_empleados_ajax():
    termino = request.args.get('q', '').strip()
    cur = mysql.connection.cursor()

    # Convertimos el término a minúsculas para la comparación
    termino_lower = termino.lower()
    like_termino = '%' + termino_lower + '%'

    if termino.isdigit():
        # Buscamos por ID exacto y por nombres/apellidos insensibles a mayúsculas
        query = """
            SELECT * FROM tb_empleados
            WHERE id = %s 
               OR LOWER(nombres) LIKE %s 
               OR LOWER(apellidos) LIKE %s
        """
        cur.execute(query, (termino, like_termino, like_termino))
    else:
        # Buscamos solo por nombres/apellidos insensibles a mayúsculas
        query = """
            SELECT * FROM tb_empleados
            WHERE LOWER(nombres) LIKE %s 
               OR LOWER(apellidos) LIKE %s
        """
        cur.execute(query, (like_termino, like_termino))

    data = cur.fetchall()
    cur.close()
    return jsonify(data)






















# FORMULARIO ENTREGA PIEZAS
@app.route('/entregas_piezas.html')
def entregas_piezas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_entregas_piezas")
    data = cur.fetchall()
    cur.close()
    return render_template('entregas_piezas.html', dato=data)





@app.route('/insertar_entregas', methods=['POST'])
def insertar_entregas():
    id_empleado = request.form['id_empleado']
    id_cliente = request.form['id_cliente']
    id_vehiculo = request.form['id_vehiculo']
    id_marca = request.form['id_marca']
    id_inventario = request.form['id_inventario']
    cantidad = int(request.form['cantidad'])
    orden = request.form['orden']
    observacion = request.form['observacion']
    fecha = request.form['fecha']

    cur = mysql.connection.cursor()

    # 1️⃣ Obtener cantidad actual
    cur.execute("SELECT cantidad FROM tb_inventario_piezas WHERE id = %s", (id_inventario,))
    result = cur.fetchone()

    if result is None:
        cur.close()
        return "ERROR: ID de inventario no existe"

    cantidad_actual = result['cantidad']   # ← CORREGIDO

    # 2️⃣ Validar cantidad
    if cantidad > cantidad_actual:
        cur.close()
        return f"ERROR: No hay suficiente inventario. Disponible: {cantidad_actual}"

    # 3️⃣ Restar inventario
    nueva_cantidad = cantidad_actual - cantidad

    cur.execute("UPDATE tb_inventario_piezas SET cantidad = %s WHERE id = %s",
                (nueva_cantidad, id_inventario))

    # 4️⃣ Insertar entrega
    cur.execute("""
        INSERT INTO tb_entregas_piezas 
        (id_cliente, id_vehiculo, id_marca, id_inventario, id_empleado, cantidad, orden, observacion, fecha)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        id_cliente, id_vehiculo, id_marca, id_inventario,
        id_empleado, cantidad, orden, observacion, fecha
    ))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for('entregas_piezas'))






@app.route('/editar_entregas', methods=['POST'])
def editar_entregas():
    id = request.form['id']
    id_cliente = request.form['id_cliente']
    id_vehiculo = request.form['id_vehiculo']
    id_marca = request.form['id_marca']
    id_inventario = request.form['id_inventario']
    id_empleado = request.form['id_empleado']
    cantidad = request.form['cantidad']
    orden = request.form['orden']
    observacion = request.form['observacion']
    fecha = request.form['fecha']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE tb_entregas_piezas 
        SET id_cliente=%s, id_vehiculo=%s, id_marca=%s, id_inventario=%s, id_empleado=%s,
            cantidad=%s, orden=%s, observacion=%s, fecha=%s
        WHERE id=%s
    """, (id_cliente, id_vehiculo, id_marca, id_inventario, id_empleado, cantidad, orden, observacion, fecha, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('entregas_piezas'))


@app.route('/get_entregas/<int:id>')
def get_entregas(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_entregas_piezas WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)


@app.route('/eliminar_entregas/<int:id>')
def eliminar_entregas(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_entregas_piezas WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('entregas_piezas'))


@app.route('/buscar_entregas_ajax', methods=['GET'])
def buscar_entregas_ajax():
    termino = request.args.get('q', '').strip()

    cur = mysql.connection.cursor()

    if termino:  # Si el usuario escribió algo, filtra
        cur.execute("""
            SELECT * FROM tb_entregas_piezas 
            WHERE id = %s
        """, (termino,))
    else:  # Si el input está vacío, trae todos los registros
        cur.execute("SELECT * FROM tb_entregas_piezas")

    data = cur.fetchall()
    cur.close()

    return jsonify(data)














#FORMULARIO INVENTARIO DE PIEZAS


#   MOSTRAR REGISTROS

@app.route('/inventario_piezas.html')
def inventario_piezas():

    cur = mysql.connection.cursor()
    
    # Consulta SQL del inventario de piezas con datos relacionados (marcas, modelos, proveedores)
    query = """
    SELECT 
       i.id, 
  
    m.marca AS marca,
    m.modelo AS modelo,
    i.anio,
    i.descripcion,
    i.cantidad,
    i.almacen,
    i.anaquel,
    i.tramo,
    i.estado,
    i.fecha
    FROM tb_inventario_piezas i
    LEFT JOIN tb_marcas m ON i.id_marca = m.id
   
   
    
    """
    
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
  
    return render_template('inventario_piezas.html', dato=data)



#   INSERTAR REGISTRO

@app.route('/insertar_inventario', methods=['POST'])
def insertar_inventario():
    id_marca = request.form['id_marca']
    anio = request.form['anio']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    almacen = request.form['almacen']
    anaquel = request.form['anaquel']
    tramo = request.form['tramo']
    estado = request.form['estado']
    fecha = request.form['fecha']

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO tb_inventario_piezas 
        (id_marca, anio, descripcion, cantidad, almacen, anaquel, tramo, estado, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (id_marca, anio, descripcion, cantidad, almacen, anaquel, tramo, estado, fecha)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario_piezas'))


#   EDITAR REGISTRO

@app.route('/editar_inventario', methods=['POST'])
def editar_inventario():
    id = request.form['id']
    id_marca = request.form['id_marca']
    anio = request.form['anio']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    almacen = request.form['almacen']
    anaquel = request.form['anaquel']
    tramo = request.form['tramo']
    estado = request.form['estado']
    fecha = request.form['fecha']

    cur = mysql.connection.cursor()
    cur.execute(
        """
        UPDATE tb_inventario_piezas 
        SET id_marca=%s, anio=%s, descripcion=%s, cantidad=%s, 
            almacen=%s, anaquel=%s, tramo=%s, estado=%s, fecha=%s
        WHERE id=%s
        """,
        (id_marca, anio, descripcion, cantidad, almacen, anaquel, tramo, estado, fecha, id)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario_piezas'))



#   OBTENER REGISTRO POR ID (AJAX)

@app.route('/get_inventario/<int:id>')
def get_inventario(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_inventario_piezas WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)



#   ELIMINAR REGISTRO

@app.route('/eliminar_inventario/<int:id>', methods=['DELETE'])
def eliminar_inventario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tb_inventario_piezas WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    except Exception as e:
        print("Error al eliminar:", e)
        return jsonify({'success': False, 'error': str(e)}), 500



#   BUSCAR REGISTROS (AJAX)

@app.route('/buscar_inventario_ajax', methods=['GET'])
def buscar_inventario_ajax():
    termino = request.args.get('q', '').strip()
    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT * FROM tb_inventario_piezas 
        WHERE descripcion LIKE %s OR almacen LIKE %s OR estado LIKE %s
        """,
        ('%' + termino + '%', '%' + termino + '%', '%' + termino + '%')
    )
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

















#FORMULARIO DE REGISTRO DE VEHICULOS
@app.route('/vehiculos.html')
def inventario_vehiculos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_vehiculos")
    data = cur.fetchall()
    cur.close()
    return render_template('vehiculos.html', v=data)


#   INSERTAR VEHÍCULO

@app.route('/insertar_vehiculo', methods=['POST'])
def insertar_vehiculo():
    marca = request.form['marca']
    modelo = request.form['modelo']
    anio = request.form['anio']
    chasis = request.form['chasis']
    color = request.form['color']
    tipo = request.form['tipo']
    combustible = request.form['combustible']
    transmision = request.form['transmision']

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO tb_vehiculos 
        (marca, modelo, anio, chasis, color, tipo, combustible, transmision)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (marca, modelo, anio, chasis, color, tipo, combustible, transmision)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario_vehiculos'))



#   EDITAR VEHÍCULO

@app.route('/editar_vehiculo', methods=['POST'])
def editar_vehiculo():
    id = request.form['id']
    marca = request.form['marca']
    modelo = request.form['modelo']
    anio = request.form['anio']
    chasis = request.form['chasis']
    color = request.form['color']
    tipo = request.form['tipo']
    combustible = request.form['combustible']
    transmision = request.form['transmision']

    cur = mysql.connection.cursor()
    cur.execute(
        """
        UPDATE tb_vehiculos 
        SET marca=%s, modelo=%s, anio=%s, chasis=%s, color=%s, tipo=%s, combustible=%s, transmision=%s
        WHERE id=%s
        """,
        (marca, modelo, anio, chasis, color, tipo, combustible, transmision, id)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario_vehiculos'))


# =============================================
#   OBTENER VEHÍCULO POR ID (AJAX)
# =============================================
@app.route('/get_vehiculo/<int:id>')
def get_vehiculo(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tb_vehiculos WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)

#   ELIMINAR VEHÍCULO

@app.route('/eliminar_vehiculo/<int:id>')
def eliminar_vehiculo(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tb_vehiculos WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('inventario_vehiculos'))


#   BUSCAR VEHÍCULOS (AJAX)

@app.route('/buscar_vehiculo_ajax', methods=['GET'])
def buscar_vehiculo_ajax():
    termino = request.args.get('q', '').strip()
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM tb_vehiculos
        WHERE CAST(id AS CHAR) LIKE %s
           OR marca LIKE %s
           OR modelo LIKE %s
    """, ('%' + termino + '%', '%' + termino + '%', '%' + termino + '%'))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)










#CONSULTA DE ENTREGA DE PIEZAS


@app.route('/consulta_piezas_entregada.html')
def consulta_entrega_piezas():
    cur = mysql.connection.cursor()
    
    # Consulta SQL usando LEFT JOIN para no perder registros aunque falten datos relacionados
    query = """
    SELECT 
        c.nombres AS cliente_nombre ,
        c.apellidos AS cliente_apellido,
        e.nombres AS empleado_nombre,
        e.apellidos AS empleado_apellido,
        v.marca AS vehiculo_marca,
         m.modelo AS vehiculo_modelo,
        i.descripcion AS inventario_descripcion,
        

        v.anio AS vehiculo_anio,
        m.marca AS vehiculo_marca,
       
        ep.cantidad,
        ep.orden,
        ep.observacion,
        ep.fecha 
    FROM tb_entregas_piezas ep
    LEFT JOIN tb_clientes c ON ep.id_cliente = c.id
    LEFT JOIN tb_empleados e ON ep.id_empleado = e.id
    LEFT JOIN tb_vehiculos v ON ep.id_vehiculo = v.id
    LEFT JOIN tb_marcas m ON ep.id_marca = m.id
    LEFT JOIN tb_inventario_piezas i ON ep.id_inventario = i.id
    ORDER BY ep.fecha DESC
    """
    
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return render_template('consulta_piezas_entregada.html', dato=data)
    





#CONSULTA INVENTARIO PIEZAS


@app.route('/consulta_inventario.html')
def consulta_inventario_piezas():
    cur = mysql.connection.cursor()
    
    # Consulta SQL del inventario de piezas con datos relacionados (marcas, modelos, proveedores)
    query = """
    SELECT 
      
        m.marca AS marca,
        m.modelo AS modelo,
        i.anio,
        i.descripcion,
        i.cantidad,
        i.almacen,
        i.tramo,
        i.anaquel,
        i.estado,
        
        i.fecha
    FROM tb_inventario_piezas i
    LEFT JOIN tb_marcas m ON i.id_marca = m.id
   
   
    
    """
    
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return render_template('consulta_inventario.html', dato=data)



if __name__ == '__main__':
    app.run()
