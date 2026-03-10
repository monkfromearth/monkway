# v2 — Router

v1 fronts one provider. v2 turns the proxy into a **router**: many providers behind one API, a cache so the
same question is not paid for twice, fallback when a provider is down, and budgets so no key can overspend.
This is where monkway stops being a script and becomes a system.

## The gatekeeper, this phase

Now the gatekeeper knows many paths, not one. He picks the best path for each traveler (cheapest, fastest, or
most capable), sends them another way when a path is closed, recognizes travelers he has already answered, and
turns people back at the gate once they have spent their allowance.

## The pieces

1. **Routing policy.** Given several providers that can serve a request, choose one by a policy: lowest cost,
   lowest latency, or highest quality. The interesting part is the tradeoff and how to measure it.
2. **Fallback.** When the chosen provider fails (even mid-stream), fall over to the next candidate without the
   caller redoing anything. Failover across providers, not just retry against one.
3. **Caching.** Two flavors: exact-match (same bytes, same answer) and **semantic** (same meaning, different
   words) using an embedding plus a vector lookup. Semantic caching is a small vector-search problem, which
   ties into the Vector Search project on the roadmap.
4. **Budgets + rate limits.** Per-key spend ceilings and request limits: count tokens and cost per key, and
   reject or slow down once a key crosses its limit. A cousin of the distributed rate-limiter problem.

## Done when

- One request can be served by any of several providers under a stated policy, with the choice logged.
- Killing the chosen provider mid-request fails over to another and the caller still gets an answer.
- A repeated question (exact, then near-duplicate) is served from cache, measurably cheaper.
- A key that exceeds its budget is rejected, and the ledger proves the accounting is right.

## Concepts this unlocks (for the course)

Routing policy as an optimization (cost vs latency vs quality) &middot; failover vs retry &middot; exact vs
semantic caching &middot; embeddings and nearest-neighbor lookup &middot; token-bucket rate limiting &middot;
per-tenant budgets and fairness.

## The senior angle (to pick once v1 lands)

The proxy is glue; the signal lives in one deep part. Candidates: the **semantic cache** (ties to vector
search), the **routing policy** (a real, measured tradeoff), or **streaming failover** (retry mid-token-
stream). Choose one to take to a senior bar with benchmarks and a written verdict.
