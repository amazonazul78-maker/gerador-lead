import streamlit as st
import urllib.request
import json
import urllib.parse
import time

API_KEY = "MTViMTM0M2NkZWJjNDI4YmI1MWJiNDlkZTNjMDc3MjJ8NTg2NjIwMzg5Zg"

st.set_page_config(
    page_title="Gerador de Leads Empresariais",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.65rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #162f5c 0%, #1e3c72 100%);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        color: white;
    }
    .lead-card {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 18px;
        border-left: 6px solid #2a5298;
        border-top: 1px solid #eaeaea;
        border-right: 1px solid #eaeaea;
        border-bottom: 1px solid #eaeaea;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Gerador de Leads Empresariais")
st.markdown("Plataforma corporativa de inteligência de mercado e prospecção B2B em alta escala.")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Central de Operações")
    st.markdown("Defina os parâmetros de captação de clientes.")
    limite_leads = st.slider("Volume Alvo de Leads:", min_value=10, max_value=60, value=20, step=10)
    st.markdown("---")
    st.markdown("### 💎 Vantagem Competitiva")
    st.success("Ferramenta pronta para uso comercial. Demonstre o sistema ao vivo e converta empresas locais em clientes recorrentes.")

col_q1, col_q2 = st.columns([4, 1])
with col_q1:
    query = st.text_input("Segmento e Localidade Alvo:", placeholder="Ex: Clínicas em São Paulo, Construtoras no Rio de Janeiro...")
with col_q2:
    st.markdown("### ")
    btn_buscar = st.button("🚀 Iniciar Varredura")

if btn_buscar:
    if not query.strip():
        st.warning("Por favor, insira um segmento e região válidos para iniciar a prospecção.")
    else:
        query_encoded = urllib.parse.quote(query)
        url_start = f"https://api.outscraper.com/maps/search-v2?query={query_encoded}&limit={limite_leads}"

        with st.spinner(f"Estabelecendo conexão segura com os servidores de inteligência para '{query}'..."):
            try:
                req = urllib.request.Request(url_start, headers={"X-API-KEY": API_KEY})
                with urllib.request.urlopen(req) as response:
                    dados_iniciais = json.loads(response.read().decode("utf-8"))
                    
                results_location = dados_iniciais.get("results_location")
                
                if not results_location:
                    st.error("A API não retornou o canal de processamento.")
                else:
                    status_placeholder = st.empty()
                    status_placeholder.info("Varrendo e estruturando dados comerciais em tempo real...")
                    
                    tentativas = 0
                    dados_finais = None
                    
                    while tentativas < 20:
                        time.sleep(5)
                        req_check = urllib.request.Request(results_location, headers={"X-API-KEY": API_KEY})
                        try:
                            with urllib.request.urlopen(req_check) as resp_check:
                                dados_finais = json.loads(resp_check.read().decode("utf-8"))
                            
                            if isinstance(dados_finais, dict) and dados_finais.get("status") == "Success":
                                break
                            elif isinstance(dados_finais, list):
                                break
                        except Exception:
                            pass
                        tentativas += 1
                        
                    if dados_finais:
                        status_placeholder.empty()
                        
                        data_list = []
                        if isinstance(dados_finais, dict):
                            raw_data = dados_finais.get("data", [])
                            if isinstance(raw_data, list):
                                for item in raw_data:
                                    if isinstance(item, list):
                                        data_list.extend(item)
                                    elif isinstance(item, dict):
                                        data_list.append(item)
                        elif isinstance(dados_finais, list):
                            for entry in dados_finais:
                                if isinstance(entry, dict):
                                    sub_data = entry.get("data", [])
                                    if isinstance(sub_data, list):
                                        for sub_item in sub_data:
                                            if isinstance(sub_item, list):
                                                data_list.extend(sub_item)
                                            elif isinstance(sub_item, dict):
                                                data_list.append(sub_item)
                                    elif isinstance(entry, list):
                                        data_list.extend(entry)

                        if not data_list:
                            st.warning("Nenhum registro localizado para esta consulta. Tente uma região mais ampla.")
                        else:
                            total_encontrados = len(data_list)
                            com_telefone = sum(1 for e in data_list if isinstance(e, dict) and e.get("phone") and e.get("phone") != "N/A")
                            com_site = sum(1 for e in data_list if isinstance(e, dict) and e.get("site") and e.get("site") != "N/A")

                            st.success(f"Prospecção concluída com sucesso! {total_encontrados} empresas mapeadas.")
                            
                            col_m1, col_m2, col_m3 = st.columns(3)
                            col_m1.metric("Leads Capturados", total_encontrados)
                            col_m2.metric("Contatos Telefônicos", com_telefone)
                            col_m3.metric("Websites Ativos", com_site)
                            
                            st.markdown("---")
                            st.markdown("### 📋 Vitrine de Leads Qualificados:")
                            
                            texto_exportacao = ""
                            
                            for i, empresa in enumerate(data_list, 1):
                                if not isinstance(empresa, dict):
                                    continue
                                nome = empresa.get("name", "N/A")
                                telefone = empresa.get("phone", "N/A")
                                endereco = empresa.get("full_address", "N/A")
                                site = empresa.get("site", "N/A")
                                
                                bloco_lead = f"--- Lead {i} ---\nEmpresa: {nome}\nTelefone: {telefone}\nEndereço: {endereco}\nSite: {site}\n\n"
                                texto_exportacao += bloco_lead
                                
                                st.markdown(f"""
                                    <div class="lead-card">
                                        <h4 style="margin:0 0 10px 0; color:#1e3c72; font-size:1.1rem;"><b>{i}. {nome}</b></h4>
                                        <p style="margin: 4px 0; color:#333;">📞 <b>Telefone de Contato:</b> <code style="background:#f1f3f5; padding:2px 6px; border-radius:4px;">{telefone}</code></p>
                                        <p style="margin: 4px 0; color:#555;">📍 <b>Endereço Completo:</b> {endereco}</p>
                                        <p style="margin: 4px 0; color:#555;">🌐 <b>Portal / Site:</b> {site}</p>
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            if texto_exportacao:
                                st.markdown("---")
                                st.download_button(
                                    label="📥 Exportar Base Completa de Leads (.txt)",
                                    data=texto_exportacao,
                                    file_name=f"leads_{query.replace(' ', '_')}.txt",
                                    mime="text/plain"
                                )
                    else:
                        st.error("Tempo limite excedido na resposta dos servidores. Por favor, tente novamente.")
            except Exception as e:
                st.error(f"Erro crítico na requisição: {e}")
