# Processador de Relatórios Corporativos com LLM & Dashboard BI

Aplicação web desenvolvida em Python para automação do fluxo de extração de dados não estruturados, persistência em banco relacional e visualização analítica de métricas corporativas.

---

##  Arquitetura do Projeto

O sistema foi estruturado seguindo o princípio de responsabilidade única (SoC - *Separation of Concerns*), mantendo o código modular e legível:

* **`app.py`**: Interface web desenvolvida em Streamlit, responsável pelas abas de processamento e visualização de dashboards.
* **`database.py`**: Camada de persistência de dados com SQLite, isolando consultas SQL, criação de tabelas e operações de leitura/escrita.
* **`llm_service.py`**: Módulo de integração com a API da Groq (LLM), responsável por enviar prompts e validar retornos estruturados em JSON.
* **`exemplos_teste.txt`**: Conjunto de dados não estruturados de teste para validação do sistema.

---

##  Tecnologias Utilizadas

* **Python 3.10+**
* **Streamlit**: Construção da interface gráfica interativa.
* **SQLite3**: Banco de dados relacional leve para armazenamento local dos registros.
* **Pandas & Plotly**: Manipulação de dados e renderização de gráficos interativos no dashboard.
* **Groq API / SDK**: Processamento de Linguagem Natural com garantia de output em formato `json_object`.

---

##  Instalação e Execução

### 1. Clonar o repositório ou extrair os arquivos

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA>