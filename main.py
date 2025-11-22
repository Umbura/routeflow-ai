import streamlit as st
import folium
from streamlit_folium import st_folium
from src.agent import LogisticsAgent
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="RouteFlow AI", page_icon="🚛", layout="wide")

# Estilização CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #2c3e50; }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Inicialização de Estado (Session State) para persistência de dados
    if "route_plan" not in st.session_state:
        st.session_state["route_plan"] = None

    st.title("🚛 RouteFlow AI")
    st.markdown("### Otimização Logística Autônoma baseada em Agentes")

    # Barra Lateral
    with st.sidebar:
        st.header("Sobre o Sistema")
        st.info(
            """
            **Arquitetura Técnica:**
            - **Agent:** Llama-3.3 (Parsing Semântico via Groq)
            - **Tools:** Nominatim (Geocoding) & TSP Heuristic
            - **Backend:** Python + Pydantic (Type Safe)
            """
        )
        if st.button("🗑️ Limpar Resultados"):
            st.session_state["route_plan"] = None
            st.rerun()

    # Layout Principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        input_text = st.text_area(
            "Entrada de Pedidos (Linguagem Natural):",
            value="Coletar pacote na Av. Paulista, 1000, SP. Entregar para cliente na Rua Augusta, 500 e depois na Rua Pamplona, 800.",
            height=200,
            help="Cole aqui mensagens de WhatsApp, e-mails ou tickets de suporte logístico."
        )
        
        if st.button("🛠️ Gerar Rota Otimizada"):
            if input_text:
                try:
                    with st.spinner("🤖 Agente analisando endereços e calculando melhor rota..."):
                        agent = LogisticsAgent()
                        # Executa o agente e salva no estado da sessão
                        st.session_state["route_plan"] = agent.process_request(input_text)
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")

    # Exibição de Resultados
    if st.session_state["route_plan"]:
        route_plan = st.session_state["route_plan"]
        
        if not route_plan.stops:
            pass # Avisos já são tratados pelo agente
        else:
            # Painel de Informações (Direita)
            with col2:
                st.success(f"✅ Rota Otimizada! Distância Total Estimada: {route_plan.total_distance_km} km")
                
                df_stops = pd.DataFrame([
                    {"Ordem": i+1, "Endereço": stop.address, "Lat": stop.latitude, "Lon": stop.longitude} 
                    for i, stop in enumerate(route_plan.stops)
                ])
                
                st.dataframe(
                    df_stops[["Ordem", "Endereço"]], 
                    use_container_width=True, 
                    hide_index=True
                )

            # Mapa Interativo (Abaixo)
            st.markdown("---")
            st.subheader("🗺️ Visualização Geográfica")
            
            # Centraliza o mapa no ponto de partida
            start_loc = route_plan.stops[0]
            m = folium.Map(location=[start_loc.latitude, start_loc.longitude], zoom_start=14)

            points = []
            for i, stop in enumerate(route_plan.stops):
                points.append([stop.latitude, stop.longitude])
                
                # Cores diferentes para início e fim
                icon_color = "green" if i == 0 else "blue"
                icon_type = "play" if i == 0 else "map-marker"
                
                folium.Marker(
                    [stop.latitude, stop.longitude],
                    popup=f"{i+1}: {stop.address}",
                    icon=folium.Icon(color=icon_color, icon=icon_type, prefix='fa')
                ).add_to(m)

            # Desenha a linha da rota
            folium.PolyLine(points, color="#2c3e50", weight=4, opacity=0.7).add_to(m)

            st_folium(m, width=1200, height=500)

if __name__ == "__main__":
    main()