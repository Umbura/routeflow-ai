# 🚛 RouteFlow AI

> **Otimização Logística de Última Milha (*Last Mile*) impulsionada por Agentes de IA Generativa.**

![Badge Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Badge Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Badge AI](https://img.shields.io/badge/AI-Llama%203.3-blue?style=flat)
![Badge Pydantic](https://img.shields.io/badge/Code-Type%20Safe-e92063?style=flat)

![Demo Principal](assets/demo_whatsapp_informal.png)
*(Exemplo real: O sistema interpretando uma mensagem informal de chat e gerando uma rota otimizada)*

---

## 💡 O Problema
No setor de logística e delivery, a eficiência da "Última Milha" é crítica. Pequenas frotas e entregadores autônomos frequentemente recebem demandas de forma **desestruturada** (mensagens de WhatsApp, e-mails, anotações), o que gera dois problemas:
1.  Tempo perdido tentando organizar endereços manualmente.
2.  Rotas ineficientes que desperdiçam combustível e tempo.

## 🚀 A Solução
O **RouteFlow AI** é um Agente Inteligente que automatiza esse fluxo. Ele atua como um despachante virtual:
1.  **Entende** pedidos em linguagem natural (textos informais).
2.  **Valida** geograficamente os endereços.
3.  **Calcula** matematicamente a melhor rota de entrega.

## 🛠️ Metodologia e Arquitetura
O projeto foi desenvolvido utilizando princípios de **Clean Architecture** e **Modularidade**, separando a lógica de negócio (Backend) da interface (Frontend).

### O Fluxo do Agente (Agentic Workflow)
O sistema não é apenas um script, mas um orquestrador de ferramentas:

1.  **Cérebro (LLM):** Utilizamos o **Llama 3.3 (via Groq)** para processamento de linguagem natural. Ele extrai entidades (endereços) de textos bagunçados e os converte para JSON estruturado.
2.  **Ferramenta Geoespacial:** O agente consulta a API do **Nominatim (OpenStreetMap)** para converter endereços em coordenadas (Latitude/Longitude).
3.  **Motor de Otimização:** Aplicamos um algoritmo heurístico para resolver o **Problema do Caixeiro Viajante (TSP - Traveling Salesman Problem)**, garantindo que o entregador percorra a menor distância possível.

### Estrutura do Projeto
```text
src/
├── agent.py       # Orquestrador do Agente e Engenharia de Prompt
├── models.py      # Modelagem de Dados com Pydantic (Garante integridade)
└── services.py    # Serviços isolados (Geocoding e Algoritmos Matemáticos)
main.py            # Interface do Usuário (Streamlit)
