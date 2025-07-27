# Touché - Cadastro de Clientes

Aplicação Streamlit para cadastro e gerenciamento de clientes da Touché.

## 🚀 Funcionalidades

- ✅ Cadastro de clientes com validação de dados
- ✅ Listagem de todos os clientes cadastrados
- ✅ Busca de clientes por nome, email, CPF ou CNPJ
- ✅ Validação de CPF e CNPJ
- ✅ Validação de email
- ✅ Interface moderna e responsiva

## 📋 Campos do Cadastro

- **Nome/Razão Social** (obrigatório)
- **Contato** (obrigatório)
- **Empresa** (opcional)
- **Representante** (opcional)
- **Email** (obrigatório)
- **CPF** (opcional - se CNPJ não for preenchido)
- **CNPJ** (opcional - se CPF não for preenchido)

## 🛠️ Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Supabase

1. Crie uma conta no [Supabase](https://supabase.com)
2. Crie um novo projeto
3. Vá em Settings > API para obter suas credenciais
4. Crie um arquivo `.env` na raiz do projeto com:

```
SUPABASE_URL=sua_url_do_supabase
SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
```

### 3. Criar tabela no Supabase

Execute o seguinte SQL no Editor SQL do Supabase:

```sql
CREATE TABLE clientes (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    contato TEXT NOT NULL,
    empresa TEXT,
    representante TEXT,
    email TEXT NOT NULL,
    cpf TEXT,
    cnpj TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX idx_clientes_nome ON clientes(nome);
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_clientes_cpf ON clientes(cpf);
CREATE INDEX idx_clientes_cnpj ON clientes(cnpj);
```

### 4. Executar a aplicação

```bash
streamlit run app.py
```

## 🌐 Hospedagem Gratuita

### Streamlit Cloud (Recomendado)

1. Faça push do código para um repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta GitHub
4. Selecione o repositório e configure as variáveis de ambiente
5. Deploy automático!

### Railway

1. Crie uma conta no [Railway](https://railway.app)
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente
4. Deploy automático!

## 📱 Como usar

1. **Cadastrar Cliente**: Preencha os campos obrigatórios e opcionais
2. **Listar Clientes**: Visualize todos os clientes cadastrados
3. **Buscar Cliente**: Encontre clientes específicos por nome, email, CPF ou CNPJ

## 🔒 Validações

- CPF e CNPJ são validados automaticamente
- Email deve ter formato válido
- Pelo menos CPF ou CNPJ deve ser preenchido
- Nome, contato e email são obrigatórios

## 🎨 Interface

- Design moderno e responsivo
- Navegação intuitiva
- Feedback visual para ações
- Tabelas organizadas e legíveis

## 📊 Tecnologias

- **Streamlit**: Interface web
- **Supabase**: Banco de dados PostgreSQL
- **Pandas**: Manipulação de dados
- **Python**: Linguagem principal

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.
