from flask import Flask, flash, render_template, redirect, url_for, request, session
from dao.DAOUsuario import DAOUsuario, DAOProducto, DAOCheckout, DAOLista
 

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"

db = DAOUsuario()
dbProducto = DAOProducto()
dbCheckout = DAOCheckout()
dbLista = DAOLista()


@app.route('/')
def principal():
    return render_template('login.html')

@app.route('/registro')
def index():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/productor/contacto/<string:usuario>')
def contactanos(usuario):
    user = db.sesion(usuario)  
    return render_template('productor/contactanos.html', user = user)

@app.route('/nuevo_inicio', methods = ['POST', 'GET'])
def ninicio():
    if request.method == 'POST'and request.form['registrar']:
        if db.create(request.form):
            if request.form['tipo'] == 'cliente':
                return redirect(url_for('cliente',usuario =request.form['usuario']))
            else:
                return redirect(url_for('productor',usuario =request.form['usuario']))
        else:
            flash("ERROR al crear usuario, emplee otro usuario")
            return render_template('registro.html')
    else:
        return render_template('registro.html')

@app.route('/iniciar', methods = ['POST'])
def iniciar():
    if request.method == 'POST'and request.form['iniciar']:
        data = db.validate(request.form)
        if data == None:
            flash("ERROR, usuario invalido")
            return redirect(url_for('ninicio'))
        else:    
            if len(data) != 0:
                if data[5] == 'cliente':
                    return redirect(url_for('cliente',usuario = data[2]))
                else:
                    return redirect(url_for('productor',usuario = data[2]))                
    else:
        return render_template('login.html')

@app.route('/productor/<string:usuario>')
def productor(usuario):
    user = db.sesion(usuario)
    stock = dbProducto.stock(user[0])
    productos = dbProducto.readProductor(user[0])
    """db.sesion es una funcion para conocer el usuario que esta conectado"""                                               
    return render_template('productor/productor_index.html', user = user, stock = stock, productos = productos) 

@app.route('/cliente/<string:usuario>')
def cliente(usuario):
    user = db.sesion(usuario)
    data = dbProducto.read(None)
    """db.sesion es una funcion para conocer el usuario que esta conectado"""                                               
    return redirect(url_for('tienda', usuario = usuario))

@app.route('/productor/producto/<string:usuario>')
def productor_producto(usuario):
    print(usuario)
    user = db.sesion(usuario)
    data = dbProducto.readProductor(user[0])
    return render_template('productor/productos.html', data = data, user = user)

@app.route('/productor/add/<string:usuario>')
def productor_add(usuario):
    user = db.sesion(usuario)
    data = dbProducto.readProductor(user[0])
    return render_template('productor/add.html', data = data, user = user)

@app.route('/productor/update/<string:usuario>/<int:producto>')
def producto_update(usuario,producto):
    user = db.sesion(usuario)
    data = dbProducto.read(producto)
    return render_template('productor/update.html', data = data, user = user)

@app.route('/productor/anadirProducto/<string:usuario>', methods = ['POST', 'GET'])
def anadirProducto(usuario):
    user = db.sesion(usuario)
    if request.method == 'POST' and request.form['guardar']:
        if dbProducto.insert(request.form):
            print(request.form)
            flash("Nuevo producto creado")
        else:
            flash("ERROR, al crear producto")

        return redirect(url_for('productor_add', usuario = user[2]))
    else:
        return redirect(url_for('productor_add', usuario = user[2]))

@app.route('/productor/update_lista/<string:usuario>/<int:producto>', methods = ['POST', 'GET'])
def producto_update_lista(usuario,producto):
    user = db.sesion(usuario)
    if request.method == 'POST' and request.form['update']:
        print(request.form)
        print(producto)
        if dbProducto.update(producto,request.form):
            flash("Nuevo producto creado")
        else:
            flash("ERROR, al crear producto")

        return redirect(url_for('productor_producto', usuario = user[2]))
    else:
        return redirect(url_for('productor_producto', usuario = user[2]))

@app.route('/productor/delete/<string:usuario>/<int:producto>')
def eliminarProducto(usuario,producto):
    user = db.sesion(usuario)
    print(producto)
    dbProducto.delete(producto)
    return redirect(url_for('productor_producto', usuario = user[2]))


########################################################################################
#INICIA PARTE MARITA MIRELLA

@app.route('/anadircarrito/<string:usuario>/<int:idproducto>')
def anadircarrito(usuario,idproducto):
    user = db.sesion(usuario)
    data = dbProducto.read(None)
    dbLista.insert(idproducto,user[0])
    return redirect(url_for('tienda', usuario = usuario))

@app.route('/Acercade/<string:usuario>')
def Acercade(usuario):
    user = db.sesion(usuario)
    return render_template('/about.html', user= user)

@app.route('/Contacto/<string:usuario>')
def contactos(usuario):
    user = db.sesion(usuario)
    return render_template('/contact.html',user= user)

@app.route('/Index/<string:usuario>')
def iniciousuario(usuario):
    user = db.sesion(usuario)
    return render_template('/index.html',user= user)

@app.route('/Registrarse/')
def registrarse():
    return render_template('/registro.html')

@app.route('/Tienda/<string:usuario>/')
def tienda(usuario):
    user = db.sesion(usuario)
    data = dbProducto.read(None)
    return render_template('/shop.html',user = user, data=data )
    
@app.route('/Carrito/<string:usuario>/')
def carrito(usuario):
    user = db.sesion(usuario)
    datalist=dbLista.readUser(user[0])
    rows=len(datalist)
    data = [[0 for x in range(3)] for y in range(rows)]
    prod = dbProducto.read(None)
    for i in range(rows):
        dat=datalist[i][1]
        print(dat)
        data[i][0]=prod[int(dat-1)][8]
        data[i][1]=prod[int(dat-1)][3]
        data[i][2]=1
    print(data)
        
        
    #return render_template('/index.html')
    return render_template('/cart.html',user= user ,data=data)

# @app.route('/Carrito/')
# def carrito():
#     datalist=dbLista.read(None)
#     rows=len(datalist)
#     data = [[0 for x in range(3)] for y in range(rows)]
#     prod = dbProducto.read(None)
#     print(prod)
#     print(datalist)
#     for i in range(rows):
#         dat=datalist[i][1]
#         print(dat)
#         print(prod[int(dat-1)][1])
#     print(data)

@app.route('/Checkout/<string:usuario>/')
def checkout(usuario):
    user = db.sesion(usuario)
    return render_template('checkout.html', user = user)

@app.route('/productSingle/<string:usuario>/<int:idproducto>')
def productSingle(usuario,idproducto):
    user = db.sesion(usuario)
    data = dbProducto.read(idproducto)
    dbLista.insert(idproducto,user[0])
    return render_template('/product-single.html', user = user, data = data)

@app.route('/QR/<string:usuario>')
def qr(usuario):
    user = db.sesion(usuario)
    return render_template('/QR.html',user= user)


@app.route('/guardarcheckout/<string:usuario>', methods = ['POST', 'GET'])
def guardarcheckout(usuario):
    user = db.sesion(usuario)
    if request.method == 'POST' and request.form['save']:
        if dbCheckout.insertUsertoo(request.form,user[0]):
            print("Se guardo el pedido")
            return redirect(url_for('qr', usuario = usuario))
        else:
            print("ERROR")
            return redirect(url_for('checkout',usuario = usuario))

    else:
        return redirect(url_for('checkout', usuario = usuario))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0",debug=True)
