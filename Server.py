import socket
import mysql.connector
import json
import random

from Client_Encoder import Client_Encoder
from Cliente import Cliente


def server_program():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="grupo2",
        database="Exam"
    )

    host = '127.0.0.1'  # obetner el nombre del host
    port = 5020  # asignarle un numero de puerto

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    while True:
        try:
            s.listen(2)  # el numero de sockets con los que se va a trabajar
            conn, address = s.accept()  # esperar la conexion del cliente
            print("Connectionn from: " + str(address))
            # while True:
            # data = conn.recv(1024).decode() #recibe un valor del cliente

            id, tipo, cuota, fecha, monto, ref = [i for i in conn.recv(4096).decode('utf-8').split('\n')]
            print(tipo + " , " + id)
            if not (id or tipo):
                break
            if (tipo == '1'):
                cursor = mydb.cursor(dictionary=True)
                listaClientes = []
                try:
                    listaClientes = []
                    cursor.execute(
                        "SELECT ID, Cuota, Monto, Fecha_Pago, Fecha_Pago_Realizacion, Estado, Referencia FROM TblEXa WHERE ID=" + str(
                            id))
                    for row in cursor:
                        cliente = Cliente()
                        cliente.setID(str(row['ID']))
                        cliente.setCuota(str(row['Cuota']))
                        cliente.setMonto(str(row['Monto']))
                        cliente.setFechaP(str(row['Fecha_Pago']))
                        cliente.setFechaPR(str(row['Fecha_Pago_Realizacion']))
                        cliente.setEstado(row['Estado'])
                        cliente.setReferencia(row['Referencia'])
                        listaClientes.append(cliente)
                    data = json.dumps(listaClientes, cls=Client_Encoder, indent=7)
                    conn.send(data.encode('utf-8'))
                except Exception as e:
                    print('Hubo un error2', e)
                # data = 'send'
                # conn.send(data.encode())
            if tipo == '2':
                cursor = mydb.cursor()
                result = pagarCuota(cursor, mydb, fecha, cuota, id)
                conn.send(str(result).encode())
            if tipo == '3':
                cursor = mydb.cursor()
                result = revertir(cursor, mydb, id, ref)
                conn.send(str(result).encode())
            conn.close()
        except Exception as e:
            print('Hubo un error 1', e)


def pagarCuota(cursor, mydb, fecha, cuota, id):
    try:
        ref = generarREf()
        sql = "UPDATE TblEXa set Fecha_Pago_Realizacion = '" + fecha + "', Estado = 'C', Referencia = '" + ref + "' WHERE ID = " + id + " and Cuota = " + cuota
        cursor.execute(sql)
        mydb.commit()
        result = '00'
        return result
    except Exception as e:
        print('Error', e)


def revertir(cursor, mydb, id, ref):
    try:
        print('id='+id+', ref='+ref)
        sql = "UPDATE TblEXa set Fecha_Pago_Realizacion = null, Estado = 'P', Referencia = '' WHERE ID = " + id + " and Referencia = '" + ref + "'"
        cursor.execute(sql)
        mydb.commit()
        result = '00'
        return result
    except Exception as e:
        print('Error', e)


def generarREf():
    ref = "XBLN-"
    for i in range(3):
        ran = random.randint(1, 9)
        num = str(ran)
        ref += num
    return ref


if __name__ == '__main__':
    server_program()
