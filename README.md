# RouteFlow AI

> **Otimização Logística de Última Milha (*Last Mile*) impulsionada por Agentes de IA Generativa.**

![Badge Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Badge Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Badge AI](https://img.shields.io/badge/AI-Llama%203.3-blue?style=flat)

![Demo Principal](https://github.com/Umbura/routeflow-ai/blob/main/assets/demo_whatsapp_msg_2.PNG)
*(Exemplo: O sistema interpretando uma mensagem informal de chat e gerando uma rota otimizada)*

---

## Sobre
No setor de logística e delivery, a eficiência da "Última Milha" é crítica. Pequenas frotas e entregadores autônomos frequentemente recebem demandas de forma **desestruturada** (mensagens de WhatsApp, e-mails, anotações), o que gera dois problemas:
1.  Tempo perdido tentando organizar endereços manualmente.
2.  Rotas ineficientes que desperdiçam combustível e tempo.

Visando solucionar isso **RouteFlow AI** é um Agente Inteligente que automatiza esse fluxo. Ele atua como um despachante virtual:
1.  **Entende** pedidos em linguagem natural (textos informais).
2.  **Valida** geograficamente os endereços.
3.  **Calcula** matematicamente a melhor rota de entrega.

## Metodologia e Arquitetura
O projeto foi desenvolvido utilizando princípios de **Clean Architecture** e **Modularidade**, separando a lógica de negócio (Backend) da interface (Frontend).

### O Fluxo do Agente (Agentic Workflow)
O sistema não é apenas um script, mas um orquestrador de ferramentas:

1.  **Cérebro (LLM):** Utilizamos o **Llama 3.3 (via Groq)** para processamento de linguagem natural. Ele extrai entidades (endereços) de textos bagunçados e os converte para JSON estruturado.
2.  **Ferramenta Geoespacial:** O agente consulta a API do **Nominatim (OpenStreetMap)** para converter endereços em coordenadas (Latitude/Longitude).
3.  **Motor de Otimização:** Aplicamos um algoritmo heurístico para resolver o **Problema do Caixeiro Viajante (TSP - Traveling Salesman Problem)**, garantindo que o entregador percorra a menor distância possível.

## Conclusão
*Foi um projeto satisfatorio e não muito dificil, já que as bibliotecas e agentes para esse tipo de ideia são bem efetivos.*
*Testei varias combinaçõe de mensagem e o agente foi capaz de interpretar de forma efetiva, mesmo usando uma linguagem extremamente informal, essas combinações podem ser visualizadas na pasta assets.*

*Para mim, um proximo passo interessante seria integra-lo ao google maps pra ter dados de transito em tempo real e posteriormente desenvolver um APP.*

## Instalação e Uso

Clone o repositorio, crie um ambiente virtual para instalação dos requerimentos e configure a chave API do seu agente(grok, openai e etc.) no `.env`.

Por fim execute com `streamlit run main.py`
