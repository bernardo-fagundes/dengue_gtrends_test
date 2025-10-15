import os
import time
import random  # Adicionado para randomizar as pausas
from datetime import datetime, timedelta

import keyboard
import pyautogui

# --- CONFIGURAÇÕES ---
# Mova o mouse para o canto superior esquerdo para parar o script.
pyautogui.FAILSAFE = True
# Defina o tempo base de pausa entre os ciclos. Será randomizado.
PAUSA_ENTRE_CICLOS = 1  # em segundos

# As datas de início e fim agora serão definidas por entrada do usuário no início do script.

# Esta variável será definida pelo usuário no início.
FORMATO_DATA_INTERFACE = ""

# Distância horizontal aproximada entre o filtro de território "Espírito Santo"
# e o seletor de período exibido à direita.
OFFSET_SELETOR_PERIODO_X = 350

# Deslocamentos aplicados ao clicar nos campos de data.
OFFSET_CAMPO_DATA_INICIO = (200, 0)
OFFSET_CAMPO_DATA_FIM = (200, 0)
OFFSET_CLIQUE_POR_IMAGEM = {
    "campo_data_inicio.png": OFFSET_CAMPO_DATA_INICIO,
    "campo_data_fim.png": OFFSET_CAMPO_DATA_FIM,
}


# --- FUNÇÕES AUXILIARES ---

def random_sleep(base_duration):
    """
    Espera por um tempo aleatório, variando entre a duração base
    e o dobro dela, para simular comportamento humano.
    """
    sleep_time = random.uniform(base_duration, base_duration * 2)
    # print(f"Debug: Pausando por {sleep_time:.2f}s (base: {base_duration}s)") # Remova o comentário para depurar
    time.sleep(sleep_time)


def encontrar_e_clicar(nome_imagem, max_scrolls=3, confianca=0.8):
    """
    Procura uma imagem na tela. Se não encontrar, rola a página para baixo
    e tenta novamente por um número máximo de vezes (max_scrolls).
    """
    caminho_completo = os.path.join("imagens_gtrends", nome_imagem)
    print(f"Procurando por '{caminho_completo}'...")

    try:
        posicao = pyautogui.locateCenterOnScreen(caminho_completo, confidence=confianca)
        if posicao:
            destino = aplicar_offset_imagem(nome_imagem, posicao)
            pyautogui.click(destino)
            print(f"Imagem encontrada na tela inicial e clicada em {destino}.")
            return True
    except pyautogui.ImageNotFoundException:
        pass

    for i in range(max_scrolls):
        print(f"Imagem não encontrada. Rolando a página... (Tentativa {i + 1}/{max_scrolls})")
        pyautogui.scroll(-300)
        random_sleep(0.5)

        try:
            posicao = pyautogui.locateCenterOnScreen(caminho_completo, confidence=confianca)
            if posicao:
                destino = aplicar_offset_imagem(nome_imagem, posicao)
                pyautogui.click(destino)
                print(f"Imagem encontrada após rolar a página e clicada em {destino}.")
                return True
        except pyautogui.ImageNotFoundException:
            continue

    print(f"ERRO: Não foi possível encontrar a imagem '{nome_imagem}' mesmo após rolar a página.")
    return False


def aplicar_offset_imagem(nome_imagem, posicao):
    """Retorna o ponto de clique considerando deslocamentos específicos por imagem."""
    offset_x, offset_y = OFFSET_CLIQUE_POR_IMAGEM.get(nome_imagem, (0, 0))
    if offset_x or offset_y:
        destino = (posicao.x + offset_x, posicao.y + offset_y)
        print(f"Aplicando deslocamento ({offset_x}, {offset_y}) para '{nome_imagem}'. Clique ajustado para {destino}.")
        return destino
    return posicao


def clicar_offset_ao_lado(nome_imagem_referencia, offset_x, offset_y=0, confianca=0.8):
    """Encontra a imagem de referência e clica em um ponto deslocado dela."""
    caminho = os.path.join("imagens_gtrends", nome_imagem_referencia)
    print(f"Tentando localizar referência para clique com deslocamento: {caminho}")

    try:
        centro = pyautogui.locateCenterOnScreen(caminho, confidence=confianca)
    except pyautogui.ImageNotFoundException:
        centro = None

    if not centro:
        print(f"Não foi possível encontrar a referência {nome_imagem_referencia} para realizar o clique deslocado.")
        return False

    destino = (centro.x + offset_x, centro.y + offset_y)
    print(f"Referência encontrada em {centro}. Clicando em {destino}.")
    pyautogui.click(destino)
    return True


def abrir_seletor_periodo():
    if clicar_offset_ao_lado("espirito_santo.png", offset_x=OFFSET_SELETOR_PERIODO_X):
        return True

    print("ERRO: Não foi possível abrir o seletor de período após tentar múltiplas estratégias.")
    return False


def formatar_data_para_interface(data):
    """Formata a data usando o formato definido pelo usuário."""
    return data.strftime(FORMATO_DATA_INTERFACE)


def gerar_intervalos_periodo(data_inicio_str, data_fim_str):
    """Gera intervalos de datas usando o formato definido pelo usuário."""
    data_inicio = datetime.strptime(data_inicio_str, FORMATO_DATA_INTERFACE).date()
    data_fim = datetime.strptime(data_fim_str, FORMATO_DATA_INTERFACE).date()

    if data_fim < data_inicio:
        raise ValueError("A data final deve ser igual ou posterior à data inicial da coleta.")

    intervalos = []
    data_atual = data_inicio
    while data_atual <= data_fim:
        fim_intervalo = data_atual + timedelta(days=6)
        if fim_intervalo > data_fim:
            fim_intervalo = data_fim
        intervalos.append((data_atual, fim_intervalo))
        data_atual = fim_intervalo + timedelta(days=1)

    return intervalos


def aplicar_periodo_personalizado(data_inicio, data_fim):
    data_inicio_fmt = formatar_data_para_interface(data_inicio)
    data_fim_fmt = formatar_data_para_interface(data_fim)

    print(f"\n--- Ajustando período personalizado: {data_inicio_fmt} a {data_fim_fmt} ---")

    if not abrir_seletor_periodo():
        return False
    random_sleep(1)

    if not encontrar_e_clicar('periodo_personalizado.png'):
        return False
    random_sleep(1)

    # --- INVERSÃO: CAMPO DATA FIM PRIMEIRO ---
    if not encontrar_e_clicar('campo_data_fim.png'):
        return False
    random_sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    partes_data = data_fim_fmt.split('/')
    pyautogui.write(partes_data[0])
    random_sleep(0.8)
    pyautogui.press('/')
    pyautogui.write(partes_data[1])
    random_sleep(0.8)
    pyautogui.press('/')
    pyautogui.write(partes_data[2])
    random_sleep(0.5)

    # --- INVERSÃO: CAMPO DATA INÍCIO DEPOIS ---
    if not encontrar_e_clicar('campo_data_inicio.png'):
        return False
    random_sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    partes_data = data_inicio_fmt.split('/')
    pyautogui.write(partes_data[0])
    random_sleep(0.8)
    pyautogui.press('/')
    pyautogui.write(partes_data[1])
    random_sleep(0.8)
    pyautogui.press('/')
    pyautogui.write(partes_data[2])
    random_sleep(1)

    if not encontrar_e_clicar('botao_aplicar_periodo.png'):
        return False

    random_sleep(2)
    print("Período personalizado aplicado com sucesso.")
    return True


def realizar_coleta(intervalo_datas, is_edge):
    """Executa um ciclo de automação, considerando o navegador."""
    print("Retornando ao topo da página...")
    pyautogui.hotkey('home')
    random_sleep(1)

    if not aplicar_periodo_personalizado(*intervalo_datas):
        print("AVISO: Falha ao ajustar o período personalizado.")

    print("\n--- Etapa: Ativar Baixo Volume ---")
    if encontrar_e_clicar('1_botao_baixo_volume.png'):
        print("Botão de 'baixo volume' ativado.")
        random_sleep(1)
    else:
        print("AVISO: Não foi possível encontrar o botão de 'baixo volume'.")

    pyautogui.hotkey('home')
    random_sleep(1)

    print("\n--- Etapa: Download do CSV de Interesse ao Longo do Tempo ---")
    if encontrar_e_clicar('2_botao_download_tempo.png'):
        random_sleep(2)
        if not is_edge:
            print("Pressionando Enter para concluir o download (Não-Edge)...")
            pyautogui.press('enter')
    else:
        print("ERRO: Não foi possível baixar o CSV de interesse ao longo do tempo.")

    print("\n--- Etapa: Download do CSV de Municípios ---")
    if encontrar_e_clicar('3_botao_download_mapa.png'):
        random_sleep(2)
        if not is_edge:
            print("Pressionando Enter para concluir o download (Não-Edge)...")
            pyautogui.press('enter')
    else:
        print("ERRO: Não foi possível baixar o CSV do mapa (municípios).")


def executar_automacao():
    global FORMATO_DATA_INTERFACE

    # --- ENTRADA DO USUÁRIO ---
    print("--- CONFIGURAÇÃO INICIAL ---")

    # 1. Pergunta sobre o navegador
    resposta_edge = input("Você está usando o navegador Microsoft Edge? (s/n): ").lower()
    is_edge = resposta_edge.startswith('s')

    # 2. Pergunta sobre o formato da data
    formato_exemplo = ""
    exemplo_inicio = ""
    exemplo_fim = ""
    while True:
        print("\nEscolha o formato de data que você vai usar:")
        print("  1: Dia/Mês/Ano (ex: 31/12/2025)")
        print("  2: Mês/Dia/Ano (ex: 12/31/2025)")
        resposta_formato = input("Digite o número da opção (1 ou 2): ")
        if resposta_formato == '1':
            FORMATO_DATA_INTERFACE = "%d/%m/%Y"
            formato_exemplo = "DD/MM/AAAA"
            exemplo_inicio = "01/01/2025"
            exemplo_fim = "28/02/2025"
            break
        elif resposta_formato == '2':
            FORMATO_DATA_INTERFACE = "%m/%d/%Y"
            formato_exemplo = "MM/DD/AAAA"
            exemplo_inicio = "01/01/2025"
            exemplo_fim = "02/28/2025"
            break
        else:
            print("Opção inválida. Por favor, digite 1 ou 2.")

    # 3. Pergunta sobre o período de coleta
    print(f"\nAgora, defina o período de coleta usando o formato {formato_exemplo}.")
    data_inicio_coleta = input(f"Digite a data de INÍCIO da coleta (ex: {exemplo_inicio}): ")
    data_fim_coleta = input(f"Digite a data de FIM da coleta (ex: {exemplo_fim}): ")

    print("\n--- AUTOMAÇÃO DE COLETA CONTÍNUA ---")
    print("INSTRUÇÕES:")
    print("1. Prepare a primeira página do Google Trends no navegador.")
    print("2. A automação começará em 5 segundos.")
    print("3. Para PARAR o script, segure a tecla 'CTRL' por um segundo.")

    for i in range(5, 0, -1):
        print(f"{i}...")
        random_sleep(1)  # Contagem regressiva com pausa aleatória

    try:
        intervalos_coleta = gerar_intervalos_periodo(data_inicio_coleta, data_fim_coleta)
    except ValueError as e:
        print(f"\nERRO DE CONFIGURAÇÃO: {e}")
        print(
            f"Verifique se as datas '{data_inicio_coleta}' e '{data_fim_coleta}' estão no formato {formato_exemplo} que você escolheu.")
        return

    total_intervalos = len(intervalos_coleta)
    for indice, intervalo in enumerate(intervalos_coleta, start=1):
        if keyboard.is_pressed('ctrl'):
            print("\nTecla 'CTRL' detectada. Encerrando o script...")
            break

        data_inicio, data_fim = intervalo
        print(f"\n================ INICIANDO CICLO DE COLETA Nº {indice} DE {total_intervalos} ================")
        print(
            f"Intervalo atual: {data_inicio.strftime(FORMATO_DATA_INTERFACE)} até {data_fim.strftime(FORMATO_DATA_INTERFACE)}")

        realizar_coleta(intervalo, is_edge)

        print(f"\n================ CICLO {indice} CONCLUÍDO ================")
        if indice < total_intervalos:
            print(f"\nPausando antes do próximo ciclo. Prepare a próxima página.")
            random_sleep(PAUSA_ENTRE_CICLOS)

    print("\n--- Automação Finalizada ---")


if __name__ == "__main__":
    executar_automacao()

