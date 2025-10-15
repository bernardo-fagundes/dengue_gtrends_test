import pyautogui
import time
import os
import keyboard

# --- CONFIGURAÇÕES ---
# Mova o mouse para o canto superior esquerdo para parar o script.
pyautogui.FAILSAFE = True
# Defina quantos segundos de pausa você quer entre o fim de uma coleta e o início da próxima.
PAUSA_ENTRE_CICLOS = 1  # em segundos


# --- FUNÇÕES AUXILIARES ---

def encontrar_e_clicar(nome_imagem, max_scrolls=7, confianca=0.8):
    """
    Procura uma imagem na tela. Se não encontrar, rola a página para baixo
    e tenta novamente por um número máximo de vezes (max_scrolls).
    """
    caminho_completo = os.path.join("imagens_gtrends", nome_imagem)
    print(f"Procurando por '{caminho_completo}'...")

    try:
        posicao = pyautogui.locateCenterOnScreen(caminho_completo, confidence=confianca)
        if posicao:
            pyautogui.click(posicao)
            print(f"Imagem encontrada na tela inicial e clicada em {posicao}.")
            return True
    except pyautogui.ImageNotFoundException:
        pass

    for i in range(max_scrolls):
        print(f"Imagem não encontrada. Rolando a página... (Tentativa {i + 1}/{max_scrolls})")
        pyautogui.scroll(-300)
        time.sleep(0.5)

        try:
            posicao = pyautogui.locateCenterOnScreen(caminho_completo, confidence=confianca)
            if posicao:
                pyautogui.click(posicao)
                print(f"Imagem encontrada após rolar a página e clicada em {posicao}.")
                return True
        except pyautogui.ImageNotFoundException:
            continue

    print(f"ERRO: Não foi possível encontrar a imagem '{nome_imagem}' mesmo após rolar a página.")
    return False


def realizar_coleta():
    """
    Executa um ciclo completo de automação na página já aberta.
    """
    # --- ALTERAÇÃO AQUI: Comandos de 'reset' no início do ciclo ---
    print("Maximizando a janela e retornando ao topo da página...")
    pyautogui.hotkey('home')
    time.sleep(1)
    # --- FIM DA ALTERAÇÃO ---

    print("\n--- Etapa: Ativar Baixo Volume ---")
    if encontrar_e_clicar('1_botao_baixo_volume.png'):
        print("Botão de 'baixo volume' encontrado e ativado.")
        time.sleep(1)
    else:
        print("AVISO: Não foi possível encontrar o botão de 'baixo volume'.")

    # Retorna ao topo após a ação, caso a página tenha rolado
    pyautogui.hotkey('home')
    time.sleep(1)

    print("\n--- Etapa: Download do CSV de Interesse ao Longo do Tempo ---")
    if encontrar_e_clicar('2_botao_download_tempo.png'):
        time.sleep(1)
        print("Pressionando Enter para retornar o foco...")
        pyautogui.press('enter')
    else:
        print("ERRO: Não foi possível baixar o CSV do mapa (municípios).")

    time.sleep(2)

    print("\n--- Etapa: Download do CSV de Municípios ---")
    if encontrar_e_clicar('3_botao_download_mapa.png'):
        time.sleep(1)
        print("Pressionando Enter para retornar o foco...")
        pyautogui.press('enter')
    else:
        print("ERRO: Não foi possível baixar o CSV de interesse ao longo do tempo.")

    time.sleep(2)


# --- SCRIPT PRINCIPAL ---

print("--- AUTOMAÇÃO DE COLETA CONTÍNUA ---")
print("INSTRUÇÕES:")
print("1. Prepare a primeira página do Google Trends no navegador.")
print("2. A automação começará em 10 segundos.")
print("3. Para PARAR o script completamente, segure a tecla 'CTRL' por um segundo.")

for i in range(5, 0, -1):
    print(f"{i}...")
    time.sleep(1)

ciclo_n = 1
while True:
    # A verificação da tecla de parada é a primeira coisa no loop
    if keyboard.is_pressed('ctrl'):
        print("\nTecla 'CTRL' detectada. Encerrando o script...")
        break

    print(f"\n================ INICIANDO CICLO DE COLETA Nº {ciclo_n} ================")

    realizar_coleta()

    print(f"\n================ CICLO {ciclo_n} CONCLUÍDO ================")

    # --- ALTERAÇÃO AQUI: Pausa automática sem necessidade de 'Enter' ---
    print(f"\nPausa de {PAUSA_ENTRE_CICLOS} segundos antes do próximo ciclo.")
    print("Prepare a próxima página no navegador agora.")

    # Pausa configurável, durante a qual o script ainda checa a tecla de parada
    for _ in range(PAUSA_ENTRE_CICLOS):
        if keyboard.is_pressed('ctrl'):
            break
        time.sleep(1)

    if keyboard.is_pressed('ctrl'):
        print("\nTecla 'CTRL' detectada. Encerrando o script...")
        break
    # --- FIM DA ALTERAÇÃO ---

    ciclo_n += 1

print("\n--- Automação Finalizada ---")