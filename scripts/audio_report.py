#!/usr/bin/env python3
"""Read integrated LUFS and measured true-peak from FFmpeg loudnorm stats; does NOT normalize audio."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


def report_audio(video, target=-14, peak_limit=-3, tolerance=2):
    if not shutil.which('ffmpeg'):
        raise RuntimeError('ffmpeg not installed')
    cmd=['ffmpeg','-hide_banner','-nostats','-i',str(video),'-af',
         f'loudnorm=I={target}:TP={peak_limit}:LRA=11:print_format=json',
         '-f','null','-']
    r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if r.returncode: raise RuntimeError(f'FFmpeg audio analysis failed: {r.stderr[-600:]}')
    # JSON from filter is normally emitted to stderr after processing.
    matches=re.findall(r'\{\s*"input_i"\s*:\s*"[^"\n]+".*?\}',r.stderr,re.S)
    if not matches: raise RuntimeError('No loudnorm statistics found (video may not have an audio stream)')
    measurement=json.loads(matches[-1])
    def safe(key):
        try: return float(measurement[key])
        except (KeyError,TypeError,ValueError): return None
    lufs,tp=safe('input_i'),safe('input_tp')
    issues=[]
    if lufs is None: issues.append('Cannot measure integrated loudness')
    elif abs(lufs-target)>tolerance: issues.append(f'Integrated loudness {lufs:.1f} LUFS is outside {target}±{tolerance} LU')
    if tp is None: issues.append('Cannot measure true peak')
    elif tp>peak_limit: issues.append(f'True peak {tp:.1f} dBTP exceeds {peak_limit} dBTP limit')
    return {'passed':not issues,'target_lufs':target,'tolerance_lu':tolerance,
            'true_peak_limit_dbtp':peak_limit,'measured_lufs':lufs,'measured_true_peak_dbtp':tp,
            'issues':issues,'raw':measurement,
            'note':'Technical loudness only. Also listen on phone speakers and headphones for voice clarity and creative balance.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('video',type=Path)
    p.add_argument('--target',type=float,default=-14)
    p.add_argument('--peak-limit',type=float,default=-3)
    p.add_argument('--tolerance',type=float,default=2)
    p.add_argument('--json-out',type=Path,default=None)
    a=p.parse_args()
    try: out=report_audio(a.video,a.target,a.peak_limit,a.tolerance)
    except (RuntimeError,OSError) as e: p.error(str(e))
    if a.json_out:
        a.json_out.parent.mkdir(parents=True,exist_ok=True)
        a.json_out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return 0 if out['passed'] else 1

if __name__=='__main__': sys.exit(main())
