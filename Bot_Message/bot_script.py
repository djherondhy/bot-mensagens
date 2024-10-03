from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializar o navegador
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

# Aguarde o tempo necessário para escanear o QR code
input("Escaneie o QR code e pressione Enter...")

# Função para enviar mensagens
def enviar_mensagens(contatos, mensagem):
    for numero in contatos:
        try:
            # Espera o WhatsApp carregar completamente
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "side")))

            # Abrir a conversa com o contato
            driver.get(f"https://web.whatsapp.com/send?phone={numero}")
            
            # Esperar até que o campo de mensagem esteja visível
            campo_mensagem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-placeholder="Digite uma mensagem"]'))
            )

            # Enviar a mensagem
            campo_mensagem.send_keys(mensagem)
            campo_mensagem.send_keys(Keys.ENTER)
            time.sleep(3)
            # Pequena pausa entre mensagens
            print(f"Mensagem enviada para {numero}")

        except Exception as e:
            print(f"Erro ao enviar mensagem para {numero}: {str(e)}")
            time.sleep(5)  # Tempo para garantir que o próximo número não seja processado rapidamente demais

    # Fechar o navegador após o envio de todas as mensagens
    driver.quit()

# Lista de contatos (substitua com os números reais)
contatos = ['55092991868099', '5509291438946', '55092984332335', '55097991405568', '55092985185665']

# Mensagem a ser enviada
mensagem = "Oi, sou o dj e estou te mandando uma mensagem automática, através do bot"

# Enviar mensagens
enviar_mensagens(contatos, mensagem)
