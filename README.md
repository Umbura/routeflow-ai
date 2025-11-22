# RouteFlow AI

> **Autonomous Last-Mile Logistics Optimization powered by Generative AI Agents.**
> 
[![Português](https://img.shields.io/badge/Lang-Português-green)](README_PT.md)
![Badge Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Badge Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Badge AI](https://img.shields.io/badge/AI-Llama%203.3-blue?style=flat)

[![Read in Portuguese](https://img.shields.io/badge/Read%20in-Portuguese-green?style=for-the-badge&logo=appveyor)](README_PT.md)

![Main Demo](https://github.com/Umbura/routeflow-ai/blob/main/assets/demo_en_whatsapp.PNG)
*(Example: The system interpreting an informal chat message and generating an optimized route)*

---

## About
In the logistics and delivery sector, "Last Mile" efficiency is critical. Small fleets and independent drivers often receive demands in **unstructured formats** (WhatsApp messages, emails, handwritten notes), leading to two main problems:
1.  Time wasted manually organizing addresses.
2.  Inefficient routes that waste fuel and time.

To solve this, **RouteFlow AI** is an Intelligent Agent that automates this workflow. It acts as a virtual dispatcher that:
1.  **Understands** natural language orders (informal text).
2.  **Validates** addresses geographically.
3.  **Calculates** the mathematically optimal route.

## Methodology and Architecture
The project was developed using **Clean Architecture** and **Modularity** principles, separating business logic (Backend) from the interface (Frontend).

### Agentic Workflow
The system is not just a script, but a tool orchestrator:

1.  **Brain (LLM):** We use **Llama 3.3 (via Groq)** for natural language processing. It extracts entities (addresses) from messy text and converts them into structured JSON.
2.  **Geospatial Tool:** The agent queries the **Nominatim API (OpenStreetMap)** to convert strings into coordinates (Latitude/Longitude).
3.  **Optimization Engine:** We apply a heuristic algorithm to solve the **Traveling Salesman Problem (TSP)**, ensuring the driver travels the shortest possible distance.

## Conclusion
*This was a rewarding project to build and relatively straightforward, as the libraries and agents available for this concept are highly effective.*

*I tested various message combinations, and the agent was able to interpret them effectively, even when using extremely informal language. These scenarios can be viewed in the `assets` folder.*

*An interesting next step would be integrating it with Google Maps to access real-time traffic data and subsequently developing a mobile App.*

## Installation and Usage

Clone the repository, create a virtual environment to install the requirements, and configure your Agent's API Key (Groq, OpenAI, etc.) in the `.env` file.

Finally, execute it with:
`streamlit run main.py`
