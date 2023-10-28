class Cliente:

    ID = ""
    Cuota = ""
    Monto = ""
    Fecha_Pago = ""
    Fecha_Pago_Realizacion = ""
    Estado = ""
    Referencia = ""

    def __init__(self, ID="", Cuota="", Monto="", Fecha_Pago="", Fecha_Pago_Realizacion="", Estado="", Referencia=""):
        self.ID = ID
        self.Cuota = Cuota
        self.Monto = Monto
        self.Fecha_Pago = Fecha_Pago
        self.Fecha_Pago_Realizacion = Fecha_Pago_Realizacion
        self.Estado = Estado
        self.Referencia = Referencia

    def getID(self):
        return self.ID

    def setID(self, value):
        self.ID = value

    def getCuota(self):
        return self.Cuota

    def setCuota(self, value):
        self.Cuota = value

    def getMonto(self):
        return self.Monto

    def setMonto(self, value):
        self.Monto = value

    def getFechaP(self):
        return self.Fecha_Pago

    def setFechaP(self, value):
        self.Fecha_Pago = value

    def getFechaPR(self):
        return self.Fecha_Pago_Realizacion

    def setFechaPR(self, value):
        self.Fecha_Pago_Realizacion = value

    def getEstado(self):
        return self.Estado

    def setEstado(self, value):
        self.Estado = value

    def getReferencia(self):
        return self.Referencia

    def setReferencia(self, value):
        self.Referencia = value