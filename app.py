import streamlit as st
from streamlit.components.v1 import html

# Função para gerar o componente HTML/JavaScript do rodapé
def display_visitor_ip_footer():
    """
    Cria e exibe um rodapé fixo que mostra o endereço IP público do visitante.
    O IP é obtido no lado do cliente usando JavaScript e uma API externa.
    """
    footer_html_code = """
    <style>
        #visitor-ip-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6; /* Cor de fundo similar ao tema claro do Streamlit */
            color: #31333F; /* Cor de texto similar ao Streamlit */
            text-align: center;
            padding: 8px 0px;
            border-top: 1px solid #E6E6E6; /* Borda superior sutil */
            font-size: 0.875rem; /* Equivalente a 14px se o base for 16px */
            z-index: 9999; /* Garante que fique acima da maioria dos outros elementos */
            box-sizing: border-box; /* Para incluir padding e borda na largura/altura total */
        }
        #visitor-ip-footer span#user-ip-address {
            font-weight: bold;
        }
    </style>

    <div id="visitor-ip-footer">
        Seu Endereço IP: <span id="user-ip-address">Carregando...</span>
    </div>

    <script>
        async function fetchAndDisplayUserIP() {
            const ipElement = document.getElementById('user-ip-address');
            try {
                // Tentativa 1: ipinfo.io (fornece mais detalhes, mas usamos apenas o IP)
                let response = await fetch('https://ipinfo.io/json', {
                    method: 'GET',
                    headers: { 'Accept': 'application/json' }
                });
                
                if (!response.ok) {
                    console.warn('Falha ao buscar IP de ipinfo.io (status: ' + response.status + '). Tentando api.ipify.org...');
                    // Tentativa 2: api.ipify.org (mais simples e direto)
                    response = await fetch('https://api.ipify.org?format=json', {
                        method: 'GET',
                        headers: { 'Accept': 'application/json' }
                    });
                }

                if (!response.ok) {
                    throw new Error('Falha na resposta da rede de todos os serviços de IP: ' + response.statusText);
                }

                const data = await response.json();

                if (data && data.ip) {
                    ipElement.textContent = data.ip;
                } else {
                    throw new Error('Endereço IP não encontrado na resposta da API.');
                }

            } catch (error) {
                console.error('Erro ao buscar o endereço IP do visitante:', error);
                if (ipElement) {
                    ipElement.textContent = 'Não disponível';
                }
            }
        }

        // Garante que o DOM está completamente carregado antes de executar o script
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fetchAndDisplayUserIP);
        } else {
            // DOMContentLoaded já foi disparado
            fetchAndDisplayUserIP();
        }
    </script>
    """
    # O componente html do Streamlit renderiza o conteúdo dentro de um iframe.
    # A altura deve ser suficiente para o conteúdo do rodapé.
    # Ajuste a altura se o padding ou font-size do rodapé for alterado significativamente.
    html(footer_html_code, height=45)


# Exemplo de uso em um aplicativo Streamlit:
if __name__ == "__main__":
    st.set_page_config(page_title="App com IP do Visitante", layout="wide")

    st.title("Meu Web App")
    st.write(
        "Bem-vindo ao meu aplicativo! Este é um exemplo de como exibir o IP do visitante no rodapé."
    )

    st.sidebar.header("Barra Lateral")
    st.sidebar.write("Conteúdo da barra lateral.")

    # Adiciona algum conteúdo para preencher a página e demonstrar o rodapé fixo
    for i in range(3):
        st.write(f"Linha de conteúdo de exemplo número {i+1}...")

    # Chama a função para exibir o rodapé com o IP do visitante
    # Esta função deve ser chamada no final do seu script principal
    # ou após a renderização da maior parte do conteúdo da sua página.
    display_visitor_ip_footer()

    st.caption("Nota: O endereço IP exibido é o seu IP público conforme detectado por serviços externos.")