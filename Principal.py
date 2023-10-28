import datetime
import socket
import tkinter as tk
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json

from mysqlx.expr_unparser import column_identifier_to_string

from Cliente import Cliente

v = Tk()
v.title('Consultas y Pagos')
v.geometry('950x650')

global crearT
global listaClientes
global cuotaSel
global suma
global fecha
global monto
cuotaSel = None
suma = 0
fecha = None
monto = 0.0
listaClientes = []

top_Frame = ttk.Frame(v)
top_Frame.pack(side="top", fill="x", padx=20, pady=20)

bottom_Frame = ttk.Frame(v)
bottom_Frame.pack(side="bottom", fill="x", padx=20, pady=20)

t_frame = ttk.Frame(v)
#t_frame.grid(row=3, column=0, padx=20, pady=20, columnspan=3)
t_frame.pack(side="top", padx=20, pady=20, fill="both", expand=True)
columns = ["ID", "Cuota", "Monto", "Fecha Pago", "Fecha Pago Realizacion", "Estado", "Referencia"]
table = ttk.Treeview(t_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)
table.pack(fill="both", expand=True)

rb_Frame = ttk.Frame(v)
rb_Frame.pack(side="left", padx=10)

rb = []


def create_Table():
    for i in range(3):
        #var = tk.BooleanVar(value=False)
        #r_Frame = ttk.Frame(t_frame)
        #r_Frame.grid(row=i, column=0)
        #r_Frame.pack(side="top")
        #radio_Button = tk.Radiobutton(rb_Frame, variable=var)
        #radio_Button.grid(row=0, column=0)
        #radio_Button.pack(side="top")
        row_Data = ('', '', '', '', '', '', '')
        table.insert('', 'end', values=row_Data)
        #rb.append(var)
    table.pack()


create_Table()


def on_treeview_select(event):
    global cuotaSel
    selected_item = table.selection()[0]
    item_values = table.item(selected_item, 'values')
    cuotaSel = item_values[1]


table.bind("<ButtonRelease-1>", on_treeview_select)

"""
1. Verificar que se selecciono algo
2. No puedo revertir el pago de la cuota 1 si la cuota 2 ya se pago

"""
def revertirPago():
    global id
    global cuotaSel
    global fecha
    global monto
    fecha = None
    monto = 0.0
    current_Time = datetime.datetime.now()

    if not cuotaSel:
        messagebox.showerror("Error", "No ha seleccionado una cuota para pagar")
    else:
        for i in range(len(listaClientes) - 1, -1, -1):
            cliente = listaClientes[i]
            if i == len(listaClientes) - 1:
                if cuotaSel == cliente.getCuota():
                    if cliente.getEstado() == 'C':
                        reverse(current_Time, cliente, cuotaSel)
                    else:
                        messagebox.showwarning("Alerta","No ha cancelado la cuota")
            else:
                if cuotaSel == cliente.getCuota():
                    nCliente = listaClientes[i + 1]
                    estado = nCliente.getEstado()
                    print(nCliente.getCuota())
                    if estado == 'C':
                        messagebox.showwarning("Alerta", "Solo puede revertir la ultima cuota pagada")
                        break
                    else:
                        reverse(current_Time, cliente, cuotaSel)
            """if i.getCuota() != cuotaSel:
                messagebox.showinfo("Aviso", "Solo puede revertir la ultima cuota pagada")
                break
            else:
                lon = len(i.getReferencia())
                if lon < 1:
                    messagebox.showwarning("Alerta", "La cuota aun no ha sido pagada")
                    break
                else:
                    host = '127.0.0.1'
                    port = 5017
                    date = current_Time.date()

                    if date == i.getFechaPR():
                        print('Son iguales')


                        try:
                        id = i.getID()
                        ref = i.getReferencia()
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((host, port))
                        tipo = 3
                        s.sendall(str.encode("\n".join([str(id), str(tipo), str(cuotaSel), str(fecha), str(monto)])))
                        data = s.recv(4096).decode('utf-8')
                        if data:
                            messagebox.showinfo("Info", "EL pago se ha revertido correctamente")
                        else:
                            messagebox.showerror("Error","Ha ocurrido un error")
                        s.close()

                    except Exception as e:
                        messagebox.showerror("Error", "Ha ocurrido un error")"""



def reverse(current_Time, cliente, cuotaSel):
    host = '127.0.0.1'
    port = 5020
    date = current_Time.date()
    print(cliente.getFechaPR())
    print(date)
    if str(date) == cliente.getFechaPR():
        print('Son iguales')
        try:
            id = cliente.getID()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            tipo = 3
            monto = 0.0
            ref = cliente.getReferencia()
            s.sendall(str.encode("\n".join([str(id), str(tipo), str(cuotaSel), str(date), str(monto), str(ref)])))
            print('id='+id+', referencia='+ref)
            data = s.recv(4096).decode('utf-8')
            print(data + 'datos')
            if data:
                messagebox.showinfo("Info", "EL pago se ha revertido correctamente")
                tipo = 1
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                listaClientes.clear()
                for item in table.get_children():
                    table.delete(item)
                search(listaClientes, id, tipo, cuotaSel, fecha, monto, s)
            else:
                print('no se recivio nada')
                messagebox.showerror("Error", "Ha ocurrido un error")
            s.close()

        except Exception as e:
            messagebox.showerror("Error", "Ha ocurrido un error")
            print('Hubo un error')
    else:
        messagebox.showinfo("Info", "Ha pasado el tiempo limite para revertir el pago")


def PagarCuota():
    global suma
    global cuotaSel

    if not cuotaSel:
        print('No ha seleccionado una cuota para pagar')
        messagebox.showerror("Error", "No ha seleccionado una cuota para pagar")
    else:
        for index, i in enumerate(listaClientes):

            if cuotaSel == '1':
                if index == 0:
                    if i.getEstado() == 'P':
                        pay(i)
                    else:
                        messagebox.showwarning("Alerta", "La cuota ya ha sido cancelada")
                        break
            else:
                if cuotaSel == i.getCuota():
                    cliente = listaClientes[index-1]
                    estado = cliente.getEstado()
                    if estado == 'P':
                        messagebox.showwarning("Alerta", "No ha pagado la cuota anterior")
                        break
                    else:
                        pay(i)


def pay(i):
    host = '127.0.0.1'
    port = 5020
    try:
        current_Time = datetime.datetime.now()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        id = i.getID()
        tipo = 2
        monto = i.getMonto()
        fecha = current_Time.date()
        ref = ''
        s.sendall(str.encode("\n".join([str(id), str(tipo), str(cuotaSel), str(fecha), str(monto), str(ref)])))
        data = s.recv(4096).decode('utf-8')
        s.close()
        if data:
            messagebox.showinfo("Info", "Pago realizado correctamente")
            tipo = 1
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            listaClientes.clear()
            for item in table.get_children():
                table.delete(item)
            search(listaClientes, id, tipo, cuotaSel, fecha, monto, s)
        else:
            messagebox.showerror("Error", "Ha ocurrido un error")

    except Exception as e:
        print('Hubo un error!! ', e)
        messagebox.showerror("Error", "Ha ocurrido un error")


def buscarCliente():
    listaClientes.clear()

    for item in table.get_children():
        table.delete(item)

    global cuotaSel
    global fecha
    global monto
    cuotaSel = None
    fecha = None
    monto = 0.0

    host = '127.0.0.1'
    port = 5020

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        id = ide.get()
        tipo = 1
        if not id:
            print('El campo no puede estar vacio')
            messagebox.showinfo("Info", "El campo no puede estar vacio")
        else:
            search(listaClientes, id, tipo, cuotaSel, fecha, monto, s)


    except Exception as e:
        print('Hubo un error de conexion', e)
        messagebox.showerror("Error", "Hubo un error de conexion")


def search(listaClientes, id, tipo, cuotaSel, fecha, monto, s):
    ref = ''
    s.sendall(str.encode("\n".join([str(id), str(tipo), str(cuotaSel), str(fecha), str(monto), str(ref)])))
    data = s.recv(4096).decode('utf-8')

    if data:
        try:
            datos = json.loads(data)

            if isinstance(datos, list):
                for item in datos:
                    cliente = Cliente()
                    cliente.setID(item['ID'])
                    cliente.setCuota(item['Cuota'])
                    cliente.setMonto(item['Monto'])
                    cliente.setFechaP(item['Fecha_Pago'])
                    cliente.setFechaPR(item['Fecha_Pago_Realizacion'])
                    cliente.setEstado(item['Estado'])
                    cliente.setReferencia(item['Referencia'])
                    listaClientes.append(cliente)
            populate_Table()
            id = ide.get()
            tipo = 1
            s.close()
        except json.JSONDecodeError as e:
            print('Error parsing', e)
            messagebox.showerror("Error", "Ha ocurrido un error")
    else:
        messagebox.showerror("Error", "Ha ocurrido un error")
        print('Data is empty')


def populate_Table():
    for item in table.get_children():
        table.delete(item)

    for i, item in enumerate(listaClientes):
        row_Data = (item.getID(), item.getCuota(), item.getMonto(), item.getFechaP(),
                                        item.getFechaPR(), item.getEstado(), item.getReferencia())
        table.insert('', 'end', values=row_Data)


def cleanTable():
    listaClientes.clear()

    for item in table.get_children():
        table.delete(item)


lblID = Label(top_Frame, text="ID del cliente a buscar")
lblID.pack(side="left", padx=10, pady=10)
global ide
ide = StringVar()
txtID = ttk.Entry(top_Frame, textvariable=ide)
txtID.pack(side="left", padx=10, pady=10)
btnSearch = Button(top_Frame, text="Buscar", command=buscarCliente)
btnSearch.pack(side="left", padx=10, pady=10)
btnPay = Button(bottom_Frame, text="Pagar", command=PagarCuota)
btnPay.pack(side="left", padx=10, pady=10)
btnRevert = Button(bottom_Frame, text="Revertir Pago", command=revertirPago)
btnRevert.pack(side="left", padx=10, pady=10)
btnClean = Button(bottom_Frame, text="Limpiar", command=cleanTable)
btnClean.pack(side="left", padx=10, pady=10)

v.mainloop()
