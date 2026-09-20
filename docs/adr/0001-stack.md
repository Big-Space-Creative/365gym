# ADR 0001 — Stack do projeto

- **Data:** 2026-09-20
- **Status:** Aceita

## Decisão

Backend em Django 5.x com Python 3.12+, front renderizado por templates do Django com HTMX, PostgreSQL em produção e SQLite em desenvolvimento.

## Contexto

O dono do projeto é estudante, sabe HTML, CSS e JavaScript básico e React básico, e quer uma stack que seja ao mesmo tempo aprendizado e experiência de mercado. A prioridade declarada é entregar rápido algo funcionando para a academia. O produto é CRUD com papéis, agenda e registros — não é um sistema de alta concorrência.

## Alternativas consideradas

| Opção | Por que foi descartada |
| --- | --- |
| Python sem framework | Exigiria implementar sessão, hash de senha, CSRF e migrações à mão, com risco de falha de segurança em dados pessoais, e não corresponde ao que o mercado usa |
| FastAPI + SQLAlchemy + React | Ensina mais fundamentos e segue a tendência mais forte do ecossistema, mas exige montar autenticação, ORM e migrações, mais dois projetos para manter — conflita com a prioridade de entrega |
| Flask | Perdeu espaço para FastAPI e Django e não oferece vantagem clara aqui |

## Base de mercado

Django e FastAPI são os dois frameworks Python relevantes hoje; no Stack Overflow Developer Survey 2025, o FastAPI teve alta de 5 pontos, uma das maiores variações entre frameworks web ([survey](https://survey.stackoverflow.co/2025/technology)). No Brasil, as vagas costumam pedir os dois em conjunto ("Django, Flask ou FastAPI"), então dominar um deles atende ao objetivo de mercado. A Django Developers Survey 2025 registra o crescimento de apps renderizados no servidor com templates Django e htmx ([resultados](https://lp.jetbrains.com/django-developer-survey-2025/)).

## Consequências positivas

Autenticação, permissões, ORM, migrações e proteções de segurança prontas; painel admin serve de back-office para a academia sem custo de desenvolvimento; um único deploy e uma única linguagem principal.

## Consequências negativas

O Django abstrai muita coisa, então o aprendizado de fundamentos exige estudo deliberado do que acontece por baixo; o HTMX é menos citado em vagas que React; o app mobile futuro vai exigir uma camada de API adicional.

## Decisões adiadas

A biblioteca de API para o app mobile (`django-ninja` ou Django REST Framework) será decidida quando o app entrar no escopo. Nenhuma das duas bibliotecas faz parte do MVP e nenhuma deve ser adicionada ao projeto antes dessa decisão ser tomada.

## Ferramentas complementares

`uv` ou `pip-tools` para dependências, `ruff` para lint e formatação, `pytest-django` para testes, `django-environ` para variáveis de ambiente, deploy inicial em Render, Railway ou Fly.io.
