from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import pandas as pd

option = webdriver.ChromeOptions()

driver = webdriver.Chrome('chromedriver', options=option)

url = 'https://famem.org.br/municipios/municipios/exibe'
driver.get(url)
time.sleep(1)
soup_prefeitos = BeautifulSoup(driver.page_source, 'html.parser')

select_municipio = soup_prefeitos.find('select', id='cboMunicipio')
options = select_municipio.find_all('option')

cidade_list = []

for option in options:
    value = option['value']
    cidade_list.append(value)
data = []
for value in cidade_list:

    driver.find_element(By.NAME, 'frmMunicipio').submit()
    
    time.sleep(2) 
    
    soup_nome_data = BeautifulSoup(driver.page_source, 'html.parser')

    prefeito_dados = soup_nome_data.find('ul', class_='lista-dados-prefeito')
    nome_prefeito = ""
    aniversario_prefeito = ""
    div_conteudo = soup_nome_data.find('div', class_='conteudo-areas-tecnicas')
    nome_municipio = div_conteudo.find('h1', class_='titulo').get_text(strip=True)

    print("Nome do municipio:", nome_municipio)

    if prefeito_dados:

        nome_element = prefeito_dados.find('span', class_='info-prefeito-red')
        if nome_element:
            nome_prefeito = nome_element.find_next_sibling(text=True)


        aniversario_element = prefeito_dados.find('span', string='Aniversário Prefeito:')
        if aniversario_element:
            aniversario_prefeito = aniversario_element.find_next_sibling(text=True)
    data.append([nome_municipio, nome_prefeito, aniversario_prefeito])
    print("Nome do Prefeito:", nome_prefeito)
    print("Aniversário do Prefeito:", aniversario_prefeito)

df = pd.DataFrame(data, columns=['Nome Município', 'Nome Prefeito', 'Aniversário Prefeito'])

df.to_csv('informacoes_prefeitos.csv', index=False)

print("Arquivo CSV salvo com sucesso!")