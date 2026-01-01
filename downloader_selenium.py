import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver(pasta_download):
    chrome_options = Options()
    prefs = {
        "download.default_directory": os.path.abspath(pasta_download),
        "download.prompt_for_download": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def baixar_apenas_erros(arquivo_erros, pasta_raiz):
    if not os.path.exists(arquivo_erros):
        print("Nenhum arquivo de erro encontrado.")
        return

    df = pd.read_csv(arquivo_erros)
    
    for _, linha in df.iterrows():
        nome = linha['nome']
        url = linha['url']
        
        caminho_final = os.path.join(pasta_raiz, nome)
        pasta_destino = os.path.dirname(caminho_final)
        os.makedirs(pasta_destino, exist_ok=True)

        print(f"🚀 Recuperando via Selenium: {nome}")
        
        driver = configurar_driver(pasta_destino)
        driver.get(url)
        time.sleep(3)
        
        try:
            botao = driver.find_element(By.ID, "downloadButton")
            botao.click()
            
            # Espera o arquivo ser criado na pasta
            timeout = 120
            while not os.path.exists(caminho_final) and timeout > 0:
                time.sleep(1)
                timeout -= 1
            print(f"✅ Recuperado!")
        except Exception as e:
            print(f"❌ Falha persistente em {nome}: {e}")
        
        driver.quit()
        time.sleep(2)

if __name__ == "__main__":
    baixar_apenas_erros('erros.csv', 'MediaFire_Arquivos')