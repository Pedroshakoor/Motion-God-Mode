#!/usr/bin/env python3
"""Scaffold a MOTION GOD MODE film: python scripts/init_project.py ./film --mode product --duration 15 --aspect 9:16"""
import argparse
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
MODES = ('showreel', 'product', 'launch-story', 'explainer')
ASPECTS = {'16:9': (1920, 1080), '9:16': (1080, 1920), '1:1': (1080, 1080), '4:5': (1080, 1350)}


def compose_scenes(frames, fps, mode):
    target_seconds = {'showreel': 1.9, 'product': 2.5, 'launch-story': 2.6, 'explainer': 2.8}[mode]
    n = max(2, min(40, round(frames / (fps * target_seconds))))
    n = min(n, frames)
    purposes = {
        'showreel': ['Stop-scroll type', 'Type transforms into form', 'Form gains depth', 'Interface responds', 'One organic breath', 'Rewind-worthy handoff', 'End mark'],
        'product': ['Product-specific hook', 'Reveal real UI', 'User action', 'Visible result', 'Second use case', 'Emotional payoff', 'Official name and URL'],
        'launch-story': ['Character hook', 'Expectation', 'Obstacle', 'Reversal', 'Release', 'Brand reveal', 'Signoff'],
        'explainer': ['Hook', 'Familiar context', 'Disruption', 'Mechanism', 'Discovery', 'Consequence', 'Recap'],
    }[mode]
    scenes = []
    for i in range(n):
        start = round(i * frames / n)
        end = round((i+1) * frames / n)
        scenes.append({
            'id': f'scene-{i+1:02d}', 'start': start, 'end': end,
            'purpose': purposes[min(len(purposes)-1, i * len(purposes) // n)],
            'visual': 'DESIGN: choose one dominant hero shape, one hierarchy',
            'action': 'Animate anticipation, movement, follow-through and settle',
            'camera': 'Locked unless a motivated move is required',
            'type': 'Enter → hold → exit with readable duration',
            'audio': f'CUE: decide the audio at frame {start}',
            'claims': [], 'transition': 'Preserve a common visual thread',
            'proof': 'What is understood without sound'
        })
    return scenes


def init(path, mode, duration, aspect, fps):
    path = Path(path).expanduser().resolve()
    if path.exists() and any(path.iterdir()):
        raise ValueError(f'{path} is not empty. Refusing to overwrite. Choose a new directory.')
    path.mkdir(parents=True, exist_ok=True)
    for name in ['assets', 'output', 'src', 'references']:
        (path / name).mkdir(exist_ok=True)
    w, h = ASPECTS[aspect]
    frames = round(duration * fps)
    substitutions = dict(PROJECT=path.name, MODE=mode, DURATION=str(duration), ASPECT=aspect, FPS=str(fps), WIDTH=str(w), HEIGHT=str(h), FRAMES=str(frames))
    brief = (ROOT / 'assets/brief.template.md').read_text(encoding='utf8')
    for key, val in substitutions.items():
        brief = brief.replace('{{' + key + '}}', val)
    (path / 'brief.md').write_text(brief, encoding='utf8')
    for src, dst in [('assets/asset-ledger.template.md', 'assets/asset-ledger.md'), ('assets/creative-ledger.template.md', 'ledger.md')]:
        shutil.copyfile(ROOT / src, path / dst)
    (path / 'facts.json').write_text(json.dumps({'facts': []}, indent=2) + '\n', encoding='utf8')
    timeline = dict(project=path.name, mode=mode, fps=fps, duration_frames=frames,
                    width=w, height=h, aspect=aspect, sound='music + sfx',
                    scenes=compose_scenes(frames, fps, mode), audio_cues=[],
                    export={'container': 'mp4', 'video_codec': 'h264', 'audio_codec': 'aac',
                            'audio_target_lufs': -14, 'true_peak_limit_dbtp': -3})
    (path / 'timeline.json').write_text(json.dumps(timeline, indent=2) + '\n', encoding='utf8')
    (path / 'src/README.md').write_text('# Film renderer\n\nCreate your code-based renderer here. See MOTION GOD MODE references/production.md for frame-driven architecture.\n', encoding='utf8')
    print(f'Created {path} — {mode}, {frames} frames, {fps} fps, {w}×{h}')
    print('Next: fill brief.md and facts.json, replace placeholder scenes, build 3–5s animatic, render and run the QA tools.')
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', help='Directory to create (must be empty/new)')
    p.add_argument('--mode', choices=MODES, default='showreel')
    p.add_argument('--duration', type=float, default=15)
    p.add_argument('--aspect', choices=ASPECTS.keys(), default='16:9')
    p.add_argument('--fps', type=int, default=None)
    args = p.parse_args()
    fps = args.fps or (60 if args.mode == 'product' else 30 if args.mode == 'launch-story' else 24)
    if not (3 <= args.duration <= 300): p.error('--duration must be between 3 and 300 seconds')
    if not (12 <= fps <= 120): p.error('--fps must be between 12 and 120')
    try: init(args.directory, args.mode, args.duration, args.aspect, fps)
    except (ValueError, OSError) as exc: p.error(str(exc))

if __name__ == '__main__':
    main()
