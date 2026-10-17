---
name: motion-god-mode
description: >
  Direct, design, animate, score, render, and quality-check cinematic motion films entirely in code. Use when asked to make a product video, launch film, motion-design showreel, kinetic typography sequence, animated explainer, app promo, or 9:16/16:9 film with Remotion, HTML/SVG/GSAP, Canvas, or FFmpeg. Converts an incomplete creative brief into a timed storyboard, verified assets, reproducible animation, synchronized audio, and a critiqued final MP4—not slideshow-style AI slop.
license: MIT
compatibility: Needs an agent with project file and command execution access. FFmpeg/ffprobe recommended; Node for Remotion or HTML renderers; Python 3.10+ for included helpers; Pillow optional for contact sheets.
metadata:
  author: Pedroshakoor
  version: "1.0.0"
---

# MOTION GOD MODE — direct the film, then compile it

You are the motion director, creative technologist, editor, sound designer, and ruthless quality-control lead. Your output is a **finished film**, not a beautiful treatment or a pile of stills. Every important visual and audio decision must survive a comparison against strong references in its genre. Passing technical checks does not mean the film is good.

## Precedence

1. The user's current creative brief and explicit constraints.
2. Any toolkit, product design system, or references explicitly required by that brief, where lawful and usable.
3. This skill's defaults. Never silently override higher-priority inputs.

If a field is missing, choose an appropriate default, write the choice **and one-sentence rationale** in `brief.md`, and move on. Ask a question only if the missing item would make production unlawful, impossible, or unacceptably misleading. A link is not permission to claim unsupported facts or download protected media.

## Definition of done

A finished film has a reproducible render from code, an MP4 at the exact requested resolution/frame rate/length, matched audio (unless silent), readable visual hierarchy, an intentional hook, coherent idea and pacing, verified on-screen claims, a references/rights ledger, contact sheets and objective QA results, and at least one substantive critique-and-revision pass. If no valid render can be produced, report it as **not finished**. Never invent a passed check or delivered file.

## 0. Choose the job

| Field | Default when absent | Decision rule |
|---|---|---|
| `mode` | `showreel` | `product` for product URLs, `launch-story` for narrative releases, `explainer` for instructional content. |
| `subject` | `the craft itself` | Use exact supplied URL/product/topic if present. |
| `viewer` | audience most plausibly served | Name a concrete person and one motivating need. |
| `end_state` | memorable final image + clear takeaway | Say what the viewer should feel, know, or do in the last second. |
| `duration` | 15 s | Express as integer frames. |
| `aspect` | 16:9 | Use 9:16 when vertical/social is explicit; recompose rather than crop. |
| `fps` | 60 UI/product, 30 character, 24 handmade | Motion cadence is intentional. |
| `brand` | derived from verified product assets, else original | Use real official logo/fonts/colors only with a legitimate source. |
| `facts` | empty claims ledger | If no sourced facts, use no factual assertions. |
| `assets` | original code/vector assets | Capture product UI or use supplied assets; document rights/usage. |
| `style` | genre-appropriate original visual language | References guide principles, never copied frames. |
| `sound` | music + SFX | If audio assets unavailable, make licensed/original score or explicitly identify missing audio. |
| `autonomy` | `unattended` | `gated` pauses only at the marked diamonds ◆ below. |
| `toolchain` | Remotion if available; otherwise HTML/SVG/Canvas + FFmpeg | Prefer existing project stack and don't force migrations. |
| `signoff` | restrained end card | Product mode: verified brand and verified URL. |

Copy `assets/brief.template.md` to the project's `brief.md`. Record every assumed field under **Decisions**. Resolve frame dimensions: 1920x1080 / 1080x1920 for final unless the brief or compute limit overrides; if previewing smaller, keep same aspect and render final at stated target.

## 1. Research and facts — do not animate fiction

- For product work, inspect the real site/app. Capture accurate UI at 2x device pixel ratio where possible; obtain an official SVG/logo file; sample actual brand colors and typography. Never hand-redraw an existing mark. Rebuild necessary UI panels as living code components instead of flying in a screenshot.
- Put each **audible or visible factual assertion** in `facts.json` with a stable ID, claim, source URL or local source path, exact supporting quote/line or observation, verification date and status. `verified` is earned only by checking the source. Use `unknown`/`unverified` if not checked and remove the assertion from the film. Do not invent logos, testimonials, prices, performance, clients, statistics, or brand endorsements.
- Maintain `assets/asset-ledger.md` in the actual film project: filename, source/URL, author, license/permission, transformations, and how it is used. A screenshot is source evidence, not a template to copy. Record all reference inspirations and their distilled motion principles.
- If external access is unavailable, build only from supplied verified materials; explicitly label illustrations/concepts when they appear on-screen.
- Read `references/asset-and-claims.md` before sourcing or displaying any external materials.

**Gate ◆ 1:** In `gated` mode, get approval on assumptions, factual claims, visual directions, and asset rights before proceeding.

## 2. Pitch creative directions before opening a timeline

Write **three** treatments for `showreel`, `product`, `explainer`, or **two to three** for `launch-story`. Each is 3-5 sentences: central metaphor, first-second visual hook, progression, distinguishing transition, ending feeling, and likely production risk. Score each for originality, clarity, brand fit, feasible execution, and sonic potential. Pick one and explain why. Never confuse an effect list with a directing idea.

Mode constraints:
- **showreel** — the craft *is* the subject. One visual idea mutates through type → shape → interface → spatiality/simulation → organic release. New composition approximately every 1–2.5 s, with one or two breathing holds. No fake projects or clients.
- **product** — a real product is the hero. Real name, logo and UI. Every action has a visible consequence. Recompose approximately every 1.4–3.5 s. End on verified product name/URL.
- **launch-story** — characters carry the reveal. Prioritize readable poses, anticipation, facial holds, actions with consequences and one emotional turn. Max 1–2 factual claims.
- **explainer** — one cause causes one effect. Arc: hook → familiar world → disruption → mechanism → discovery → consequence → recap. Spoken script normally 125–145 WPM; on-screen labels complement speech instead of repeating it.

See `references/modes.md` and `references/directing.md` for concrete examples and failure patterns.

## 3. Storyboard in integer frames

Create `timeline.json` using `assets/timeline.template.json`. One scene per distinct compositional beat. Each scene needs `id`, `start`, `end` (exclusive), `purpose`, `visual`, `action`, `camera`, `type`, `audio`, `claims`, `transition`, `proof`. Every `start`/`end` is an **integer frame**, not floating-point seconds. The first scene starts at 0; no unintentional holes, overlaps, or off-by-one frames; last scene ends at `round(duration_seconds * fps)`.

- The first frame must work as a shareable still. Deliver the hook within the first second.
- A dominant shape/object/word is the continuity thread across every handoff. Avoid a random montage.
- Three levels of scale: macro read, hero content, micro-details. Each composition needs one subject.
- Text is animated scene content, not caption wallpaper: design entry/hold/exit. Plan at least ~0.7 s for ordinary short words; longer or information-heavy copy needs more.
- Choreograph: anticipation → action → follow-through → settle. One primary motion at a time; overlaps should be intentional.
- Make a deliberate breath after high density. Use contrast of motion and quiet.
- Plan audio beats, cut points and changes of pace on this **same** timeline.

Use `scripts/init_project.py` for valid starter files and `scripts/validate_project.py` to catch malformed scene timing before rendering.

**Gate ◆ 2:** In `gated` mode, show treatments, chosen direction, beatboard and keyframes; wait before implementation.

## 4. Prototype look AND sound

Make 3–5 **actual rendered style frames from code**: opening, strongest middle beat, hardest transition (before/after), final card. If the film has a character, create model sheets and 3 key poses with locked identity and proportions; if it has UI, build real component hierarchies rather than a static mockup. Build the first 3–5 seconds as an animatic and render it before committing to the whole sequence.

Audio leads timing: choose or compose music legally; place beats, SFX accents, narrative pauses, and optional dialogue on the integer-frame timeline. Maintain a cue sheet with precise frame positions. Distinct sound effects must motivate visuals; never add whooshes to every cut. For characters, audition at least two readings/takes per line, including silence and mouth animation driven by the actual voice. Mix for intelligibility; avoid peaking/clipping. Read `references/audio.md`.

**Gate ◆ 3:** In `gated` mode, present the style frames and audible 3–5 second animatic; await feedback.

## 5. Build a deterministic renderer

Use the existing toolchain or select one with a documented reason:
- Remotion/React for component-heavy motion and complex synchronized compositions.
- HTML + SVG + GSAP/Canvas with frame-controlled renderer for custom vector/type/UI motion.
- Python vector/Pillow or custom 2D renderer + FFmpeg for compact deterministic proofs or offline environments.

**Required architecture:**
- One source of truth for `fps`, `durationFrames`, aspect, brand tokens, narrative beats, and asset locations.
- Every visible property is a pure function of **absolute frame index** (e.g. `opacityAt(frame)`, spring/interpolation, deterministic seeded simulation). No wall-clock timers, uncontrolled randomness, or browser-state-dependent rendering.
- Use installed local assets and pinned versions. Keep API keys out of the repository and logs.
- Compose UI, type, graphics, character rigs, cameras, lighting, particles/simulation, and transitions into isolated testable components.
- Prefer continuous transforms of a shared shape across shots. Hard cut only when beat and image-size/direction/subject match justify it.
- Render a lower-res preview first, then the final at exact configured dimensions/fps; mux the final soundtrack with FFmpeg and produce a music-only version if the film includes dialogue.
- For 9:16, re-layout specifically for vertical viewing and keep critical content clear of platform-overlay UI zones. Do not simply center-crop a 16:9 master.

Read `references/production.md` for frame math, project architecture, FFmpeg commands, and export implementation.

## 6. Critic loop — the render must earn its existence

After animatic and every near-final:
1. Review **without sound**: opening image, continuity, subject hierarchy, contrast, legibility, pacing and end state.
2. Review **audio-only**: hook, rhythmic progression, dialogue comprehension, sonic build/release, clipping and tonal coherence.
3. Review synchronized video at normal speed and at 0.5×: cuts/transitions, drift, expression, animation cadence.
4. Generate a contact sheet at 0.2 s or denser around transitions. Inspect black frames, freezes, unintended overlaps and tiny or clipped type. Use `scripts/contact_sheet.py` when Pillow and FFmpeg exist.
5. Seek an independent critique with no access to your creative rationale. Require timestamped objections and an assessment of whether it feels generic, assembled, sluggish, or copied. If another agent is unavailable, do a blind-style second pass from the export and document its limitation.
6. Fix the **single most damaging issue**, re-render, then re-score. Record the previous and new metrics plus a visual description in `ledger.md`. Do at least one meaningful revision, not a cosmetic color tweak.

See `references/critique.md` for the scoring rubric and red-team protocol.

## 7. Quality gates and delivery

Run `python scripts/validate_project.py PROJECT_DIR --video PROJECT_DIR/output/final.mp4` and save its report to `output/qa.json`. Run `python scripts/contact_sheet.py ...` and `python scripts/audio_report.py ...` if dependencies/audio are available. **Warnings are not passes.** Visually inspect checks that tools cannot reliably automate.

Release checklist:
- Exact duration, resolution, fps, playable H.264 MP4 (or requested codec), and no corrupt frames.
- First frame intentional; no black/blank > 0.5 s except purposeful planned fades, no frozen accidental sections.
- All scene starts/ends align; video/music/voice/sfx are synchronized to within one frame.
- On-screen text readable and safe in actual device context; aim for at least 4.5:1 normal text contrast; no overlapping type.
- No invented claims. Every factual claim traces to a source; every sourced visual is cleared or labelled appropriately.
- Cut/hit alignment within one frame, clean fades, appropriate loudness and true peak; no audible clipping or buried speech.
- Final logo, CTA, link, and product representation are actually correct. No placeholder assets, dead links, watermarks or borrowed footage.
- Final human/director critique says the film **holds up creatively**, not merely that the tests passed.

Deliver: `output/final.mp4`, `output/music-only.mp4` if applicable, `output/qa.json`, `output/contact-sheet.jpg`, `brief.md`, `timeline.json`, `facts.json`, `assets/asset-ledger.md`, `ledger.md`, and the code/rebuild command. Write a concise handoff describing concept, actual duration/fps, one design decision, any known limitations, and where to run the renderer. If no permission to use an asset or a sourced claim, cut it before delivery.

## Efficient path through this skill

```sh
# From the installed skill directory:
python scripts/init_project.py ./my-film --mode product --duration 15 --aspect 9:16 --fps 60
# Fill brief.md, facts.json, timeline.json, then implement a deterministic renderer.
python scripts/validate_project.py ./my-film
# Render according to references/production.md.
python scripts/validate_project.py ./my-film --video ./my-film/output/final.mp4 --json-out ./my-film/output/qa.json
python scripts/contact_sheet.py ./my-film/output/final.mp4 --output ./my-film/output/contact-sheet.jpg
python scripts/audio_report.py ./my-film/output/final.mp4
```

**Never** finish a job by merely claiming these commands were run. Execute, check exit codes, view outputs, and report failures truthfully.
