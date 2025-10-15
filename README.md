# Automatizador de Coleta de Dados do Google Trends

Este script automatiza o processo de download de dados de séries temporais e de municípios do **Google Trends** para um período estendido.  
Ele contorna a limitação da plataforma, que só exibe dados diários para intervalos curtos, dividindo o período total em segmentos semanais e baixando os relatórios de cada um.

---

## 🧩 Funcionalidades

- **Coleta Contínua:** Baixa dados para longos períodos (meses ou anos) de forma automática.  
- **Configuração Interativa:** Pergunta ao usuário qual navegador está usando, o formato de data desejado e o período de coleta antes de iniciar.  
- **Simulação Humana:** Utiliza pausas aleatórias para tornar a automação mais robusta e menos propensa a erros.  
- **Robustez:** Tenta localizar os elementos visuais múltiplas vezes, rolando a página se necessário.

---

## ⚙️ 1. Pré-requisitos

Antes de executar, você precisa ter o **Python** instalado e as seguintes bibliotecas.  
Instale-as com:

```bash
pip install pyautogui keyboard opencv-python
```

A biblioteca `opencv-python` é necessária para a funcionalidade de reconhecimento de imagem do `pyautogui`.

---

## 🖼️ 2. Configuração Inicial: As Imagens de Referência

A automação funciona reconhecendo imagens na tela.  
Por isso, a etapa mais crucial é a **captura de tela dos botões e campos** que o script irá usar.

### Passos:

1. Crie uma pasta chamada `imagens_gtrends` no mesmo diretório onde o script `teste_auto.py` está salvo.
   
**OBS: Ou utilize a pasta padrão disponibilizada neste repositório.**

2. Abra o **Google Trends** no seu navegador.
   
3. Tire screenshots pequenos e precisos de cada um dos elementos listados abaixo e salve-os na pasta `imagens_gtrends` com os nomes exatos:

| Arquivo | Descrição |
|----------|------------|
| `1_botao_baixo_volume.png` | Botão de alternância "Baixo volume de pesquisa" |
| `2_botao_download_tempo.png` | Ícone de download do gráfico "Interesse ao longo do tempo" |
| `3_botao_download_mapa.png` | Ícone de download do mapa "Interesse por sub-região" |
| `periodo_dropdown.png` | Botão que mostra o período atual (ex: "Últimos 12 meses") |
| `periodo_personalizado.png` | Opção "Período personalizado" após abrir o seletor de datas |
| `campo_data_inicio.png` | Campo com o rótulo "De" (data inicial) |
| `campo_data_fim.png` | Campo com o rótulo "A" (data final) |
| `botao_aplicar_periodo.png` | Botão "OK" ou "Aplicar" |
| `espirito_santo.png` *(opcional)* | Screenshot do filtro de localização já aplicado (ex: "Espírito Santo") |

⚠️ **Importante:**
- Mantenha o zoom do navegador em **100%**.  
- A resolução da tela deve ser a **mesma** durante a captura e execução.  
- Se o script não encontrar uma imagem, provavelmente a captura de tela é diferente do que está sendo exibido. Refazê-la costuma resolver.

---

## 🚀 3. Como Usar

### Etapa 1: Preparação Manual no Navegador (Essencial!)

1. Abra o **Google Trends**.  
2. Busque pelo termo de interesse (ex: *“Inteligência Artificial”*).  
3. Configure os filtros desejados (país, categoria, etc.).  
4. Clique no seletor de período (ex: “Últimos 12 meses”) e escolha **“Período personalizado”**.  
5. Selecione um intervalo **anterior ao desejado** (ex: de `15/12/2023` a `20/12/2023` se a coleta começar em `01/01/2024`).  
   > Isso prepara a interface e evita que o Google Trends reajuste as datas automaticamente.  
6. Deixe a página aberta — o script tomará o controle a partir daí.

---

### Etapa 2: Executando o Script

1. Abra o terminal ou prompt de comando.  
2. Navegue até a pasta onde o script e a pasta `imagens_gtrends` estão salvos.  
3. Execute o comando:

```bash
python teste_auto.py
```

4. O script fará algumas perguntas:
   - Se usa o **Microsoft Edge**: responda `s` (sim) ou `n` (não).  
   - Formato de data: escolha entre `DD/MM/AAAA` ou `MM/DD/AAAA`.  
   - Período de coleta: insira as datas de início e fim no formato escolhido.  

5. Após responder, haverá uma contagem regressiva de **5 segundos**.  
   Clique na janela do navegador para garantir que ela esteja em foco.  
6. **Não mexa no mouse ou teclado!** O script tomará o controle para realizar as tarefas.

---

### 🛑 Para Parar o Script

- Segure a tecla **CTRL** por um segundo.  
- **Ou** mova o cursor do mouse para o **canto superior esquerdo** da tela.  

O script será interrompido de forma segura.

---

## 📚 Sumário

- Automatizador de Coleta de Dados do Google Trends  
  - Funcionalidades  
  - 1. Pré-requisitos  
  - 2. Configuração Inicial: As Imagens de Referência  
    - Passos  
  - 3. Como Usar  
    - Etapa 1: Preparação Manual no Navegador  
    - Etapa 2: Executando o Script  
    - Para Parar o Script
