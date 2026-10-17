# Claims, source verification and permitted assets

## Fact discipline

Treat all claims as **unverified** until linked to a trustworthy primary source. A brand's marketing statement can accurately establish what it **claims**, but isn't necessarily independent evidence that results occur. Disclose uncertainty when appropriate.

`facts.json` production entry:

```json
{
  "facts": [
    {
      "id": "claim-001",
      "claim": "Product supports drag-and-drop task organization",
      "source": "https://example.com/features",
      "evidence": "Feature page says: 'Move tasks between lists by dragging them.'",
      "verified_at": "2026-10-17",
      "status": "verified"
    }
  ]
}
```

Then reference `claim-001` in each scene where that fact appears. If a scene uses the number `42%`, that number needs a supported fact ID; a number that is merely a design element must not be mistaken for a metric. Avoid client quotes, endorsements, real-person depictions or financial/health claims without suitable sourcing and authorization.

## Asset acquisition and rights

- Real product: prefer official downloadable SVG and permitted screenshot of the actual product. If SVG isn't accessible, use supplied official raster logo instead of recreating it with a similar font.
- Preserve exact colors, stroke weights, ratios and type as best the source permits. Verify with a screen comparison.
- External footage/music/layouts: *references only* unless license/permission is clear. Analyze cut timing and compositional principles, not replicate shots, original audio, logos or branded scenes.
- Generative pictures: references and concept boards only by default. If included in finished film with user consent, identify them correctly as concept/illustration; the skill's strict code-only path can instead create original vectors from the reference.
- Fonts: package only redistributable font binaries and comply with their licenses. Do not bundle commercial fonts borrowed from installed systems.
- On-screen brands: real third-party logos should never imply an endorsement or paying client without support.

## Asset ledger

Make one row per asset:

`Asset | source URI | owner | license/authorization | hash/version | transformation | scene`.

Record local capture datetime and app version when relevant. For site capture at 2× pixel density, preserve the source capture separately from the animated reconstruction.

## When the source is unavailable

Stop claiming real UI/product effects. Replace with a concept design *clearly marked* concept only if user consent covers concept material; otherwise return a truthfully incomplete result and list what source access is needed. No fabricated documentation or testimonials.
