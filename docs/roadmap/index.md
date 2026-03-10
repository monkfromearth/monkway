# monkway roadmap

monkway is built in two stages. v1 is a gateway you can read end to end: one request in, one provider out,
retries on failure, every call logged. v2 turns that proxy into a router: many providers, a cache, fallback,
and budgets. Build v1 to learn the moving parts, then layer v2 on top.

The guiding image is the **gatekeeper monk**: every feature below is one more thing the gatekeeper does at
the gate.

| Phase | What it is | Status |
| ----- | ---------- | ------ |
| [v1 — Proxy](./v1-proxy.md) | A single-provider proxy with retry, backoff, and structured request logging. | In progress |
| [v2 — Router](./v2-router.md) | Multi-provider routing, a semantic cache, cross-provider fallback, and per-key budgets and rate limits. | Planned |

## Principles

- **Beginner-first, then senior.** v1 is the textbook proxy, written by hand to learn the basics. v2 is the
  researched, systems-grade version. See the workspace operating principles.
- **One clear job per piece.** Proxy, then retry, then routing, then cache, then budgets. Each lands with a
  test and an honest note on what it does not yet handle.
- **The course tracks the code.** Each concept gets a lesson in `knowledge/` that teaches the idea without
  shipping the implementation.

## What it does NOT try to be (yet)

A drop-in replacement for LiteLLM or OpenRouter on day one. The point is to build the gateway from first
principles so every decision (why backoff, why a semantic cache, how to weigh cost against latency) is
understood, not imported.
