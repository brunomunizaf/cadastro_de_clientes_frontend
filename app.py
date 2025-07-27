import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import re

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Touché - Cadastro de Clientes",
    page_icon="👔",
    layout="wide"
)

# Inicializar Supabase
@st.cache_resource
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("⚠️ Configure as variáveis de ambiente SUPABASE_URL e SUPABASE_ANON_KEY")
        return None
    return create_client(url, key)

supabase = init_supabase()

# Função para validar CPF
def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    return cpf[-2:] == f"{digito1}{digito2}"

# Função para validar CNPJ
def validar_cnpj(cnpj):
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False
    
    # Validação do primeiro dígito verificador
    multiplicadores = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores[i] for i in range(12))
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    # Validação do segundo dígito verificador
    multiplicadores = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores[i] for i in range(13))
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    return cnpj[-2:] == f"{digito1}{digito2}"

# Função para validar email
def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Função para verificar se CPF/CNPJ já existe
def verificar_inscricao_existe(inscricao):
    try:
        result = supabase.table('clientes').select('nome, email').eq('inscricao', inscricao).execute()
        return len(result.data) > 0, result.data[0] if result.data else None
    except Exception as e:
        st.error(f"Erro ao verificar inscrição: {str(e)}")
        return False, None

# Função para cadastrar cliente
def cadastrar_cliente(dados):
    try:
        result = supabase.table('clientes').insert(dados).execute()
        return True, "Cliente cadastrado com sucesso!"
    except Exception as e:
        error_msg = str(e)
        if "duplicate key value violates unique constraint" in error_msg and "inscricao" in error_msg:
            return False, "CPF/CNPJ já está cadastrado no sistema!"
        return False, f"Erro ao cadastrar cliente: {error_msg}"

# Função para buscar clientes
def buscar_clientes():
    try:
        result = supabase.table('clientes').select('*').execute()
        return result.data
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {str(e)}")
        return []

# Interface principal
def main():
    st.title("👔 Touché - Cadastro de Clientes")
    st.markdown("---")
    
    # Sidebar para navegação
    st.sidebar.title("Menu")
    pagina = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["📝 Cadastrar Cliente", "📋 Listar Clientes", "🔍 Buscar Cliente"]
    )
    
    if pagina == "📝 Cadastrar Cliente":
        cadastrar_cliente_page()
    elif pagina == "📋 Listar Clientes":
        listar_clientes_page()
    elif pagina == "🔍 Buscar Cliente":
        buscar_cliente_page()

def cadastrar_cliente_page():
    st.header("📝 Cadastrar Novo Cliente")
    
    with st.form("cadastro_cliente"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome/Razão Social *", placeholder="Digite o nome completo ou razão social")
            contato = st.text_input("Contato *", placeholder="(11) 99999-9999")
            email = st.text_input("Email *", placeholder="exemplo@email.com")
            
        with col2:
            representante = st.text_input("Representante", placeholder="Nome do representante")
            pessoa = st.selectbox("Tipo de Pessoa *", ["fisica", "juridica"], help="Física = CPF, Jurídica = CNPJ")
            inscricao = st.text_input("CPF/CNPJ *", placeholder="000.000.000-00 ou 00.000.000/0000-00")
        
        # Validações
        erros = []
        
        if not nome:
            erros.append("Nome é obrigatório")
        
        if not contato:
            erros.append("Contato é obrigatório")
        
        if not email:
            erros.append("Email é obrigatório")
        elif not validar_email(email):
            erros.append("Email inválido")
        
        if not inscricao:
            erros.append("CPF/CNPJ é obrigatório")
        elif pessoa == "fisica" and not validar_cpf(inscricao):
            erros.append("CPF inválido")
        elif pessoa == "juridica" and not validar_cnpj(inscricao):
            erros.append("CNPJ inválido")
        
        # Verificar se CPF/CNPJ já existe
        if inscricao and not erros:
            inscricao_limpa = re.sub(r'[^0-9]', '', inscricao)
            existe, cliente_existente = verificar_inscricao_existe(inscricao_limpa)
            if existe:
                erros.append(f"CPF/CNPJ já cadastrado para: {cliente_existente['nome']} ({cliente_existente['email']})")
        
        # Exibir erros
        if erros:
            for erro in erros:
                st.error(erro)
        
        submitted = st.form_submit_button("Cadastrar Cliente", type="primary")
        
        if submitted and not erros:
            dados = {
                "nome": nome,
                "contato": contato,
                "representante": representante if representante else None,
                "email": email,
                "inscricao": re.sub(r'[^0-9]', '', inscricao),  # Remove formatação
                "pessoa": pessoa
            }
            
            sucesso, mensagem = cadastrar_cliente(dados)
            
            if sucesso:
                st.success(mensagem)
                st.balloons()
            else:
                st.error(mensagem)

def listar_clientes_page():
    st.header("📋 Lista de Clientes")
    
    if st.button("🔄 Atualizar Lista"):
        st.rerun()
    
    clientes = buscar_clientes()
    
    if clientes:
        df = pd.DataFrame(clientes)
        
        # Formatar inscrição (CPF/CNPJ) para exibição
        def formatar_inscricao(row):
            inscricao = str(row['inscricao'])
            if row['pessoa'] == 'fisica' and len(inscricao) == 11:
                return f"{inscricao[:3]}.{inscricao[3:6]}.{inscricao[6:9]}-{inscricao[9:]}"
            elif row['pessoa'] == 'juridica' and len(inscricao) == 14:
                return f"{inscricao[:2]}.{inscricao[2:5]}.{inscricao[5:8]}/{inscricao[8:12]}-{inscricao[12:]}"
            return inscricao
        
        df['inscricao_formatada'] = df.apply(formatar_inscricao, axis=1)
        
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "nome": "Nome/Razão Social",
                "contato": "Contato",
                "representante": "Representante",
                "email": "Email",
                "inscricao_formatada": "CPF/CNPJ",
                "pessoa": "Tipo"
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.info(f"Total de clientes cadastrados: {len(clientes)}")
    else:
        st.info("Nenhum cliente cadastrado ainda.")

def buscar_cliente_page():
    st.header("🔍 Buscar Cliente")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        termo_busca = st.text_input("Digite o nome, email ou CPF/CNPJ:", placeholder="Digite para buscar...")
    
    with col2:
        if st.button("🔍 Buscar", type="primary"):
            if termo_busca:
                buscar_e_exibir_clientes(termo_busca)
            else:
                st.warning("Digite um termo para buscar.")

def buscar_e_exibir_clientes(termo):
    clientes = buscar_clientes()
    
    if clientes:
        # Filtrar clientes
        resultados = []
        termo_lower = termo.lower()
        
        for cliente in clientes:
            if (termo_lower in cliente.get('nome', '').lower() or
                termo_lower in cliente.get('email', '').lower() or
                termo_lower in str(cliente.get('inscricao', '')).lower()):
                resultados.append(cliente)
        
        if resultados:
            df = pd.DataFrame(resultados)
            
            # Formatar inscrição
            def formatar_inscricao(row):
                inscricao = str(row['inscricao'])
                if row['pessoa'] == 'fisica' and len(inscricao) == 11:
                    return f"{inscricao[:3]}.{inscricao[3:6]}.{inscricao[6:9]}-{inscricao[9:]}"
                elif row['pessoa'] == 'juridica' and len(inscricao) == 14:
                    return f"{inscricao[:2]}.{inscricao[2:5]}.{inscricao[5:8]}/{inscricao[8:12]}-{inscricao[12:]}"
                return inscricao
            
            df['inscricao_formatada'] = df.apply(formatar_inscricao, axis=1)
            
            st.success(f"Encontrados {len(resultados)} cliente(s)")
            st.dataframe(
                df,
                column_config={
                    "id": "ID",
                    "nome": "Nome/Razão Social",
                    "contato": "Contato",
                    "representante": "Representante",
                    "email": "Email",
                    "inscricao_formatada": "CPF/CNPJ",
                    "pessoa": "Tipo"
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("Nenhum cliente encontrado com esse termo.")
    else:
        st.info("Nenhum cliente cadastrado ainda.")

if __name__ == "__main__":
    main() 