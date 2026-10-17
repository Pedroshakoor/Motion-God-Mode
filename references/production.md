# Code-rendering implementation guide

## Technical contract

All animation must be reproducible and controlled by a **frame index**. Output must be inspectable and re-renderable from versioned code, available assets and pinned dependencies.

### Frame math

```js
const fps = 60;
const durationFrames = 900;   // 15.000 s
const seconds = (frame) => frame / fps;
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const smooth = (t) => { t = clamp01(t); return t*t*(3-2*t); };
const moveX = (frame, from, to, start, end) =>
  from + (to - from) * smooth((frame - start) / (end - start));
```

Avoid `requestAnimationFrame`, `Date.now()`, `setTimeout`, browser random seeds, variable-size images loading mid-render, and animation state that depends on what frame was rendered previously. Rendering frame 417 before frame 12 must still yield the same pixels. If using a physics simulation, bake it ahead of time or seek deterministically from fixed seed and initial conditions.

### Toolchain A: Remotion

Best when React components and UI playback are available. Compose all scenes via timeline frames; move individual brand UI panels, not screenshots. Keep `durationInFrames`, `fps`, `width`, `height` in one config. Prefer interpolation/spring driven by the passed `frame`. If the project has Remotion already, use its existing dependencies and rendering CLI instead of migrating.

Representative React component pattern:

```tsx
import { useCurrentFrame, interpolate } from 'remotion';
export const Hero = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 24, 48], [-200, 0, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return <div style={{transform: `translateX(${x}px)`}}>ONE IDEA</div>;
};
```

### Toolchain B: HTML + SVG/GSAP render pipeline

Build a static DOM once, implement `renderFrame(frame)` that sets all visual properties from the passed frame, then drive it with an offline browser capture or programmatic renderer. For GSAP, a *paused* timeline can be deterministically sought to `frame/fps` (do not let it free-run). Export PNG sequence frames in deterministic order and encode:

```sh
ffmpeg -y -framerate 60 -i frames/%06d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 17 -preset slow -movflags +faststart picture.mp4
```

### Toolchain C: Pure Python/Pillow or SVG renderer

Suitable for portable offline prototypes and original vector/typographic pieces. Compute transformations from frame, draw them, feed raw RGB frames to FFmpeg. See `scripts/render_demo.py` for a **working** deterministic film sample that also synthesizes an original audio score. It is a technique demonstration, not a style pack to copy blindly.

### Audio mux

Render image-only MP4 with exact frame count, then mux a scored WAV. The `-shortest` option alone can hide duration drift; use `-t` at target seconds and validate after:

```sh
ffmpeg -y -i picture.mp4 -i original-score.wav \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k \
  -t 15 -movflags +faststart final.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames -of json final.mp4
```

For voice or third-party audio, obtain permissions/rights, record source and verify synchronization. Check loudness without overwriting source via `scripts/audio_report.py`.

## Sample production paths

```text
film-project/
  brief.md
  facts.json
  timeline.json
  ledger.md
  assets/
    asset-ledger.md
    official-logo.svg
    fonts/                   # only if properly licensed
  src/
    composition.tsx
    brand.ts
    soundtrack.ts
  output/
    animatic.mp4
    final.mp4
    contact-sheet.jpg
    qa.json
```

## Build and performance strategy

1. Renderer smoke test: 3–5 seconds of actual output; check frame 0 and the trickiest transition.
2. Low-res full-film draft: catch holes, readability failures and sound sync.
3. Full-resolution final only after storyboard pacing and music are stable.
4. Recompose separate timelines for 9:16 vs 16:9. Shared components, distinct layouts.
5. Render independent scenes in parallel only with frame-index deterministic code and versioned assets; verify the join frame and audio timeline.
6. Record exact commands and dependency versions in the film project's `README.md` or ledger.

## Compliance and safe defaults

Keep credentials in environment variables; never embed them in source or output. Use no unlicensed stock packs or vendor music. A script may fail if dependencies are missing: document the failure rather than claiming export happened.
