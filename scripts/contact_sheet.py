#!/usr/bin/env python3
"""Sample an MP4 into a labelled contact sheet; report dark, frozen and abrupt motion spans.

Requires FFmpeg and Pillow: pip install Pillow
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def sheet(video, output, every=0.2, cols=5, sample_width=280):
    from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat
    if every <= 0: raise ValueError('--every must be > 0')
    if not shutil.which('ffmpeg'): raise RuntimeError('ffmpeg not found')
    with tempfile.TemporaryDirectory(prefix='motion-god-mode-') as tmp:
        # -fps_mode vfr avoids obsolete -vsync and one invocation handles the whole video.
        command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(video),
                   '-vf', f'fps={1/every:.8f},scale={sample_width}:-2', '-fps_mode', 'vfr', f'{tmp}/%05d.png']
        r = subprocess.run(command, capture_output=True, text=True)
        if r.returncode: raise RuntimeError(f'ffmpeg extraction failed: {r.stderr[-400:]}')
        frames = sorted(Path(tmp).glob('*.png'))
        if not frames: raise RuntimeError('No frames extracted')
        if len(frames) > 1500: raise ValueError('Too many samples; increase --every to reduce memory')
        first = Image.open(frames[0]).convert('RGB')
        w, h = first.size; pad, header = 12, 26
        rows = (len(frames) + cols - 1) // cols
        canvas = Image.new('RGB', (cols * (w+pad)+pad, rows * (h+header+pad)+pad), '#151515')
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()
        dark_spans, still_spans, abrupt_changes = [], [], []
        previous_small = None
        for i, path in enumerate(frames):
            with Image.open(path) as raw: img = raw.convert('RGB')
            imgray = img.resize((64, 36)).convert('L')
            brightness = ImageStat.Stat(imgray).mean[0]
            if brightness < 9: dark_spans.append(round(i*every, 3))
            if previous_small is not None:
                delta = ImageStat.Stat(ImageChops.difference(previous_small, imgray)).mean[0]
                if delta < .22: still_spans.append(round(i*every,3))
                if delta > 45: abrupt_changes.append({'time_s': round(i*every,3), 'mean_delta': round(delta,1)})
            previous_small = imgray
            x = pad + (i%cols)*(w+pad); y = pad+(i//cols)*(h+header+pad)
            draw.text((x,y), f'{i*every:06.2f}s | sample {i:03d}', font=font, fill='white')
            canvas.paste(img,(x,y+header))
        def group_spans(instants):
            if not instants:return []
            groups=[]; first=last=instants[0]
            for t in instants[1:]:
                if t-last>every*1.1:
                    groups.append({'start_s':round(max(0,first-every),3),'end_s':last,'duration_s':round(last-max(0,first-every),3)})
                    first=t
                last=t
            groups.append({'start_s':round(max(0,first-every),3),'end_s':last,'duration_s':round(last-max(0,first-every),3)})
            return groups
        long_stills=[x for x in group_spans(still_spans) if x['duration_s']>=.5]
        long_darks=[x for x in group_spans(dark_spans) if x['duration_s']>=.5]
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output, quality=88)
        return {'samples':len(frames), 'sample_interval_s':every,
                'contact_sheet':str(output), 'sampled_dark_times_s':dark_spans,
                'sampled_still_times_s':still_spans,'long_still_spans_s':long_stills,'long_dark_spans_s':long_darks,'abrupt_sample_deltas':abrupt_changes,
                'interpretation':'Sample-based diagnostic only. Holds and fades may be intentional. Inspect dense 0.1s samples around cuts manually.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('video',type=Path)
    p.add_argument('--output',type=Path,default=Path('contact-sheet.jpg'))
    p.add_argument('--every',type=float,default=.2)
    p.add_argument('--cols',type=int,default=5)
    p.add_argument('--sample-width',type=int,default=280)
    p.add_argument('--json-out',type=Path,default=None)
    a=p.parse_args()
    if not a.video.is_file(): p.error(f'video not found: {a.video}')
    if a.cols<1 or a.sample_width<64: p.error('cols must be ≥1; sample-width ≥64')
    try: report=sheet(a.video,a.output,a.every,a.cols,a.sample_width)
    except (ValueError,RuntimeError,ImportError) as e: p.error(str(e))
    if a.json_out:
        a.json_out.parent.mkdir(parents=True,exist_ok=True)
        a.json_out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
