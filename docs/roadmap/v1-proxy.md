# v1 — Proxy

The floor under everything: a gateway that fronts **one** provider, retries when the call fails, and logs
every request. Small in lines, but it forces the core questions: what does a proxy actually do, and what does
"the call failed" mean?

## What it is

A small HTTP service that speaks an OpenAI-style chat API. A request comes in, the gateway forwards it to one
upstream provider, streams or returns the answer, and records what happened. When the upstream fails in a way
worth retrying, it retries with backoff before giving up.

## The gatekeeper, this phase

The gatekeeper stands at one gate. A traveler arrives, he walks them to the one path he knows, and if that
path is briefly blocked (a closed door, a busy guard) he waits a moment and tries again. He writes every
crossing in the ledger.

## Build steps

1. **The endpoint.** A `POST /v1/chat/completions` route that accepts an OpenAI-shaped body.
2. **Forward.** Send it upstream to one provider with an async HTTP client; return the response unchanged.
3. **Retry + backoff.** Retry only the retryable failures (HTTP 429, 5xx, timeouts, connection errors), with
   exponential backoff and jitter and a cap on attempts. Do not retry a 400 — that is the caller's bug.
4. **Structured logging.** For every request log: model, status, latency, attempt count, prompt/completion
   tokens, and an estimated cost. One structured line per request.
5. **Streaming (stretch).** Proxy a streamed (SSE) response token by token, not just the buffered body.

## Done when

- A real request round-trips through the gateway to a live provider and back.
- A forced upstream 429/timeout is retried with visible backoff, then succeeds or fails cleanly.
- Every request produces one structured log line with tokens, latency, and cost.
- Tests cover: a happy path, a retryable failure that recovers, and a non-retryable failure that does not
  retry.

## Concepts this unlocks (for the course)

What a reverse proxy is &middot; idempotency and why only some failures are safe to retry &middot; exponential
backoff and jitter (the thundering-herd problem) &middot; timeouts and deadlines &middot; how token usage maps
to cost.
