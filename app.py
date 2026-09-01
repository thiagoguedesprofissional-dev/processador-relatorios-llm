import streamlit as st
import pandas as pd
import plotly.express as px

# Importando os módulos criados
from database import init_db, insert_record, get_all_records, seed_data, clear_db
from llm_service import process_text_with_llm

# Inicializa o banco ao abrir a aplicação
init_db()

st.set_page_config(
    page_title="Extrator Inteligente e Dashboard Analítico",
    layout="wide"
)

# Sidebar: Configurações e Dados Demo
st.sidebar.title("Configurações e API")
groq_api_key = st.sidebar.text_input("Groq API Key (Gratuito)", type="password", help="Obtenha uma chave gratuita em console.groq.com")

st.sidebar.markdown("---")
st.sidebar.subheader("Ferramentas de Teste")

if st.sidebar.button("Popular Banco com Dados Demo"):
    seed_data()
    st.sidebar.success("Dados de teste inseridos com sucesso!")
    st.rerun()

if st.sidebar.button("Limpar Banco de Dados"):
    clear_db()
    st.sidebar.warning("Banco de dados resetado!")
    st.rerun()

# Cabeçalho Principal
st.title("Extrator de Relatórios e Dashboard Analítico")
st.caption("Projeto Integrado: Processamento por LLM + Banco SQL + Dashboard Streamlit em Tempo Real")

# Abas de Navegação
tab1, tab2, tab3 = st.tabs(["Processamento e Extração (LLM)", "Dashboard Analítico", "Registros no SQL"])

# ABA 1: EXTRAÇÃO DE TEXTO
with tab1:
    st.header("Extração de Dados Não Estruturados")
    st.markdown("Cole um relatório, e-mail, ordem de serviço ou nota de atendimento para extrair os dados estruturados via IA.")

    exemplo_texto = "Recebemos um chamado urgente do cliente PRS Tecnologia solicitando apoio na otimização de consultas SQL e integração do pipeline de dados com o Microsoft Fabric. O serviço de consultoria foi estimado em R$ 3.500,00 e o status atual é Em Andamento. A prioridade definida foi Alta."

    col_btn, col_blank = st.columns([1, 4])
    with col_btn:
        if st.button("Usar Exemplo de Texto"):
            st.session_state["input_texto"] = exemplo_texto

    input_texto = st.text_area(
        "Insira o texto bruto aqui:", 
        value=st.session_state.get("input_texto", ""), 
        height=180,
        placeholder="Cole a mensagem do cliente, e-mail de suporte ou ordem de serviço..."
    )

    if st.button("Processar com LLM e Salvar no Banco SQL", type="primary"):
        if not input_texto.strip():
            st.error("Por favor, insira um texto para processar.")
        elif not groq_api_key.strip():
            st.warning("Aviso: Insira sua Groq API Key na barra lateral para utilizar o modelo de IA. (Obtenha em console.groq.com)")
        else:
            with st.spinner("Analisando texto com LLM e extraindo dados estruturados..."):
                try:
                    dados_extraidos = process_text_with_llm(input_texto, groq_api_key)
                    
                    insert_record(
                        cliente=dados_extraidos.get("cliente", "N/A"),
                        categoria=dados_extraidos.get("categoria", "N/A"),
                        valor=float(dados_extraidos.get("valor", 0.0)),
                        status=dados_extraidos.get("status", "N/A"),
                        urgencia=dados_extraidos.get("urgencia", "N/A"),
                        resumo=dados_extraidos.get("resumo", "N/A"),
                        texto_original=input_texto
                    )

                    st.success("Sucesso: Dados extraídos e salvos no Banco SQL com sucesso!")
                    st.json(dados_extraidos)

                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar: {e}")

# ABA 2: DASHBOARD ANALÍTICO
with tab2:
    st.header("Métricas e Indicadores de Atendimento")
    df = get_all_records()

    if df.empty:
        st.info("O banco de dados está vazio. Processe um relatório na Aba 1 ou clique em 'Popular Banco com Dados Demo' na barra lateral.")
    else:
        total_registros = len(df)
        valor_total = df['valor'].sum()
        ticket_medio = df['valor'].mean() if total_registros > 0 else 0
        concluidos = len(df[df['status'] == 'Concluído'])
        percentual_concluido = (concluidos / total_registros * 100) if total_registros > 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total de Registros", total_registros)
        c2.metric("Valor Total Processado", f"R$ {valor_total:,.2f}")
        c3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
        c4.metric("Taxa de Conclusão", f"{percentual_concluido:.1f}%")

        st.markdown("---")

        g1, g2 = st.columns(2)

        with g1:
            st.subheader("Faturamento / Valor por Cliente")
            df_cliente = df.groupby('cliente')['valor'].sum().reset_index()
            fig_cliente = px.bar(
                df_cliente, 
                x='cliente', 
                y='valor', 
                text_auto='.2s',
                labels={'valor': 'Valor (R$)', 'cliente': 'Cliente'},
                color='cliente',
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_cliente.update_layout(showlegend=False)
            st.plotly_chart(fig_cliente, use_container_width=True)

        with g2:
            st.subheader("Distribuição por Categoria de Serviço")
            df_cat = df['categoria'].value_counts().reset_index()
            df_cat.columns = ['categoria', 'quantidade']
            fig_cat = px.pie(
                df_cat, 
                names='categoria', 
                values='quantidade', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        g3, g4 = st.columns(2)

        with g3:
            st.subheader("Status dos Chamados")
            df_status = df['status'].value_counts().reset_index()
            df_status.columns = ['status', 'quantidade']
            fig_status = px.bar(
                df_status, 
                x='status', 
                y='quantidade',
                color='status',
                color_discrete_map={'Concluído': '#2ecc71', 'Em Andamento': '#f1c40f', 'Pendente': '#e74c3c'}
            )
            st.plotly_chart(fig_status, use_container_width=True)

        with g4:
            st.subheader("Nível de Urgência")
            df_urg = df['urgencia'].value_counts().reset_index()
            df_urg.columns = ['urgencia', 'quantidade']
            fig_urg = px.pie(
                df_urg, 
                names='urgencia', 
                values='quantidade',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig_urg, use_container_width=True)

# ABA 3: VISUALIZAÇÃO DE REGISTROS
with tab3:
    st.header("Consulta à Base de Dados SQLite")
    df = get_all_records()

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar Dados da Tabela (CSV)",
            data=csv,
            file_name="relatorios_extraidos_sql.csv",
            mime="text/csv",
        )
    else:
        st.info("Nenhum registro encontrado no banco de dados.")