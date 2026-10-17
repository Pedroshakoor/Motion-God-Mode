# Creative critique and QA — make revision measurable

## Blind critic instructions

> Inspect the rendered file without reading the creator's pitch. Give timestamps for each issue. Rate every category 0–5: first frame and first-second hook, clarity without audio, singular visual idea, timing and visual rhythm, quality of animation/easing, typography hierarchy, originality, use of sound, verified product/fact fidelity, and final-second payoff. Identify the one moment that feels cheap or assembled. Propose a specific change that can be verified in the next render. If you don't see or hear evidence, say 'not assessed'.

If a distinct independent agent is unavailable, use a fresh pass after watching output in three modalities. Do not falsely describe a self-review as independent.

## Scoring anchors

| Score | Meaning |
| --- | --- |
| 0 | Broken, illegible or missing |
| 1 | Technically renders but reads generic, bad or confusing |
| 2 | Understandable, but looks templated/unpolished |
| 3 | Competent creative motion with a few weak moments |
| 4 | Cohesive, impressive, few clearly fixable issues |
| 5 | Distinctive, polished, emotionally/rhythmically memorable |

Averages conceal showstopper failures. No signoff if claims aren't sourced, there is a frame/codec failure, a critical caption is unreadable or final CTA is incorrect. Even with high numeric scores, require an actual revision documented in `ledger.md`.

## Repeatable passes

**Mute test**
- Pause at frame 0. Can someone who doesn't know the brief understand or feel an immediate premise?
- Pause at 0.2 s intervals. Do subjects remain legible? Are compositions meaningfully different or just random?
- At each seam, which shared visual thread physically carries across?
- Read every textual phrase out loud at the speed shown.

**Audio-only test**
- Listen without looking. Do events sound causally motivated?
- Is there a dynamic contour, with changes of energy and moments of breath?
- Are voices audible, with realistic peaks and no muddy overlap?

**Technical and sync test**
- Compare audio hit frames to cut/impact frames, within ±1 video frame.
- Inspect contact sheet density at 0.2 s, and 0.1 s around transitions.
- Flag black/blank or accidentally still sections >0.5 s. Purposeful visual rests are okay when logged.
- Validate MP4 resolution, fps, frame count, duration and the audio track.
- Check real device safe areas manually for each destination platform; overlay dimensions change.

**Revisions**
- Each change log entry captures timestamp, observed problem, chosen edit, and difference from previous output.
- Fix one major issue and **re-render** before declaring it solved.
- Include critic's notes, numbers, and a clear honest known-limitations section.
