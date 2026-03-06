"""monkway: the Monk LLM Gateway.

One API in front of many model providers. v1 is a single-provider proxy with retry
and logging; v2 adds routing, a semantic cache, fallback, and per-key budgets.

The implementation is written by hand as the project is built; this package starts
as a placeholder so the repo, tests, and CI have a home from day one.
"""

__version__ = "0.0.1"
