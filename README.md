# Automatizador de Coleta de Dados do Google Trends

Este repositório reúne um **robô de automação** para baixar relatórios de séries temporais e por município do
**Google Trends** em períodos longos. O script divide a linha do tempo em janelas semanais e faz o download de cada
relatório individualmente, contornando a limitação da plataforma que só disponibiliza dados diários para intervalos
reduzidos.

> ✅ Ideal para pesquisadores, jornalistas de dados e equipes de vigilância epidemiológica que precisam manter séries
> históricas atualizadas sem intervenção manual.

## 🗂️ Sumário

- [Funcionalidades](#-funcionalidades)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Pré-requisitos](#-1-pré-requisitos)
- [Configuração Inicial: Imagens de Referência](#-2-configuração-inicial-imagens-de-referência)
- [Como Usar](#-3-como-usar)
- [Boas Práticas e Limitações](#-boas-práticas-e-limitações)
- [Solução de Problemas](#-solução-de-problemas)
- [Licença](#-licença)

---

## 🧩 Funcionalidades

- **Coleta contínua:** agenda downloads semana a semana para cobrir meses ou anos inteiros.
- **Configuração interativa:** solicita navegador, formato de data e período desejado antes de iniciar.
- **Simulação humana:** aplica pausas aleatórias e múltiplas tentativas para reduzir erros de detecção.
- **Monitoramento de segurança:** oferece atalhos fáceis para encerrar a automação caso algo saia do esperado.

---

## 🏗️ Arquitetura do Projeto

```
.
├── README.md              # Documentação e orientações gerais
├── teste_auto.py          # Script principal de automação
└── imagens_gtrends/       # Pacote com exemplos de imagens de referência
```

O script principal (`teste_auto.py`) usa `pyautogui`, `keyboard` e `opencv-python` para identificar elementos na tela do
navegador e executar cliques/entradas de texto de forma automatizada. As imagens armazenadas em `imagens_gtrends/`
servem de referência visual para localizar botões, campos de data e filtros no Google Trends.

---

## ⚙️ 1. Pré-requisitos

Certifique-se de ter **Python 3.9+** instalado e execute o comando abaixo para instalar as dependências mínimas:

```bash
pip install pyautogui keyboard opencv-python
```

> 💡 Dica: utilize um ambiente virtual (`python -m venv .venv && source .venv/bin/activate`) para isolar as dependências
> do projeto.

A biblioteca `opencv-python` é necessária para a funcionalidade de reconhecimento de imagem do `pyautogui`.

---

## 🖼️ 2. Configuração Inicial: Imagens de Referência

A automação depende da detecção de elementos visuais na página. Portanto, a etapa mais importante é capturar ou ajustar
as imagens de referência utilizadas pelo script.

### Passos

1. Certifique-se de que existe uma pasta chamada `imagens_gtrends` no mesmo diretório de `teste_auto.py`.
   - Você pode reutilizar o conjunto fornecido neste repositório.
2. Abra o **Google Trends**, pesquise o termo desejado e aplique filtros de localização quando necessário.
3. Capture screenshots pequenas (o mais justas possível) dos elementos abaixo e salve-os na pasta `imagens_gtrends` com
   os nomes listados:

| Arquivo | Descrição |
|---------|-----------|
| `1_botao_baixo_volume.png` | Botão de alternância "Baixo volume de pesquisa" |
| `2_botao_download_tempo.png` | Ícone de download do gráfico "Interesse ao longo do tempo" |
| `3_botao_download_mapa.png` | Ícone de download do mapa "Interesse por sub-região" |
| `periodo_dropdown.png` | Botão que mostra o período atual (ex.: "Últimos 12 meses") |
| `periodo_personalizado.png` | Opção "Período personalizado" após abrir o seletor de datas |
| `campo_data_inicio.png` | Campo com o rótulo "De" (data inicial) |
| `campo_data_fim.png` | Campo com o rótulo "A" (data final) |
| `botao_aplicar_periodo.png` | Botão "OK" ou "Aplicar" |
| `espirito_santo.png` *(opcional)* | Screenshot do filtro de localização já aplicado |

> ⚠️ **Importante**
>
> - Mantenha o zoom do navegador em **100%**.
> - Utilize a mesma resolução de tela na captura e na execução.
> - Se a interface do Google Trends estiver em outro idioma, capture novamente as imagens para o idioma correspondente.

---

## 🚀 3. Como Usar

### 3.1 Preparação Manual (obrigatória)

1. Abra o Google Trends.
2. Realize a busca desejada (ex.: *"Dengue"*).
3. Ajuste filtros como país, período ou categoria.
   - A pasta padrão está preparada para o estado do Espírito Santo. Para outras regiões, substitua `espirito_santo.png` e
     atualize a lógica no script.
4. Abra o seletor de período e escolha **Período personalizado**.
5. Selecione um intervalo **anterior** ao período final que deseja coletar (ex.: configure `15/12/2023` a `20/12/2023` se a
   coleta começará em `01/01/2024`). Isso evita que o Google Trends reajuste datas automaticamente.
6. Deixe a aba ativa para que o script assuma o controle.

### 3.2 Execução

1. Abra o terminal.
2. Navegue até a pasta do projeto.
3. Execute:

   ```bash
   python teste_auto.py
   ```

4. Responda às perguntas interativas:
   - Uso do **Microsoft Edge** (`s`/`n`).
   - Escolha do formato de data (`DD/MM/AAAA` ou `MM/DD/AAAA`).
   - Datas inicial e final do período.
5. Aguarde a contagem regressiva de 5 segundos e garanta que o navegador esteja em foco.
6. Evite movimentar o mouse ou teclado durante a execução.

### 3.3 Encerrando manualmente

- Segure a tecla **CTRL** por 1 segundo; **ou**
- Movimente o cursor para o canto superior esquerdo da tela.

O script será interrompido com segurança.

---

## 📏 Boas Práticas e Limitações

- A automação depende da estabilidade da interface do Google Trends. Mudanças visuais podem exigir novas capturas.
- Utilize sempre a mesma configuração de idioma, zoom e resolução da tela.
- Evite executar o script em ambientes com múltiplos monitores em resoluções diferentes.
- O download simultâneo de grandes quantidades de dados pode ser bloqueado pelo Google. Considere espaçar execuções.

---

## 🛠️ Solução de Problemas

| Sintoma | Possível causa | Como resolver |
|---------|----------------|----------------|
| Script não encontra um botão | Screenshot desatualizado ou com zoom diferente | Refaça a captura com zoom 100% e salve novamente |
| Mensagem de erro sobre bibliotecas | Dependências não instaladas | Execute `pip install pyautogui keyboard opencv-python` |
| Download não começa | Aba do navegador fora de foco | Clique na aba antes do fim da contagem regressiva |
| Automatização para em estado inesperado | Mudança na interface do Trends | Revise as imagens e ajuste os tempos de espera |

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE) (quando disponível) para mais
detalhes.

---

💬 **Dúvidas ou sugestões?** Abra uma _issue_ ou envie uma mensagem. Ficaremos felizes em ajudar!
