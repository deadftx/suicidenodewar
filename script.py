import os
import time
import requests
from playwright.sync_api import sync_playwright

# Puxa a URL do webhook escondida no GitHub Secrets
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')
SITE_URL = "https://deadftx.github.io/suicidenodewar/"

def tirar_prints_e_enviar():
    # Verifica se a URL secreta foi configurada
    if not WEBHOOK_URL:
        print("Erro: A URL do Webhook não foi encontrada nas variáveis de ambiente.")
        return

    print("Acessando o site...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SITE_URL)
        
        # Espera a página carregar 100% para evitar prints em branco
        page.wait_for_load_state("networkidle")
        time.sleep(2) # Pausa de segurança extra
        
        # O seletor com vírgula busca TODOS os elementos que têm uma classe OU a outra
        seletor = '.card, .mvp-container'
        
        # Pega a lista de todos os quadros encontrados
        elementos = page.locator(seletor).all()
        
        if not elementos:
            print("Nenhum quadro encontrado!")
            browser.close()
            return

        print(f"Encontrados {len(elementos)} quadros. Tirando prints...")
        
        # Faz um loop para tirar a print e enviar cada um deles
        for index, elemento in enumerate(elementos):
            nome_arquivo = f"ranking_{index}.png"
            
            # Tira a print do elemento específico
            elemento.screenshot(path=nome_arquivo)
            
            print(f"Enviando print {index + 1} para o Discord...")
            
            # Envia a imagem para o Webhook
            with open(nome_arquivo, "rb") as imagem:
                payload = {"content": f"**🏆 Atualização de Ranking - Parte {index + 1}**"}
                files = {"file": (nome_arquivo, imagem, "image/png")}
                
                resposta = requests.post(WEBHOOK_URL, data=payload, files=files)
                
                if resposta.status_code in [200, 204]:
                    print(f"Print {index + 1} enviada com sucesso!")
                else:
                    print(f"Erro ao enviar print {index + 1}: {resposta.status_code}")
            
            # Pausa de 2 segundos entre cada envio para o Discord não bloquear por spam (Rate Limit)
            time.sleep(2) 
            
        browser.close()

if __name__ == "__main__":
    tirar_prints_e_enviar()
