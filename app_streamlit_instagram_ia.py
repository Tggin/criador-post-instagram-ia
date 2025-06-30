
import streamlit as st
import google.generativeai as genai
from datetime import date

# Configuração da API do Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
MODEL_ID = "gemini-2.0-flash"

# Função para chamar o Gemini
def call_gemini(instruction, input_text):
    try:
        model = genai.GenerativeModel(MODEL_ID)
        prompt = f"{instruction}\n\nEntrada:\n{input_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erro: {str(e)}"

# Classe de agente
class MockAgent:
    def __init__(self, name, model, instruction, description, tools=None):
        self.name = name
        self.model = model
        self.instruction = instruction
        self.description = description
        self.tools = tools if tools else []

# Agentes
def search_subtopics(theme, date_today):
    return f"Subtemas encontrados para '{theme}' em {date_today}:\n" \
           f"1. Como {theme} impulsiona o engajamento no Instagram\n" \
           f"2. Ferramentas de {theme} para criar conteúdo viral\n" \
           f"3. Tendências de {theme} para 2025\n" \
           f"4. Impacto de {theme} na fidelização de clientes\n" \
           f"5. Estudos sobre o uso de {theme} por influenciadores"

def agente_buscador(theme, date_today):
    agente = MockAgent("agente_buscador", MODEL_ID,
        "Pesquise subtemas para Instagram.",
        "Busca subtemas")
    return search_subtopics(theme, date_today)

def agente_planejador(theme, subtopics):
    agente = MockAgent("agente_planejador", MODEL_ID,
        "Escolha e justifique o melhor subtema.",
        "Planeja o post")
    input_text = f"Tópico: {theme}\nSubtemas: {subtopics}"
    return call_gemini(agente.instruction, input_text)

def agente_redator(theme, plan):
    agente = MockAgent("agente_redator", MODEL_ID,
        "Você é um redator criativo. Crie um post com emojis, CTA e hashtags.",
        "Cria conteúdo")
    input_text = f"Tópico: {theme}\nPlano: {plan}"
    return call_gemini(agente.instruction, input_text)

def agente_revisor(theme, draft):
    agente = MockAgent("agente_revisor", MODEL_ID,
        "Revise o post para clareza, tom e erros.",
        "Revisa texto")
    input_text = f"Tópico: {theme}\nRascunho: {draft}"
    return call_gemini(agente.instruction, input_text)

def agente_leonardo_da_vinci(theme, final_post):
    agente = MockAgent("leonardo_da_vinci", MODEL_ID,
        "Descreva uma imagem para acompanhar o post.",
        "Cria imagem visual")
    input_text = f"Tópico: {theme}\nTexto final: {final_post}"
    return call_gemini(agente.instruction, input_text)

# Interface do Streamlit
st.title("🤖 Criador de Posts para Instagram com IA")
theme = st.text_input("Digite o tema geral (ex: futebol, tecnologia, moda)")

if st.button("Gerar Post"):
    if theme:
        date_today = date.today().strftime("%d/%m/%Y")
        st.info("🔍 Buscando subtemas...")
        subtopics = agente_buscador(theme, date_today)
        st.text(subtopics)

        st.info("🧠 Escolhendo subtema ideal...")
        plan = agente_planejador(theme, subtopics)
        st.text(plan)

        st.info("✍️ Criando rascunho do post...")
        draft = agente_redator(theme, plan)
        st.text(draft)

        st.info("🧐 Revisando post...")
        final_post = agente_revisor(theme, draft)
        st.text(final_post)

        st.info("🎨 Gerando ideia de imagem para o post...")
        image = agente_leonardo_da_vinci(theme, final_post)
        st.text(image)
    else:
        st.warning("Por favor, digite um tema antes de continuar.")
