# Processo de Desenvolvimento — 365-Gym

- Tech Lead: João Filho
- Equipe Responsável: Equipe 01
- Vigente desde: 20 / 09 / 2026

Este documento define como o trabalho é quebrado, acompanhado e considerado
pronto. O conteúdo técnico do projeto está em `docs/documento-do-projeto.md`.

## 1. Ferramenta escolhida

**GitHub Issues + GitHub Projects (kanban) + Milestones**, tudo dentro do próprio
repositório.

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

## 2. Marcos (milestones)

A ordem não é sugestão: cada marco depende do anterior. O M1 antes do M0 força
refazer o user model; o M4 antes do M3 não tem aula sobre a qual fazer chamada.

| Marco | Nome | Entrega | Requisitos |
| :--- | :--- | :--- | :--- |
| **M0** | Fundação | Projeto Django rodando, custom user model, configuração por ambiente, lint e testes no CI | RNF-02, RNF-04, RNF-08 |
| **M1** | Autenticação e papéis | Os três papéis entram e enxergam apenas o que lhes cabe | RF-01, RF-02, RNF-01, RNF-03 |
| **M2** | Cadastros do administrador | Alunos, professores, turmas e matrículas | RF-10, RF-11, RF-12 |
| **M3** | Agenda | Aluno vê sua semana; professor vê suas turmas e alunos | RF-03, RF-06 |
| **M4** | Presença | Chamada do professor e histórico de frequência do aluno | RF-07, RF-04 |
| **M5** | Evolução | Avaliações e observações — **bloqueado por PA-01** | RF-08, RF-09, RF-05 |
| **M6** | Relatórios | Frequência por turma e por período | RF-13 |
| **M7** | LGPD | Consentimento, aceite datado, exclusão lógica, anonimização, auditoria | LGPD-01 a LGPD-09 |
| **M8** | Produção | Responsividade, deploy, HTTPS, backup, log de erros | RF-14, RNF-05, RNF-06, RNF-07, RNF-10 |

**M7 não é uma etapa final.** Os requisitos de LGPD que afetam modelagem
(LGPD-01, LGPD-02, LGPD-03, LGPD-06) entram junto com o M2, quando as tabelas de
aluno nascem. O M7 agrupa o que sobra: telas, textos, rotinas e auditoria.

## 3. Rótulos (labels)

Quatro famílias. Toda issue recebe um `tipo`, uma `área` e uma `prioridade`.

**tipo** — `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
(os mesmos tipos do commit convencional, para não manter dois vocabulários)

**área** — `area:auth`, `area:turmas`, `area:presenca`, `area:avaliacao`,
`area:relatorios`, `area:lgpd`, `area:infra`, `area:ui`

**prioridade** — `P0` (trava outra pessoa ou está quebrado em produção),
`P1` (escopo do MVP), `P2` (desejável, pode sair do MVP)

**situação** — `bloqueado` (com o motivo no corpo da issue),
`aguarda-cliente` (depende de PA-01 a PA-05 ou de premissa não confirmada),
`boa-primeira-tarefa`

A label `aguarda-cliente` é a mais importante do conjunto: ela é a lista de
perguntas que precisam ser feitas na próxima conversa com a academia.

## 4. Quadro kanban

Colunas, com a regra de entrada de cada uma:

| Coluna | Entra quando |
| :--- | :--- |
| **Backlog** | A issue existe e tem requisito associado |
| **Pronto para começar** | Critério de aceite escrito e nenhuma dependência aberta |
| **Em progresso** | Alguém assumiu e criou a branch. **Máximo 2 issues por pessoa** |
| **Em revisão** | PR aberto, CI verde |
| **Concluído** | PR mesclado na branch principal |

O limite de 2 issues em progresso por pessoa existe para impedir cinco frentes
abertas e nenhuma entregue — o modo de falha mais comum em projeto de uma pessoa
só.

Campos personalizados do Project: `Requisito` (texto, ex.: RF-07), `Marco`
(seleção M0 a M8), `Estimativa` (P / M / G, onde G significa quebrar em issues
menores).

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
Depende de #12 (geração de aulas)
```

O critério de aceite é escrito **antes** de começar. Issue sem critério de aceite
não sai do Backlog — é ali que se descobre que o requisito não estava entendido.

## 6. Branches, commits e PR

- Branch a partir de `main`: `feat/rf-07-chamada`, `fix/rf-04-taxa-frequencia`
- Commits no formato convencional: `feat: registrar presença na chamada da aula`
- PR sempre referencia a issue com `Closes #NN`, para o fechamento automático
- `main` protegida: merge só com CI verde. Sem exceção — é o RNF-08

## 7. Definição de pronto

Uma issue só vai para Concluído quando **todos** forem verdade:

- [ ] Todos os critérios de aceite da issue marcados
- [ ] `ruff` sem erros e `pytest` passando
- [ ] Cobertura de testes do código novo >= 80%
- [ ] Autorização por papel verificada na view e testada (RNF-03)
- [ ] Nenhum segredo fora de variável de ambiente (RNF-04)
- [ ] Testado em 360 px de largura, se houver tela (RNF-07)
- [ ] Nenhum dado pessoal novo coletado sem justificativa registrada (LGPD-01)

## 8. Ritmo

Projeto de um desenvolvedor aprendendo: o ritmo é o que a semana permite, não um
sprint fixo que gera dívida de culpa quando não fecha. O que é fixo:

- **Uma revisão de quadro por semana:** o que saiu de Em progresso, o que travou,
  o que virou `aguarda-cliente`
- **Nada fica em Em progresso por mais de uma semana** sem ser quebrado em issues
  menores ou movido de volta com o motivo escrito
- **Perguntas ao cliente são acumuladas e enviadas em lote**, a partir das issues
  com `aguarda-cliente` — evita cinco mensagens soltas no WhatsApp da academia

## 9. Como montar isso no GitHub

Os comandos abaixo são para o Tech Lead executar quando decidir publicar o
repositório. Exigem o `gh` autenticado (`gh auth login`).

```bash
# 1. Versionar o repositório local
git init
git add .
git commit -m "chore: estrutura, documentação e configuração iniciais"

# 2. Criar o repositório remoto (privado: projeto de cliente, licença indefinida)
gh repo create 365-Gym --private --source=. --remote=origin --push

# 3. Marcos
gh api repos/:owner/:repo/milestones -f title="M0 - Fundação"
gh api repos/:owner/:repo/milestones -f title="M1 - Autenticação e papéis"
gh api repos/:owner/:repo/milestones -f title="M2 - Cadastros do administrador"
gh api repos/:owner/:repo/milestones -f title="M3 - Agenda"
gh api repos/:owner/:repo/milestones -f title="M4 - Presença"
gh api repos/:owner/:repo/milestones -f title="M5 - Evolução"
gh api repos/:owner/:repo/milestones -f title="M6 - Relatórios"
gh api repos/:owner/:repo/milestones -f title="M7 - LGPD"
gh api repos/:owner/:repo/milestones -f title="M8 - Produção"

# 4. Rótulos de área e situação (os de tipo e prioridade seguem o mesmo padrão)
gh label create "area:auth" --color 1D76DB
gh label create "area:turmas" --color 1D76DB
gh label create "area:presenca" --color 1D76DB
gh label create "area:avaliacao" --color 1D76DB
gh label create "area:relatorios" --color 1D76DB
gh label create "area:lgpd" --color B60205
gh label create "area:infra" --color 5319E7
gh label create "area:ui" --color 0E8A16
gh label create "bloqueado" --color D93F0B
gh label create "aguarda-cliente" --color FBCA04
gh label create "P0" --color B60205
gh label create "P1" --color D93F0B
gh label create "P2" --color FEF2C0

# 5. Quadro kanban
gh project create --owner @me --title "365-Gym — MVP"
# Depois, no navegador: adicionar as colunas da seção 4 e os campos
# Requisito, Marco e Estimativa, e ligar o Project ao repositório.
```

## 10. Backlog inicial sugerido

Primeiras issues do M0 e do M1, na ordem de execução. As do M0 vêm do
`docs/setup.md` e precisam acontecer antes de qualquer código de funcionalidade.

| # | Marco | Issue | Rótulos |
| :-- | :-- | :--- | :--- |
| 1 | M0 | Criar projeto Django e estrutura de apps | `chore`, `area:infra`, `P0` |
| 2 | M0 | Custom user model com `AbstractUser` antes da primeira migração | `feat`, `area:auth`, `P0` |
| 3 | M0 | Configuração por ambiente com `django-environ` e `.env` | `chore`, `area:infra`, `P0` |
| 4 | M0 | CI no GitHub Actions: `ruff` e `pytest` obrigatórios no PR | `ci`, `area:infra`, `P0` |
| 5 | M1 | Login e logout por e-mail e senha (RF-01) | `feat`, `area:auth`, `P1` |
| 6 | M1 | Recuperação de senha por e-mail (RF-01) | `feat`, `area:auth`, `P1`, `aguarda-cliente` |
| 7 | M1 | Decorator ou mixin de autorização por papel (RNF-03) | `feat`, `area:auth`, `P0` |
| 8 | M1 | Edição dos próprios dados e troca de senha (RF-02) | `feat`, `area:auth`, `P1` |
| 9 | M2 | Modelagem de Aluno com exclusão lógica e responsável legal | `feat`, `area:lgpd`, `P0`, `aguarda-cliente` |

A issue 6 nasce com `aguarda-cliente` porque depende do provedor de e-mail
(PA-05); a 9, porque depende da regra de consentimento de menores (PA-02).
