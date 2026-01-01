import csv
import os
import requests
from bs4 import BeautifulSoup
import time

def obter_link_direto(sessao, url_mediafire):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        r = sessao.get(url_mediafire, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        botao = soup.find('a', {'id': 'downloadButton'})
        if botao:
            return botao.get('href')
    except:
        return None

def baixar_com_log_de_erros(arquivo_entrada, pasta_destino):
    sessao = requests.Session()
    arquivos_com_erro = []
    
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    with open(arquivo_entrada, mode='r', encoding='utf-8') as f:
        leitor = list(csv.DictReader(f))
        total = len(leitor)

        for i, linha in enumerate(leitor, 1):
            nome = linha['nome']
            url = linha['url']
            caminho_local = os.path.join(pasta_destino, nome)
            
            os.makedirs(os.path.dirname(caminho_local), exist_ok=True)

            if os.path.exists(caminho_local) and os.path.getsize(caminho_local) > 0:
                print(f"[{i}/{total}] Pulando: {nome}")
                continue

            sucesso = False
            for tentativa in range(3):
                link_direto = obter_link_direto(sessao, url)
                if link_direto:
                    try:
                        print(f"[{i}/{total}] Tentativa {tentativa+1}: {nome}")
                        with sessao.get(link_direto, stream=True, timeout=20) as r:
                            r.raise_for_status()
                            with open(caminho_local, 'wb') as f_out:
                                for chunk in r.iter_content(chunk_size=1024*1024):
                                    f_out.write(chunk)
                        sucesso = True
                        break 
                    except Exception as e:
                        print(f"  ! Erro temporário: {e}")
                        time.sleep(2)
            
            if not sucesso:
                print(f"❌ FALHA CRÍTICA: {nome}")
                arquivos_com_erro.append({'nome': nome, 'url': url})
            
            time.sleep(0.5)

    # Gera o CSV de erros se houver algum
    if arquivos_com_erro:
        with open('erros.csv', 'w', newline='', encoding='utf-8') as f_erro:
            escritor = csv.DictWriter(f_erro, fieldnames=['nome', 'url'])
            escritor.writeheader()
            escritor.writerows(arquivos_com_erro)
        print(f"\n➔ {len(arquivos_com_erro)} erros encontrados. Lista salva em 'erros.csv'")
    else:
        print("\n➔ Todos os arquivos foram baixados com sucesso!")

if __name__ == "__main__":
    baixar_com_log_de_erros('mediafire_links.csv', 'MediaFire_Arquivos')