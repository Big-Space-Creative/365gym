# Visão do Produto — 365-Gym

Data de referência: 2026-09-20

## 1. Problema

A 365 Boxe Gym é uma academia dedicada exclusivamente ao boxe, situada no Cariri (CE). A operação diária de controle de horários, chamadas de turmas e acompanhamento dos alunos é realizada de forma manual ou descentralizada (papel e WhatsApp).

A plataforma web 365-Gym tem como objetivo digitalizar e centralizar essa rotina operacional:
- Permitir que o aluno visualize seus horários e acompanhe sua evolução técnica e física.
- Permitir que o professor registre turmas, chamadas e o desempenho de cada aluno com facilidade.
- Permitir que o administrador gerencie turmas, matrículas e relatórios gerais.

## 2. Usuários e Papéis

A plataforma atende a três papéis de usuário:

- **Aluno:** consulta horários das turmas em que está matriculado, confirma presença, acompanha seu histórico e taxa de frequência, e visualiza avaliações e observações feitas pelo professor.
- **Professor:** gerencia suas turmas, realiza a chamada das aulas (marcando presença ou falta), registra a evolução técnica e física dos alunos e insere observações individuais.
- **Administrador:** cadastra, edita e inativa alunos e professores; cadastra turmas com horários semanais, capacidades e professores responsáveis; gerencia matrículas e desmatrículas; e visualiza relatórios de frequência da academia.

## 3. Escopo do MVP

O Produto Mínimo Viável (MVP) contempla:

- **Autenticação:** login com e-mail e senha, controle de acesso por papel e recuperação de senha por e-mail.
- **Agenda de Turmas:** visualização de horários semanais e gestão de turmas.
- **Controle de Presença:** realização de chamadas pelos professores e acompanhamento da frequência pelos alunos e administradores.
- **Acompanhamento de Evolução:** registro e consulta de avaliações e observações técnicas/físicas dos alunos.

## 4. Fora de Escopo do MVP

Ficam explicitamente fora do escopo do MVP:

- Controle de pagamentos, cobranças, mensalidades e financeiro (a academia continua cobrando por fora).
- Loja virtual ou comércio de produtos e equipamentos.
- Aplicativo mobile nativo (iOS / Android).
- Notificações push.

## 5. Evolução Futura

Um aplicativo mobile nativo é provável no futuro da plataforma. A arquitetura e a stack tecnológica foram definidas de modo a manter a lógica de negócio desacoplada, garantindo que o caminho para expor uma API REST ao aplicativo móvel permaneça aberto sem necessidade de reescrita da aplicação.
