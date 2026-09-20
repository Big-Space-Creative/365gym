# Requisitos — 365-Gym

Data de referência: 2026-09-20

## 1. Premissas não confirmadas

Aviso: As premissas abaixo foram assumidas e ainda não confirmadas pelo dono do projeto. Se alguma premissa for negada, os requisitos funcionais correspondentes mudam e devem ser reescritos antes do desenvolvimento.

- [ ] Controle de mensalidade e pagamento fica FORA do MVP (a academia continua cobrando por fora)
- [ ] Check-in de presença é feito pelo professor na chamada, não pelo aluno no portão
- [ ] O cadastro de alunos é feito pelo administrador; não há auto-cadastro público
- [ ] A plataforma não armazena dados de saúde (lesões, condições médicas, atestados) no MVP
- [ ] Um aluno pertence a uma ou mais turmas com horário fixo semanal

## 2. Requisitos funcionais

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

## 3. Requisitos não funcionais

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

## 4. LGPD

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

## 5. Perguntas abertas

- **PA-01:** Conteúdo exato da avaliação de evolução do RF-08 (campos e métricas a serem registrados).
- **PA-02:** Idade mínima dos alunos e como a academia coleta hoje o consentimento dos responsáveis para alunos menores de 18 anos.
- **PA-03:** Licença definitiva do projeto a ser formalizada com a academia.
- **PA-04:** Identificação de quem é o encarregado de dados (DPO) nos termos do LGPD-09.
- **PA-05:** Onde será realizado o deploy em produção (Render, Railway ou Fly.io) e qual provedor de e-mail transacional atenderá o RF-01.
