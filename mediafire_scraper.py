import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class MediaFireScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.visited_folders = set()
        self.all_files = []
        
    def scroll_and_collect_all(self):
        """Faz scroll GRADUAL coletando arquivos DURANTE o processo"""
        print("  ⟳ Iniciando scroll e coleta simultânea...")
        
        # Volta pro topo primeiro
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        collected_urls = set()  # Para evitar duplicatas
        files_collected = []
        no_change_count = 0
        scroll_step = 0
        
        while no_change_count < 5:
            # COLETA os arquivos visíveis AGORA
            file_elements = self.driver.find_elements(By.CSS_SELECTOR, ".cf.filename_outer a")
            
            for element in file_elements:
                try:
                    file_url = element.get_attribute("href")
                    
                    # Só adiciona se for arquivo e ainda não coletou
                    if file_url and "/file/" in file_url and file_url not in collected_urls:
                        file_name = element.find_element(By.CSS_SELECTOR, "span.item-name").text
                        files_collected.append({
                            "nome": file_name,
                            "url": file_url
                        })
                        collected_urls.add(file_url)
                        print(f"    ✓ Coletado: {file_name}")
                except:
                    continue
            
            # Agora faz o scroll
            last_count = len(collected_urls)
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1.5)
            
            scroll_step += 1
            
            # Verifica se chegou no fim
            is_at_bottom = self.driver.execute_script(
                "return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;"
            )
            
            if is_at_bottom:
                time.sleep(2)
                # Coleta mais uma vez no final
                file_elements = self.driver.find_elements(By.CSS_SELECTOR, ".cf.filename_outer a")
                for element in file_elements:
                    try:
                        file_url = element.get_attribute("href")
                        if file_url and "/file/" in file_url and file_url not in collected_urls:
                            file_name = element.find_element(By.CSS_SELECTOR, "span.item-name").text
                            files_collected.append({"nome": file_name, "url": file_url})
                            collected_urls.add(file_url)
                            print(f"    ✓ Coletado: {file_name}")
                    except:
                        continue
                
                new_count = len(collected_urls)
                if new_count == last_count:
                    no_change_count += 1
                else:
                    no_change_count = 0
            
            if scroll_step > 200:
                print("  ⚠ Limite de scrolls atingido")
                break
        
        print(f"  ✓ Coleta completa - {len(files_collected)} arquivos únicos coletados")
        return files_collected
    
    def get_files_from_page(self):
        """DEPRECIADO - Agora usa scroll_and_collect_all()"""
        # Esta função não é mais usada, mantida para compatibilidade
        pass
    
    def get_folders_from_page(self):
        """Coleta todos os links de pastas da página atual"""
        folders = []
        
        try:
            folder_elements = self.driver.find_elements(By.CSS_SELECTOR, ".cf.info a.foldername")
            
            for element in folder_elements:
                folder_url = element.get_attribute("href")
                folder_name = element.text
                
                if folder_url and folder_url not in self.visited_folders:
                    folders.append({
                        "nome": folder_name,
                        "url": folder_url
                    })
                    
        except NoSuchElementException:
            pass
        
        return folders
    
    def scrape_folder(self, url, depth=0):
        """Scrape recursivo de uma pasta"""
        if url in self.visited_folders:
            return
        
        self.visited_folders.add(url)
        indent = "  " * depth
        
        print(f"\n{indent}📁 Acessando: {url}")
        self.driver.get(url)
        
        # Espera a página carregar
        time.sleep(3)
        
        # Faz scroll E coleta simultaneamente
        print(f"{indent}⟳ Coletando arquivos com scroll...")
        files = self.scroll_and_collect_all()
        self.all_files.extend(files)
        print(f"{indent}✓ {len(files)} arquivo(s) coletado(s)")
        
        # Volta pro topo para coletar pastas
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # Coleta pastas
        print(f"{indent}📂 Procurando subpastas...")
        folders = self.get_folders_from_page()
        print(f"{indent}✓ {len(folders)} subpasta(s) encontrada(s)")
        
        # Scrape recursivo nas subpastas
        for folder in folders:
            self.scrape_folder(folder["url"], depth + 1)
    
    def save_to_csv(self, filename="mediafire_links.csv"):
        """Salva os resultados em CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["nome", "url"])
            writer.writeheader()
            writer.writerows(self.all_files)
        
        print(f"\n✓ Resultados salvos em: {filename}")
    
    def run(self):
        """Executa o scraper"""
        try:
            print("=" * 60)
            print("MEDIAFIRE SCRAPER - Iniciando...")
            print("=" * 60)
            
            self.scrape_folder(self.start_url)
            
            print("\n" + "=" * 60)
            print(f"CONCLUÍDO! Total de arquivos encontrados: {len(self.all_files)}")
            print("=" * 60)
            
            # Salva resultados
            self.save_to_csv()
            
            # Mostra os primeiros resultados
            print("\nPrimeiros 10 arquivos encontrados:")
            for i, file in enumerate(self.all_files[:10], 1):
                print(f"{i}. {file['nome']}")
                print(f"   {file['url']}\n")
            
        finally:
            self.driver.quit()

# ============================================
# USO DO SCRIPT
# ============================================

if __name__ == "__main__":
    # Coloque sua URL aqui
    START_URL = "SUA_URL"
    
    scraper = MediaFireScraper(START_URL)
    scraper.run()