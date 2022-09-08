from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from Livro import Livro


class App:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get('https://sigaa.ufma.br/sigaa/verTelaLogin.do')
        self.driver.implicitly_wait(30)
        self.username = ''
        self.password = ''
        self.dados = {}

    def login(self, id, password):
        self.username = self.driver.find_element(By.CSS_SELECTOR, '#usuarioLogin')
        self.password = self.driver.find_element(By.CSS_SELECTOR, '#senhaLogin')
        self.username.send_keys(id)
        self.password.send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, '#formLogin > input.botao-entrar').click()

    def buscar(self):
        self.driver.find_element(By.CSS_SELECTOR, '#menu\:formbiblioteca\:menubiblioteca').click()
        self.driver.find_element(By.CSS_SELECTOR, '#menu\:formbiblioteca\:subMenubib_emprestimos').click()
        self.driver.find_element(By.CSS_SELECTOR, '#menu\:formbiblioteca\:bib_renovarEmprestimos').click()

    def importDados(self):
        dados_gerais = self.driver.find_elements(By.CSS_SELECTOR,
                                                 '#formularioRenovamaMeusEmprestimos > table > tbody > tr')
        for dado in dados_gerais:
            cod = dado.text.split('-')[
                0].strip()  # split('-').strip()
            titulo = dado.text.split('-')[1].strip()
            dataInicial = dado \
                .find_element(By.CSS_SELECTOR,
                              '#formularioRenovamaMeusEmprestimos > table > tbody > tr > td:nth-child(3)').text
            dataFinal = dado \
                .find_element(By.CSS_SELECTOR,
                              '#formularioRenovamaMeusEmprestimos > table > tbody > tr > td:nth-child(4)') \
                .text.split(" ")[0].strip()
            livro = Livro(cod, titulo, dataInicial, dataFinal)
            self.dados[livro.getCod()] = livro.toJson()