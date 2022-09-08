class Livro:
    def __init__(self, cod, titulo, dataemp, datafinal):
        self.cod = cod
        self.titulo = titulo
        self.dataemp = dataemp
        self.datafinal = datafinal

    def fromJson(self, json):
        self.cod = json['cod']
        self.titulo = json['titulo']
        self.dataemp = json['dataemp']
        self.datafinal = json['datafinal']

    def toJson(self):
        data = {}
        data['cod'] = self.cod
        data['titulo'] = self.titulo
        data['dataemp'] = self.dataemp
        data['datafinal'] = self.datafinal
        return data

    def getCod(self):
        return self.cod

    def getTitulo(self):
        return self.titulo

    def getDataEmp(self):
        return self.dataemp

    def getDataFinal(self):
        return self.datafinal
