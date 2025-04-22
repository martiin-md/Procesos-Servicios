import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flaskext.mysql import MySQL
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps
import re

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Usar la variable de entorno para la clave secreta
app.secret_key = os.environ.get('SECRET_KEY')

# Configuración de la base de datos MySQL utilizando las variables del .env
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('MYSQL_DATABASE_DB')
mysql.init_app(app)

@app.before_request
def require_login():
    # Define endpoints que no requieren autenticación
    exempt_endpoints = ['login', 'register', 'static']
    if request.endpoint not in exempt_endpoints and "user" not in session:
        flash("Por favor, inicia sesión", "warning")
        return redirect(url_for("login"))

@app.template_filter('format_number')
def format_number_filter(value):
    try:
        # Formatea el número usando comas como separador, luego reemplaza las comas por puntos
        return "{:,.0f}".format(value).replace(',', '.')
    except (ValueError, TypeError):
        return value

# Decorador para requerir que el usuario inicie sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Por favor, inicia sesión", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para roles específicos (opcional)
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                flash("Por favor, inicia sesión primero.", "warning")
                return redirect(url_for("login"))
            user_role = session.get("role")
            if user_role not in roles:
                flash("No tienes permiso para acceder a esta página.", "danger")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Ruta de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Maneja el registro de nuevos usuarios """
    if request.method == 'POST':
        codigoUsuario = request.form.get('codigoUsuario')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validar que el código sea de 4 cifras
        if not re.match(r'^\d{4}$', codigoUsuario):
            flash('El código de usuario debe ser una cadena de 4 cifras', 'danger')
            return redirect(url_for('register'))

        # Verificar campos requeridos
        if not codigoUsuario or not password or not confirm_password:
            flash('Faltan campos requeridos', 'warning')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('register'))

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE codigoUsuario = %s", (codigoUsuario,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('El código de usuario ya está en uso', 'warning')
                cursor.close()
                return redirect(url_for('register'))

            # Inserta el nuevo usuario. Ajusta el role según lo que necesites, por ejemplo 'recepcion'
            cursor.execute("INSERT INTO usuarios (codigoUsuario, password, role) VALUES (%s, %s, %s)",
                           (codigoUsuario, password, 'recepcion'))
            conn.commit()
            cursor.close()
            flash('Registro exitoso. Puedes iniciar sesión ahora', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error en el registro: {str(e)}', 'danger')
            return redirect(url_for('register'))
    return render_template('formularios/register.html')

# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Maneja la autenticación de usuarios """
    if request.method == 'POST':
        codigoUsuario = request.form.get('codigoUsuario')
        password = request.form.get('password')

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT codigoUsuario, password, role FROM usuarios WHERE codigoUsuario = %s", (codigoUsuario,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and user[1] == password:
                # Almacena en la sesión el código y el rol
                session["user"] = user[0]
                session["role"] = user[2]
                flash("Inicio de sesión correcto", "success")
                return redirect(url_for("index"))
            flash('Login fallido. Verifica tu código de usuario y/o contraseña', 'danger')
        except Exception as e:
            flash(f"Error en el login: {str(e)}", "danger")
    return render_template("formularios/login.html")

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("login"))

# Ruta de prueba para verificar la autenticación
@app.route('/test_auth')
@login_required
def test_auth():
    return f"User {session.get('user')} con rol {session.get('role')} está autenticado."

def format_european(value):
    try:
        number = float(value)
        if number.is_integer():
            # Si es entero, formatearlo sin decimales.
            formatted = f"{int(number):,}"
        else:
            # Si tiene decimales, mostrar 1 decimal.
            formatted = f"{number:,.1f}"
        # Ajuste para notación europea.
        formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
        return formatted
    except (ValueError, TypeError):
        return value

app.jinja_env.filters['euroformat'] = format_european


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # Recibir datos del formulario
        contrato_marco = request.form['contrato_marco']
        paraje = request.form['paraje']
        anio_cosecha = request.form['anio_cosecha']
        proveedor_id = request.form['proveedor']
        tipo_paja_cereal_id = request.form['tipo_paja_cereal']
        fecha_acuerdo = request.form['fecha_acuerdo']
        localidad = request.form['localidad']
        coordenadas = request.form['coordenadas']
        kilos = request.form['kilos']
        num_paquetes = request.form['num_paquetes']
        kilos_paquete = request.form['kilos_paquete']
        precio_tonelada = request.form['precio_tonelada']
        tipo_paja_riego = request.form['tipo_paja_riego']
        tipo_calidad = request.form['tipo_calidad']
        planta_destino = request.form['planta_destino']
        comentarios = request.form['comentarios']
        estado_pedido = 'pendiente'

        # Obtener nombres de proveedor y cereal
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT nombreProveedor FROM proveedores WHERE idProveedor = %s", (proveedor_id,))
            proveedor_nombre = cursor.fetchone()[0]
            cursor.execute("SELECT cereal FROM pajacereal WHERE idCereal = %s", (tipo_paja_cereal_id,))
            cereal_nombre = cursor.fetchone()[0]
            cursor.close()
            
            # Generar código CINA con nombres
            codigo_cina = f"{contrato_marco}/{anio_cosecha}/{proveedor_nombre}/{paraje}/{cereal_nombre}"

            # Insertar datos en la base de datos
            cursor = conn.cursor()
            sql = """INSERT INTO registrocinas (contrato_marco, paraje, anio_cosecha, codigo_cina, fecha_acuerdo, proveedorID, localidad, coordenadas, kilos, num_paquetes, kilos_paquete, precio_tonelada, tipo_paja_riego, pajaCerealID, tipo_calidad, planta_destino, comentarios, estado_pedido)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (contrato_marco, paraje, anio_cosecha, codigo_cina, fecha_acuerdo, proveedor_id, localidad, coordenadas, kilos, num_paquetes, kilos_paquete, precio_tonelada, tipo_paja_riego, tipo_paja_cereal_id, tipo_calidad, planta_destino, comentarios, estado_pedido))
            conn.commit()
            flash('Datos guardados correctamente', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al guardar los datos: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('index'))

    # Obtener proveedores y cereales para mostrar en el formulario
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT idProveedor, nombreProveedor FROM proveedores")
    proveedores = cursor.fetchall()
    cursor.execute("SELECT idCereal, cereal FROM pajacereal")
    cereales = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('formularios/index.html', active_page='form1', proveedores=proveedores, cereales=cereales)

@app.route('/estados', methods=['GET', 'POST'])
@login_required
def estados():
    if request.method == 'POST':
        # Procesamiento del formulario POST para actualizar el estado
        try:
            codigo_cina = request.form.get('codigo_cina')
            nuevo_estado = request.form.get('nuevo_estado')
            
            if not codigo_cina or not nuevo_estado:
                flash('Datos insuficientes para actualizar el estado.', 'danger')
                return redirect(url_for('estados'))
            
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "UPDATE registrocinas SET estado_pedido = %s WHERE codigo_cina = %s"
            cursor.execute(sql, (nuevo_estado, codigo_cina))
            conn.commit()
            flash('Estado actualizado correctamente', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar el estado: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    # Obtener filtros del formulario vía GET
    anio_cosecha   = request.args.get('anio_cosecha', '')
    planta_destino = request.args.get('planta_destino', '')
    kg_diferencia  = request.args.get('kg_diferencia', '')
    estado_pedido  = request.args.get('estado_pedido', '')
    busqueda       = request.args.get('busqueda', '')
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Obtener valores únicos para los filtros de año y planta
    cursor.execute("SELECT DISTINCT anio_cosecha FROM registrocinas")
    años = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT planta_destino FROM registrocinas")
    plantas = [row[0] for row in cursor.fetchall()]
    
    # Consulta SQL actualizada para incluir el filtro de búsqueda (por código o proveedor)
    sql = """SELECT rc.fecha_acuerdo, rc.codigo_cina, rc.kilos, rc.kg_entregados, rc.kg_diferencia, rc.estado_pedido,
                    p.nombreProveedor, c.cereal, rc.planta_destino, rc.anio_cosecha, 
                    ROUND((rc.kg_entregados / rc.kilos) * 100, 2) AS porcentaje_completado
            FROM registrocinas rc
            LEFT JOIN proveedores p ON rc.proveedorID = p.idProveedor
            LEFT JOIN pajacereal c ON rc.pajaCerealID = c.idCereal
            WHERE (%s = '' OR rc.anio_cosecha = %s)
                AND (%s = '' OR rc.planta_destino LIKE %s)
                AND (%s = '' OR (rc.kg_diferencia >= 0 AND %s = 'positivo') OR (rc.kg_diferencia < 0 AND %s = 'negativo'))
                AND (%s = '' OR rc.estado_pedido = %s)
                AND (%s = '' OR (rc.codigo_cina LIKE %s OR p.nombreProveedor LIKE %s))
            ORDER BY rc.fecha_acuerdo ASC"""

    cursor.execute(sql, (
        anio_cosecha, anio_cosecha,
        planta_destino, f'%{planta_destino}%',
        kg_diferencia, kg_diferencia, kg_diferencia,
        estado_pedido, estado_pedido,
        busqueda, f'%{busqueda}%', f'%{busqueda}%'
    ))
    cinas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('formularios/estados.html', active_page='form2',
                           cinas=cinas, 
                           años=años, 
                           plantas=plantas,
                           anio_cosecha=anio_cosecha, 
                           planta_destino=planta_destino,
                           kg_diferencia=kg_diferencia, 
                           estado_pedido=estado_pedido,
                           busqueda=busqueda)

@app.route('/detalle/<path:codigo_cina>', methods=['GET'], strict_slashes=False)
@login_required
def detalle(codigo_cina):
    try:
        # Primero, eliminar espacios al inicio y al final
        codigo_cina = codigo_cina.strip()
        
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT r.*, p.nombreProveedor, c.cereal 
            FROM registrocinas r
            JOIN proveedores p ON r.proveedorID = p.idProveedor
            LEFT JOIN pajacereal c ON r.pajaCerealID = c.idCereal
            WHERE LOWER(TRIM(r.codigo_cina)) = LOWER(TRIM(%s))
        """, (codigo_cina,))
        
        detalle = cursor.fetchone()
        cursor.close()
        conn.close()

        if detalle is None:
            flash('No se encontró el registro solicitado.', 'danger')
            return redirect(url_for('estados'))

        return render_template('formularios/detalle.html', detalle=detalle)
    except Exception as e:
        flash(f'Error al obtener los detalles: {str(e)}')
        return redirect(url_for('estados'))

from datetime import datetime

@app.route('/entradas', methods=['GET', 'POST'])
@login_required
def entradas():
    if request.method == 'POST':
        codigo_cina = request.form['codigo_cina']
        fecha = request.form['fecha']
        kg_entrada = request.form['kg_entrada']
        kg_descuento = request.form.get('kg_descuento', 0)
        n_paquetes = request.form['n_paquetes']
        # Campos para destino
        destino = request.form.get('destino')
        destino_tipo = request.form.get('destino_tipo')  # 'PCHAMPI' o 'PSETAS'
        # Campos de producción
        num_op = request.form.get('num_op', '')
        observaciones = request.form.get('observaciones', '')

        # Determinar si es modo producción (si se ingresa num_op, por ejemplo)
        production_mode = True if num_op.strip() != "" else False

        # Validar campos obligatorios generales
        if not codigo_cina or not fecha or not kg_entrada or not n_paquetes:
            flash('Faltan campos obligatorios.', 'warning')
            return redirect(url_for('entradas'))
            
        # Si no es producción, se requiere seleccionar destino
        if not production_mode and not destino:
            flash('Debe seleccionar un destino.', 'warning')
            return redirect(url_for('entradas'))

        # Si es producción, ignoramos el destino
        if production_mode:
            destino_setas = None
            destino_champis = None
        else:
            if destino_tipo == 'PCHAMPI':
                destino_champis = destino
                destino_setas = None
            elif destino_tipo == 'PSETAS':
                destino_setas = destino
                destino_champis = None
            else:
                destino_setas = None
                destino_champis = None

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Obtener idRegistro, kg_entregados y precio_tonelada para el código CINA
            cursor.execute(
                'SELECT idRegistro, kg_entregados, precio_tonelada FROM registrocinas WHERE codigo_cina = %s', 
                (codigo_cina,)
            )
            registro = cursor.fetchone()
            if registro:
                id_registro = registro[0]
                precio_tonelada = registro[2]
            else:
                flash('Código CINA no encontrado en la base de datos.', 'danger')
                return redirect(url_for('entradas'))
            
            # Calcular los kilos netos y el precio de la entrada
            net_kilos = float(kg_entrada) - float(kg_descuento)
            precio_entrada = (net_kilos / 1000) * precio_tonelada

            # Insertar la entrada en la tabla entradaspaja (sin campos de producción)
            cursor.execute('''
                INSERT INTO entradaspaja (
                    cdCina, fecha, kg_entrada, kg_descuento, n_paquetes, destino_setas,
                    destino_champis, observaciones, cd_cina, precio_entrada
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                codigo_cina, fecha, kg_entrada, kg_descuento, n_paquetes,
                destino_setas, destino_champis, observaciones, id_registro, precio_entrada
            ))
            
            # Actualizar los kg_entregados en registrocinas
            update_sql = """
                UPDATE registrocinas 
                SET kg_entregados = kg_entregados + (%s - %s)
                WHERE idRegistro = %s
            """
            cursor.execute(update_sql, (float(kg_entrada), float(kg_descuento), id_registro))
            
            net_paquetes = int(n_paquetes)
            
            if not production_mode:
                # Actualizar el stock según el destino
                if destino_tipo == 'PCHAMPI':
                    update_stock_sql = """
                        UPDATE stockcinas
                        SET kilos = kilos + (%s - %s), paquetes = paquetes + %s
                        WHERE id_destino_champ = %s 
                    """
                    cursor.execute(update_stock_sql, (float(kg_entrada), float(kg_descuento), net_paquetes, destino_champis))
                    cursor.execute("SELECT id_stock FROM stockcinas WHERE id_destino_champ = %s", (destino_champis,))
                elif destino_tipo == 'PSETAS':
                    update_stock_sql = """
                        UPDATE stockcinas
                        SET kilos = kilos + (%s - %s), paquetes = paquetes + %s
                        WHERE id_destino_setas = %s
                    """
                    cursor.execute(update_stock_sql, (float(kg_entrada), float(kg_descuento), net_paquetes, destino_setas))
                    cursor.execute("SELECT id_stock FROM stockcinas WHERE id_destino_setas = %s", (destino_setas,))

            # Si se está en modo producción, insertar el registro en produccion con los nuevos campos
            valor_compra = precio_entrada
            insert_mov_sql = """
                    INSERT INTO produccion
                    (fecha, id_stock_origen, kilos, paquetes, observaciones, num_op, valor_compra, origen_entrada)
                    VALUES (%s, NULL, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(insert_mov_sql, (fecha, net_kilos, net_paquetes, observaciones, num_op, valor_compra, True))

            conn.commit()
            flash('Entrada registrada con éxito', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al registrar la entrada: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('entradas'))

    # Método GET: carga de datos para el formulario
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT codigo_cina FROM registrocinas WHERE estado_pedido = "comenzado"')
    cinas = cursor.fetchall()
    cursor.execute('SELECT id_dest_setas, nom_dest_setas FROM destinossetas')
    destinos_setas = cursor.fetchall()
    cursor.execute('SELECT id_dest_champ, nom_dest_champ FROM destinoschamp')
    destinos_champis = cursor.fetchall()   
    conn.close()
    
    

    fecha_actual = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('formularios/entradas.html', active_page='form3',
                           cinas=cinas, 
                           fecha_actual=fecha_actual,
                           destinos_setas=destinos_setas, 
                           destinos_champis=destinos_champis,
                           )

# Vista en Crear Entradas para ver el historial entradas
@app.route('/historial_entradas')
@login_required
def historial_entradas():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = """
            SELECT 
                e.cdCina,
                e.fecha,
                e.kg_entrada,
                e.kg_descuento,
                e.n_paquetes,
                ds.nom_dest_setas,
                dc.nom_dest_champ,
                e.observaciones,
                p.num_op,
                e.idEntrada
            FROM entradaspaja e
            LEFT JOIN destinossetas ds ON e.destino_setas = ds.id_dest_setas
            LEFT JOIN destinoschamp dc ON e.destino_champis = dc.id_dest_champ
            LEFT JOIN produccion p ON e.cd_cina = p.idMovimiento
            ORDER BY e.fecha DESC
        """

        cursor.execute(query)
        entradas = cursor.fetchall()
        conn.close()

        return render_template('formularios/historial_entradas.html', entradas=entradas)
    except Exception as e:
        flash(f"Error al obtener el historial: {e}", 'danger')
        return redirect(url_for('entradas'))

# Ruta para editar una entrada
@app.route('/editar_entrada/<int:idEntrada>', methods=['GET', 'POST'])
@login_required
def editar_entrada(idEntrada):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Obtener los datos del formulario
            kg_entrada = request.form['kg_entrada']
            kg_descuento = request.form['kg_descuento']
            n_paquetes = request.form['n_paquetes']
            observaciones = request.form['observaciones']

            # Actualizar la entrada en la base de datos
            update_query = """
                UPDATE entradaspaja
                SET kg_entrada = %s, kg_descuento = %s, n_paquetes = %s, 
                      observaciones = %s
                WHERE idEntrada = %s
            """
            cursor.execute(update_query, (kg_entrada, kg_descuento, n_paquetes, observaciones, idEntrada))
            conn.commit()
            conn.close()

            flash('Entrada actualizada con éxito', 'success')
            return redirect(url_for('historial_entradas'))

        # Si es un GET, obtenemos los detalles de la entrada
        select_query = """
            SELECT 
                e.cdCina, e.fecha, e.kg_entrada, e.kg_descuento, e.n_paquetes,
                ds.nom_dest_setas, dc.nom_dest_champ, e.observaciones, e.idEntrada
            FROM entradaspaja e
            LEFT JOIN destinossetas ds ON e.destino_setas = ds.id_dest_setas
            LEFT JOIN destinoschamp dc ON e.destino_champis = dc.id_dest_champ
            WHERE e.idEntrada = %s
        """
        cursor.execute(select_query, (idEntrada,))
        entrada = cursor.fetchone()
        conn.close()

        # Pasar los datos de la entrada a la plantilla
        return render_template('formularios/editar_entrada.html', entrada=entrada)

    except Exception as e:
        flash(f"Error al editar la entrada: {e}", 'danger')
        return redirect(url_for('historial_entradas'))



@app.route('/eliminar_entrada/<int:idEntrada>', methods=['POST'])  # CAMBIADO A POST
@login_required
def eliminar_entrada(idEntrada):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entradaspaja WHERE idEntrada = %s", (idEntrada,))
        conn.commit()
        conn.close()

        flash("Entrada eliminada con éxito.", "success")
    except Exception as e:
        flash(f"Error al eliminar la entrada: {e}", "danger")

    return redirect(url_for('historial_entradas'))


@app.route('/entrada/<int:idEntrada>')
def ver_entrada(idEntrada):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Obtener la entrada específica
        cursor.execute("SELECT * FROM entradaspaja WHERE idEntrada = %s", (idEntrada,))
        entrada = cursor.fetchone()

        if not entrada:
            flash("Entrada no encontrada.")
            return redirect(url_for("entradas"))

        # Obtener los destinos de champiñones y setas
        cursor.execute("SELECT id_dest_setas, nom_dest_setas FROM destinossetas")
        destinos_setas = cursor.fetchall()

        cursor.execute("SELECT id_dest_champ, nom_dest_champ FROM destinoschamp")
        destinos_champis = cursor.fetchall()

        # Obtener las diferentes CINAs
        cursor.execute("SELECT DISTINCT cdCina FROM entradaspaja")
        cinas = cursor.fetchall()

        # Obtener el destino relacionado con la entrada (setas o champiñones)
        cursor.execute("""
            SELECT e.destino_setas, e.destino_champis
            FROM entradaspaja e
            WHERE e.idEntrada = %s
        """, (idEntrada,))
        destino_entrada = cursor.fetchone()

        # Determinar el destino actual
        if destino_entrada:
            if destino_entrada[0]:  # Si hay destino de setas
                destino_actual = destino_entrada[0]
                destino_tipo = "PSETAS"
            elif destino_entrada[1]:  # Si hay destino de champiñones
                destino_actual = destino_entrada[1]
                destino_tipo = "PCHAMPI"
            else:
                destino_actual = None
                destino_tipo = None
        else:
            destino_actual = None
            destino_tipo = None

        conn.close()

        # Pasar los datos a la plantilla
        return render_template("formularios/editar_entrada.html",
                               entrada=entrada,
                               cinas=cinas,
                               destinos_champis=destinos_champis,
                               destinos_setas=destinos_setas,
                               destino_actual=destino_actual,
                               destino_tipo=destino_tipo)

    except Exception as e:
        flash(f"Error al obtener la entrada: {e}", 'danger')
        return redirect(url_for('entradas'))



@app.route('/get_planta_destino', methods=['POST'])
@login_required
def get_planta_destino():
    codigo_cina = request.form.get('codigo_cina')
    if codigo_cina:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            # Consulta el campo 'planta_destino' del registro correspondiente
            cursor.execute("SELECT planta_destino FROM registrocinas WHERE codigo_cina = %s", (codigo_cina,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                return jsonify({'planta_destino': result[0]})
            else:
                return jsonify({'planta_destino': None})
        except Exception as e:
            return jsonify({'planta_destino': None, 'error': str(e)})
    return jsonify({'planta_destino': None})

# Vista para mostrar todas las CINA con filtros y enlace para ver su historial de entradas
@app.route('/ver_entradas', methods=['GET'])
@login_required
def ver_entradas():
    # Recuperar los parámetros de filtro enviados por GET
    anio_cosecha   = request.args.get('anio_cosecha', '')
    planta_destino = request.args.get('planta_destino', '')
    kg_diferencia  = request.args.get('kg_diferencia', '')
    estado_pedido  = request.args.get('estado_pedido', '')
    busqueda       = request.args.get('busqueda', '')
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Obtener los valores únicos para los filtros
        cursor.execute("SELECT DISTINCT anio_cosecha FROM registrocinas")
        años = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT planta_destino FROM registrocinas")
        plantas = [row[0] for row in cursor.fetchall()]
        
        # Consulta que obtiene los registros de CINA con los filtros aplicados,
        # incluyendo un filtro de búsqueda sobre el código de CINA
        sql = """SELECT rc.fecha_acuerdo, 
                rc.codigo_cina, 
                rc.kilos, 
                rc.kg_entregados, 
                rc.kg_diferencia, 
                rc.estado_pedido,
                rc.planta_destino, 
                rc.anio_cosecha,
                ROUND((rc.kg_entregados / rc.kilos) * 100, 2) AS porcentaje_completado
         FROM registrocinas rc
         WHERE (%s = '' OR rc.anio_cosecha = %s)
           AND (%s = '' OR rc.planta_destino = %s)
           AND (%s = '' OR (rc.kg_diferencia >= 0 AND %s = 'positivo') OR (rc.kg_diferencia < 0 AND %s = 'negativo'))
           AND (%s = '' OR rc.estado_pedido = %s)
           AND (%s = '' OR rc.codigo_cina LIKE %s)
         ORDER BY rc.fecha_acuerdo ASC"""
        
        cursor.execute(sql, (
            anio_cosecha, anio_cosecha,
            planta_destino, planta_destino,
            kg_diferencia, kg_diferencia, kg_diferencia,
            estado_pedido, estado_pedido,
            busqueda, f'%{busqueda}%'
        ))
        cinas = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error al obtener las CINA: {str(e)}')
        cinas = []
        años = []
        plantas = []
    
    return render_template('formularios/ver_entradas.html', active_page='ver_entradas',
                           cinas=cinas, 
                           años=años, 
                           plantas=plantas,
                           anio_cosecha=anio_cosecha,
                           planta_destino=planta_destino,
                           kg_diferencia=kg_diferencia,
                           estado_pedido=estado_pedido,
                           busqueda=busqueda)

# Vista para mostrar las entradas de una CINA seleccionada
@app.route('/ver_entradas/<path:codigo_cina>', methods=['GET'])
@login_required
def ver_entradas_detalle(codigo_cina):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # Obtener el idRegistro correspondiente al código de CINA
        cursor.execute("SELECT idRegistro FROM registrocinas WHERE codigo_cina = %s", (codigo_cina,))
        cina = cursor.fetchone()
        if not cina:
            flash('CINA no encontrada.', 'danger')
            return redirect(url_for('ver_entradas'))
        id_registro = cina[0]
        
        # Obtener los kilos contratados y los kilos entregados de la CINA
        cursor.execute("SELECT kilos, kg_entregados FROM registrocinas WHERE idRegistro = %s", (id_registro,))
        result = cursor.fetchone()
        if result:
            kilos_contrato, kg_entregados = result
            kg_faltantes = kilos_contrato - kg_entregados
            
            # Calcular el porcentaje completado, cuidando evitar división por cero
            if kilos_contrato > 0:
                porcentaje_completado = round((kg_entregados / kilos_contrato) * 100, 2)
            else:
                porcentaje_completado = 0
        else:
            kilos_contrato = kg_entregados = kg_faltantes = 0
            porcentaje_completado = 0
        
        # Obtener las entradas ordenadas por fecha descendente
        cursor.execute("""
            SELECT e.fecha, e.kg_entrada, e.kg_descuento, e.n_paquetes,
                ds.nom_dest_setas, dc.nom_dest_champ, e.observaciones
            FROM entradaspaja e
            LEFT JOIN destinossetas ds ON e.destino_setas = ds.id_dest_setas
            LEFT JOIN destinoschamp dc ON e.destino_champis = dc.id_dest_champ
            WHERE e.cd_cina = %s
            ORDER BY e.fecha DESC, e.idEntrada DESC
        """, (id_registro,))
        entradas = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('formularios/ver_entradas_historial.html', 
                       codigo_cina=codigo_cina, 
                       entradas=entradas,
                       kg_entregados_total=kg_entregados,
                       kg_faltantes=kg_faltantes,
                       porcentaje_completado=porcentaje_completado)

    except Exception as e:
        flash(f'Error al obtener las entradas: {str(e)}')
        return redirect(url_for('ver_entradas'))

@app.route('/entradas_proveedor', methods=['GET'])
@login_required
def entradas_proveedor():
    # Recuperar parámetros de filtro: fechas y proveedor
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    proveedor = request.args.get('proveedor', '')

    query = """
        SELECT e.fecha, e.kg_entrada, e.kg_descuento, e.n_paquetes, e.observaciones, e.cdCina, 
               p.idProveedor, p.nombreProveedor
        FROM entradaspaja e
        JOIN registrocinas rc ON e.cd_cina = rc.idRegistro
        JOIN proveedores p ON rc.proveedorID = p.idProveedor
    """
    params = []
    conditions = []
    if fecha_inicio:
        conditions.append("e.fecha >= %s")
        params.append(fecha_inicio)
    if fecha_fin:
        conditions.append("e.fecha <= %s")
        params.append(fecha_fin)
    if proveedor:
        conditions.append("p.idProveedor = %s")
        params.append(proveedor)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    # Ordenar de fecha más reciente a más antigua
    query += " ORDER BY e.fecha DESC"

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convertir cada tupla en un diccionario para facilitar el acceso en la plantilla
        entradas = []
        for row in rows:
            entrada = {
                'fecha': row[0],
                'kg_entrada': row[1],
                'kg_descuento': row[2],
                'n_paquetes': row[3],
                'observaciones': row[4],
                'cdCina': row[5],
                'proveedorID': row[6],
                'nombreProveedor': row[7]
            }
            entradas.append(entrada)
    except Exception as e:
        flash(f'Error al obtener el informe: {str(e)}', 'danger')
        entradas = []

    # Obtener la lista de proveedores para el filtro en la vista
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idProveedor, nombreProveedor FROM proveedores")
        proveedores_data = cursor.fetchall()
        cursor.close()
        conn.close()
        proveedores = [{'idProveedor': row[0], 'nombreProveedor': row[1]} for row in proveedores_data]
    except Exception as e:
        proveedores = []

    return render_template('formularios/entradas_proveedor.html',  active_page='informes',
                           entradas=entradas,
                           proveedores=proveedores,
                           selected_proveedor=proveedor)

@app.route('/produccion', methods=['GET', 'POST'])
@login_required
def produccion():
    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_stock = request.form.get('tipo_stock')  # 'PCHAMPI' o 'PSETAS'
        fecha = request.form.get('fecha')            # Formato "YYYY-MM-DDTHH:MM"
        kg_mover = request.form.get('kg_mover')
        paquetes_mover = request.form.get('paquetes_mover')
        origen_stock = request.form.get('origen_stock')  # id_stock seleccionado
        observaciones = request.form.get('observaciones', '')
        # Campo para número de operación
        num_op = request.form.get('num_op', '')

        # Validar campos obligatorios
        if not tipo_stock or not fecha or not kg_mover or not paquetes_mover or not origen_stock:
            flash('Todos los campos son obligatorios.', 'warning')
            return redirect(url_for('produccion'))
        
        try:
            # Convertir a números
            kg_mover = float(kg_mover)
            paquetes_mover = int(paquetes_mover)
            
            conn = mysql.connect()
            cursor = conn.cursor()

            # Consultar stock actual del origen seleccionado
            cursor.execute("SELECT kilos, paquetes FROM stockcinas WHERE id_stock = %s", (origen_stock,))
            stock_data = cursor.fetchone()
            if not stock_data:
                flash("No se encontró el registro de stock seleccionado.", "danger")
                return redirect(url_for('produccion'))
            
            current_kilos, current_paquetes = stock_data
            if current_kilos < kg_mover or current_paquetes < paquetes_mover:
                flash("Stock insuficiente para realizar el movimiento.", "danger")
                return redirect(url_for('produccion'))
            
            # Actualizar stock: restar los kilos y paquetes a mover
            update_stock_sql = """
                UPDATE stockcinas 
                SET kilos = kilos - %s, paquetes = paquetes - %s
                WHERE id_stock = %s
            """
            cursor.execute(update_stock_sql, (kg_mover, paquetes_mover, origen_stock))
            
            # Determinar el idOperacion para la operación
            idOperacion = None
            if num_op:
                # Buscar si ya existe un idOperacion para este num_op
                cursor.execute("SELECT idOperacion FROM produccion WHERE num_op = %s LIMIT 1", (num_op,))
                result = cursor.fetchone()
                if result and result[0] is not None:
                    idOperacion = result[0]
                else:
                    # Generar un nuevo idOperacion: se toma el mayor actual y se incrementa en 1
                    cursor.execute("SELECT COALESCE(MAX(idOperacion), 0) + 1 FROM produccion")
                    idOperacion = cursor.fetchone()[0]
            
            # Insertar el movimiento en la tabla de produccion, incluyendo el idOperacion
            insert_mov_sql = """
                INSERT INTO produccion
                (fecha, id_stock_origen, kilos, paquetes, observaciones, num_op, idOperacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_mov_sql, (fecha, origen_stock, kg_mover, paquetes_mover, observaciones, num_op, idOperacion))
            
            conn.commit()
            flash("Movimiento a Producción registrado con éxito.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error al registrar el movimiento: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('produccion'))
    
    # Método GET: preparar datos para el formulario
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # Fecha actual para input datetime-local
    fecha_actual = datetime.now().strftime('%Y-%m-%dT%H:%M')
    
    # Consultar stock para destinos de setas
    cursor.execute("""
        SELECT s.id_stock, d.nom_dest_setas, s.kilos, s.paquetes 
        FROM stockcinas s
        JOIN destinossetas d ON s.id_destino_setas = d.id_dest_setas
    """)
    stock_setas = cursor.fetchall()
    
    # Consultar stock para destinos de champiñones
    cursor.execute("""
        SELECT s.id_stock, d.nom_dest_champ, s.kilos, s.paquetes 
        FROM stockcinas s
        JOIN destinoschamp d ON s.id_destino_champ = d.id_dest_champ
    """)
    stock_champis = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('formularios/produccion.html', active_page='produccion',
                           fecha_actual=fecha_actual, 
                           stock_setas=stock_setas, 
                           stock_champis=stock_champis)
    
@app.route('/deuda_proveedor')
@login_required
def deuda_proveedor():
    # Recuperar el filtro del proveedor desde la URL
    proveedor = request.args.get('proveedor', '')
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = """
            SELECT 
                p.idProveedor, 
                p.nombreProveedor, 
                SUM(rc.kilos) AS total_kilos, 
                SUM(rc.kg_entregados) AS total_entregados, 
                SUM(rc.kilos - rc.kg_entregados) AS deuda
            FROM registrocinas rc
            JOIN proveedores p ON rc.proveedorID = p.idProveedor
        """
        params = []
        if proveedor:
            query += " WHERE p.idProveedor = %s"
            params.append(proveedor)
        query += " GROUP BY p.idProveedor, p.nombreProveedor HAVING deuda > 0 ORDER BY deuda DESC;"
        
        cursor.execute(query, tuple(params))
        deudas = cursor.fetchall()  
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error al obtener la deuda de los proveedores: {str(e)}', 'danger')
        deudas = []
        
    # Query para mostrar la lista de proveedores en el select
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idProveedor, nombreProveedor FROM proveedores")
        proveedores_data = cursor.fetchall()
        cursor.close()
        conn.close()
        proveedores = [{'idProveedor': row[0], 'nombreProveedor': row[1]} for row in proveedores_data]
    except Exception as e:
        proveedores = []
    
    return render_template('formularios/deuda_proveedor.html', active_page='informes', deudas=deudas, proveedores=proveedores)

@app.route('/contratos_pendientes')
@login_required
def contratos_pendientes():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = """
            SELECT 
                rc.contrato_marco, 
                rc.anio_cosecha,
                p.nombreProveedor,
                rc.codigo_cina,
                SUM(rc.kilos) AS total_kilos, 
                SUM(rc.kg_entregados) AS total_entregados, 
                SUM(rc.kilos - rc.kg_entregados) AS pendientes
            FROM registrocinas rc
            JOIN proveedores p ON rc.proveedorID = p.idProveedor
            GROUP BY rc.contrato_marco, rc.anio_cosecha, p.nombreProveedor, rc.codigo_cina
            HAVING pendientes > 0
            ORDER BY pendientes DESC;
        """
        cursor.execute(query)
        contratos = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error al obtener contratos pendientes: {str(e)}', 'danger')
        contratos = []
    
    return render_template('formularios/contratos_pendientes.html', active_page='informes', contratos=contratos)

#Vista que muestra el stock de cinas (champiñones o setas)
@app.route('/stock_cinas', methods=['GET'])
@login_required
def stock_cinas():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # Consulta para recuperar los datos de stockcinas con las tablas relacionadas:
        query = """
            SELECT s.id_stock,
                   s.kilos,
                   s.paquetes,
                   ds.nom_dest_setas,
                   dc.nom_dest_champ
            FROM stockcinas s
            LEFT JOIN destinossetas ds  ON s.id_destino_setas = ds.id_dest_setas
            LEFT JOIN destinoschamp dc  ON s.id_destino_champ = dc.id_dest_champ
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Convertimos el resultado en una lista de diccionarios
        stock_data = []
        for row in rows:
            id_stock        = row[0]
            kilos           = float(row[1]) if row[1] else 0.0
            paquetes        = int(row[2])   if row[2] else 0
            nom_dest_setas  = row[3]
            nom_dest_champ  = row[4]
            
            # Determinamos el tipo de cina y el nombre a mostrar
            if nom_dest_setas:
                tipo = 'Setas'
                destino = nom_dest_setas
            elif nom_dest_champ:
                tipo = 'Champiñones'
                destino = nom_dest_champ
            else:
                tipo = 'Desconocido'
                destino = 'N/A'
            
            # Calculamos los kilos por paquete, evitando división por cero
            kilos_por_paquete = kilos / paquetes if paquetes > 0 else 0
            
            stock_data.append({
                'id_stock': id_stock,
                'kilos': kilos,
                'paquetes': paquetes,
                'tipo': tipo,
                'destino': destino,
                'kilos_por_paquete': kilos_por_paquete
            })
        
        # Calculamos el máximo de kilos
        max_kilos = max([d['kilos'] for d in stock_data]) if stock_data else 1
        
        return render_template('formularios/stock_cinas.html', active_page='stock_cinas',
                               stock=stock_data, 
                               max_kilos=max_kilos)
    except Exception as e:
        flash(f"Error al obtener el stock de cinas: {e}", "danger")
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()

@app.route('/detalle_cina/<tipo>/<path:destino>', methods=['GET'])
@login_required
def detalle_cina(tipo, destino):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Según el tipo, obtenemos el id del destino
        if tipo == 'setas':
            cursor.execute("SELECT id_dest_setas FROM destinossetas WHERE LOWER(TRIM(nom_dest_setas)) = LOWER(TRIM(%s))",(destino,))
            result = cursor.fetchone()
            if result:
                id_dest = result[0]
            else:
                flash("Destino no encontrado.", "warning")
                return redirect(url_for('stock_cinas'))
            
            # Consulta de entradas para destino de setas
            query_entradas = """
                SELECT fecha, kg_entrada, n_paquetes, cdCina
                FROM entradaspaja
                WHERE destino_setas = %s
                ORDER BY fecha DESC
            """
            # Consulta de movimientos (producción) para destino de setas
            query_produccion = """
                SELECT p.fecha, p.kilos, p.paquetes, p.num_op
                FROM produccion p
                JOIN stockcinas s ON p.id_stock_origen = s.id_stock
                WHERE s.id_destino_setas = %s
                ORDER BY p.fecha DESC
            """
            
        elif tipo == 'champiñones':
            cursor.execute("SELECT id_dest_champ FROM destinoschamp WHERE nom_dest_champ = %s", (destino,))
            result = cursor.fetchone()
            if result:
                id_dest = result[0]
            else:
                flash("Destino no encontrado.", "warning")
                return redirect(url_for('stock_cinas'))
            
            # Consulta de entradas para destino de champiñones
            query_entradas = """
                SELECT fecha, kg_entrada, n_paquetes, cdCina
                FROM entradaspaja
                WHERE destino_champis = %s
                ORDER BY fecha DESC
            """
            # Consulta de movimientos (producción) para destino de champiñones
            query_produccion = """
                SELECT p.fecha, p.kilos, p.paquetes, p.num_op
                FROM produccion p
                JOIN stockcinas s ON p.id_stock_origen = s.id_stock
                WHERE s.id_destino_champ = %s
                ORDER BY p.fecha DESC
            """
        else:
            flash("Tipo de CINA no válido.", "warning")
            return redirect(url_for('stock_cinas'))
        
        # Ejecutamos las consultas
        cursor.execute(query_entradas, (id_dest,))
        entradas = cursor.fetchall()
        
        cursor.execute(query_produccion, (id_dest,))
        produccion = cursor.fetchall()
        
        return render_template('formularios/detalle_cina.html', 
                               tipo=tipo,
                               destino=destino,
                               entradas=entradas,
                               produccion=produccion)
    except Exception as e:
        flash(f"Error al obtener los movimientos para {destino}: {e}", "danger")
        return redirect(url_for('stock_cinas'))
    finally:
        cursor.close()
        conn.close()

@app.route('/crear_cina', methods=['POST'])
@login_required
def crear_cina():
    cina_type = request.form.get('cinaType')
    destino_nombre = request.form.get('destinoNombre')
    
    # Valores por defecto: 0 kilos y 0 paquetes
    initial_kilos = 0
    initial_paquetes = 0
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        if cina_type == 'setas':
            # Insertar nuevo destino en la tabla destinossetas
            cursor.execute("INSERT INTO destinossetas (nom_dest_setas) VALUES (%s)", (destino_nombre,))
            conn.commit()
            dest_id = cursor.lastrowid
            # Crear nuevo stock asociado al destino de setas
            cursor.execute("INSERT INTO stockcinas (id_destino_setas, kilos, paquetes) VALUES (%s, %s, %s)", 
                           (dest_id, initial_kilos, initial_paquetes))
        elif cina_type == 'champiñones':
            # Insertar nuevo destino en la tabla destinoschamp
            cursor.execute("INSERT INTO destinoschamp (nom_dest_champ) VALUES (%s)", (destino_nombre,))
            conn.commit()
            dest_id = cursor.lastrowid
            # Crear nuevo stock asociado al destino de champiñones
            cursor.execute("INSERT INTO stockcinas (id_destino_champ, kilos, paquetes) VALUES (%s, %s, %s)", 
                           (dest_id, initial_kilos, initial_paquetes))
        else:
            flash("Tipo de CINA no válido", "danger")
            return redirect(url_for('stock_cinas'))
        
        conn.commit()
        flash("Nueva CINA creada correctamente", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error al crear nueva CINA: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('stock_cinas'))

@app.route('/crear_proveedor', methods=['POST'])
@login_required
def crear_proveedor():
    nombre_proveedor = request.form.get('nombreProveedor').upper() 
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # Insertar el nuevo proveedor en la tabla con el nombre en mayúsculas
        cursor.execute("INSERT INTO proveedores (nombreProveedor) VALUES (%s)", (nombre_proveedor,))
        conn.commit()
        flash("Nuevo proveedor creado correctamente", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error al crear nuevo proveedor: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('index'))

@app.route('/ver_operaciones', methods=['GET'])
@login_required
def ver_operaciones():
    # Obtener parámetros de filtrado
    year = request.args.get('year', None)       
    month = request.args.get('month', None)       
    num_op_search = request.args.get('num_op', None)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Consulta de agrupación con filtros
        query = """
            SELECT 
                num_op,
                CONCAT(DATE(MIN(fecha)), ' - ', DATE(MAX(fecha))) AS resumen_fecha,
                SUM(kilos) AS total_kilos,
                SUM(paquetes) AS total_paquetes
            FROM produccion
            WHERE num_op IS NOT NULL AND num_op <> ''
        """
        params = []
        
        # Filtro por año
        if year:
            query += " AND YEAR(fecha) = %s"
            params.append(year)
        
        # Filtro por mes
        if month:
            query += " AND MONTH(fecha) = %s"
            params.append(month)
        
        # Filtro para buscar un número de operación en concreto
        if num_op_search:
            query += " AND num_op = %s"
            params.append(num_op_search)
        
        query += " GROUP BY num_op ORDER BY MAX(fecha) DESC;"
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        columns = [col[0] for col in cursor.description]
        operaciones = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error al obtener las operaciones: {str(e)}', 'danger')
        operaciones = []
    
    return render_template('formularios/ver_operaciones.html', operaciones=operaciones)

@app.route('/detalle_operacion/<num_op>', methods=['GET'])
@login_required
def detalle_operacion(num_op):
    try:
        # Conexión a la base de datos
        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Consulta para obtener los registros de la operación junto con el nombre del destino
        query = """
            SELECT 
                p.idMovimiento,
                p.fecha,
                COALESCE(ds.nom_dest_setas, dc.nom_dest_champ, 'Sin destino') AS destino,
                p.kilos,
                p.paquetes,
                p.observaciones
            FROM produccion p
            LEFT JOIN stockcinas sc ON p.id_stock_origen = sc.id_stock
            LEFT JOIN destinossetas ds ON sc.id_destino_setas = ds.id_dest_setas
            LEFT JOIN destinoschamp dc ON sc.id_destino_champ = dc.id_dest_champ
            WHERE p.num_op = %s
            ORDER BY p.fecha ASC;
        """
        cursor.execute(query, (num_op,))
        registros = cursor.fetchall()
        
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error al obtener los registros: {str(e)}', 'danger')
        registros = []
    
    return render_template('formularios/detalle_operacion.html', registros=registros, num_op=num_op)

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
 
        # Verifica si se ha enviado una búsqueda
        search = request.args.get('search', '')
       
        # Si se realiza una búsqueda, agrego el filtro en la consulta
        if search:
            cursor.execute('SELECT * FROM usuarios WHERE codigoUsuario LIKE %s', ('%' + search + '%',))
        else:
            cursor.execute('SELECT * FROM usuarios')
       
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f'Error al gestionar los roles: {str(e)}', 'danger')
        usuarios = []
   
    return render_template('formularios/usuarios.html', usuarios=usuarios)
 
 
 
@app.route('/cambiar_rol', methods=['POST'])
def cambiar_rol():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
 
        # Se Obtiene datos del formulario
        codigoUsuario = request.form['codigoUsuario']
        nuevo_rol = request.form['role']
 
        # Y Ejecuto la actualización en la base de datos
        cursor.execute("UPDATE usuarios SET role = %s WHERE codigoUsuario = %s", (nuevo_rol, codigoUsuario))
        conn.commit()
 
        flash("Rol actualizado correctamente", "success")
    except Exception as e:
        flash(f"Error al actualizar el rol: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
 
    return redirect(url_for('usuarios'))
 
 
 
@app.route('/eliminar_usuario/<string:codigoUsuario>', methods=['GET'])
def eliminar_usuario(codigoUsuario):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
 
        # Eliminar el usuario con el código proporcionado
        cursor.execute("DELETE FROM usuarios WHERE codigoUsuario = %s", (codigoUsuario,))
        conn.commit()
 
        flash("Usuario eliminado correctamente", "success")
    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
 
    return redirect(url_for('usuarios'))  # Se redirije a la página de usuarios
 
 
 
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
 
        # Se Obtiene datos del formulario
        codigoUsuario = request.form['codigoUsuario']
        contrasena = request.form['password']
        role = request.form['role']
 
        # Se Inserta el nuevo usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (codigoUsuario, password, role) VALUES (%s, %s, %s)",
                       (codigoUsuario, contrasena, role))
        conn.commit()
 
        flash("Usuario agregado correctamente", "success")
    except Exception as e:
        flash(f"Error al agregar usuario: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
 
    return redirect(url_for('usuarios'))

# Ruta para la página principal
@app.route('/')
@login_required
def log():
    return redirect(url_for('index'))

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 4000))
    debug = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']
    app.run(host=host, port=port, debug=debug)