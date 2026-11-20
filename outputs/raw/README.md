# Raw outputs

This folder contains append-only execution records. Files named `TC*.json` are generated from the eight synthetic assignment cases. Records with `mode: DEMO` are deterministic simulations, not genuine LLM responses. Do not describe them as live AI results.

To generate genuine Gemini runs, set `GEMINI_API_KEY` in `.env` and run `python scripts/run_evaluations.py --live`. The runner explicitly passes the key into the pipeline and refuses to accept a non-live result as a live run. Review every file manually before filling the evaluation tracker.

Interactive records may contain user-provided personal data. They are ignored by Git; review and remove sensitive information before sharing any record. Raw files are created with exclusive file creation and are never overwritten.
