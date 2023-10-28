import mysql.connector

from Cliente import Cliente

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="grupo2",
    database="Exam"
)

cursor = mydb.cursor(dictionary=True)

#sql = "UPDATE TblEXa SET Fecha_Pago_Realizacion = '2023-10-19', Estado='C' WHERE ID = 1 AND Cuota = 1"

#cursor.execute(sql)

#mydb.commit()

#search
listaClientes = []
#cliente = Cliente()
id = 1
cursor.execute("SELECT ID, Cuota, Monto, Fecha_Pago, Estado FROM TblEXa WHERE ID=" + str(id))
#result = cursor.fetchall()
for row in cursor:
    cliente = Cliente()
    cliente.setID(row['ID'])
    cliente.setCuota(row['Cuota'])
    cliente.setMonto(row['Monto'])
    cliente.setFechaP(row['Fecha_Pago'])
    cliente.setFechaPR("")
    cliente.setEstado(row['Estado'])
    listaClientes.append(cliente)
    print(row['Fecha_Pago'])

print(len(listaClientes))
#Insert
#sql = ("INSERT INTO TblExa (ID, Cuota, Monto, Fecha_Pago, Fecha_Pago_Realizacion, Estado) "
       #"values (%s, %s, %s, %s, %s, %s)")
#data1 = (4, 1, 900.00, "2023-10-1", "", "P")
#cursor.execute(sql, data1)
#mydb.commit()

#print(mydb)