# **Projeto central (bootcamp)**

## **AgentForge — Um agentic assistant modular para automatizar tarefas de suporte a produto**

### **Descrição curta**

Um sistema multi-agente orquestrado que aceita solicitações de usuário (via API/CLI), identifica sub-tarefas, consulta memória e conhecimento (RAG moderno), chama ferramentas externas (APIs, comandos, DB), coordena agentes (planner, worker, verifier), registra telemetria e gera explicações e avaliações automáticas das respostas.

### **Escopo**

Pequeno o bastante para terminar como MVP em semanas; abrangente o bastante para cobrir agentes, RAG, memória, function-calling, instrumentação, debugging, avaliações automáticas e integração com APIs externas.

---

# **Por que esse projeto é ideal**

* Toca todos os temas que você listou: agentic design, orchestration, tool-use, memory, RAG, function calling, pipeline dinâmico, logging/observability e avaliações.
* É prático: resolverá tarefas reais (ex.: “investigue este bug no crashlog”; “resuma este contrato”; “prepare email para reembolso de voo”).
* Força trade-offs comuns em produção (latência vs contexto, custo vs qualidade, consistência vs adaptabilidade).
* Evolui do simples ao sofisticado (single LLM → multi-agent async com state machines e rerankers).

---

# **Stack sugerida (modular)**

### **Linguagens / runtime**

* Python 3.11 (async)
* FastAPI para API

### **LLMs**

* OpenAI (gpt-4o/5 family)
* Anthropic (Claude 2/3)
* AWS Bedrock
* *→ via adaptador com strategy pattern*

### **Orquestração**

* Workflow engine leve (state machine em memória + persistência em DB)
  ou
* LangGraph / DSPy / Prefect / Temporal

### **Vector DB**

* FAISS (local, protótipo)
* Milvus / Pinecone / Chroma (produção)

### **Embeddings**

* OpenAI
* Modelos locais (opcional)

### **Observability**

* Structured logging (JSON)
* Traces (OpenTelemetry)
* Metrics (Prometheus/Grafana — opcional)

### **Testes**

* pytest + contract tests

### **Infra mínima**

* Docker
* PostgreSQL (state + metadata)
* Redis (fila/locks)
* S3-compatible para artefatos

### **CI/CD**

* GitHub Actions (lint + unit tests)

---

# **Entregáveis do bootcamp (MVP incremental)**

* Repo inicial com estrutura e scripts
* Adapter LLM unificado (pluggable)
* Simple agent (prompt → LLM → resposta)
* RAG pipeline (retrieval + condense + LLM)
* Multi-agent orchestration (planner + workers + verifier)
* Memory system (short-term, episodic, semantic)
* Tool integrations (HTTP, shell sandbox, DB)
* Observability (logs, traces, metrics)
* Auto-evaluator (rubric + self-critique loop)
* Demo (endpoint + UI/CLI + README)

---

# **Módulos do bootcamp (ordem progressiva)**

---

## **Módulo 0 — Preparação e priming do ambiente**

**Conceito:** preparar infra dev e ferramentas.
**Por que importa:** sem ambiente estável não há iteração rápida.
**Exemplo:** monorepo leve, Docker, providers mock.

**Exercício:** criar repo, virtualenv, Dockerfile, run script, README.
**Desafio:** GitHub Actions (lint + testes).

**Perguntas:**

1. Que variáveis de ambiente são necessárias para alternar entre provedores?
2. Por que usar Docker para prototipar agents?

---

## **Módulo 1 — Adapter unificado de LLMs (Provider Layer)**

**Conceito:** normalizar chamadas de diferentes LLMs.
**Importância:** fácil troca de provedores e fallback.

**Exemplo:** ProviderBase + OpenAIProvider + AnthropicProvider + BedrockProvider.

**Exercício:** implementar adapter mínimo + fallback.
**Desafio:** function-calling automático + parsing robusto.

**Perguntas:**

1. O que o adapter deve padronizar?
2. Como tratar rate-limit e erros transitórios?

---

## **Módulo 2 — RAG moderno: retrieval, compression & rewrite**

**Conceito:** recuperar, compactar e injetar contexto.
**Importância:** mais eficiência e menos custo.

**Exemplo:** retrieval → chunking → rerank → condense → use.

**Exercício:** indexar docs em FAISS; retriever + reranker.
**Desafio:** query rewriting + query expansion.

**Perguntas:**

1. Por que reescrever contexto antes do LLM?
2. Como medir qualidade do RAG?

---

## **Módulo 3 — Memory systems**

**Conceito:** camadas: working, episodic, semantic.
**Importância:** personalização, contexto, eficiência.

**Exemplo:** Redis (short-term), Postgres (episodic), vector DB (semantic).

**Exercício:** memória básica de conversas + salient facts.
**Desafio:** memory rewrite com permanence score.

**Perguntas:**

1. Quando mover memória para o vector store?
2. O que é “memory hallucination”?

---

## **Módulo 4 — Agents e patterns (ReAct, CoT, ToT)**

**Conceito:** padrões de raciocínio e ferramentas.
**Importância:** define como agentes agem no mundo.

**Exemplo:** ReAct, Tree-of-Thought, Reflexion.

**Exercício:** agent ReAct inspeccionando buglog.
**Desafio:** ToT planner com reranking.

**Perguntas:**

1. Quando ToT supera ReAct?
2. Como garantir idempotência de tool-calls?

---

## **Módulo 5 — Orquestração multi-agente**

**Conceito:** planner / dispatcher / worker / verifier + state machine.
**Importância:** paralelismo e resiliência.

**Exemplo:** subtarefas para retriever, API-tool, summarizer.

**Exercício:** planner com 2 subtarefas paralelas.
**Desafio:** retries, compensating actions, saga pattern.

**Perguntas:**

1. O que é uma saga?
2. Como lidar com timeouts sem corromper estado?

---

## **Módulo 6 — Function calling avançado**

**Conceito:** schemas, validação, segurança.
**Importância:** reduzir hallucinations, garantir integridade.

**Exercício:** JSON-schema para 3 ferramentas.
**Desafio:** permission system de ferramentas.

**Perguntas:**

1. Quando function-calling é melhor que embeddings-only?
2. Como validar retorno de tool externa?

---

## **Módulo 7 — Instrumentação, logging e debugging**

**Conceito:** logs, traces, metrics.
**Importância:** debugar e otimizar.

**Exercício:** instrumentar fluxo com logs JSON + trace simples.
**Desafio:** replay de sessão.

**Perguntas:**

1. Que dados mínimos para debugar uma LLM call?
2. Como medir custo por request?

---

## **Módulo 8 — Avaliações automáticas**

**Conceito:** métricas, rubricas, self-checks.
**Importância:** qualidade e segurança.

**Exercício:** avaliador por similarity + heuristics.
**Desafio:** closed-loop para atualizar prompts ou estratégias.

**Perguntas:**

1. Como medir factuality?
2. O que é “calibration”?

---

## **Módulo 9 — Deploy mínimo e demo**

**Conceito:** container + endpoint HTTP + script de demo.
**Importância:** transformar protótipo em produto.

**Exercício:** Dockerize app; run script.
**Desafio:** autoscaling + monitoring.

**Perguntas:**

1. Quais recursos para produção inicial?
2. Como limitar custo de LLM em produção?

---

# **Cronograma sugerido**

| Semana   | Conteúdo                                         |
| -------- | ------------------------------------------------ |
| Semana 0 | Módulo 0 + 1 (setup + adapters)                  |
| Semana 1 | Módulo 2 (RAG)                                   |
| Semana 2 | Módulo 3 (memória)                               |
| Semana 3 | Módulos 4 + 5 (agents + orquestração)            |
| Semana 4 | Módulos 6 + 7 (function-calling + observability) |
| Semana 5 | Módulos 8 + 9 (avaliações + deploy)              |

---
