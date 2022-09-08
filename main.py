from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request
import os,json
from time import sleep


# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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


class App:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        # self.driver.get('https://sigaa.ufma.br/sigaa/verTelaLogin.do')
        self.driver.implicitly_wait(30)
        self.username = ''
        self.password = ''
        self.dados = []
        self.ativo = True

    def getSite(self):
        if self.ativo:
            self.driver.get('https://sigaa.ufma.br/sigaa/verTelaLogin.do')
            return True
        return False

    def login(self):
        self.username = self.driver.find_element(By.CSS_SELECTOR, '#usuarioLogin')
        self.password = self.driver.find_element(By.CSS_SELECTOR, '#senhaLogin')
        with open("credentials.json") as file:
            data = json.load(file)
            self.username.send_keys(data["id"])
            self.password.send_keys(data["pass"])
        self.driver.find_element(By.CSS_SELECTOR, '#formLogin > input.botao-entrar').click()

    def buscar(self):
        self.driver.find_element(By.CSS_SELECTOR, '#menu\:formbiblioteca\:menubiblioteca').click()
        self.driver.find_element(By.CSS_SELECTOR, '#menu\:formbiblioteca\:subMenubib_emprestimos').click()
        self.driver.find_element(By.CSS_SELECTOR, '#menu\:formbiblioteca\:bib_renovarEmprestimos').click()

    def importDados(self):
        dados_gerais = self.driver.find_elements(By.CSS_SELECTOR,
                                                 '#formularioRenovamaMeusEmprestimos > table > tbody > tr')
        for dado in dados_gerais:
            cod = dado.text.split('-')[0].strip()  # split('-').strip()
            titulo = dado.text.split('-')[1].strip()
            dataInicial = dado \
                .find_element(By.CSS_SELECTOR,
                              '#formularioRenovamaMeusEmprestimos > table > tbody > tr > td:nth-child(3)').text
            dataFinal = dado \
                .find_element(By.CSS_SELECTOR,
                              '#formularioRenovamaMeusEmprestimos > table > tbody > tr > td:nth-child(4)') \
                .text.split(" ")[0].strip()
            livro = Livro(cod, titulo, dataInicial, dataFinal)
            # self.dados[livro.getCod()] = livro.toJson()
            self.dados.append(livro.toJson())
        # self.ativo = False
        self.driver.quit()


app = Flask(__name__)


@app.route("/")
def hello():
    return "Olá, Mundo!"


@app.route('/teste', methods=['GET'])
def teste():
    app2 = App()
    entrar = app2.getSite()
    if entrar:
        app2.login()
        app2.buscar()
        app2.importDados()
    return app2.dados

    # return 'testando 2'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    #########################
    #
    # app = App()
    # app.login('araujo.lucas', 'cargap10')
    # app.buscar()
    # while True:
    #     app.importDados()
    #     for cod, livro in app.dados.items():
    #         print(f"{cod} --  {livro}")
    #     key = input()
    #     print(f"Cód: {str(cod)}\tTítulo: {str(livro.getTitulo())}\n"
    #           f"DataInicial {str(livro.getDataEmp())}"
    #           f"\tDataEntrega {str(livro.getDataFinal())}"
    #           f"\n-----------------------------")
    # # print(app.dados)
