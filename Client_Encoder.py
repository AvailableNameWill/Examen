import json

from Cliente import Cliente


class Client_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cliente):
            return {
                'ID': obj.ID,
                'Cuota': obj.Cuota,
                'Monto': obj.Monto,
                'Fecha_Pago': obj.Fecha_Pago,
                'Fecha_Pago_Realizacion': obj.Fecha_Pago_Realizacion,
                'Estado': obj.Estado,
                'Referencia': obj.Referencia
            }
        return super().default(obj)