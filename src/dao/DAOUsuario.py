import pymysql

class DAOUsuario:
    def connect(self):
        return pymysql.connect("localhost","root","","db_chaka" )

    def validate(self,data):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("select * from usuario where correo = %s and clave = %s",(data['correo'],data['clave'],))
            return cursor.fetchone()
        except:
            return ()
        finally:
            con.close()

    def create(self,data):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO usuario(nombre,usuario,correo,clave,tipo) VALUES(%s, %s, %s, %s, %s)", (data['nombre'],data['usuario'],data['correo'],data['clave'],data['tipo'],)) 
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    
    def sesion(self,user):
        con = DAOUsuario.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("select * from usuario where usuario = %s",(user,))
            return cursor.fetchone()
        except:
            return ()
        finally:
            con.close()   

class DAOProducto:
    def connect(self):
        return pymysql.connect("localhost","root","","db_chaka" )

    def read(self, id):
        con = DAOProducto.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM producto order by titulo asc")
            else:
                cursor.execute("SELECT * FROM producto where idproducto = %s order by titulo asc", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
            
    def readProductor(self, id):
        con = DAOProducto.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM producto order by titulo asc")
            else:
                cursor.execute("SELECT * FROM producto where idproductor = %s order by titulo asc", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def stock(self, id):
        con = DAOProducto.connect(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT sum(stock) FROM producto where idproductor = %s", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,data):
        con = DAOProducto.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO producto(idproductor,categoria,precio,stock,descripcion,valoracion,imagen,titulo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (data['idproductor'],data['categoria'],data['precio'],data['stock'],data['descripcion'],data['valoracion'],data['imagen'],data['titulo']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update(self, id, data):
        con = DAOProducto.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE producto set idproductor = %s, categoria = %s, precio = %s , stock = %s , descripcion = %s, valoracion = %s, imagen = %s, titulo = %s where idproducto = %s", (data['idproductor'],data['categoria'],data['precio'],data['stock'],data['descripcion'],data['valoracion'],data['imagen'],data['titulo'],id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, id):
        con = DAOProducto.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM producto where idproducto = %s", (id))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()  

class DAOLista:
    def connect(self):
        return pymysql.connect("localhost","root","","db_chaka" )

    def read(self, id):
        con = DAOLista.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM lista")
            else:
                cursor.execute("SELECT * FROM lista where idlista = %s", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def readUser(self, idusuario):
        con = DAOLista.connect(self)
        cursor = con.cursor()

        try:
            if idusuario == None:
                cursor.execute("SELECT * FROM lista")
            else:
                cursor.execute("SELECT * FROM lista where idusuario = %s", (idusuario,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
 
    def insert(self,idproducto,idusuario):
        con = DAOLista.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO lista(idproducto,idusuario) VALUES(%s, %s)", (idproducto,idusuario))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    
    def update(self, id, data):
        con = DAOLista.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE lista set idproducto = %s, idusuario = %s where idlista = %s", (data['idproducto'],data['idusuario'],id))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, id):
        con = DAOLista.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM lista where idlista = %s", (id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

class DAOCheckout:
    def connect(self):
        return pymysql.connect("localhost","root","","db_chaka" )

    def read(self, idcheckout):
        con = DAOCheckout.connect(self)
        cursor = con.cursor()

        try:
            if idcheckout == None:
                cursor.execute("SELECT * FROM checkout order by nombre asc")
            else:
                cursor.execute("SELECT * FROM checkout where idcheckout = %s order by nombre asc", (idcheckout,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,data):
        con = DAOCheckout.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO checkout(departamento,direccion,zipcode,telefono) VALUES(%s,%s, %s, %s)", (data['departamento'],data['direccion'],data['zipcode'],data['telefono']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def insertUsertoo(self,data, idusuario):
        con = DAOCheckout.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO checkout(idusuario,departamento,direccion,zipcode,telefono) VALUES(%s,%s,%s, %s, %s)", (idusuario,data['departamento'],data['direccion'],data['zipcode'],data['telefono']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update(self, idcheckout, data):
        con = DAOCheckout.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE checkout set departamento = %s, direccion = %s, zipcode = %s, telefono = %s,  where idcheckout = %s", (data['departamento'],data['direccion'],data['zipcode'],data['telefono']),idcheckout,)
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, idcheckout):
        con = DAOCheckout.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM checkout where idcheckout = %s", (idcheckout,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()