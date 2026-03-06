# monkway

Monk LLM Gateway: an LLM gateway and router built from scratch. One API in front of many model providers,
built in two stages: a single-provider proxy with retry and logging (v1), then a multi-provider router with
caching, fallback, and budgets (v2). This file is the entry point for any new session working in this repo.

## Reading order for a new session

1. **This file** — what monkway is and how we work on it.
2. **[docs/roadmap/index.md](./docs/roadmap/index.md)** — the phased plan; start with the current phase
   ([v1](./docs/roadmap/v1-proxy.md)).
3. **[knowledge/](./knowledge)** — the course that teaches every concept the gateway is built on. If writing
   or editing course content, read **[knowledge/AUTHORING.md](./knowledge/AUTHORING.md)** first.

## Collaboration mode (the rule that overrides convenience)

- **v1 is learn-by-building.** The implementation is written by hand, by Sameer. The assistant is a teacher
  and reviewer: guide the theory and the stack, explain plain-English-first then the precise term, scaffold,
  ask Socratic questions, review code, unblock. **The assistant does not write the gateway's implementation
  in v1.**
- **The course teaches concepts, never the implementation.** `knowledge/` explains how a proxy, retries,
  routing, and caching work (the ideas, the tradeoffs, worked examples) but never ships the gateway's source.
  Knowledge, not documentation. See `knowledge/AUTHORING.md` rule 1.
- **v2 is pairing.** Once v1 is done, the heavier v2 work (routing, semantic cache, budgets) is
  collaborative, code included.

## The metaphor (the spine of the whole project)

A **gatekeeper monk** at the monastery gate. Every request arrives at one door. He greets it, decides which
path to send it down (routing), reroutes when a door is closed (retry and fallback), recognizes travelers he
has seen before (caching), and keeps the ledger of who came and what it cost (cost and rate limits). Every
lesson and feature is one more thing the gatekeeper does.

## Repository layout

```
monkway/
├── src/monkway/       the gateway (written by hand; starts as the v1 proxy)
├── tests/             tests for the gateway
├── knowledge/         the learning course — Astro site, deployed to GitHub Pages
├── docs/roadmap/      phased plan: index + per-phase files
├── public/            brand assets (logo, wordmark, light + dark)
└── pyproject.toml     project + shared dev tooling (pytest, ruff)
```

## Quality bars

- **No hallucinated facts.** Verify provider APIs, model names, rate-limit/cost numbers, and any claim
  against primary sources before they reach the README, docs, or course.
- **Senior-repo bar.** A phase is done with tests, a latency/throughput story that means something, a real
  README, and honest notes on what's left — not just "it runs."
- **No em-dashes in course prose; no emojis anywhere in the course.** See `knowledge/AUTHORING.md`.

## Working with the knowledge site

```bash
cd knowledge
bun install
bun run dev      # local dev at /monkway/
bun run build    # static build into knowledge/dist (what Pages deploys)
```

The site is served under the `/monkway/` base path. Brand assets live in `knowledge/public/` (Astro serves
that directory). Every internal link/asset goes through `import.meta.env.BASE_URL`.

## Stack

- **Knowledge site:** Astro + Tailwind + GSAP, built with bun.
- **Gateway:** Python (FastAPI + httpx), managed with uv. Dev tooling: pytest, ruff. Run from the repo root:
  `uv sync`, `uv run pytest`, `uv run ruff check`. _(Starting choice; v2 may revisit the hot path.)_
