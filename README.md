# LLM Engineer Career Roadmap

A structured path to becoming a job-ready AI Engineer, with a bridge to LLM research.

**Flagship domain:** FastAPI open source codebase docs assistant  
**One repo, many releases:** v0.1 → v0.6

---

## Flagship Project

**Project:** FastAPI Docs Assistant

**What it does:** Answers questions about FastAPI with grounded citations to official docs (and later, selected source files + issues/PRs).

### Data Scope by Phase

| Release | Data |
|---------|------|
| v0.1 | FastAPI docs only (quick win) |
| v0.2 | docs + changelog/release notes + FAQ-style pages |
| v0.3 | docs + curated "problem pages" + common pitfalls + small source code slice (optional) |
| v0.6 | add issues/PRs for "why" questions (optional, for research macro) |

### Repo Structure

```
app/          # API (+ optional minimal UI)
rag/          # ingestion, chunking, retrieval, rerank
tools/        # function calling tools
eval/         # datasets, metrics, runners
ops/          # logging, tracing, dashboards, load tests
infra/        # docker, azure deployment
docs/         # writeups, diagrams, research notes
```

### Invariants (true for every release)

- `make run` starts the app
- `make eval` produces a report file
- `make test` runs smoke tests
- Docker builds and runs

---

## Macro 1 — Ship a Modern LLM App End to End

**Duration:** 3–4 weeks  
**Goal:** Job-ready quickly with a real LLM product artifact.

### Build

- **RAG baseline:** chunking + embeddings + retrieval over FastAPI docs
- **Citations:** every answer links to exact docs
- **Tool calling** (2–3 tools max):
  - `search_docs(query)`
  - `open_source(doc_id)` — returns the cited text
  - `summarize_section(doc_id)` — optional
- **Guardrails:**
  - prompt injection defenses ("answer only from retrieved sources")
  - refuse to execute "unsafe instructions" from docs text
- **Packaging:** FastAPI service + Docker

### Evaluation (minimum)

- Gold set: 20–60 Q/A prompts (FastAPI focused)
- Retrieval: Recall@k, MRR
- Answer quality: rubric + LLM-as-judge + 20–30 human spot checks
- Citation correctness: "does it cite relevant docs section?"

### Gold Set Starters

- "How do I add middleware?"
- "How do dependencies work and how do I use Depends?"
- "How do I enable CORS?"
- "How do I return a custom response model?"
- "How do I run background tasks?"
- "How do I handle auth with OAuth2?"
- "How do I mount sub-applications?"
- "What is the difference between @app.get and APIRouter usage?"

### Open Source Target

File 1 issue or doc improvement to FastAPI repo based on gaps discovered during ingestion.

### Deliverables

- [ ] Repo release v0.1
- [ ] README: architecture + design choices + eval results
- [ ] Announce v0.1 on LinkedIn/Twitter

---

## Macro 2 — Data + Evaluation Rigour

**Duration:** 3–4 weeks  
**Goal:** Make your work measurable and defensible.

### Add

- **Test set v1:**
  - coverage: routing, dependency injection, validation, responses, security, deployment
  - adversarial: "ignore the docs and do X" style injections
  - edge cases: version-specific behaviors, ambiguous questions
- Prompt regression tests (don't break behavior)
- Retrieval regression tests (don't degrade recall/citations)
- Dataset versioning + experiment tracking (MLflow or W&B)

### Open Source Target

Scope issues in lm-evaluation-harness or RAGAS (docs gaps, missing metrics, small bugs).

### Deliverables

- [ ] Repo release v0.2 with `eval/` as a first-class module
- [ ] Public "mini eval kit" inside the repo
- [ ] Post: "How I Evaluate My FastAPI Docs Assistant"
- [ ] Announce v0.2 on LinkedIn/Twitter

---

## Macro 3 — Agents + Production Hard Skills

**Duration:** 5–6 weeks  
**Goal:** Build agentic capabilities and make the system production-ready.

### Agent Mode

- **Multi-step reasoning:** ReAct pattern (Thought → Action → Observation loop)
- **Planning:** break complex questions into sub-queries
- **Tool chaining:** search → read → compare → synthesize → answer
- **Expanded tool set:**
  - `search_docs(query)`
  - `read_section(doc_id)`
  - `compare_versions(topic, v1, v2)`
  - `find_related_docs(doc_id)`
  - `check_deprecations(feature)`
- **Agent guardrails:** max steps, cost limits, stuck detection

### Agent Evaluation

- Multi-hop questions: "How did dependency injection change between 0.68 and 0.100?"
- Task completion rate
- Step efficiency (did it solve in reasonable steps?)
- Tool selection accuracy

### Production Hardening

- **Caching:**
  - retrieval results caching
  - tool output caching
  - prompt response caching (where safe)
- Streaming responses
- Load testing (k6/locust) + latency budget
- **Failure handling:**
  - timeouts
  - fallback when retrieval is empty
  - tool failure fallbacks
  - agent stuck/loop detection
- **Observability:**
  - agent traces (full reasoning chain)
  - structured logs
  - prompt metrics (latency, token usage, retrieval hits, steps per query)
  - dashboard screenshot in README

### Open Source Target

First meaningful PR to lm-evaluation-harness, RAGAS, LlamaIndex, or LangGraph (bug fix, new metric, agent evaluation pattern).

### Deliverables

- [ ] Repo release v0.3
- [ ] Agent mode with ReAct loop + expanded tools
- [ ] Agent evaluation results (multi-hop accuracy, step efficiency)
- [ ] Benchmark report: before vs after (latency, cost, failure rate)
- [ ] "Production mode" config flags

---

## Macro 4 — Azure Cloud Deployment + AI-102 Certification

**Duration:** 3–4 weeks  
**Goal:** Port your app to Azure and prove enterprise deployment skills.

### Azure Stack

- Azure OpenAI (inference)
- Azure AI Search (retrieval)
- Key Vault + Managed Identity
- Container Apps or App Service
- Application Insights (monitoring)
- Quotas + cost controls

### Hiring Signal Docs (required)

- `docs/threat-model.md` — injection + exfiltration + mitigations
- `docs/cost-model.md` — cost per 100 queries + 2 reduction levers
- `docs/runbook.md` — latency spikes, retrieval failures, rate limits

### Deliverables

- [ ] Repo release v0.4-azure (branch in same repo)
- [ ] Architecture diagram: local Docker vs Azure
- [ ] Threat model + cost model + runbook
- [ ] AI-102 certification

**Start applying here.** You have: shipped product + eval + production hardening + Azure deployment + cert.

---

## Macro 5 — Model Adaptation for Engineers

**Duration:** 3–5 weeks  
**Goal:** Learn fine-tuning without turning it into an infra war.

### Rule

Do not start with "fine-tune 7B" unless you have compute and a clear reason.

### Path

- Fine-tune a small model (0.5B–3B) with LoRA/QLoRA
- Training data: FastAPI Q/A pairs + doc-grounded examples (leakage checks)
- Compare against baselines:
  - prompt only
  - RAG only
  - fine-tuned only
  - RAG + fine-tuned

### Must Include

- Training recipe + configs
- Ablations: dataset size, LoRA rank, prompt template
- Evaluation uses the same harness from Macro 2

### Open Source Target

Contribute a training recipe or doc fix to PEFT or TRL.

### Deliverables

- [ ] Repo release v0.5
- [ ] Model card + training notes
- [ ] Comparison table: base vs RAG vs fine-tuned vs RAG + fine-tuned
- [ ] Announce results on LinkedIn/Twitter

---

## Macro 6 — Research Bridge: Reproduce + Extend

**Duration:** 6–8 weeks  
**Goal:** Shift from builder to evidence producer.

### Pick One Tractable Theme (FastAPI assistant aligned)

- Query rewriting for better doc retrieval
- Reranking improvements and their tradeoffs
- Evaluation reliability: LLM-as-judge vs human, rubric stability
- Latency/caching strategies and measured impact

### Research Discipline (non-negotiable)

- Fixed seeds + configs
- Baselines + ablations
- Results table + limitations

### Open Source Target

PR to the paper codebase / reproduction repo, or publish your reproduction cleanly.

### Deliverables

- [ ] Repo release v0.6-research
- [ ] Technical report (blog or preprint)
- [ ] PR or standalone reproduction release

**Note:** v0.6 is a differentiator, not a prerequisite. If interviews are flowing after v0.4–v0.5, prioritize job hunting.

---

## Mini-Threads (Run in Parallel)

### Mini-Thread A — Transformer Intuition

**When:** Alongside Macros 2–3 (complete before starting Macro 5)  
**Duration:** 5–7 days total  
**Goal:** nanoGPT-level understanding of attention, loss, training loop

**Deliverable:** Notebook + notes in `docs/internals/`

---

### Mini-Thread B — Alignment Literacy

**When:** Alongside Macros 4–5  
**Duration:** 1–2 weeks part-time  
**Goal:** Intuition, not infrastructure

**Do:**
- Read InstructGPT + DPO summaries
- Add safety tests (refusal + jailbreak prompts) to `eval/`
- Post: "When SFT vs DPO Makes Sense for Engineers"

**Deliverable:** Post + safety tests in eval suite

---

## Timeline

| Macro | Duration | Milestone |
|-------|----------|-----------|
| 1 | 3–4 weeks | v0.1 — working app + demo |
| 2 | 3–4 weeks | v0.2 — eval rigor + post |
| 3 | 5–6 weeks | v0.3 — agent mode + production ready + first PR |
| 4 | 3–4 weeks | v0.4-azure + AI-102 cert |
| 5 | 3–5 weeks | v0.5 — fine-tuned model |
| 6 | 6–8 weeks | v0.6-research — technical report |

**Job-ready checkpoint:** After Macro 4–5 (~18–24 weeks)

---

## Resources

**RAG & LLM Apps:**
- [LangChain docs](https://python.langchain.com/)
- [LangGraph docs](https://langchain-ai.github.io/langgraph/)
- [LlamaIndex docs](https://docs.llamaindex.ai/)
- [Pinecone learning center](https://www.pinecone.io/learn/)

**Evaluation:**
- [RAGAS](https://docs.ragas.io/)
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

**Fine-tuning:**
- [Hugging Face PEFT](https://huggingface.co/docs/peft)
- [Hugging Face TRL](https://huggingface.co/docs/trl)

**Transformers:**
- [Andrej Karpathy's nanoGPT](https://github.com/karpathy/nanoGPT)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

**Alignment:**
- [InstructGPT paper](https://arxiv.org/abs/2203.02155)
- [DPO paper](https://arxiv.org/abs/2305.18290)

**FastAPI:**
- [FastAPI docs](https://fastapi.tiangolo.com/)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)

---

## License

Feel free to fork and adapt this roadmap to your own goals.
