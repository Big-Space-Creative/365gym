# Guia de Preparação do Ambiente de Desenvolvimento

Data de referência: 2026-09-20

Este guia contém o passo a passo completo para configurar o ambiente de desenvolvimento do projeto 365-Gym a partir do zero.

---

## 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- **Python 3.12 ou superior:** verifique com `python --version` (ou `python3 --version`).
- **Git:** para controle de versão local e remoto.
- **uv (opcional, recomendado):** gerenciador rápido de pacotes e ambientes Python.
- **PostgreSQL (opcional no desenvolvimento):** para testar localmente com o mesmo banco de produção, caso prefira não usar SQLite no dia a dia.

---

## 2. Criar e Ativar o Ambiente Virtual

No diretório raiz do projeto (`gym365`):

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(Se o PowerShell bloquear a execução de scripts, execute previamente `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*

### Linux / macOS (Bash/Zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instalar as Dependências

Com o ambiente virtual ativado, você pode instalar as dependências de duas formas:

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

## 4. Configurar as Variáveis de Ambiente

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
Copie a chave gerada e substitua o valor de `SECRET_KEY` no seu `.env`.

---

## 5. Inicializar o Projeto Django

Execute o comando para criar a estrutura base do projeto na raiz:

```bash
django-admin startproject gym365 .
```

> **Por que o pacote se chama `gym365` e não `365-Gym`?**
> Em Python, identificadores de módulos e pacotes não podem começar com números nem conter hifens (`-`). Por isso, o repositório é `365-Gym` (ou diretório `gym365`), mas o pacote Python interno do Django é nomeado `gym365`.

---

## 6. Criar os Apps Django dentro da pasta `apps/`

Para manter a raiz organizada, todos os apps da aplicação devem residir no diretório `apps/`.

Exemplo de criação do app `accounts` (ou app inicial correspondente):

### Windows (PowerShell)
```powershell
New-Item -ItemType Directory -Path apps\accounts
python manage.py startapp accounts apps\accounts
```

### Linux / macOS
```bash
mkdir -p apps/accounts
python manage.py startapp accounts apps/accounts
```

> **Ajuste obrigatório no `apps.py`:**
> Após criar um app dentro de `apps/<nome_do_app>`, edite o arquivo `apps/<nome_do_app>/apps.py` e altere o atributo `name` para incluir o prefixo do pacote:
>
> ```python
> class AccountsConfig(AppConfig):
>     default_auto_field = "django.db.models.BigAutoField"
>     name = "apps.accounts"
> ```
> Em seguida, registre `'apps.accounts'` no `INSTALLED_APPS` em `gym365/settings.py`.

---

## 7. AVISO CRÍTICO: Custom User Model antes da primeira migração

> **ATENÇÃO: LEIA ANTES DE EXECUTAR QUALQUER MIGRAÇÃO**
>
> O Django recomenda fortemente configurar um Custom User Model logo no início do projeto, **antes de rodar a primeira migração (`migrate`)**.
>
> Trocar o modelo de usuário depois que a tabela `auth_user` já foi criada e populada é um processo de refatoração complexo e propenso a inconsistências no banco de dados.
>
> **Como proceder antes de rodar `python manage.py migrate`:**
> 1. No app de usuários (ex.: `apps/accounts/models.py`), crie o modelo herdando de `AbstractUser`:
>    ```python
>    from django.contrib.auth.models import AbstractUser
>
>    class User(AbstractUser):
>        # Adicione campos customizados se necessário futuramente
>        pass
>    ```
> 2. No arquivo `gym365/settings.py`, configure:
>    ```python
>    AUTH_USER_MODEL = "accounts.User"
>    ```
> 3. Crie a migração inicial do app:
>    ```bash
>    python manage.py makemigrations accounts
>    ```

---

## 8. Primeira Migração, Superusuário e Servidor de Desenvolvimento

Após configurar o `AUTH_USER_MODEL` e o `INSTALLED_APPS`:

1. Aplique as migrações no banco de dados:
   ```bash
   python manage.py migrate
   ```

2. Crie um superusuário para acessar o painel administrativo:
   ```bash
   python manage.py createsuperuser
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
   Acesse a aplicação em `http://127.0.0.1:8000/` e o admin em `http://127.0.0.1:8000/admin/`.

---

## 9. Comandos do Dia a Dia

### Verificação e formatação de código (Ruff)
```bash
# Verificar problemas de linting e boas práticas
ruff check .

# Corrigir problemas automáticos
ruff check --fix .

# Formatar o código
ruff format .
```

### Execução de testes automatizados (Pytest)
```bash
# Executar a suíte de testes
pytest

# Executar com relatório de cobertura de código
pytest --cov=apps
```

---

## 10. Banco de Dados: Desenvolvimento vs. Produção

- **Desenvolvimento:** por padrão, a variável `DATABASE_URL` no `.env` aponta para `sqlite:///db.sqlite3`. Não requer nenhum serviço externo em execução.
- **Produção:** configure `DATABASE_URL` para uma conexão PostgreSQL válida (ex.: `postgres://usuario:senha@host:5432/nome_banco`). O pacote `django-environ` lê a URL e configura o Django automaticamente, utilizando o driver `psycopg` (v3).
