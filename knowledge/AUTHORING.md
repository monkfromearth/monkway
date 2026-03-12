# Authoring the knowledge course

How every unit and lesson in `knowledge/` is written. Read this before adding or editing a lesson.
The point of this file is that the course stays one voice and one set of decisions no matter who
(or which session) writes the next unit. Copy it into the project's `knowledge/` folder and adapt the
bracketed bits.

---

## 0. Pick your stance (decide once, write it here)

Two kinds of knowledge site, same craft:

- **Teaching course (learner builds it).** Teaches the *concepts* so the reader can build the thing
  themselves; it deliberately never shows the project's own implementation. (This was monktensor's mode.)
- **Documentation (shows the code).** Explains how the built thing works, code included.

Most of this guide applies to both. The one rule that differs is §1. State your choice at the top of this
file for the project: **[this project is a TEACHING COURSE / DOCUMENTATION].**

## 1. The rule that overrides everything (teaching-course mode)

**This is knowledge, not documentation.** Teach the idea, the math, and worked examples. NEVER paste the
project's real implementation; the reader writes the code, which is where understanding sticks. The test:
"would copying this snippet build the thing for them?" If yes, cut it. (Skip this section if you chose
DOCUMENTATION mode.)

## 2. Voice

- **Plain words first, the precise term second.** Say the real-world meaning, then name the term once.
- **Calm, curious, smart-friend.** No hype, no emojis, ever.
- **Concrete over abstract.** Lead with an analogy or a worked number, not a definition.
- **Worked examples over proofs.** "Nudge it and watch the number move" beats a wall of symbols.
- **One technical term per idea, max.** Three pieces of jargon in a sentence means rewrite it.
- **No em-dashes** in prose (a comma, period, colon, or parentheses instead). They are an AI tell.

## 3. Lesson structure

Each lesson is one `.astro` page using these pieces, in this order:

1. Frontmatter: import `LessonLayout`, `LessonHeader`, `LessonNav`, and the boxes/demos it uses.
2. `<LessonLayout title lessonNumber section>` wrapping everything.
3. `<LessonHeader lessonNumber title description>` with 1-2 `<TagBadge>` (a topic tag + a read-time).
4. 3-6 `<section class="mb-14">` blocks. Rhythm per section: **hook/analogy, the concept, a worked
   example, an `InsightBox`** naming the takeaway.
5. Optional "What it is NOT" section to kill misconceptions; optional `<ExerciseBox>`.
6. A "Key takeaways" section: 3 numbered points.
7. `<LessonNav prevHref prevLabel nextHref nextLabel>` chaining to the neighbours.

Aim for a 8-12 minute read. Longer means split it.

## 4. Components (in `src/components/`)

`LessonLayout` (page shell) · `LessonHeader` · `LessonNav` · `InsightBox` (the "remember this" callout) ·
`ExerciseBox` (work-it-by-hand) · `Formula` (centered math, no KaTeX) · `StepNumber` · `TagBadge`.
Interactive demos live in `src/components/demos/`.

## 5. Visual constraints

- Palette is the `mt-*` Tailwind tokens only (warm beige default; swap the values in `tailwind.config.mjs`
  to your brand). No raw hex in pages.
- Fonts loaded in the layout. Code blocks dark, used sparingly.
- **No emojis anywhere.**
- Every internal link and asset path goes through `import.meta.env.BASE_URL` (the site is served under a
  base path on GitHub Pages). Hardcoding `/foo` breaks in production.
- Brand assets (logo, etc.) must live in **`knowledge/public/`** — Astro serves that dir, not the repo root.

## 6. Animation policy (the heart of this)

Motion has to *teach*, or it doesn't ship.

- **Metaphor first, not charts.** Find the image that makes the idea click (gears for a chain of rates, a
  cell that fires, water filling a bucket, a ball on a hill, a line that can't split two groups) and animate
  *that*. Reach for a plain chart only when the metaphor is the chart.
- **The test:** "does seeing it move explain the idea better than a sentence?" If no, use a sentence.
- **Direct manipulation, not sliders.** The reader grabs the actual thing on the figure and moves it; the
  relationship redraws live. A slider sitting below the figure is the weak fallback.
- **Discrete where it's a value.** Snap dragged *values* to clean steps (e.g. 0.5) so they land on round
  numbers. Keep *positioning* continuous (dragging a fit-line, a point on a curve, a ball on a surface).
- **One demo per lesson, max.** A lesson is prose with a single illuminating interaction.
- **Respect `prefers-reduced-motion`.** Show the final/static state and skip tweens; every demo must still
  make sense with motion off. Use the `REDUCED` flag from `src/lib/interact.ts`.
- **Self-contained.** Each demo is one file in `src/components/demos/`, owns its markup + client `<script>`
  (import the shared helpers from `../../lib/interact`), and is scoped via a root class + `querySelectorAll`
  so multiple instances don't collide. Animate transforms/opacity/text, not expensive layout properties.

## 7. Adding a lesson, checklist

1. File: `src/pages/<unit>/<slug>.astro`.
2. Follow §2 voice, §3 structure, §1 stance.
3. Wire `LessonNav` to both neighbours.
4. If it earns one, add a single meaningful demo per §6.
5. Update `src/pages/index.astro` (or your course map): the lesson row, the unit count, the header total.
6. `bun run build` must pass before the lesson is "done."
