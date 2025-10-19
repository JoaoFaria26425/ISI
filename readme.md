# 🏎️ Projeto ETL F1 — Integração de Sistemas de Informação

## 📘 Descrição Geral

Este projeto foi desenvolvido no âmbito da Unidade Curricular **Integração de Sistemas de Informação (ISI)** e tem como objetivo a **implementação de um processo completo de ETL (Extract, Transform, Load)** aplicado a dados da **Fórmula 1**.

O sistema integra dados reais obtidos através da **API pública da Ergast (ergast.com/api)**, processa-os via **n8n**, armazena-os num **Supabase (PostgreSQL em cloud)** e apresenta-os numa aplicação **Streamlit** sob a forma de um **dashboard interativo**.

---

## 🎯 Objetivos

- Aplicar conceitos de **ETL** na integração e transformação de dados reais.  
- Implementar um **pipeline automatizado** utilizando o **n8n**.  
- Utilizar uma **base de dados em cloud (Supabase)** para garantir acessibilidade e escalabilidade.  
- Criar uma **interface visual (Streamlit)** que permita explorar os dados de forma intuitiva.  
- Demonstrar o potencial da integração entre diferentes ferramentas modernas de software.

---

## 🧩 Arquitetura do Sistema

O projeto segue uma estrutura modular composta por três grandes componentes:

### 1. **Extração (Extract)**
- Fonte: API pública da **Ergast F1**  
- Dados recolhidos: **Circuitos, Corridas, Pilotos e Voltas**  
- Ferramenta: **n8n (nó HTTP Request)**  

### 2. **Transformação (Transform)**
- Conversão dos dados JSON para formato relacional.  
- Limpeza e normalização dos valores (por exemplo: coordenadas, nomes e tempos).  
- Evita redundância ao verificar registos existentes antes de criar novos.  
- Ferramenta: **n8n (nó Code)** com JavaScript.  

### 3. **Carregamento (Load)**
- Inserção e atualização dos dados no **Supabase** (PostgreSQL cloud).  
- Registo de logs de execução em tabela própria (`etl_log`).  
- Ferramenta: **n8n (nó Supabase)**.

---

## 🧠 Tecnologias Utilizadas

| Categoria | Ferramenta | Função |
|------------|-------------|--------|
| ETL | [n8n](https://n8n.io/) | Orquestração e automação do processo ETL |
| Base de Dados | [Supabase](https://supabase.com/) | Armazenamento em cloud (PostgreSQL) |
| Frontend / Dashboard | [Streamlit](https://streamlit.io/) | Visualização dos dados |
| Fonte de Dados | [Ergast API](https://ergast.com/mrd/) | Dados oficiais da Fórmula 1 |

---

## 🚀 Dashboard (Streamlit)

O **dashboard** foi desenvolvido em **Python + Streamlit** e permite:

- Filtrar por **Circuito**, **Temporada (Season)** e **Ronda (Round)**.  
- Visualizar o **Leaderboard dos pilotos** com a melhor volta e média de tempos.  
- Ver automaticamente a **imagem do circuito** correspondente.  
- Comparar desempenhos de forma clara e interativa.

### Exemplo de layout:
- Dropdowns no topo (Circuito, Season, Round)  
- Tabela ordenada (Posição 🏁, Nome, Apelido, Melhor Volta, Média)  
- Imagem do circuito no final da página  

---

## 🗃️ Estrutura da Base de Dados (Supabase)

As tabelas principais:

- **f1_circuits** — Informação dos circuitos  
- **f1_drivers** — Dados dos pilotos  
- **f1_races** — Informação das corridas  
- **f1_laps** — Voltas de cada piloto  
- **etl_log** — Registo das execuções ETL  

---

## 🕒 Automação (Jobs n8n)

O **n8n workflow** é executado automaticamente **a cada hora** e realiza:
1. Extração de dados via API.  
2. Transformação de cada conjunto de dados.  
3. Inserção e atualização no Supabase.  
4. Registo do resultado no log ETL.

![ETL Workflow Screenshot](./docs/n8n_workflow.png)

---

## 🧭 Melhorias Futuras

- Adicionar comparação com **tempos obtidos em simuladores** (ex: Assetto Corsa).  
  Seria uma funcionalidade divertida e interessante, permitindo analisar a proximidade entre o desempenho real e o simulado.
- Criar um painel de **estatísticas históricas** com evolução dos tempos por circuito.
- Implementar alertas automáticos via **email ou Telegram** quando novos dados forem carregados.

---

## 📦 Instalação e Execução

### 1. Clonar o repositório:
```bash
git clone https://github.com/teu-utilizador/f1-etl.git
cd f1-etl
