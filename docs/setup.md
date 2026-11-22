# Guia de Preparação do Ambiente de Desenvolvimento

Data de referência: 2026-09-20 (Atualizado: 2026-10-16)

Este guia contém o passo a passo completo para reproduzir e configurar o ambiente de desenvolvimento do projeto **365-Gym** a partir do zero em uma máquina limpa.

---

## 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- **Python 3.12 ou superior:** verifique com `python --version` (ou `python3 --version`).
- **Git:** para controle de versão local e remoto.
- **uv (opcional, recomendado):** gerenciador rápido de pacotes e ambientes Python.
- **PostgreSQL (opcional no desenvolvimento):** caso prefira utilizar o mesmo banco de dados de produção localmente, embora o SQLite seja suportado por padrão no desenvolvimento.

---

## 2. Clonar o Repositório

Se você ainda não clonou o repositório, faça o clone e acesse o diretório do projeto:

```bash
git clone https://github.com/Big-Space-Creative/365gym.git
cd 365gym
```

---

## 3. Criar e Ativar o Ambiente Virtual

No diretório raiz do projeto:

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(Se o PowerShell bloquear a execução de scripts, execute previamente no terminal: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*

> **Nota sobre o nome do ambiente (`.venv` vs `venv`):**
> O padrão recomendado no projeto é `.venv`, mas você também pode utilizar `venv` sem o ponto (`python -m venv venv` e `.\venv\Scripts\Activate.ps1`). Ambos são ignorados pelo Git (`.gitignore`) e pelo formatador/linter Ruff (`pyproject.toml`).

### Linux / macOS (Bash/Zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Instalar as Dependências

Com o ambiente virtual ativado, você pode instalar as dependências de desenvolvimento de duas formas:

### Opção A: Usando `uv` (Recomendado)
```bash
uv pip install -r pyproject.toml --extra dev
```

### Opção B: Usando `pip` padrão
```bash
pip install --upgrade pip
pip install "django>=5.0,<6.0" django-environ "psycopg[binary]>=3.1" ruff pytest pytest-django pytest-cov
```

---

## 5. Configurar as Variáveis de Ambiente

Crie o arquivo local `.env` a partir do modelo `.env.example`:

### Windows (PowerShell)
```powershell
Copy-Item .env.example .env
```

### Linux / macOS
```bash
cp .env.example .env
```

### Gerando uma SECRET_KEY segura
Abra o terminal com o ambiente ativado e execute:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
Copie a chave gerada no console e preencha o valor de `SECRET_KEY` no seu `.env`.

> **Importante:** A aplicação falha de forma explícita caso `SECRET_KEY` não seja fornecida no ambiente ou no `.env`.

---

## 6. Aplicar as Migrações e Iniciar o Servidor

O esqueleto inicial do projeto e o Custom User Model (`accounts.User`) já estão configurados e com as migrações criadas. Para inicializar o banco de dados e o servidor:

1. **Aplique as migrações no banco de dados:**
   ```bash
   python manage.py migrate
   ```

2. **(Opcional) Crie um superusuário para acessar o painel administrativo:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

4. **Verifique no navegador:**
   - Página inicial: `http://127.0.0.1:8000/` (retorna HTTP 200 com a tela de boas-vindas do Django em modo `DEBUG=True`)
   - Painel de administração: `http://127.0.0.1:8000/admin/login/` (retorna HTTP 200 com o formulário de login)

---

## 7. Comandos do Dia a Dia

### Verificação e formatação de código (Ruff)
```bash
# Verificar problemas de linting e boas práticas
ruff check .

# Corrigir problemas automáticos
ruff check --fix .

# Formatar o código
ruff format .

# Verificar se a formatação está em conformidade
ruff format --check .
```

### Execução de testes automatizados (Pytest)
```bash
# Executar a suíte de testes
pytest

# Executar com relatório de cobertura de código
pytest --cov=apps
```

---

## 8. Banco de Dados: Desenvolvimento vs. Produção

- **Desenvolvimento (padrão):** a variável `DATABASE_URL` no `.env` aponta para `sqlite:///db.sqlite3`. Não requer nenhum serviço externo ou banco PostgreSQL instalado.
- **Produção / PostgreSQL local:** configure `DATABASE_URL` para uma conexão PostgreSQL válida:
  ```env
  DATABASE_URL=postgres://usuario:senha@localhost:5432/gym365
  ```
  O Django utiliza o `django-environ` e o driver `psycopg` (v3) automaticamente a partir dessa URL, sem necessidade de alterar nenhuma linha de código.
