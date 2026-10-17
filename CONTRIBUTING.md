# Contribute to MOTION GOD MODE

MOTION GOD MODE is allergic to impressive-sounding instructions without a way to test them.

1. File an issue with the mode (`showreel`, `product`, `launch-story`, `explainer`), the exact brief, expected behavior and what failed.
2. For scripts, include a reproducible sample and tests. Keep helper scripts standard-library-first; optional dependencies should fail clearly.
3. For creative rules, include a screenshot/contact sheet or a timestamped critique showing the improvement. Prefer a concrete action to abstract taste advice.
4. Do not add example media you lack rights to distribute. No fake client logos, personal data, fabricated testimonials or copyrighted music.
5. Run `python -m unittest discover -s tests -v` and `python scripts/validate_project.py examples/showreel` before opening a PR.

Please keep `SKILL.md` focused enough to load in one agent context; move in-depth material into `references/`. No gated products, trackers or hidden SaaS accounts are required.
