#!/usr/bin/env python3
"""Validate a frame-accurate MOTION GOD MODE timeline, verified claims and optional rendered video."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import shutil
import subprocess
import sys

MANDATORY = ('id', 'start', 'end', 'purpose', 'visual', 'action', 'camera', 'type', 'audio', 'claims', 'transition', 'proof')


def _int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def validate(project: Path, video=None):
    errors, warnings, info = [], [], {}
    project = Path(project)
    timeline_file, facts_file, brief_file = [project / s for s in ('timeline.json', 'facts.json', 'brief.md')]
    if not brief_file.is_file(): warnings.append('Missing brief.md: decisions and creative intent are unauditable')
    for f in (timeline_file, facts_file):
        if not f.is_file(): errors.append(f'Missing required file: {f.name}')
    if errors: return {'passed': False, 'errors': errors, 'warnings': warnings, 'info': info}
    try:
        tl, data = json.loads(timeline_file.read_text()), json.loads(facts_file.read_text())
    except (json.JSONDecodeError, UnicodeError) as exc:
        return {'passed': False, 'errors': [f'Invalid JSON: {exc}'], 'warnings': warnings, 'info': info}
    fps, frames, width, height = (tl.get(x) for x in ('fps', 'duration_frames', 'width', 'height'))
    if not _int(fps) or fps < 1 or fps > 240: errors.append('fps must be an integer in 1..240')
    if not _int(frames) or frames < 1: errors.append('duration_frames must be a positive integer')
    if not _int(width) or not _int(height) or width < 100 or height < 100:
        errors.append('width/height must be integers ≥100')
    if _int(frames) and _int(fps) and fps > 0:
        info['expected_duration_seconds'] = round(frames / fps, 6)
    if tl.get('mode') not in ['showreel', 'product', 'launch-story', 'explainer']:
        errors.append('mode must be showreel, product, launch-story or explainer')
    scenes = tl.get('scenes')
    if not isinstance(scenes, list) or not scenes:
        errors.append('scenes must be a nonempty array'); scenes = []
    facts = data.get('facts') if isinstance(data, dict) else None
    if not isinstance(facts, list): errors.append('facts.json must contain a facts array'); facts = []
    facts_by_id = {}
    for i, fact in enumerate(facts):
        if not isinstance(fact, dict): errors.append(f'facts[{i}] must be an object'); continue
        fid = fact.get('id')
        if not isinstance(fid, str) or not fid: errors.append(f'facts[{i}] has no id'); continue
        if fid in facts_by_id: errors.append(f'Duplicate fact id: {fid}')
        facts_by_id[fid] = fact
    if len(scenes) > 1 and any(not isinstance(s, dict) for s in scenes):
        errors.append('scenes entries must be objects')
    expected_start, seen_ids = 0, set()
    for i, s in enumerate(scenes):
        if not isinstance(s, dict): continue
        sid = s.get('id') or f'index {i}'
        missing = [k for k in MANDATORY if k not in s]
        if missing: errors.append(f'{sid}: missing {", ".join(missing)}')
        if sid in seen_ids: errors.append(f'Duplicate scene id: {sid}')
        seen_ids.add(sid)
        start, end = s.get('start'), s.get('end')
        if not _int(start) or not _int(end): errors.append(f'{sid}: frame boundaries must be integers'); continue
        if start != expected_start: errors.append(f'{sid}: starts at {start}, expected {expected_start} (gap/overlap)')
        if end <= start: errors.append(f'{sid}: end frame must exceed start frame')
        if _int(frames) and end > frames: errors.append(f'{sid}: extends past final frame')
        if _int(fps) and fps > 0 and (end-start)/fps > 5:
            warnings.append(f'{sid}: composition lasts {(end-start)/fps:.1f}s; check for an intentional hold')
        expected_start = end
        claims = s.get('claims', [])
        if not isinstance(claims, list): errors.append(f'{sid}: claims must be an array'); continue
        for claim in claims:
            if not isinstance(claim, str): errors.append(f'{sid}: claim IDs must be strings'); continue
            fact = facts_by_id.get(claim)
            if not fact: errors.append(f'{sid}: missing source fact {claim}'); continue
            if fact.get('status') != 'verified': errors.append(f'{sid}: claim {claim} not verified')
            if not all(isinstance(fact.get(k), str) and fact[k].strip() for k in ('source','claim','evidence','verified_at')):
                errors.append(f'{sid}: claim {claim} lacks source/claim/evidence/verified_at')
        for field in ['purpose','visual','action','audio','proof']:
            text = str(s.get(field, ''))
            if any(q in text for q in ['DESIGN:', 'CUE:', 'TODO', 'PLACEHOLDER']):
                warnings.append(f'{sid}: {field} contains scaffold placeholder')
    if _int(frames) and expected_start != frames:
        errors.append(f'Last scene ends at {expected_start}; must end at frame {frames}')
    info['scene_count'] = len(scenes)
    info['verified_fact_count'] = sum(f.get('status') == 'verified' for f in facts if isinstance(f, dict))
    cues = tl.get('audio_cues', [])
    if not isinstance(cues, list): errors.append('audio_cues must be an array'); cues = []
    for j, cue in enumerate(cues):
        if not isinstance(cue, dict) or not _int(cue.get('frame')) or not _int(frames) or not 0 <= cue['frame'] < frames:
            errors.append(f'audio_cues[{j}]: frame must be an integer inside the film')
    if video:
        v = Path(video)
        if not v.is_file(): errors.append(f'Video not found: {v}')
        elif not shutil.which('ffprobe'): errors.append('ffprobe unavailable: requested video validation cannot be completed')
        else:
            command = ['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration', '-of', 'json', str(v)]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode: errors.append(f'ffprobe failed: {result.stderr.strip()[-400:]}')
            else:
                probe = json.loads(result.stdout)
                streams = probe.get('streams', [])
                vids = [x for x in streams if x.get('codec_type') == 'video']
                auds = [x for x in streams if x.get('codec_type') == 'audio']
                info['video_path'] = str(v)
                if not vids: errors.append('No video stream in render')
                else:
                    stream = vids[0]
                    info['video_codec'] = stream.get('codec_name')
                    if _int(width) and stream.get('width') != width: errors.append(f'Video width {stream.get("width")} ≠ {width}')
                    if _int(height) and stream.get('height') != height: errors.append(f'Video height {stream.get("height")} ≠ {height}')
                    try:
                        actual_fps = float(Fraction(stream['r_frame_rate']))
                        info['actual_fps'] = actual_fps
                        if _int(fps) and abs(actual_fps-fps) > .01: errors.append(f'Video fps {actual_fps:g} ≠ {fps}')
                    except (ValueError, KeyError, ZeroDivisionError): errors.append('Cannot determine video frame rate')
                    if stream.get('nb_frames', '').isdigit() and _int(frames) and int(stream['nb_frames']) != frames:
                        errors.append(f'Video frame count {stream["nb_frames"]} ≠ {frames}')
                try:
                    dur = float(probe['format']['duration'])
                    info['actual_duration_seconds'] = dur
                    if _int(fps) and fps > 0 and _int(frames) and abs(dur-frames/fps) > max(0.06, 1.5/fps):
                        errors.append(f'Container duration {dur:.3f}s ≠ expected {frames/fps:.3f}s')
                except (KeyError, TypeError, ValueError): warnings.append('Cannot read container duration')
                if not auds and tl.get('sound') != 'silent': errors.append('No audio stream; project sound is not silent')
                info['audio_stream_count'] = len(auds)
    return {'passed': not errors, 'errors': errors, 'warnings': warnings, 'info': info}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('project', type=Path)
    p.add_argument('--video', type=Path, default=None)
    p.add_argument('--json-out', type=Path, default=None)
    args = p.parse_args()
    report = validate(args.project, args.video)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    sys.exit(main())
