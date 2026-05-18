import requests
from playwright.sync_api import sync_playwright

# 🔴 COLOQUE A URL DO SEU WEBHOOK AQUI
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1505954251656921108/mStLGkpDksCtRBp8emDzSPEgKf4PPRrqpJERj4fU_0TaQtLewHeL2YX9swwtPy8q4OvW'
SITE_URL = "https://deadftx.github.io/suicidenodewar/"

def tirar_print_e_enviar():
    print("Acessando o site...")
    
    # 1. Tira a print usando o navegador invisível
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SITE_URL)
        
        # Substitua pelo ID ou classe correta do seu quadro no HTML
        seletor_do_quadro = '.seu-seletor-aqui'
        elemento = page.wait_for_selector(seletor_do_quadro, timeout=15000)
        
        # Salva a imagem temporariamente
        elemento.screenshot(path="ranking.png")
        browser.close()

    print("Print tirada! Enviando para o Discord...")
    
    # 2. Envia a imagem para o Webhook do Discord
    with open("ranking.png", "rb") as imagem:
        payload = {"content": "**🏆 Atualização: Média de Kills por Node!**"}
        files = {"file": ("ranking.png", imagem, "image/png")}
        
        resposta = requests.post(WEBHOOK_URL, data=payload, files=files)
        
        if resposta.status_code in [200, 204]:
            print("Enviado com sucesso!")
        else:
            print(f"Erro ao enviar: {resposta.status_code}")

if __name__ == "__main__":
    tirar_print_e_enviar()
