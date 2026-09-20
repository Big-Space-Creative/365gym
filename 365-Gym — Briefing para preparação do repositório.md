# 365-Gym — Briefing para preparação do repositório

2026-09-20 · @Someone

## Instrução ao agente

Sua tarefa é preparar o repositório, a documentação e o ambiente de desenvolvimento do projeto 365-Gym. Você não vai construir a aplicação: quem programa é o dono do projeto, e o código de aplicação é o aprendizado dele.

**Você deve criar:**

- A árvore de pastas descrita na seção "Estrutura do repositório"
- Os arquivos de documentação (README, requisitos, ADR, visão, CONTRIBUTING se aplicável)
- Arquivos de configuração: `.gitignore`, `.env.example`, `pyproject.toml` ou `requirements/`, configuração do `ruff`, `pytest.ini` ou equivalente, `.editorconfig`
- Um `docs/setup.md` com o passo a passo de ambiente (virtualenv, instalação, banco, comandos)

**Você não deve criar, em nenhuma hipótese:**

- Código Python de aplicação: models, views, forms, urls, admin, serializers, middlewares, migrations
- Templates HTML de páginas, CSS de layout, JavaScript da aplicação
- Executar `django-admin startproject` ou `startapp` — documente os comandos no `docs/setup.md` para o dono rodar
- Qualquer regra de negócio, mesmo como exemplo ou stub comentado

Se você julgar que algum arquivo de código é indispensável, pare e pergunte antes de criar. Não decida sozinho.

## Contexto do produto

O 365-Gym é a plataforma web da 365 Boxe Gym, academia dedicada exclusivamente ao boxe, no Cariri (CE). O objetivo é tirar a operação do WhatsApp e do papel: o aluno enxerga seus horários e sua evolução; o professor registra e acompanha o desempenho de cada aluno.

Três papéis de usuário:

- **Aluno** — consulta horários das turmas, confirma presença, vê o próprio histórico e as avaliações do professor.
- **Professor** — gerencia turmas e chamadas, registra evolução técnica e física dos alunos, deixa observações.
- **Administrador** — cadastra alunos, professores, turmas e horários; gerencia matrículas e dados da academia.

Aplicativo mobile nativo é provável no futuro, mas está fora do MVP. A decisão de stack precisa deixar esse caminho aberto sem custo hoje.

## Escopo do MVP e premissas

O MVP entrega autenticação, agenda de turmas, presença e acompanhamento de evolução. Pagamentos, loja, app nativo e notificações push ficam fora.

As premissas abaixo foram assumidas e ainda não confirmadas pelo dono do projeto. Elas estão marcadas como tarefa: confirme antes de escrever qualquer requisito derivado delas.

- [ ] Controle de mensalidade e pagamento fica FORA do MVP (a academia continua cobrando por fora)
- [ ] Check-in de presença é feito pelo professor na chamada, não pelo aluno no portão
- [ ] O cadastro de alunos é feito pelo administrador; não há auto-cadastro público
- [ ] A plataforma não armazena dados de saúde (lesões, condições médicas, atestados) no MVP
- [ ] Um aluno pertence a uma ou mais turmas com horário fixo semanal

Se alguma premissa for negada, os requisitos funcionais correspondentes mudam e devem ser reescritos antes do desenvolvimento.

## Requisitos funcionais

Estes são os requisitos do MVP, agrupados por papel. Transcreva-os para `docs/requisitos.md` sem inventar novos: se faltar algo, registre como pergunta aberta no fim do arquivo.

| ID | Papel | Requisito |
| --- | --- | --- |
| RF-01 | Todos | Autenticar com e-mail e senha, com recuperação de senha por e-mail |
| RF-02 | Todos | Editar os próprios dados de contato e trocar a senha |
| RF-03 | Aluno | Ver a agenda semanal das turmas em que está matriculado |
| RF-04 | Aluno | Ver o próprio histórico de presenças e a taxa de frequência |
| RF-05 | Aluno | Ver as avaliações e observações lançadas pelo professor |
| RF-06 | Professor | Ver suas turmas e a lista de alunos de cada uma |
| RF-07 | Professor | Fazer a chamada de uma aula, marcando presença ou falta |
| RF-08 | Professor | Registrar avaliação de evolução de um aluno em uma data |
| RF-09 | Professor | Escrever observações por aluno, visíveis ao próprio aluno |
| RF-10 | Admin | Cadastrar, editar e inativar alunos e professores |
| RF-11 | Admin | Cadastrar turmas com horário semanal, professor e capacidade |
| RF-12 | Admin | Matricular e desmatricular alunos em turmas |
| RF-13 | Admin | Ver relatório de frequência por turma e por período |
| RF-14 | Todos | Acessar a plataforma pelo celular com layout responsivo |

O conteúdo exato da avaliação de evolução (RF-08) ainda não foi definido pelo dono do projeto. Registre como pergunta aberta, não invente campos.

## Requisitos não funcionais

| ID | Categoria | Requisito |
| --- | --- | --- |
| RNF-01 | Segurança | Senhas armazenadas com o hasher padrão do Django; nunca em texto claro ou hash próprio |
| RNF-02 | Segurança | Proteção CSRF ativa em todos os formulários; `DEBUG=False` e `ALLOWED_HOSTS` restrito em produção |
| RNF-03 | Segurança | Autorização por papel em toda view: aluno só acessa os próprios dados |
| RNF-04 | Segurança | Segredos apenas em variáveis de ambiente; `.env` no `.gitignore` |
| RNF-05 | Disponibilidade | Backup diário automático do banco em produção, com restauração testada |
| RNF-06 | Desempenho | Páginas principais respondem em até 2 s em conexão 4G comum |
| RNF-07 | Usabilidade | Interface em português do Brasil, responsiva, usável em telas a partir de 360 px |
| RNF-08 | Manutenção | `ruff` sem erros e testes passando antes de qualquer merge na branch principal |
| RNF-09 | Evolução | A lógica de negócio fica em camada reutilizável, para expor API REST ao app mobile depois sem reescrita |
| RNF-10 | Observabilidade | Log de erros em produção com rastreio de exceções |

### LGPD

A plataforma trata dados pessoais de alunos, incluindo menores de idade, o que exige base legal e consentimento específico. Estes requisitos vão em `docs/requisitos.md` e devem ser respeitados desde a modelagem.

| ID | Requisito |
| --- | --- |
| LGPD-01 | Coletar o mínimo necessário: nome, contato, data de nascimento e dados de treino; nada além disso sem justificativa registrada |
| LGPD-02 | Não armazenar dados de saúde no MVP; se for necessário depois, tratar como dado sensível com regra própria |
| LGPD-03 | Para aluno menor de 18 anos, registrar responsável legal e consentimento dele |
| LGPD-04 | Publicar política de privacidade e termo de uso, com aceite registrado com data |
| LGPD-05 | Permitir que o titular solicite correção e exclusão dos seus dados, com processo definido |
| LGPD-06 | Exclusão de aluno é lógica por padrão, com rotina de anonimização definida para exclusão definitiva |
| LGPD-07 | Registrar quem acessou ou alterou dados sensíveis de alunos (log de auditoria) |
| LGPD-08 | Tráfego sempre em HTTPS; banco de produção não acessível publicamente |
| LGPD-09 | Nomear o controlador dos dados (a academia) e o encarregado nos documentos públicos |

Registre em `docs/requisitos.md` uma pergunta aberta: qual a idade mínima dos alunos e como a academia coleta hoje o consentimento dos responsáveis.

## ADR 0001 — Stack do projeto

Copie esta seção para `docs/adr/0001-stack.md`, com status Aceita.

**Decisão:** backend em Django 5.x com Python 3.12+, front renderizado por templates do Django com HTMX, PostgreSQL em produção e SQLite em desenvolvimento.

**Contexto:** o dono do projeto é estudante, sabe HTML, CSS e JavaScript básico e React básico, e quer uma stack que seja ao mesmo tempo aprendizado e experiência de mercado. A prioridade declarada é entregar rápido algo funcionando para a academia. O produto é CRUD com papéis, agenda e registros — não é um sistema de alta concorrência.

**Alternativas consideradas:**

| Opção | Por que foi descartada |
| --- | --- |
| Python sem framework | Exigiria implementar sessão, hash de senha, CSRF e migrações à mão, com risco de falha de segurança em dados pessoais, e não corresponde ao que o mercado usa |
| FastAPI + SQLAlchemy + React | Ensina mais fundamentos e segue a tendência mais forte do ecossistema, mas exige montar autenticação, ORM e migrações, mais dois projetos para manter — conflita com a prioridade de entrega |
| Flask | Perdeu espaço para FastAPI e Django e não oferece vantagem clara aqui |

**Base de mercado:** Django e FastAPI são os dois frameworks Python relevantes hoje; no Stack Overflow Developer Survey 2025, o FastAPI teve alta de 5 pontos, uma das maiores variações entre frameworks web ([survey](https://survey.stackoverflow.co/2025/technology)). No Brasil, as vagas costumam pedir os dois em conjunto ("Django, Flask ou FastAPI"), então dominar um deles atende ao objetivo de mercado. A Django Developers Survey 2025 registra o crescimento de apps renderizados no servidor com templates Django e htmx ([resultados](https://lp.jetbrains.com/django-developer-survey-2025/)).

**Consequências positivas:** autenticação, permissões, ORM, migrações e proteções de segurança prontas; painel admin serve de back-office para a academia sem custo de desenvolvimento; um único deploy e uma única linguagem principal.

**Consequências negativas:** o Django abstrai muita coisa, então o aprendizado de fundamentos exige estudo deliberado do que acontece por baixo; o HTMX é menos citado em vagas que React; o app mobile futuro vai exigir uma camada de API adicional.

**Decisões adiadas:** a biblioteca de API para o app mobile (`django-ninja` ou Django REST Framework) será decidida quando o app entrar no escopo. Não crie nenhuma das duas agora.

**Ferramentas complementares:** `uv` ou `pip-tools` para dependências, `ruff` para lint e formatação, `pytest-django` para testes, `django-environ` para variáveis de ambiente, deploy inicial em Render, Railway ou Fly.io.

## Estrutura do repositório

Repositório `365-Gym`. Atenção: pacote Python não pode começar com número nem conter hífen, então o projeto Django interno se chamará `gym365` — mas quem roda `startproject` é o dono, não você. Crie apenas as pastas vazias com `.gitkeep` onde indicado.

```
365-Gym/
├── README.md
├── LICENSE                      # proprietária: ver observação abaixo
├── .gitignore                   # template Python + Django + .env + db.sqlite3
├── .editorconfig
├── .env.example                 # SECRET_KEY, DEBUG, DATABASE_URL, ALLOWED_HOSTS, EMAIL_*
├── pyproject.toml               # dependências e config do ruff
├── docs/
│   ├── visao.md                 # problema, usuários, escopo do MVP, fora de escopo
│   ├── requisitos.md            # RF, RNF, LGPD e perguntas abertas
│   ├── setup.md                 # ambiente do zero, incluindo os comandos startproject/startapp
│   ├── glossario.md             # turma, aula, chamada, matrícula, avaliação
│   └── adr/
│       ├── 0000-template.md
│       └── 0001-stack.md
├── apps/                        # .gitkeep — apps Django ficam aqui, criados pelo dono
├── templates/                   # .gitkeep
├── static/                      # .gitkeep
├── tests/                       # .gitkeep
└── .github/
    └── workflows/               # .gitkeep — CI entra depois, não crie agora
```

Sobre a licença: o projeto é de um cliente comercial, então não use MIT por hábito. Crie o `LICENSE` com um aviso de "todos os direitos reservados" e deixe uma nota no README de que a licença definitiva precisa ser confirmada com a academia.

O `docs/setup.md` deve conter, como texto para o dono executar e não como script rodado por você: criação do ambiente virtual, instalação das dependências, `django-admin startproject gym365 .`, criação do app inicial, configuração do `.env` a partir do `.env.example`, e o aviso de criar um custom user model herdando de `AbstractUser` antes da primeira migração — trocar isso depois, com dados no banco, é caro.

## Conteúdo base do README

Use este esqueleto, preenchendo o que já está definido neste briefing e deixando marcado o que ainda não está.

```markdown
# 365-Gym

Plataforma web da 365 Boxe Gym: agenda de turmas, controle de presença e
acompanhamento da evolução dos alunos.

## Status

Em preparação. Ambiente e documentação prontos; aplicação ainda não iniciada.

## Stack

- Python 3.12+ / Django 5.x
- Templates do Django + HTMX
- PostgreSQL (produção) / SQLite (desenvolvimento)
- ruff, pytest-django

Decisão registrada em `docs/adr/0001-stack.md`.

## Documentação

- `docs/visao.md` — o que é o produto e para quem
- `docs/requisitos.md` — requisitos funcionais, não funcionais e LGPD
- `docs/setup.md` — como preparar o ambiente
- `docs/adr/` — decisões de arquitetura

## Como rodar

Ver `docs/setup.md`.

## Licença

Todos os direitos reservados. Licença definitiva a confirmar com a academia.
```

Não adicione badges, seção de contribuição externa nem roadmap com datas: nada disso está definido.

## Critérios de aceite

A tarefa está concluída quando todos os itens abaixo forem verdadeiros.

- [ ] Todos os arquivos e pastas da seção "Estrutura do repositório" existem
- [ ] `docs/requisitos.md` contém os 14 requisitos funcionais, os 10 não funcionais e os 9 de LGPD deste briefing
- [ ] `docs/adr/0001-stack.md` contém a decisão com contexto, alternativas e consequências
- [ ] `docs/setup.md` descreve o ambiente do zero e inclui o aviso sobre o custom user model
- [ ] O repositório não contém nenhum arquivo `.py` de aplicação, nenhum template HTML de página e nenhuma migration
- [ ] `.env` não está versionado e `.env.example` não contém nenhum segredo real
- [ ] As premissas não confirmadas e as perguntas abertas estão listadas em `docs/requisitos.md`

Ao terminar, produza um relatório curto: arquivos criados, decisões que você precisou tomar por conta própria e perguntas que ficaram em aberto. Não comece a programar depois disso, mesmo que pareça o passo natural.
