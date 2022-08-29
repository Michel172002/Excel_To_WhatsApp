import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# links e xpaths

WPP_LINK = "https://web.whatsapp.com/"
SEND_BUTTON = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
INV_BUTTON = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(WPP_LINK)  # abre o whatsapp. necessita autenticacao via QRCode
sleep(20)

#Verifica se já foi conectado o whatsapp
try:
    while driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div/a'):
        sleep(1)
except selenium.common.exceptions.NoSuchElementException:
    print("Usuario Conectado!")

def send_message(numero, msg):
    # chama a api para enviar mensagem a um numero
    url = "https://web.whatsapp.com/send?phone={}&text={}"
    driver.get(url.format(numero, msg))
    sleep(10)

    #Verifica se o contato existe
    try:
        # clica no botao de enviar mensagem
        send_button = driver.find_element(By.XPATH, SEND_BUTTON)
        send_button.click()
        sleep(3)
    except selenium.common.exceptions.NoSuchElementException:
        #caso o numero não existe vai fechar a mensagem
        driver.find_element(By.XPATH, INV_BUTTON).click()


# coloque o caminho do arquivo
df = pd.read_excel('lista_contatos_bot_wpp.xlsx')
numeros = df['Telefone'].values.tolist()
nomes = df['Nome'].values.tolist()
# defina abaixo a mensagem que quer enviar
mensagem = "Ola {}, sou um bot te enviando uma mensagem!"

for numero, nome in zip(numeros, nomes):
    send_message(numero, mensagem.format(nome))