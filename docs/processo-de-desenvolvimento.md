# Processo de Desenvolvimento — 365-Gym

- Tech Lead: João Filho
- Equipe Responsável: Equipe 01
- Vigente desde: 20 / 09 / 2026
- Atualizado em: 16 / 10 / 2026

Este documento define como o trabalho é quebrado, acompanhado e considerado
pronto. O conteúdo técnico do projeto está em `docs/documento-do-projeto.md`.

## 1. Ferramenta escolhida

**GitHub Issues + GitHub Projects (kanban) + Milestones**, no repositório
`Big-Space-Creative/365gym` e no quadro **365-Gym** da mesma organização
(projeto nº 8).

Por quê, em vez de Jira, Trello ou planilha: o trabalho já vive no GitHub, e a
issue fecha sozinha quando o pull request que a referencia é mesclado. Isso
elimina o ritual de atualizar o quadro à mão, que é onde todo acompanhamento
morre em equipe pequena. Cada commit, PR, revisão e decisão fica ligada ao
requisito que originou o trabalho, sem ferramenta intermediária.

Três camadas, cada uma respondendo a uma pergunta diferente:

| Camada | Responde | Granularidade |
| :--- | :--- | :--- |
| **Milestone** | Em que etapa do produto estamos | Semanas |
| **Project (kanban)** | O que está em andamento agora | Dias |
| **Issue** | Qual é a próxima unidade de trabalho | Horas a 2 dias |

**O repositório é público**, por contrato de desenvolvimento de código aberto
com a academia. Consequência prática: nada que esteja em issue, PR, commit,
print ou log pode conter dado real de aluno. Dados de teste são sempre fictícios.

## 2. Marcos (milestones)

A ordem não é sugestão: cada marco depende do anterior. O M1 antes do M0 força
refazer o user model; o M4 antes do M3 não tem aula sobre a qual fazer chamada.

| Marco | Nome | Entrega | Requisitos |
| :--- | :--- | :--- | :--- |
| **M0** | Fundação | Projeto Django rodando, custom user model, convenções de código, licença, lint e testes no CI | RNF-02, RNF-04, RNF-08, RNF-09 |
| **M1** | Autenticação e papéis | Os três papéis entram e enxergam apenas o que lhes cabe, sobre um layout base responsivo | RF-01, RF-02, RF-14, RNF-01, RNF-03 |
| **M2** | Cadastros do administrador | Alunos, professores, turmas e matrículas | RF-10, RF-11, RF-12 |
| **M3** | Agenda | Aluno vê sua semana; professor vê suas turmas e alunos | RF-03, RF-06 |
| **M4** | Presença | Chamada do professor e histórico de frequência do aluno | RF-07, RF-04 |
| **M5** | Evolução | Avaliações e observações — **bloqueado por PA-01** | RF-08, RF-09, RF-05 |
| **M6** | Relatórios | Frequência por turma e por período | RF-13 |
| **M7** | LGPD | Consentimento, aceite datado, exclusão lógica, anonimização, auditoria | LGPD-01 a LGPD-09 |
| **M8** | Produção | Deploy, HTTPS, backup, log de erros, provedor de e-mail real | RNF-05, RNF-06, RNF-07, RNF-10 |

**M7 não é uma etapa final.** Os requisitos de LGPD que afetam modelagem
(LGPD-01, LGPD-02, LGPD-03, LGPD-06) entram junto com o M2, quando as tabelas de
aluno nascem. O M7 agrupa o que sobra: telas, textos, rotinas e auditoria.

**O backlog é criado marco a marco.** As issues de um marco só são escritas
quando ele está perto de começar. Hoje existem as do M0, M1 e M2, mais uma do M8
que depende do cliente. Escrever 40 issues agora produziria 40 issues
desatualizadas na primeira semana.

## 3. Rótulos (labels)

Três famílias. Toda issue recebe um `tipo` e uma `área`. A prioridade não é
rótulo: é o campo **Priority** do quadro (seção 4).

**tipo** — `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
(os mesmos tipos do commit convencional, para não manter dois vocabulários)

**área** — `area:auth`, `area:turmas`, `area:presenca`, `area:avaliacao`,
`area:relatorios`, `area:lgpd`, `area:infra`, `area:ui`

**situação** — `bloqueado` (com o motivo no corpo da issue),
`aguarda-cliente` (depende de PA-01 a PA-05 ou de premissa não confirmada),
`boa-primeira-tarefa`

A label `aguarda-cliente` é a mais importante do conjunto: ela é a lista de
perguntas que precisam ser feitas na próxima conversa com a academia.

## 4. Quadro kanban

Colunas (campo **Status**), com a regra de entrada de cada uma:

| Coluna | Entra quando |
| :--- | :--- |
| **Backlog** | A issue existe e tem requisito associado |
| **Ready** | Critério de aceite escrito e nenhuma dependência aberta |
| **In progress** | Alguém assumiu e criou a branch. **Máximo 2 issues por pessoa** |
| **In review** | PR aberto, CI verde |
| **Done** | PR mesclado na branch principal |

O limite de 2 issues em progresso por pessoa existe para impedir cinco frentes
abertas e nenhuma entregue, que é o modo de falha mais comum em equipe pequena.

Outros campos do quadro:

- **Priority** — `P0` (trava outra pessoa ou está quebrado em produção), `P1`
  (escopo do MVP), `P2` (desejável, pode sair do MVP)
- **Size** — `XS`, `S`, `M`, `L`, `XL`, preenchido por quem vai fazer a issue ao
  puxá-la para Ready. `L` e `XL` significam quebrar em issues menores
- **Milestone** — o marco, campo nativo do GitHub; use-o para agrupar o quadro
  por etapa
- **Assignees** — um responsável por issue

## 5. Anatomia de uma issue

```markdown
## Requisito
RF-07 — Fazer a chamada de uma aula, marcando presença ou falta

## Contexto
Como professor, quero marcar presença ou falta de cada aluno de uma aula,
para acompanhar a frequência da turma.

## Critério de aceite
- [ ] Professor vê a lista de alunos matriculados na turma na data da aula
- [ ] Enviar a mesma chamada duas vezes deixa o banco no mesmo estado
- [ ] Professor de outra turma recebe 403 ao acessar esta chamada por URL direta
- [ ] A tela é usável em 360 px de largura

## Definição de pronto
- [ ] `ruff check .` e `ruff format --check .` sem erros
- [ ] `pytest` passando, cobertura do trecho novo >= 80%
- [ ] Regra de negócio em função de serviço, com teste que a chama sem HTTP
- [ ] Verificação de papel na view, não só no template
- [ ] Nenhum segredo, nenhum `print` ou log de depuração

## Dependências
Depende de #13 (decisão de modelagem das aulas)
```

O critério de aceite é escrito **antes** de começar. Issue sem critério de aceite
não sai do Backlog — é ali que se descobre que o requisito não estava entendido.

## 6. Branches, commits e PR

- Branch a partir de `main`: `feat/rf-07-chamada`, `fix/rf-04-taxa-frequencia`
- Commits no formato convencional: `feat: registrar presença na chamada da aula`
- PR sempre referencia a issue com `Closes #NN`, para o fechamento automático
- **Todo PR recebe ao menos 1 aprovação de outro dev**, inclusive os do Tech Lead
- `main` protegida: merge só com CI verde e aprovação. Sem exceção — é o RNF-08.
  A proteção só pode ser ligada depois que a CI existir (issue #6) e o `ruff`
  estiver limpo na `main`; até lá a regra vale por combinação

## 7. Definição de pronto

Uma issue só vai para Done quando **todos** forem verdade:

- [ ] Todos os critérios de aceite da issue marcados
- [ ] `ruff` sem erros e `pytest` passando
- [ ] Cobertura de testes do código novo >= 80%
- [ ] Autorização por papel verificada na view e testada (RNF-03)
- [ ] Nenhum segredo fora de variável de ambiente (RNF-04)
- [ ] Testado em 360 px de largura, se houver tela (RNF-07)
- [ ] Nenhum dado pessoal novo coletado sem justificativa registrada (LGPD-01)
- [ ] Nenhum dado real de aluno em código, teste, fixture, print ou log

## 8. Divisão do trabalho entre os devs

Três devs, divididos por **fatia vertical**, não por camada. Neste projeto o
front é renderizado pelo Django com HTMX, então tela e view andam juntas: cada
issue entrega model, regra de negócio, view, template e teste, e tem um dono.

| Dev | Fatia | Issues hoje |
| :--- | :--- | :--- |
| **João** (Tech Lead) | Fundação e núcleo de segurança | #9, #8, #10, #11, #3, #1 |
| **Enzo** | Entrada e interface | #6, #12, #5, #2, #4 |
| **Davi** | Domínio de turmas | #13, #14 |

Regras para três pessoas trabalharem em paralelo sem se atropelar:

- **Um app Django, um dono por vez.** O conflito mais chato é migração: dois devs
  criam `0002_...` no mesmo app e o histórico quebra. A divisão por área (`area:*`)
  segue a divisão por app
- **Arquivos compartilhados são pontos quentes:** `settings.py`, o `urls.py` raiz
  e o `base.html`. Mudança neles é pequena, sai em PR próprio e é revisada rápido
- **Respeitar as dependências:** o Davi só inicia o modelo de Turma (#14) depois
  que a decisão de modelagem (#13) estiver aceita. Ninguém pega issue
  `aguarda-cliente`
- **O Tech Lead também desenvolve.** Por isso a revisão de PR é obrigatória em
  todas as direções: os PRs dele também são aprovados por outro dev

## 9. Ritmo

O ritmo é o que a semana permite, não um sprint fixo que gera dívida de culpa
quando não fecha. O que é fixo:

- **Uma revisão de quadro por semana:** o que saiu de In progress, o que travou,
  o que virou `aguarda-cliente`
- **Nada fica em In progress por mais de uma semana** sem ser quebrado em issues
  menores ou movido de volta com o motivo escrito
- **Perguntas ao cliente são acumuladas e enviadas em lote**, a partir das issues
  com `aguarda-cliente` — evita cinco mensagens soltas no WhatsApp da academia

## 10. Operação no dia a dia

Criar a issue e pô-la no quadro (substitua `N` pelo número da issue criada):

```bash
gh issue create --repo Big-Space-Creative/365gym \
  --title "..." --body-file corpo.md \
  --milestone "M2 - Cadastros do administrador" --label feat --label area:turmas

gh project item-add 8 --owner Big-Space-Creative \
  --url https://github.com/Big-Space-Creative/365gym/issues/N
```

Depois, no quadro, preencha **Status**, **Priority** e **Size**.

**Atenção no Windows:** texto acentuado ou com aspas duplas passado direto na
linha de comando já corrompeu issues deste projeto. Prefira a interface web ou
`--body-file` com um arquivo salvo em UTF-8.

## 11. Backlog atual

Retrato de 16 / 10 / 2026. A fonte da verdade é o quadro; esta tabela serve para
leitura sem sair do repositório.

A numeração **não segue a ordem de execução**: as issues mudaram de número quando
o repositório foi transferido para a organização. A ordem está nos marcos e no
quadro.

| # | Marco | Issue | Dono | Prioridade |
| :-- | :-- | :--- | :--- | :--- |
| 9 | M0 | Esqueleto do projeto Django com configuração por ambiente | João | P0 |
| 8 | M0 | Custom user model com papel e login por e-mail | João | P0 |
| 10 | M0 | Convenções de código e ADR de arquitetura da aplicação | João | P0 |
| 11 | M0 | Definir e aplicar a licença open source (PA-03) | João | P1 |
| 6 | M0 | CI no GitHub Actions, proteção da `main` e modelos de PR e issue | Enzo | P0 |
| 3 | M1 | Mecanismo reutilizável de autorização por papel (RNF-03) | João | P0 |
| 12 | M1 | Layout base responsivo e navegação por papel | Enzo | P1 |
| 5 | M1 | Login e logout por e-mail e senha (RF-01) | Enzo | P1 |
| 2 | M1 | Edição dos próprios dados e troca de senha (RF-02) | Enzo | P1 |
| 4 | M1 | Recuperação de senha por e-mail (RF-01) | Enzo | P1 |
| 13 | M2 | Decisão de modelagem: aulas materializadas ou calculadas | Davi | P1 |
| 14 | M2 | Turma com professor, capacidade e horários semanais (RF-11) | Davi | P1 |
| 1 | M2 | Perfis de Aluno e Professor com exclusão lógica (RF-10, LGPD) | João | P1 |
| 15 | M2 | Responsável legal e consentimento de menor (LGPD-03) — `aguarda-cliente` | — | P1 |
| 16 | M2 | Cadastro de alunos e professores pelo administrador (RF-10) | — | P1 |
| 17 | M8 | Provedor de e-mail real em produção (PA-05) — `aguarda-cliente` | — | P2 |

A issue #7 (configuração por ambiente) foi absorvida pela #9 e está fechada.

Ordem de execução dentro do que já está escrito:

1. **M0 é sequencial para o João:** #9 → #8. A #10 e a #11 podem andar em paralelo.
2. **A CI (#6) pode começar já**, mas só vira check obrigatório depois que o
   `ruff` estiver limpo na `main` (parte da #9).
3. **A #13 (decisão de aulas, Davi) não depende de nada e pode começar já.**
   Depois da #8, abrem em paralelo a #3 (João) e a #12 (Enzo).
4. **A #5 (login) depende da #12 e da #8**, e a #2 depende da #5.
5. **A #14 (Turma) depende da decisão da #13.**
6. **A #15 e a #17 esperam o cliente** (PA-02 e PA-05); a #16 espera a #1, a #12
   e a #3.
