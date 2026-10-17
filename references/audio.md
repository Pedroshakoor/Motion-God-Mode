# Direct sound, don't decorate a silent slideshow

## First make a cue sheet

Place audio cues on the **same integer-frame timeline** as visuals. Example at 60 fps:

| Frame | Time | Cue | Visual purpose |
| --- | --- | --- | --- |
| 0 | 0.000 s | Low attack | Hook silhouette arrives |
| 42 | 0.700 s | First syncopated click | Secondary title enters |
| 105 | 1.750 s | Sub impulse, 0.15s | Circle transforms into physical object |
| 172 | 2.867 s | All sound drops for 0.35 s | Let the reveal land |

Music is a dramaturgical structure, not a wallpaper track. Compose or select a legal score with an intro, pulse, variation and conclusion; shift camera/cuts *with* that structure. Don't name an artist and ask the model to imitate them; describe instrumentation, energy, tempo and physical timbre.

## Mix order

1. Dialogue for clarity (if present). Record two distinct reads/takes per line; choose by character and emphasis, not by waveform smoothness.
2. Music to set tempo and emotion.
3. Effects for physical cause and consequence (impact, drag, release). Avoid auto-whoosh on every transform.
4. Silence to emphasize a dramatic beat.
5. Final measured master. Suggested online starting point: integrated -14 LUFS ±2 LU and true peak ≤ -3 dBTP. **These are defaults, not universal platform requirements**; honor platform brief if different.

Voice-over of an explainer is normally paced around 125–145 WPM, allowing room for moments of silence. On-screen text adds information instead of transcribing full voice lines. Characters shouldn't lip-sync when not speaking and mouth animation should be timed to actual dialogue.

## Operational checks

```sh
python scripts/audio_report.py my-film/output/final.mp4 --target -14 --peak-limit -3
# If needed, normalize intentionally AFTER listening to the unprocessed mix:
ffmpeg -i raw.wav -af 'loudnorm=I=-14:TP=-3:LRA=11' -ar 48000 mastered.wav
```

Check both headphones and phone speakers. Technical LUFS checks cannot detect bad voice intelligibility, distracting sound effects, wrong rhythm or mood.
