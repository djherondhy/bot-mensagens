from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Imprimir o diretório de trabalho atual
print(os.getcwd())

# Configurar o driver do Selenium
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

# Aguarde o tempo necessário para escanear o QR code
input("Escaneie o QR code e pressione Enter...")

def aguardar_elemento(selector, timeout=30):
    """Aguarda até que o elemento esteja presente na página."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(selector))

def verificar_envio():
    """Verifica se a mensagem foi enviada com sucesso."""
    try:
        # Aguarda a presença do indicador de mensagem enviada
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="msg-dblcheck"]'))
        )
        return True
    except Exception:
        return False

def enviar_arquivo(caminho_arquivo, legenda=None):
    """Envia um arquivo (imagem ou vídeo) para o contato selecionado."""
    try:
        # Encontrar o botão de anexar (clipe)
        clip_button = aguardar_elemento((By.CSS_SELECTOR, 'span[data-icon="plus"]'))
        clip_button.click()
        time.sleep(3)

        # Encontrar o input de arquivos para imagens e vídeos
        image_box = aguardar_elemento((By.CSS_SELECTOR, 'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        image_box.send_keys(caminho_arquivo)
        time.sleep(2)  # Aguarde um pouco para o arquivo carregar

        # Se houver legenda, enviá-la
        if legenda:
            legenda_box = aguardar_elemento((By.CSS_SELECTOR, 'div[aria-placeholder="Adicione uma legenda"]'))
            legenda_box.send_keys(legenda)

        # Clicar no botão de enviar
        send_button = aguardar_elemento((By.CSS_SELECTOR, 'span[data-icon="send"]'))
        send_button.click()

        # Verificar se o envio foi bem-sucedido
        if verificar_envio():
            print(f"Arquivo enviado: {caminho_arquivo}")
        else:
            print(f"Falha no envio do arquivo: {caminho_arquivo}")

    except Exception as e:
        print(f"Erro ao enviar arquivo {caminho_arquivo}: {str(e)}")
        time.sleep(5)  # Tempo para garantir que o próximo arquivo não seja processado rapidamente demais

def enviar_imagens(contatos, arquivos):
    """Envia imagens e vídeos para a lista de contatos."""
    for numero in contatos:
        try:
            # Abrir a conversa com o contato
            driver.get(f"https://web.whatsapp.com/send?phone={numero}")

            # Esperar até que o campo de mensagem esteja visível
            aguardar_elemento((By.CSS_SELECTOR, 'div[aria-placeholder="Digite uma mensagem"]'))

            for arquivo in arquivos:
                enviar_arquivo(arquivo['caminho'], arquivo.get('legenda'))
                
        except Exception as e:
            print(f"Erro ao enviar arquivo para {numero}: {str(e)}")
            time.sleep(5)  # Aguarde um pouco antes de continuar com o próximo contato

    # Fechar o navegador após o envio de todas as imagens
    driver.quit()

# Lista de contatos (substitua com os números reais)
contatos = ['55097991405568', '55092985185665']

# Lista de arquivos a serem enviados
arquivos = [
    {
        'caminho': 'C:/Users/djher/Documents/Bots/Bot_Message/imagem_1.jpg',
        'legenda': 'Esta imagem foi enviada como teste de um bot.'
    },
    {
        'caminho': 'C:/Users/djher/Documents/Bots/Bot_Message/video-1.mp4',
        'legenda': 'Este vídeo foi enviado como teste de um bot.'
    }
]

# Enviar imagens e vídeos
enviar_imagens(contatos, arquivos)
