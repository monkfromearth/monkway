# Authoring the monkway knowledge course

How every unit and lesson in `knowledge/` is written. Read this before adding or editing a lesson. The point
of this file is that the course stays one voice and one set of decisions, no matter who (or which chat) writes
the next unit.

---

## 1. The one rule that overrides everything

**This is knowledge, not documentation.** The course teaches the *concepts* a reader needs in order to build
monkway themselves. It never shows monkway's implementation.

- Teach the idea, the tradeoff, and worked examples (a request, a status code, a backoff schedule by hand).
- NEVER write the gateway: no FastAPI routes, no `httpx` client, no retry decorator, no router/cache/limiter
  source, no "here is the code, copy it." If a page hands over the implementation, it has become documentation
  and failed its job.
- The line: explain backoff as *"wait, and double the wait each time, with a little randomness"* with a worked
  schedule. Do **not** write the function that does it. The reader writes the code; that is where the
  understanding sticks.
- Tiny illustrative snippets that are NOT the gateway (a JSON request body, a worked cost sum, a status table)
  are fine. The test: would copying this snippet build monkway for them? If yes, cut it.

## 2. The spine: the gatekeeper monk

Every lesson is one more thing the **gatekeeper monk** does at the monastery gate. Greets every request at one
door (proxy), picks which path to send it down (routing), reroutes when a door is closed (retry and fallback),
recognizes travelers seen before (caching), and keeps the ledger (cost and limits). Lead with that image when
it fits; never force it.

## 3. Voice

- **Plain words first, the precise term second.** "Wait longer each time you retry (exponential backoff)."
- **Calm, curious, smart-friend.** Never lecture-y, never hype. **No emojis, ever.**
- **Concrete over abstract.** Lead with an everyday analogy or a worked number, not a definition.
- One technical term per idea, max. Vary sentence shape; do not lean on em-dashes.

## 4. Lesson structure

Each lesson is one `.astro` page using these pieces, in this order:

1. Frontmatter: `import '../../styles/global.css';` then import `LessonLayout`, `LessonHeader`, `LessonNav`,
   and whatever boxes/demo it uses. **Lessons live at `src/pages/<unit>/<slug>.astro` (two levels deep), so all
   imports use `../../` and demo imports use `../../components/demos/<Name>.astro`.**
2. `<LessonLayout title lessonNumber section>` wrapping everything.
3. `<LessonHeader lessonNumber title description>` with 1-2 `<TagBadge>` (one topic tag + a read-time).
4. 3-6 `<section class="mb-14">` blocks. Rhythm per section: **hook/analogy -> the concept -> a worked
   example -> an `InsightBox`** that names the takeaway.
5. Optional `<ExerciseBox>` (something to work by hand).
6. A "Key takeaways" section: exactly three numbered points (copy the markup from `_example-lesson.astro`).
7. `<LessonNav prevHref prevLabel nextHref nextLabel>` chaining to the neighbours (hrefs WITHOUT the base; the
   component prepends it).

Keep a lesson to a 7-11 minute read. Escape JSX braces in inline text as `&#123;`/`&#125;`.

## 5. Components (props)

| Component | Use / props |
|-----------|-------------|
| `LessonLayout` | page shell. props: `title`, `lessonNumber`, `section`. Required. |
| `LessonHeader` | props: `lessonNumber`, `title`, `description`; slot holds `TagBadge`s. Required. |
| `LessonNav` | props: `prevHref`,`prevLabel`,`nextHref`,`nextLabel` (hrefs like `/proxy/streaming-the-answer`). Required. |
| `TagBadge` | prop `variant`: `concepts`/`intuition`/`math`/`exercise`/`glossary`/`links`/`default`. |
| `InsightBox` | the coral "remember this" callout. Slot only. |
| `ExerciseBox` | green "work it by hand" box. prop `title` (default "Try it yourself"). |
| `Formula` | centered display. prop `caption`. Use `<span class="var">` / `<span class="op">`. |
| `StepNumber` | numbered circle. props `number`, `color` (`accent`/`lav`/`blue`/`green`). |
| demos (`components/demos/`) | one per lesson, see section 6. |

Palette is the `mt-*` Tailwind tokens only (`mt-bg`,`mt-card`,`mt-border`,`mt-text`,`mt-muted`,`mt-accent`,
`mt-accentLight`,`mt-lav`,`mt-blue`,`mt-green`,`mt-amber`,`mt-rose`,`mt-locked` + their `*Light`). No raw hex
in pages except inside demo `<svg>` (the demo files use literal hex, matching `_ExampleDragDemo.astro`).

## 6. Animation policy (one demo per lesson, max)

Motion has to *teach*, or it doesn't ship.

- **Meaningful only.** Animate to make visible what a static page can't: a backoff delay doubling, a request
  failing over to another provider, a token bucket draining and refilling, a query finding its nearest cached
  neighbor. Never animate for polish.
- **Direct manipulation beats autoplay.** Prefer demos the reader drives: drag a value (attempt count,
  timeout, cost/latency weight, similarity threshold, refill rate) or press a button (send a request, kill a
  provider, stream). Snap dragged *values* to clean steps; keep free *positioning* continuous.
- **Build each demo by copying `src/components/demos/_ExampleDragDemo.astro`.** It owns its markup + a client
  `<script>` that imports `{ gsap, draggable, clamp, REDUCED, countTo }` from `../../lib/interact`. Scope to a
  root class via `querySelectorAll` (never global ids), so instances don't collide.
- **Respect `prefers-reduced-motion`** (`REDUCED`): show the final/static state, skip tweens. Every demo must
  make sense with motion off.
- **One demo per lesson, max.** A lesson is prose with a single illuminating interaction. Some lessons earn no
  demo; that is fine (use a worked table or `StepNumber` walkthrough instead).

## 7. Adding a lesson — checklist

1. File `src/pages/<unit>/<slug>.astro`; demo (if any) `src/components/demos/<Name>.astro`.
2. Follow structure (s4), voice (s3), the one rule (s1).
3. Wire `LessonNav` to both neighbours per the curriculum below.
4. Update `src/pages/learn.astro` (course map) if the lesson list changes.
5. `bun run build` must pass before the lesson is "done."

## 8. The curriculum

Stance: a teaching course that withholds the implementation (the reader writes the gateway). Linear order; each
lesson's `LessonNav` points to the previous and next in this list. Folder = unit slug; section = the unit name.

- **0 The Gate** (`gate`): what a gateway is `what-a-gateway-is` &middot; a request's journey `the-request-journey`
  &middot; why a gateway at all `why-a-gateway`
- **1 The Proxy** (`proxy`): what a proxy does `what-a-proxy-does` &middot; one API, many providers
  `one-api-many-providers` &middot; streaming the answer `streaming-the-answer`
- **2 When It Fails** (`failure`): ways a call fails `ways-a-call-fails` &middot; idempotency `idempotency`
  &middot; backoff and jitter `backoff-and-jitter` &middot; timeouts and deadlines `timeouts-and-deadlines`
- **3 Choosing a Path** (`routing`): routing policy `routing-policy` &middot; cost, latency, quality
  `cost-latency-quality` &middot; fallback `fallback`
- **4 Remembering Answers** (`cache`): exact-match cache `exact-match-cache` &middot; caching by meaning
  `semantic-cache` &middot; nearest-neighbor lookup `nearest-neighbor`
- **5 The Ledger** (`ledger`): tokens and cost `tokens-and-cost` &middot; rate limiting `rate-limiting`
  &middot; budgets and fairness `budgets-and-fairness`
- **Glossary** (`/glossary`): every term, plain English then precise.

First lesson's `prevHref` is `/learn` ("Course map"). The last lesson (`budgets-and-fairness`) `nextHref` is
`/glossary`. The glossary `prevHref` is `/ledger/budgets-and-fairness`, `nextHref` `/learn`.

## 9. Current demos

| Demo file | Lesson | Teaches |
|-----------|--------|---------|
| `GateDoorDemo` | 0.1 | one door routes to whichever provider is up |
| `ProxyTranslateDemo` | 1.2 | the same request, remapped to each provider's shape |
| `StreamingDemo` | 1.3 | tokens arriving one at a time vs all at once |
| `RetryableDemo` | 2.1 | which failures are safe to retry |
| `BackoffDemo` | 2.3 | drag attempts; delays double, jitter spreads them |
| `TimeoutDemo` | 2.4 | drag the timeout; watch how many requests get cut |
| `TradeoffDemo` | 3.2 | drag the cost/latency weight; the winner changes |
| `FallbackDemo` | 3.3 | kill a provider; the request fails over |
| `NearestDemo` | 4.3 | drag a query; its nearest cached neighbor lights up |
| `TokenBucketDemo` | 5.2 | drag the refill rate; the bucket drains and refills |

(Lessons not listed here ship without a drag demo: prose + a worked table or `StepNumber` walkthrough.)
