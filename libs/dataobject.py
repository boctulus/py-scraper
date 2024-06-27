'''
Convierte diccionario en un objeto

Uso:

data = DataObject(**ins_dict)
'''
class DataObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
