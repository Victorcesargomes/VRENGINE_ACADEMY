import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente
load_dotenv()

# Cria instância do cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuração da página
st.set_page_config(page_title="VR Engine - Serviços Acadêmicos", page_icon=":mortar_board:")

# CSS customizado
st.markdown(
    """
    <style>
        .main, .block-container {
            background-color: #e0e0de;
            color: #000000;
        }
        .css-1cypcdb.e1fqkh3o3, .css-1cypcdb.e1fqkh3o1 {
            background-color: #dedfdc !important;
            color: #000000 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000;
        }
        .stChatMessage.user {
            background-color: #dbdbd9 !important;
            color: #000000 !important;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatMessage.assistant {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #dedfdc;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatInput {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #dbdbd9;
            border-radius: 5px;
        }
        .stChatInput textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stChatInput textarea::placeholder {
            color: #000000 !important;
        }
        .css-1offfwp p, .css-1vgnld6 {
            color: #000000 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Função para a barra lateral
def sidebar():
    st.sidebar.image("loogo.png", use_container_width=True)
    st.sidebar.markdown("### VR ENGINE - Serviços Acadêmicos")
    st.sidebar.markdown("**Consultoria acadêmica, mentoria, escrita acadêmica e serviços educacionais.**")
    return st.sidebar.selectbox(
        "Selecione o tipo de serviço:",
        [
            "Consultoria em Escrita Acadêmica",
            "Mentoria sobre Publicação Científica",
            "Apoio em Metodologia de Pesquisa",
            "Formatação e Normas Acadêmicas",
        ],
    )

# Função para a página de chat
def pagina_chat(servico_escolhido):
    st.title("Bem-vindo à Plataforma de Consultoria Acadêmica")
    st.markdown(
        """
        Esta aplicação utiliza modelos da OpenAI para auxiliar em diversas etapas do trabalho acadêmico.
        Selecione um serviço na barra lateral e faça suas perguntas no campo abaixo.
        """
    )

    # Define o contexto inicial com base no serviço selecionado
    if servico_escolhido == "Consultoria em Escrita Acadêmica":
        acao = "Forneça sugestões detalhadas de aprimoramento na escrita acadêmica."
    elif servico_escolhido == "Mentoria sobre Publicação Científica":
        acao = "Forneça orientação sobre os próximos passos para publicação, possíveis revistas científicas adequadas e dicas para melhorar a probabilidade de aceitação."
    elif servico_escolhido == "Apoio em Metodologia de Pesquisa":
        acao = "Forneça orientação metodológica sólida, sugestões de desenhos de pesquisa, técnicas analíticas e referências."
    else:
        acao = "Explique as normas, a formatação e dê exemplos claros."

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"Você é um consultor acadêmico sênior da empresa 'Veloso e Almeida - Serviços Acadêmicos', especialista em orientação, mentoria, escrita e serviços educacionais no âmbito acadêmico. {acao}"
            }
        ]

    # Exibe as mensagens existentes
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        elif msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    # Campo de entrada no estilo chat
    user_input = st.chat_input("Digite sua pergunta ou mensagem...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Chamada ao modelo
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            max_tokens=1500,
            temperature=0.7,
        )

        resposta = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.write(resposta)

    # Botões lado a lado: Download da conversa e Iniciar Nova Conversa
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.messages:
            conversation_json = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
            st.download_button(
                label="Baixar Conversa",
                data=conversation_json,
                file_name="conversa.json",
                mime="application/json",
            )

    with col2:
        if st.button("Iniciar Nova Conversa"):
            st.session_state.clear()  # Limpa o estado da sessão
            st.session_state["new_conversation"] = True  # Sinaliza que deve reiniciar

# Função principal
def main():
    if st.session_state.get("new_conversation", False):
        st.session_state.clear()  # Reinicia todo o estado
        st.session_state["new_conversation"] = False  # Reseta o gatilho

    servico_escolhido = sidebar()
    pagina_chat(servico_escolhido)

# Executa a aplicação
if __name__ == "__main__":
    main()
