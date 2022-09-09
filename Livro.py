class Livro:
    def __init__(self, cod, titulo, dataemp, datafinal, status):
        self.cod = cod
        self.titulo = titulo
        self.dataemp = dataemp
        self.datafinal = datafinal
        self.status = status

    def fromJson(self, json):
        self.cod = json['cod']
        self.titulo = json['titulo']
        self.dataemp = json['dataemp']
        self.datafinal = json['datafinal']
        self.status = json['status']

    def toJson(self):
        data = {}
        data['cod'] = self.cod
        data['titulo'] = self.titulo
        data['dataemp'] = self.dataemp
        data['datafinal'] = self.datafinal
        data['status'] = self.status
        return data

    def getCod(self):
        return self.cod

    def getTitulo(self):
        return self.titulo

    def getDataEmp(self):
        return self.dataemp

    def getDataFinal(self):
        return self.datafinal
