<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./public/logo-wordmark-dark.svg" />
    <img src="./public/logo-wordmark.svg" alt="monkway" width="420" />
  </picture>

  <p><strong>Monk LLM Gateway &mdash; one API in front of every model.</strong></p>

  <p>An LLM gateway and router, built from scratch: it takes one request, routes it to the right provider, retries and falls back on failure, caches answers, and tracks cost and limits.</p>

  <p>
    <a href="https://monkfromearth.github.io/monkway/">Course</a> &middot;
    <a href="./docs/roadmap/index.md">Roadmap</a>
  </p>
</div>

---

## What this is

monkway is an LLM gateway and router built from the ground up to make one thing concrete: what actually
happens between your app and a language model. Every gateway (OpenRouter, LiteLLM, Cloudflare AI Gateway) is
the same machine &mdash; it takes one request, picks a provider, forwards it, and handles everything that
goes wrong on the way: a provider rate-limits you, times out, or costs too much. monkway builds that machine
one piece at a time, starting from a plain proxy you can read end to end.

Think of a **gatekeeper monk** at the monastery gate. Every traveler (request) arrives at one door. The
gatekeeper greets them, decides which path to send them down (routing), quietly reroutes when a door is
closed (retry and fallback), recognizes travelers he has seen before (caching), and keeps the ledger of who
came and what it cost (cost and rate-limit tracking). That one monk *is* the gateway.

## What's different

- **No magic proxy.** v1 is a gateway you can read in one sitting: request in, provider out, retry on
  failure, every call logged. Nothing hidden behind a framework.
- **Taught, not just shipped.** An interactive course ships *with* the code. It teaches the concepts &mdash;
  proxying, retries and backoff, routing policy, caching, budgets &mdash; and leaves the implementation to
  you, which is where the understanding sticks.
- **A real path to a real gateway.** v1 is a single-provider proxy with retry and logging. v2 climbs to
  multi-provider routing, a semantic cache, cross-provider fallback, and per-key budgets &mdash; the parts
  that make it a system, not a script.
- **Built to a senior bar.** Tests, a load/latency story, and honest docs &mdash; not a notebook that runs
  once.

## The two stages

| Stage                | What it is                                                                                                                                  | Status      |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **v1 — Proxy**       | A single-provider proxy with retry, backoff, and structured request logging (tokens, latency, cost). Small in lines, the floor under it all. | In progress |
| **v2 — Router**      | Multi-provider routing (cost vs latency vs quality), a semantic cache, cross-provider fallback, and per-key budgets and rate limits.        | Planned     |

Full detail: [docs/roadmap/](./docs/roadmap/index.md).

## Tech stack

| Part                 | Stack                                                                                                                                          |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **`monkway` (v1)**   | Python (FastAPI + httpx) for the proxy, with retry/backoff and structured logging. Dev tooling: [uv](https://docs.astral.sh/uv/), pytest, ruff. _(Starting choice; v2 may revisit the hot path for performance.)_ |
| **`monkway` (v2)**   | Adds a routing layer, a semantic cache (embeddings + vector lookup), provider fallback, and a per-key budget/rate-limit store.                  |
| **Knowledge course** | [Astro](https://astro.build) + [Tailwind CSS](https://tailwindcss.com) + [GSAP](https://gsap.com) for the demos, built with [bun](https://bun.sh). Deployed to GitHub Pages. |

## Learn it: the course

The [`knowledge/`](./knowledge) folder is an interactive course that teaches the concepts behind monkway:
what a proxy is, why retries need backoff, how a router weighs cost against latency, what a semantic cache
buys you, and how budgets are enforced. It is live at
**[monkfromearth.github.io/monkway](https://monkfromearth.github.io/monkway/)**.

Run it locally:

```bash
cd knowledge
bun install
bun run dev      # http://localhost:4321/monkway/
```

Authoring the course follows [`knowledge/AUTHORING.md`](./knowledge/AUTHORING.md) (voice, structure, and the
animation policy).

## Repository layout

```
monkway/
├── src/monkway/       the gateway (written by hand; starts as the v1 proxy)
├── tests/             tests for the gateway
├── knowledge/         the interactive course (Astro site) — concepts, not implementation
├── docs/roadmap/      phased plan: index + per-phase files
├── public/            brand assets (logo, wordmark, light + dark)
└── pyproject.toml     project + shared dev tooling (pytest, ruff)
```

## Status

Early. The brand and the course shell are up; v1 (the proxy) is next. Structure and docs grow with the
project.

## License

MIT (see [`LICENSE`](./LICENSE)).

---

<div align="center">
  <sub>Built by <a href="https://monkfrom.earth">Sameer Khan (@monkfromearth)</a> &middot; part of the <a href="https://github.com/monkfromearth">monk</a> family &middot; <a href="https://github.com/monkfromearth/monkway">source</a></sub>
</div>
