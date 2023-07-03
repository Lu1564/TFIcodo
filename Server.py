from flask import Flask, jsonify, request, redirect, url_for,render_template,session,send_file,send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'cifrador de seguridad'

CORS(app)
# Parámetros de conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/clientes'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'clientes': 'mysql+pymysql://root@localhost:3306/clientes',
    'productos': 'mysql+pymysql://root@localhost:3306/prueba'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Producto (db.Model):
    __bind_key__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(100))
    id_fabricante = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    
    def __init__(self,nombre,precio,stock,imagen,id_fabricante):
    
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.id_fabricante = id_fabricante
        
    
class Fabricante (db.Model):
    __bind_key__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_fabricante = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    
    def __init__(self,nombre,logo,pais):
        self.nombre_fabricante = nombre
        self.logo = logo
        self.pais = pais
        


class Usuario(db.Model,UserMixin):
    __bind_key__ = 'clientes'
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    
    def __init__(self,email,password):
        self.email =email
        self.password = password
    
    def get_id(self):
        return self.email
        
with app.app_context():
    db.create_all()
    
ma = Marshmallow(app)
# Crea clases que determinan que atributos de la tabla sql se mostrara en las consultas

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "precio", "stock", "imagen", "id_fabricante")

schema_producto = ProductoSchema()
schema_productos = ProductoSchema(many=True)

class FabricanteSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre_fabricante", "logo", "pais")

schema_fabricante = FabricanteSchema()
schema_fabricantes = FabricanteSchema(many=True)
#Rutas producto
@app.route("/prueba/producto", methods=["GET"])
def getProductos():
    todos_productos = Producto.query.all()
    resultado = schema_productos.dump(todos_productos)
    return jsonify(resultado)

@app.route("/prueba/producto/<id>", methods=["GET"])
def getProducto(id):
    producto = Producto.query.get(id)
    return schema_producto.jsonify(producto)

@app.route("/prueba/producto/<id>", methods=["DELETE"])
def deleteProducto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return schema_producto.jsonify(producto)

@app.route("/prueba/producto", methods=["POST"])
def agregarProducto():
    nombre = request.json["nombre"]
    precio = request.json["precio"]
    stock = request.json["stock"]
    imagen = request.json["imagen"]
    id_fabricante = request.json["id_fabricante"]
    productoNuevo = Producto(nombre, precio, stock, imagen, id_fabricante)
    db.session.add(productoNuevo)
    db.session.commit()
    return schema_producto.jsonify(productoNuevo)

@app.route("/prueba/producto/<id>", methods=["PUT"])
def modificarProducto(id):
    producto = Producto.query.get(id)
    producto.nombre = request.json["nombre"]
    producto.precio = request.json["precio"]
    producto.stock = request.json["stock"]
    producto.imagen = request.json["imagen"]
    producto.id_fabricante = request.json["id_fabricante"]
    db.session.commit()
    return schema_producto.jsonify(producto)

@app.route("/prueba/fabricante", methods=["GET"])
def getFabricantes():
    todos_fabricantes = Fabricante.query.all()
    resultado = schema_fabricantes.dump(todos_fabricantes)
    return jsonify(resultado)

@app.route("/prueba/fabricante/<id>", methods=["GET"])
def getFabricante(id):
    fabricante = Fabricante.query.get(id)
    return schema_fabricante.jsonify(fabricante)

@app.route("/prueba/fabricante/<id>", methods=["DELETE"])
def deleteFabricante(id):
    fabricante = Fabricante.query.get(id)
    db.session.delete(fabricante)
    db.session.commit()
    return schema_fabricante.jsonify(fabricante)

@app.route("/prueba/fabricante", methods=["POST"])
def agregarFabricante():
    nombre_fabricante = request.json["nombre_fabricante"]
    logo = request.json["logo"]
    pais = request.json["pais"]
    fabricanteNuevo = Fabricante(nombre_fabricante, logo, pais)
    db.session.add(fabricanteNuevo)
    db.session.commit()
    return schema_fabricante.jsonify(fabricanteNuevo)

@app.route("/prueba/fabricante/<id>", methods=["PUT"])
def modificarFabricante(id):
    fabricante = Fabricante.query.get(id)
    fabricante.nombre_fabricante = request.json["nombre_fabricante"]
    fabricante.logo = request.json["logo"]
    fabricante.pais = request.json["pais"]
    db.session.commit()
    return schema_fabricante.jsonify(fabricante)

# Rutas Cliente
@app.route('/inicio')
def index():
    return render_template('index.html')
@app.route('/formulario.js')
def js():
    print("hola")
    return render_template('formulario.js')

@app.route('/HeaderFooter.js')
def jsPyF():
    return render_template('HeaderFooter.js')

@app.route('/login', methods=['POST'])
def login():
    print("hola2")
    email2 = request.json.get('email')
    password2 = request.json.get('password')
    print(email2)
    print(password2)

    user = Usuario.query.filter_by(email=email2, password=password2).first()
    print(user)
    if user:
        login_user(user)
        return redirect(url_for('protected'))
    
@app.route('/signin', methods=['POST'])
def signin():
    print("hola 3")
    email2 = request.json.get('email')
    password2 = request.json.get('password')
    print(email2)
    print(password2)
    user = Usuario.query.filter_by(email=email2, password=password2).first()
    if not user :
        nuevoUsuario = Usuario(email=email2, password=password2)
        db.session.add(nuevoUsuario)
        db.session.commit()
        session['email'] = email2
        return redirect(url_for('registrado'))
    else:
        return redirect(url_for('inicio'))
    
@app.route('/registrado')
def registrado():
    email = session.get('email')
    if email:
        return 'Logeado como: ' + email
    else:
        return 'No hay usuario registrado'
    
@app.route('/protected')
@login_required
def protected():
    # return 'Logeado como: ' + current_user.email
    return redirect(url_for('producto'))

@app.route('/producto')
@login_required
def producto():
    return send_file('Templates/productos.html')

@app.route('/productos.js')
def jsProductos():
    return render_template('productos.js')

@app.route('/<filename>')
@login_required
def productoX(filename):
    return send_from_directory('static', filename)

@app.route('/crear-producto')
@login_required
def crearProducto():
    return send_file('Templates/producto-create.html')

@app.route('/update-producto/<id>')
@login_required
def updateProducto(id):
    return send_file('Templates/producto-update.html')


@app.route('/update-producto/producto-edit.js')
def jsProductoEdit():
    return render_template('producto-edit.js')

@app.route('/update-producto/HeaderFooter.js')
def jsPyFo():
    return render_template('HeaderFooter.js')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return send_file('Templates/logout.html')


# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(email):
    user = Usuario.query.get(email)
    return user


if __name__ == '__main__':
    app.run(port=5000, debug=True)

