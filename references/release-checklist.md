# Pre-release signoff sheet

Copy this into the project and check after a final render. `scripts/validate_project.py` cannot replace a human visual review.

## Source truth
- [ ] All claims in `facts.json`, status verified, no unsourced visual/audio claims.
- [ ] Official names, logos, links, real UI and color palette accurately represented.
- [ ] Referenced media analysed for principles, not copied without permission.
- [ ] Asset rights and font licenses documented in `assets/asset-ledger.md`.

## Story and art direction
- [ ] Strong meaningful **first frame**, understandable hook within 1 s.
- [ ] One continuous visual idea through the film; not a transitions sampler.
- [ ] Type remains legible for its informational load; contrast checked.
- [ ] Motion includes anticipation/follow-through and satisfying changes of pace.
- [ ] Each product action has visible result; ending provides requested end state.

## Output and sound
- [ ] MP4 decodes; exact video resolution, fps, frame count and acceptable length.
- [ ] Properly authored 9:16 if required; all key items safe from UI overlays.
- [ ] Video and sound aligned to within a single frame at named cue points.
- [ ] Loudness and true peak measured; no clipping or dialogue buried by music.
- [ ] First and final frames intentional, no accidental long dead frames or slides.
- [ ] Visual mute test, audio-only test and 0.5× playback review complete.

## Creative signoff
- [ ] Saved a labelled, usable contact sheet and QA JSON.
- [ ] Independent (or transparently self-described) blind-style critique attached.
- [ ] At least one substantial edit re-rendered with before/after evidence.
- [ ] Builder would show this beside the brief's best reference without apology.
- [ ] Film, project source, exact rebuild command and limitations included.
