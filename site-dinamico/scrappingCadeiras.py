# pip install selenium
# Módulo para controlar o navegador WEB
from selenium import webdriver

# Localizador de elementos
from selenium.webdriver.common.by import By

# Serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# Classe que permite executar ações avançadas como por exemplo mover o mouse, clicar e arrastar etc...
from selenium.webdriver.common.action_chains import ActionChains

# Classe que espera de forma explicita até que uma condição seja satisfeita
from selenium.webdriver.support.ui import WebDriverWait

# Condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Trabalhar com dataframe
import pandas as pd

# Uso de funções relacionadas ao tempo
import time

# Uso de tratamento de exceção
from selenium.common.exceptions import TimeoutException

# Definir o caminho do chromedriver
chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

# Configurarção do WebDriver
service = Service(chrome_driver_path) # Navegador controlado pelo selenium
options = webdriver.ChromeOptions() # Configurar as opções do navegador
options.add_argument("--disable-gpu") # Evita possíveis gráficos
options.add_argument("--window-size=1920,1080") # Define uma resolução fixa

# Inicialização do WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL inicial
url_base = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'
driver.get(url_base)
time.sleep(5) # Aguarda 5 segundos para garantir que a página carregue

# Criar um dicionário vazio para armazenar as marcas e preços das cadeiras
dic_produtos = {
    "marca": [], 
    "preco": [],
    }

# Inicar na página 1 e incrementamos a cada troca de página
pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}")

    try:
    # WebDriverWait(driver, 10): Cria uma espera de até 10 segundos
    # until(...): Faz com que o codigo espere até que a condição seja verdadeira
    # ec.presence_of_all_elements_located(...): Verifica se todos os elementos estão acessiveis
    # By.CLASS_NAME, "productCard": Indica a classe que sera buscada
        WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.CLASS_NAME, "productCard"))
    )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")
    

    produtos = driver.find_elements(By.CLASS_NAME, "productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{nome}: {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)
        except Exception:
            print("Erro ao coletar dados", Exception)
        

# Encontrar o acesso para a próxima página
# Fechar o navegador
# Criar DataFrame
# Salvar os dados em .csv






