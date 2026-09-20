# Documento do Projeto — 365-Gym

- Cliente/Produto: 365 Gym (365 Boxe Gym — Cariri/CE)
- Data de início: 20 / 09 / 2026
- Tech Lead: João Filho
- Equipe Responsável: Equipe 01<br>

> Documento vivo. A fonte de verdade dos requisitos é `docs/requisitos.md` e a da
> stack é `docs/adr/0001-stack.md`. Quando divergirem, o erro está aqui e deve ser
> corrigido neste arquivo.

## 1. Stack Tecnológica

| Stack | Tecnologia |
| :---- | :------- |
| Linguagem principal | Python 3.12+ |
| Framework/Backend | Django 5.x (templates renderizados no servidor, camada de serviços desacoplada das views) |
| Frontend (se houver) | Templates do Django + HTMX; CSS próprio, responsivo a partir de 360 px. Sem SPA, sem build de JavaScript |
| Banco de dados | PostgreSQL 16 em produção; SQLite em desenvolvimento. Acesso via ORM do Django, conexão por `DATABASE_URL` (`django-environ`) |
| Infraestrutura/Deploy | Deploy único (monolito) em Render, Railway ou Fly.io — **provedor ainda não decidido (PA-05)**. Variáveis de ambiente via painel do provedor; backup diário do banco com restauração testada |
| Segurança | Autenticação nativa do Django com o hasher padrão; CSRF em todos os formulários; autorização por papel em toda view; segredos apenas em variáveis de ambiente; HTTPS obrigatório; log de auditoria para acesso e alteração de dados de alunos |

**Ferramentas de apoio:** `uv` (ou `pip`) para dependências, `ruff` para lint e
formatação, `pytest-django` para testes, `django-environ` para configuração.

**Fora da stack por decisão explícita:** nenhuma biblioteca de API REST
(`django-ninja` ou DRF) entra antes do app mobile ser escopado — ver
`docs/adr/0001-stack.md`.

## 2. Requisitos

### 2.1. Requisitos Funcionais

O que o sistema deve fazer. Os IDs são os mesmos de `docs/requisitos.md` — não
renumerar, para não quebrar a rastreabilidade com as issues.

| ID | Requisito | Descrição(Opcional) |
| :--: | :------- | :------ |
| RF-01 | Autenticação | Todos os papéis. Login com e-mail e senha, com recuperação de senha por e-mail |
| RF-02 | Edição dos próprios dados | Todos os papéis. Editar dados de contato e trocar a senha |
| RF-03 | Agenda semanal do aluno | Aluno. Ver a agenda das turmas em que está matriculado |
| RF-04 | Histórico de presenças | Aluno. Ver o próprio histórico e a taxa de frequência |
| RF-05 | Consulta de avaliações | Aluno. Ver as avaliações e observações lançadas pelo professor |
| RF-06 | Turmas do professor | Professor. Ver suas turmas e a lista de alunos de cada uma |
| RF-07 | Chamada de aula | Professor. Marcar presença ou falta de cada aluno em uma aula |
| RF-08 | Registro de evolução | Professor. Registrar avaliação de evolução de um aluno em uma data. **Campos não definidos (PA-01)** |
| RF-09 | Observações por aluno | Professor. Escrever observações visíveis ao próprio aluno |
| RF-10 | Gestão de pessoas | Admin. Cadastrar, editar e inativar alunos e professores |
| RF-11 | Gestão de turmas | Admin. Cadastrar turmas com horário semanal, professor e capacidade |
| RF-12 | Gestão de matrículas | Admin. Matricular e desmatricular alunos em turmas |
| RF-13 | Relatório de frequência | Admin. Frequência por turma e por período |
| RF-14 | Acesso mobile | Todos os papéis. Layout responsivo no celular |

### 2.2. Requisitos Não Funcionais

Desempenho, segurança, escalabilidade etc.

| ID | Requisito | Descrição(Opcional) |
| :--: | :------- | :------ |
| RNF-01 | Hash de senha padrão do Django | Segurança. Nunca texto claro, nunca hash próprio |
| RNF-02 | CSRF e configuração de produção | Segurança. CSRF ativo em todos os formulários; `DEBUG=False` e `ALLOWED_HOSTS` restrito em produção |
| RNF-03 | Autorização por papel | Segurança. Toda view verifica papel; aluno só acessa os próprios dados |
| RNF-04 | Segredos fora do código | Segurança. Apenas variáveis de ambiente; `.env` no `.gitignore` |
| RNF-05 | Backup diário | Disponibilidade. Backup automático do banco em produção, com restauração testada |
| RNF-06 | Tempo de resposta | Desempenho. Páginas principais em até 2 s em conexão 4G comum |
| RNF-07 | Interface pt-BR responsiva | Usabilidade. Usável em telas a partir de 360 px |
| RNF-08 | Qualidade antes do merge | Manutenção. `ruff` sem erros e testes passando antes de qualquer merge na branch principal |
| RNF-09 | Lógica em camada reutilizável | Evolução. Regra de negócio fora das views, para expor API REST ao app mobile depois sem reescrita |
| RNF-10 | Log de erros em produção | Observabilidade. Rastreio de exceções |

### 2.3. Requisitos de LGPD

Extensão do formato padrão. O produto trata dados pessoais de alunos, incluindo
menores de idade, o que exige base legal e consentimento específico. Estes
requisitos valem desde a modelagem, não são uma etapa final.

| ID | Requisito | Descrição(Opcional) |
| :--: | :------- | :------ |
| LGPD-01 | Minimização de dados | Nome, contato, data de nascimento e dados de treino; nada além sem justificativa registrada |
| LGPD-02 | Sem dados de saúde no MVP | Se for necessário depois, tratar como dado sensível com regra própria |
| LGPD-03 | Consentimento de responsável | Aluno menor de 18 anos exige responsável legal registrado e consentimento dele |
| LGPD-04 | Política e termo com aceite | Publicar política de privacidade e termo de uso, com aceite registrado com data |
| LGPD-05 | Direito de correção e exclusão | Titular pode solicitar, com processo definido |
| LGPD-06 | Exclusão lógica e anonimização | Exclusão de aluno é lógica por padrão; rotina de anonimização para exclusão definitiva |
| LGPD-07 | Log de auditoria | Registrar quem acessou ou alterou dados sensíveis de alunos |
| LGPD-08 | HTTPS e banco fechado | Tráfego sempre em HTTPS; banco de produção não acessível publicamente |
| LGPD-09 | Controlador e encarregado nomeados | Nomear a academia como controladora e o encarregado nos documentos públicos |

### 2.4. Bloqueios e perguntas abertas

Nenhum destes deve ser respondido pela equipe por conta própria. Cada um bloqueia
o trabalho indicado.

| ID | Pergunta | Bloqueia |
| :--: | :------- | :------ |
| PA-01 | Quais campos compõem a avaliação de evolução | RF-08, RF-05 e a modelagem de Avaliação |
| PA-02 | Idade mínima dos alunos e como o consentimento do responsável é coletado hoje | LGPD-03 e o cadastro de aluno (RF-10) |
| PA-03 | Licença definitiva do projeto | Publicação do repositório |
| PA-04 | Quem é o encarregado de dados (DPO) | LGPD-09 e a política de privacidade |
| PA-05 | Provedor de deploy e provedor de e-mail transacional | RF-01 (recuperação de senha) e o marco de produção |

Além disso, cinco premissas do briefing seguem **não confirmadas** pelo cliente e
estão listadas em `docs/requisitos.md`. Se qualquer uma for negada, os requisitos
derivados mudam antes do desenvolvimento.

## 3. Funcionalidades Complexas

### 3.1

- **Funcionalidade:** Autenticação e autorização por papel
- **Descrição:** Login por e-mail e senha, recuperação por e-mail e controle de
  acesso dos três papéis (aluno, professor, administrador) em toda a aplicação.
- **Regras de negócio:** O e-mail é o identificador de login. Um usuário tem
  exatamente um papel. O aluno só enxerga dados vinculados a ele próprio; o
  professor só enxerga as turmas em que é o responsável; o administrador enxerga
  tudo. Usuário inativado não autentica, mas seus registros históricos
  permanecem. Não há auto-cadastro público — o administrador cria as contas
  (premissa ainda não confirmada).
- **Dependências:** `django.contrib.auth`; custom user model herdando de
  `AbstractUser` criado **antes da primeira migração**; provedor de e-mail
  transacional (PA-05).
- **Riscos técnicos conhecidos:** trocar o user model depois da primeira migração
  é caro e arriscado — é a decisão mais irreversível do projeto. Autorização
  aplicada só no template (esconder o botão) sem verificação na view é falha de
  segurança, não de layout. Links de recuperação de senha precisam de expiração
  curta e uso único.
- **Critério de aceite:** os três papéis autenticam; um aluno autenticado recebe
  403 ao tentar acessar por URL direta o histórico ou a avaliação de outro aluno;
  o fluxo de recuperação envia e-mail e invalida o link após o uso; existe teste
  automatizado de negação de acesso para cada papel.

### 3.2

- **Funcionalidade:** Turmas com horário recorrente e geração de aulas
- **Descrição:** A turma tem horário fixo semanal; as aulas são as ocorrências
  concretas desse horário no calendário, e é sobre a aula que a chamada acontece.
- **Regras de negócio:** Uma turma tem professor responsável, capacidade máxima e
  um ou mais horários semanais. Um aluno pode pertencer a mais de uma turma. A
  matrícula não pode ultrapassar a capacidade da turma. Alterar o horário de uma
  turma não pode reescrever as aulas já realizadas nem as chamadas já feitas.
- **Dependências:** RF-11 e RF-12 (cadastro de turmas e matrículas); definição de
  fuso horário da aplicação (America/Fortaleza).
- **Riscos técnicos conhecidos:** decidir entre materializar as aulas no banco ou
  calcular a agenda por regra de recorrência — materializar facilita a chamada e
  o histórico, calcular evita lixo no banco; a escolha errada aparece tarde.
  Feriados e semanas sem aula não estão especificados. Horário de verão não é
  problema no Ceará hoje, mas a modelagem não deve assumir isso para sempre.
- **Critério de aceite:** a agenda semanal do aluno (RF-03) e a lista de turmas do
  professor (RF-06) saem da mesma fonte de dados; alterar o horário de uma turma
  preserva integralmente o histórico anterior; matrícula acima da capacidade é
  recusada com mensagem clara.

### 3.3

- **Funcionalidade:** Chamada e cálculo de frequência
- **Descrição:** O professor marca presença ou falta de cada aluno matriculado em
  uma aula; disso derivam o histórico do aluno (RF-04) e o relatório do admin
  (RF-13).
- **Regras de negócio:** A chamada é feita pelo professor, não pelo aluno
  (premissa ainda não confirmada). Só entram na chamada os alunos matriculados na
  turma na data da aula. Refazer a chamada corrige os registros existentes, nunca
  duplica. Aula sem chamada registrada não conta como falta de ninguém. A taxa de
  frequência é presenças sobre aulas realizadas no período, e não sobre aulas
  previstas.
- **Dependências:** 3.2 (aulas existirem); RF-12 (matrículas com data).
- **Riscos técnicos conhecidos:** idempotência — duplo clique ou reenvio do
  formulário não pode gerar dois registros para o mesmo aluno na mesma aula;
  aluno matriculado ou desmatriculado no meio do mês distorce a taxa se a
  matrícula não tiver data; a tela de chamada e o relatório são candidatos
  naturais a N+1 queries.
- **Critério de aceite:** enviar a mesma chamada duas vezes deixa o banco no
  mesmo estado; a taxa de frequência de um aluno matriculado no meio do período
  considera apenas as aulas a partir da matrícula; a tela de chamada de uma turma
  cheia responde em até 2 s e é usável em tela de 360 px.

### 3.4

- **Funcionalidade:** Avaliação de evolução e observações
- **Descrição:** Registro periódico, feito pelo professor, da evolução técnica e
  física do aluno, mais observações em texto visíveis ao próprio aluno.
- **Regras de negócio:** **BLOQUEADA POR PA-01** — os campos que compõem a
  avaliação não foram definidos pelo cliente e não devem ser inventados. O que já
  está definido: a avaliação pertence a um aluno numa data, é escrita pelo
  professor e é visível ao aluno avaliado; a observação escrita pelo professor é
  visível ao aluno, portanto não é um campo de anotação privada.
- **Dependências:** PA-01 respondida; 3.1 (visibilidade por papel); LGPD-02
  (nenhum campo pode ser dado de saúde).
- **Riscos técnicos conhecidos:** modelar os campos antes da resposta gera
  migração de dados depois. O risco de LGPD é concreto: descrições livres de
  lesão, dor ou condição física transformam o campo em dado sensível, que o MVP
  não está preparado para tratar.
- **Critério de aceite:** não começar enquanto PA-01 estiver aberta. Depois de
  respondida: o aluno vê suas avaliações e observações e não vê as de outro
  aluno; nenhum campo coletado é dado de saúde; existe teste de visibilidade.

### 3.5

- **Funcionalidade:** Conformidade com a LGPD — consentimento, exclusão e auditoria
- **Descrição:** Conjunto de mecanismos transversais: consentimento do responsável
  por menor, aceite datado da política, exclusão lógica com anonimização e log de
  auditoria.
- **Regras de negócio:** Aluno menor de 18 anos exige responsável legal
  registrado e consentimento dele antes do uso da plataforma. O aceite da política
  e do termo é registrado com data e versão do documento. Exclusão de aluno é
  lógica por padrão; a exclusão definitiva anonimiza os dados pessoais e preserva
  os registros agregados de frequência. Todo acesso ou alteração a dados de aluno
  por outro usuário é registrado em log de auditoria.
- **Dependências:** PA-02 e PA-04 respondidas; LGPD-04 exige os textos jurídicos,
  que não são produzidos pela equipe de desenvolvimento.
- **Riscos técnicos conhecidos:** exclusão lógica mal feita vaza dados em
  relatórios e listagens que esquecem de filtrar o registro inativo. Log de
  auditoria cresce rápido e, se guardar o conteúdo acessado, vira um segundo
  banco de dados pessoais a proteger — deve registrar quem, quando, o quê e qual
  ação, não o conteúdo. A idade vira maioridade durante a vida do cadastro: o
  vínculo com o responsável precisa de regra de transição.
- **Critério de aceite:** aluno excluído logicamente não aparece em nenhuma
  listagem, relatório ou busca; a rotina de anonimização roda e o histórico
  agregado da turma continua correto; o log registra quem acessou dados de qual
  aluno, quando e em qual ação; cadastro de menor sem consentimento registrado é
  recusado.

### 3.6

- **Funcionalidade:** Relatório de frequência por turma e período
- **Descrição:** Visão do administrador com a frequência consolidada por turma
  dentro de um intervalo de datas.
- **Regras de negócio:** O período é escolhido pelo administrador. O relatório
  considera apenas aulas realizadas com chamada registrada. Alunos inativados ou
  desmatriculados aparecem no período em que estiveram matriculados e somem
  depois. O número apresentado precisa bater com o que o aluno vê no próprio
  histórico (RF-04).
- **Dependências:** 3.3 (chamada); definição com o cliente do que conta como
  "aula realizada" quando não houve chamada.
- **Riscos técnicos conhecidos:** agregação sobre presenças é o ponto mais
  provável de consulta lenta e de N+1; divergência entre o número do relatório e
  o número do histórico do aluno destrói a confiança na plataforma inteira e
  costuma vir de regras de contagem duplicadas em dois lugares.
- **Critério de aceite:** a taxa de frequência é calculada por uma única função de
  domínio, usada tanto pelo relatório quanto pelo histórico do aluno, com teste
  que compara os dois; o relatório de um período de três meses responde em até
  2 s; há paginação ou limite explícito na listagem.

### 3.7

- **Funcionalidade:** Camada de serviços reutilizável (preparo para a API mobile)
- **Descrição:** Manter a regra de negócio fora das views, em funções de domínio
  chamáveis por qualquer interface, para que o app mobile futuro exponha uma API
  sem reescrever a lógica (RNF-09).
- **Regras de negócio:** Nenhuma regra de negócio dentro de view, template ou
  formulário. As views orquestram: recebem entrada validada, chamam o serviço e
  renderizam o resultado. Toda operação que altera dados passa por uma função de
  serviço, e é essa função que verifica a permissão de domínio.
- **Dependências:** transversal a todas as funcionalidades acima; nenhuma
  biblioteca de API entra agora.
- **Riscos técnicos conhecidos:** é a regra mais fácil de quebrar sob pressa, e a
  quebra só cobra o preço quando o app mobile entrar — tarde demais para ser
  barata. O oposto também é risco: criar camadas e abstrações especulativas antes
  da necessidade real contraria o YAGNI e atrasa a entrega.
- **Critério de aceite:** para cada funcionalidade entregue, existe ao menos um
  teste que exercita a regra de negócio chamando a função de serviço direto, sem
  passar por HTTP; nenhuma view contém cálculo de frequência, regra de capacidade
  ou regra de visibilidade.

## 4. Rastreabilidade

Cada requisito funcional vira uma ou mais issues no GitHub, e cada issue nomeia o
ID do requisito que atende. O processo de acompanhamento, os marcos, os rótulos e
a definição de pronto estão em `docs/processo-de-desenvolvimento.md`.
