from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request
import os, json
import Livro

from Livro import Livro

#teste
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

    def getSite(self, url):
        if self.ativo:
            self.driver.get(url)
            return True
        return False

    def login(self):
        self.username = self.driver.find_element(By.CSS_SELECTOR, '#usuarioLogin')
        self.password = self.driver.find_element(By.CSS_SELECTOR, '#senhaLogin')
        self.username.send_keys('araujo.lucas')
        self.password.send_keys('cargap10')
        self.driver.find_element(By.CSS_SELECTOR, '#formLogin > input.botao-entrar').click()

    def buscar_historico(self):
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#menu\:formbiblioteca\:menubiblioteca').click()  # abre painel biblioteca
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#menu\:formbiblioteca\:subMenubib_emprestimos').click()  # clica em empréstimos
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#menu\:formbiblioteca\:bib_historicoEmprestimos').click()  # clica em ver historico
        dataInicialBuscaHistorico = self.driver.find_element(By.CSS_SELECTOR,
                                                             '#j_id_jsp_50816789_1\:j_id_jsp_50816789_23')
        dataInicialBuscaHistorico.clear()  # deixando em branco mostra todos
        # dataInicialBuscaHistorico.send_keys('10/03/2018')
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#j_id_jsp_50816789_1 > table.formulario > tfoot > tr > td > input[type=submit]:nth-child(1)').click()

    def importEmprestimos(self):
        linhas_pares = self.driver.find_elements(By.CLASS_NAME, 'linhaPar')
        linhas_impares = self.driver.find_elements(By.CLASS_NAME, 'linhaImpar')
        # pegar os dois primeiros elemento ,processar, e dar um pop nos 2 primeiros
        i = 0
        while (True):
            try:
                dataEmp = linhas_pares[i].find_elements(By.TAG_NAME, 'td')[1].text.split(" ")[0]
                dataFinal = linhas_pares[i].find_elements(By.TAG_NAME, 'td')[3].text.split(" ")[0]
                status = linhas_pares[i].find_elements(By.TAG_NAME, 'td')[5].text
                cod = linhas_pares[i + 1].text.split('-')[0].strip()
                titulo = linhas_pares[i + 1].text.split('-')[1].strip()
                print(cod, titulo, dataEmp, status)
                i += 2
                livro = Livro(cod, titulo, dataEmp, dataFinal, status)
                self.dados.append(livro.toJson())
                print('-----')
            except:
                break
        i = 0
        print("<<<>>>>>")
        while (True):
            try:
                dataEmp = linhas_impares[i].find_elements(By.TAG_NAME, 'td')[1].text.split(" ")[0]
                dataFinal = linhas_pares[i].find_elements(By.TAG_NAME, 'td')[3].text.split(" ")[0]
                status = linhas_impares[i].find_elements(By.TAG_NAME, 'td')[5].text
                cod = linhas_impares[i + 1].text.split('-')[0].strip()
                titulo = linhas_impares[i + 1].text.split('-')[1].strip()
                print(cod, titulo, dataEmp, status)
                i += 2
                livro = Livro(cod, titulo, dataEmp, dataFinal, status)
                self.dados.append(livro.toJson())
                print('-----')
            except:
                break
        self.driver.quit()

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

#
# app = App()
# app.getSite('https://sigaa.ufma.br/sigaa/verTelaLogin.do')
# app.login()
# app.buscar_historico()
# app.importEmprestimos()
# print(app.dados)
# print(len(app.dados))

app = Flask(__name__)


@app.route("/")
def hello():
    return "Olá, Mundo!"


@app.route('/teste', methods=['GET'])
def teste():
    app = App()
    app.getSite('https://sigaa.ufma.br/sigaa/verTelaLogin.do')
    app.login()
    app.buscar_historico()
    app.importEmprestimos()
    return app.dados

    # return 'testando 2'


port = int(os.environ.get('PORT', 5001))
app.run(host='0.0.0.0', port=port)
