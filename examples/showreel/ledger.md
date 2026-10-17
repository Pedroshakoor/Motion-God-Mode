# Creative ledger — original 8-second demonstration

## Baseline
- Renderer: `python scripts/render_demo.py --out media/demo.mp4 --gif media/preview.gif`.
- Timeline: 192 frames at 24 fps, 960×540; original synthesized score.
- Continuity idea: lime bar → typographic underline → ring → end-mark rectangle.
- QA first pass: video frame count and duration passed; audio initially measured -20.54 LUFS, too quiet for default online listening target.
- Visual review from contact sheet: end brand cropped by colored panel; one moving underline crossed secondary type; preview GIF did not scale full compositions correctly.

## Revision 1 — fix actual problems
- Move `MOTION GOD MODE` inside the lime end panel; it is no longer masked by the panel boundary.
- Move and shorten the second-scene underline to eliminate interference with text.
- Move `EVERY FRAME EARNS IT.` away from the footer safe line.
- Rasterize GIF from native-layout frames and scale afterward, instead of rendering native typography at half-sized canvas dimensions.
- Mix an original synthesized score to the target using FFmpeg loudness processing. Use -3.7 dBTP target headroom before AAC encoding to retain measured ≤ -3 dBTP.

## After re-render / objective checks
- Exact 8.000 s, 192 frames, 24.0 fps, 960×540, H.264 + AAC.
- Integrated loudness **-14.11 LUFS**; measured true peak **-3.64 dBTP** — passed default limits.
- Zero sampled black frames. Sampled still 6.2–7.8 seconds is the **intentional final mark hold**, not a frozen rendering defect.
- On-screen type verified on contact sheet. No factual assertions, borrowed media, claims or endorsements.
- Tests: six validator tests passed. `qa.json` and `audio-report.json` generated from actual output.

## Signoff limits
- This is a proof of deterministic rendering, readable type, asset-free shape animation and measured audio; not an independently commissioned professional film or a live-product reproduction.
- We conducted visual contact-sheet review, but **no independent external critic** has assessed this demo. Do not misrepresent it as blind-critic-approved.
