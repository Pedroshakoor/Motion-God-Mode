#!/usr/bin/env python3
"""Render an original 8-second MOTION GOD MODE motion teaser entirely in code, with synthesized score.

Not a generic production template: shows deterministic frame rendering + programmatic sound.
Requires Pillow and FFmpeg. Uses installed fonts for rasterized demo only; no font files are bundled.
"""
import argparse
import math
from pathlib import Path
import shutil
import subprocess
import struct
import tempfile
import wave

from PIL import Image, ImageDraw, ImageFont

INK = '#10120F'
LIME = '#D7FC65'
WHITE = '#EDF0E9'
DIM = '#666E61'
FPS = 24
DURATION = 8
FRAMES = FPS * DURATION
FONTS = ['/usr/share/fonts/opentype/inter/InterDisplay-Black.otf',
         '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']


def font(size):
    for p in FONTS:
        if Path(p).is_file(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def mix(a, b, t):return a+(b-a)*min(1,max(0,t))
def smooth(t): t=min(1,max(0,t));return t*t*(3-2*t)
def pop(t):
    t=max(0,t)
    return 1 - math.exp(-10*t) * math.cos(16*t) if t else 0


def text(draw, pos, value, size, color, anchor='la'):
    draw.text(pos, value, font=font(size), fill=color, anchor=anchor, stroke_width=0)


def draw_frame(f, w=960, h=540):
    t=f/FPS
    im=Image.new('RGB',(w,h), INK)
    d=ImageDraw.Draw(im)
    # Tiny rational grid: an editorial screen-space texture, not noise.
    for x in range(45,w,72):
        d.line((x,42,x,h-42),fill='#1C201A',width=1)
    for y in range(50,h,72):
        d.line((42,y,w-42,y),fill='#1C201A',width=1)
    d.rectangle((24,24,w-24,h-24),outline='#38402F',width=2)
    text(d,(48,38),'M / G',18,LIME)
    text(d,(w-48,43),f'{f:03d} / {FRAMES:03d}',13,DIM,'ra')
    d.line((48,h-49,w-48,h-49),fill='#556041',width=1)
    text(d,(48,h-38),'MOTION IS A DECISION.',14,LIME)
    text(d,(w-48,h-38),'MADE ENTIRELY IN CODE',13,DIM,'ra')
    # Single hero line persists across the entire sequence: progresses, folds into glyph/shape, then signs off.
    progress=t/DURATION
    d.rounded_rectangle((47,h-53,47+int((w-94)*progress),h-49),radius=2,fill=LIME)
    if t<1.9:
        u=smooth(t/.6)
        text(d,(60,194+int(mix(25,0,u))),'STOP',132,WHITE)
        text(d,(60,326),'SCROLLING.',111,LIME)
        # The same electric bar becomes a deliberate statement of intent.
        x=int(mix(80,760,smooth((t-.8)/.8)))
        d.rectangle((x,430,x+120,440),fill=LIME)
        text(d,(64,94),'A FILM SHOULD INTERRUPT.',21,WHITE)
    elif t<3.7:
        u=smooth((t-1.9)/.5)
        x=mix(-550,67,u)
        text(d,(int(x),200),'DIRECT.',126,LIME)
        text(d,(70,317),'DON\'T DECORATE.',66,WHITE)
        # shape inherited from previous bar stretches into underline and turns at the edge
        prog=smooth((t-2.55)/.8)
        d.rectangle((72,403,72+int(740*prog),413),fill=LIME)
        d.line((812,413,812,413-int(100*prog)),fill=LIME,width=12)
        text(d,(72,98),'01 / INTENT',18,DIM)
    elif t<5.6:
        u=smooth((t-3.7)/.7)
        cx,cy=int(mix(812,479,u)),235
        r=int(mix(20,105,u))
        # Bar curls into a ring: one idea, changing state.
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=LIME,width=14)
        sweep=smooth((t-4.1)/.9)
        d.line((cx-210,cy+159,cx-210+int(420*sweep),cy+159),fill=WHITE,width=4)
        text(d,(65,95),'02 / RHYTHM',18,DIM)
        text(d,(62,410),'EVERY FRAME EARNS IT.',45,WHITE)
        for j in range(7):
            xx=185+96*j
            yy=255+int(56*math.sin(t*3-j*.58))
            d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=WHITE)
    else:
        u=smooth((t-5.6)/.55)
        block_h=int(260*u)
        d.rectangle((44,125,w-44,125+block_h),fill=LIME)
        # Letterform is revealed as the hero resolves to its finished mark.
        if block_h>170:
            text(d,(64,250),'MOTION GOD MODE',69,INK)
        text(d,(65,430),'NO CAMERA. NO SLOP. JUST CINEMA, COMPILED.',21,WHITE)
        text(d,(65,94),'03 / THE SIGNATURE',18,DIM)
    return im


def score(path):
    sample_rate=24000
    n=DURATION*sample_rate
    keys=(55.0,65.406,73.416,82.407)  # original synth frequencies only
    with wave.open(str(path),'wb') as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(sample_rate)
        buf=bytearray()
        for i in range(n):
            t=i/sample_rate
            fade=min(1,t/.25,(DURATION-t)/.36)
            bass=.17*math.sin(2*math.pi*keys[int(t//2)%len(keys)]*t)
            pad=.06*math.sin(2*math.pi*110*t)+.04*math.sin(2*math.pi*164.81*t)
            beat_phase=(t*2)%1
            kick=.32*math.exp(-beat_phase*30)*math.sin(2*math.pi*(53+85*math.exp(-beat_phase*45))*beat_phase)
            ticks=.07*math.exp(-((t*4)%1)*52)*math.sin(2*math.pi*1300*t)
            # One beat of actual sonic silence/negative space before final mark.
            hole=min(1,abs(t-5.65)/.18)
            value=(bass+pad+kick+ticks)*fade*hole
            buf.extend(struct.pack('<h',int(max(-1,min(1,value))*32767)))
        out.writeframes(buf)


def render(path,w=960,h=540,fps=FPS,preview_gif=None):
    if fps != FPS: raise ValueError('Demo is authored for 24 fps; do not interpolate or retime it')
    if not shutil.which('ffmpeg'): raise RuntimeError('FFmpeg not found')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='motion-god-mode-demo-') as tmp:
        picture=Path(tmp)/'picture.mp4';wav=Path(tmp)/'score.wav'
        cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo',
             '-pixel_format','rgb24','-video_size',f'{w}x{h}','-framerate',str(fps),
             '-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','19',
             '-preset','fast','-movflags','+faststart',str(picture)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for i in range(FRAMES):proc.stdin.write(draw_frame(i,w,h).tobytes())
            proc.stdin.close();err=proc.stderr.read().decode(errors='replace');ret=proc.wait()
        except BrokenPipeError:
            err=proc.stderr.read().decode(errors='replace');proc.wait()
            raise RuntimeError(f'Frame encoder exited early: {err[-500:]}')
        if ret: raise RuntimeError(f'Frame encoding failed: {err[-500:]}')
        score(wav)
        mux=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(picture),'-i',str(wav),
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-af','loudnorm=I=-14:TP=-3.7:LRA=11','-ar','48000','-c:a','aac','-b:a','192k',
             '-t',str(DURATION),'-movflags','+faststart',str(path)]
        subprocess.run(mux,check=True)
    if preview_gif:
        # Compact looping preview for GitHub; continuous deterministic frames, rendered from same code.
        selected=[draw_frame(i,w,h).resize((480,270),Image.Resampling.LANCZOS).convert('P',palette=Image.Palette.ADAPTIVE,colors=64) for i in range(0,FRAMES,4)]
        target=Path(preview_gif);target.parent.mkdir(parents=True,exist_ok=True)
        selected[0].save(target,save_all=True,append_images=selected[1:],duration=int(1000*4/FPS),loop=0,optimize=True,disposal=2)
    print(f'Rendered {path}: {FRAMES} deterministic frames, {fps} fps, {DURATION}s, original synthesized score')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=Path('media/demo.mp4'))
    p.add_argument('--gif',type=Path,default=None)
    p.add_argument('--width',type=int,default=960)
    p.add_argument('--height',type=int,default=540)
    a=p.parse_args()
    render(a.out,a.width,a.height,preview_gif=a.gif)

if __name__=='__main__':main()
