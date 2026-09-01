import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "relatorios.db"

def init_db():
    """Inicializa a tabela de dados se não existir."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_registro TEXT,
            cliente TEXT,
            categoria TEXT,
            valor REAL,
            status TEXT,
            urgencia TEXT,
            resumo TEXT,
            texto_original TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(cliente, categoria, valor, status, urgencia, resumo, texto_original):
    """Insere um novo registro extraído no banco SQL."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO chamados (data_registro, cliente, categoria, valor, status, urgencia, resumo, texto_original)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data_atual, cliente, categoria, valor, status, urgencia, resumo, texto_original))
    conn.commit()
    conn.close()

def get_all_records():
    """Retorna todos os registros em um DataFrame Pandas."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM chamados ORDER BY id DESC", conn)
    conn.close()
    return df

def seed_data():
    """Insere dados fictícios para teste rápido do dashboard."""
    exemplo_dados = [
        ("PRS Tecnologia", "Suporte TI", 1200.00, "Concluído", "Média", "Migração de servidor de banco SQL concluída."),
        ("Empresa Alpha", "Desenvolvimento", 4500.00, "Em Andamento", "Alta", "Desenvolvimento de automação de extrator de dados."),
        ("Beta Services", "Consultoria IA", 3200.00, "Concluído", "Baixa", "Treinamento de equipe em uso de LLMs e Engenharia de Prompt."),
        ("Gama Log", "Infraestrutura", 800.00, "Pendente", "Alta", "Falha de conexão com a API de integração do ERP."),
        ("PRS Tecnologia", "Consultoria IA", 5000.00, "Concluído", "Alta", "Implementação do Copiloto de Atendimento Interno.")
    ]
    for cliente, cat, val, st_val, urg, res in exemplo_dados:
        insert_record(cliente, cat, val, st_val, urg, res, "Dados fictícios de demonstração.")

def clear_db():
    """Apaga todos os registros do banco de dados."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chamados")
    conn.commit()
    conn.close()