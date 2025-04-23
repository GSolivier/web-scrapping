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
caminho_driver = "C:\Program Files\chromedriver-win64\chromedriver.exe"

# Configurarção do WebDriver
service = Service(caminho_driver) # Navegador controlado pelo selenium
controle = webdriver.ChromeOptions() # Configurar as opções do navegador
controle.add_argument("--disable-gpu") # Evita possíveis gráficos
controle.add_argument("--window-size=1920,1080") # Define uma resolução fixa
# controle.add_argument("--headless") # Executa o navegador sem abrir a interface visual

# Inicialização do WebDriver
driver = webdriver.Chrome(service=service, options=controle)

# URL inicial
url_base = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'
driver.get(url_base)
time.sleep(5) # Aguarda 5 segundos para garantir que a página carregue

# Criar um dicionário vazio para armazenar as marcas e preços das cadeiras
dic_produtos = {
    "titulo": [], 
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
    except TimeoutException as te:
        print("Tempo de espera excedido!", te)
    
    produtos = driver.find_elements(By.CLASS_NAME, "productCard")

    for produto in produtos:
        try:
            titulo = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{titulo}: {preco}")

            dic_produtos["titulo"].append(titulo)
            dic_produtos["preco"].append(preco)
        except Exception as e:
            print("Erro ao coletar dados", e)
    
    # Encontrar botão para a próxima página
    try:

        botao_proximo = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )

        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            # Clicar no botão
            driver.execute_script("arguments[0].click();", botao_proximo)
            pagina += 1
            print(f"Indo para a pagina {pagina}")
            time.sleep(5)

    except TimeoutException:
        print("Você chegou na última página.")
        break

    except Exception as e:
        print("Erro inesperado ao tentar ir para a próxima página:", e)

# Fecha o navegador
driver.quit()

df = pd.DataFrame(dic_produtos)

df.to_excel("cadeiras.xlsx", index=False)

print(f"Arquivo 'cadeiras' salvo com sucesso! {len(df)} produtos armazenados!")








