#!/usr/bin/env python3
"""Draw a themed pond around a transparent git-koi GIF.

Cyber Koi Pond by Dr Asegul Hulus (Ace). MIT licensed.
The input fish is generated separately by Anthony Yalong's git-koi.
"""
from pathlib import Path
import argparse
import json
import math
import random
from PIL import Image, ImageDraw, ImageSequence, ImageFont, ImageChops

DEFAULTS = {
    "title": "CYBER KOI POND",
    "subtitle": "ORGANIC INSTINCT. MACHINE INTELLIGENCE.",
    "theme": "teal",
    "robotic": True,
    "ai_label_1": "ARTIFICIAL",
    "ai_label_2": "INTELLIGENCE",
    "deep_learning_label": "DEEP LEARNING",
    "machine_learning_label": "MACHINE LEARNING",
    "cybersecurity_label": "CYBER DEFENCE",
}


def load_config(path=None):
    values = json.loads(Path(path).read_text(encoding="utf-8")) if path else {}
    if not isinstance(values, dict):
        raise ValueError("Configuration must be a JSON object.")
    unknown = values.keys() - DEFAULTS.keys()
    if unknown:
        raise ValueError("Unknown configuration keys: " + ", ".join(sorted(unknown)))
    config = DEFAULTS | values
    if config["theme"] not in ("teal", "midnight", "violet"):
        raise ValueError("theme must be teal, midnight or violet")
    if not isinstance(config["robotic"], bool):
        raise ValueError("robotic must be true or false")
    for key in DEFAULTS.keys() - {"theme", "robotic"}:
        limit = 42 if key in ("title", "subtitle") else 22
        if not isinstance(config[key], str) or len(config[key]) > limit:
            raise ValueError(f"{key} must be text of at most {limit} characters")
    return config


def render_pond(input_path, output_path, config=None, still_path=None):
    config = DEFAULTS | (config or {})
    src = Image.open(input_path)
    fish = [f.convert('RGBA').copy() for f in ImageSequence.Iterator(src)]
    durations = []
    for i in range(src.n_frames):
        src.seek(i)
        durations.append(src.info.get('duration', 70))
    src.close()
    boxes = [f.getbbox() for f in fish if f.getbbox()]
    if not boxes:
        raise ValueError('The input GIF contains no visible fish pixels.')
    box = (min(b[0] for b in boxes), min(b[1] for b in boxes),
           max(b[2] for b in boxes), max(b[3] for b in boxes))
    W, H = 800, 360
    base = Image.new('RGB', (W,H), '#101f29')
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((10,10,790,350),radius=70,fill='#34464b')
    d.rounded_rectangle((21,21,779,339),radius=61,fill='#62736c')
    d.rounded_rectangle((31,31,769,329),radius=53,fill='#0a424e')
    for j in range(16):
        c = (9+j//2, 65+j, 77+j)
        d.rounded_rectangle((38+j*3,38+j*3,762-j*3,322-j*3), radius=48,fill=c)
    rng = random.Random(7)
    for x in range(65,750,48):
        for y in (18,342):
            r = rng.randint(10,17)
            d.ellipse((x-r,y-7,x+r,y+7),fill=rng.choice(['#455b5a','#738379','#526764']))
    for x in (20,780):
        for y in (95,145,195,245,295):
            d.ellipse((x-9,y-14,x+9,y+14),fill='#526764')
    # Stones and plants belong to the scene; only the central koi represents activity.
    for x,y,r in [(113,104,30),(157,127,21),(668,248,33),(714,226,22),(624,269,21)]:
        d.ellipse((x-r+3,y-r+7,x+r+3,y+r+7),fill='#0a4650')
        d.pieslice((x-r,y-r,x+r,y+r),20,350,fill='#3c9677',outline='#75b88c',width=2)
        d.line((x,y,x+r*.65,y-r*.3),fill='#75b88c',width=2)
    for x,y in [(113,101),(669,246)]:
        for k in range(8):
            a=k*math.pi/4
            px,py=x+math.cos(a)*10,y+math.sin(a)*8
            d.ellipse((px-6,py-9,px+6,py+9),fill='#d482b0')
        d.ellipse((x-7,y-6,x+7,y+6),fill='#f6bbd2')
        d.ellipse((x-3,y-3,x+3,y+3),fill='#efd38c')
    font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    try:
        title=ImageFont.truetype(font_path,17)
        small=ImageFont.truetype(font_path,10)
    except OSError:
        title=small=ImageFont.load_default()
    d.text((400,62),config['title'],fill='#b6ded7',font=title,anchor='mm',stroke_width=0)
    d.text((400,84),config['subtitle'],fill='#75b9ba',font=small,anchor='mm')
    # An original, generic AI emblem: a brain connected to a processor.
    brain = [(228,77),(220,74),(212,78),(211,83),(205,85),(203,92),
             (207,98),(205,104),(210,111),(217,112),(221,117),(228,114),(228,77)]
    d.polygon(brain,fill='#123b50')
    d.line(brain,fill='#8cded8',width=2)
    d.line([(217,80),(219,87),(214,92),(219,99),(214,105),(219,111)],fill='#5bbec6',width=2)
    d.line([(207,92),(214,92)],fill='#5bbec6',width=2)
    d.line([(219,99),(227,99)],fill='#5bbec6',width=2)
    d.rounded_rectangle((232,79,257,111),radius=3,fill='#123b50',outline='#66d5db',width=2)
    d.text((245,95),'AI',fill='#c6fff2',font=small,anchor='mm')
    for yy in (84,94,104):
        d.line((228,yy,232,yy),fill='#8cded8',width=1)
        d.line((257,yy,263,yy),fill='#66d5db',width=2)
        d.ellipse((262,yy-1,264,yy+1),fill='#8cded8')
    for xx in (237,245,253):
        d.line((xx,74,xx,79),fill='#66d5db',width=2)
        d.line((xx,111,xx,116),fill='#66d5db',width=2)
    d.text((235,130),config['ai_label_1'],fill='#8bcac9',font=small,anchor='mm')
    d.text((235,143),config['ai_label_2'],fill='#8bcac9',font=small,anchor='mm')
    # A small neural-network motif in the left shallows.
    layers = [[(91,y) for y in (176,198,220)],
              [(117,y) for y in (165,187,209,231)],
              [(143,y) for y in (165,187,209,231)],
              [(169,y) for y in (187,209)]]
    for left,right in zip(layers,layers[1:]):
        for a in left:
            for b in right:
                d.line([a,b],fill='#226b77',width=1)
    for layer in layers:
        for x,y in layer:
            d.ellipse((x-3,y-3,x+3,y+3),fill='#77d1d0',outline='#258b9c')
    d.text((134,246),config['deep_learning_label'],fill='#73b5bb',font=small,anchor='mm')
    # Microchip motif in the opposite shallows.
    d.rounded_rectangle((648,117,694,159),radius=5,fill='#123b50',outline='#55bfc9',width=2)
    for off in range(7,40,8):
        d.line((648+off,111,648+off,117),fill='#55bfc9',width=2)
        d.line((648+off,159,648+off,165),fill='#55bfc9',width=2)
        d.line((642,117+off,648,117+off),fill='#55bfc9',width=2)
        d.line((694,117+off,700,117+off),fill='#55bfc9',width=2)
    d.text((671,138),'ML',fill='#b5f7ec',font=title,anchor='mm')
    d.text((671,183),config['machine_learning_label'],fill='#73b5bb',font=small,anchor='mm')
    # A shield and padlock represent cyber defence in the centre of the pond.
    shield = [(400,148),(424,157),(421,185),(413,198),(400,207),(387,198),(379,185),(376,157),(400,148)]
    d.polygon(shield,fill='#123b4c')
    d.line(shield,fill='#66c5cc',width=2)
    d.arc((392,164,408,181),180,360,fill='#a0ded7',width=2)
    d.rounded_rectangle((390,173,410,188),radius=3,fill='#a0ded7')
    d.ellipse((398,177,402,181),fill='#153b4e')
    d.line((400,180,400,184),fill='#153b4e',width=2)
    d.text((400,221),config['cybersecurity_label'],fill='#8bcac9',font=small,anchor='mm')
    # Circuit traces and data strings are decorative, not live security metrics.
    for points in [[(260,176),(295,176),(310,161),(353,161)],[(447,190),(485,190),(503,172),(535,172)],[(280,203),(310,203),(323,190),(353,190)]]:
        d.line(points,fill='#287280',width=1)
        for xx,yy in (points[0],points[-1]):
            d.ellipse((xx-2,yy-2,xx+2,yy+2),outline='#5caaaf')
    d.text((225,270),'01001001',fill='#327f88',font=small,anchor='mm')
    for x1,x2,label in [(170,213,'AI'),(222,357,'MACHINE LEARNING'),(366,480,'DEEP LEARNING'),(489,630,'CYBERSECURITY')]:
        d.rounded_rectangle((x1,286,x2,308),radius=8,fill='#103c4b',outline='#397b85')
        d.text(((x1+x2)/2,297),label,fill='#a2d8d3',font=small,anchor='mm')

    def cyborg(sprite, phase):
        # Preserve the live koi silhouette and organic tail; armour the head half.
        w,h = sprite.size
        split = int(w*.53)
        alpha = sprite.getchannel('A')
        robot_mask = Image.new('L',(w,h),0)
        ImageDraw.Draw(robot_mask).rectangle((split,0,w,h),fill=255)
        robot_mask = ImageChops.multiply(alpha,robot_mask)
        metal = sprite.copy()
        pixels = metal.load()
        for yy in range(h):
            for xx in range(split,w):
                red,green,blue,a = pixels[xx,yy]
                if not a:
                    continue
                if max(red,green,blue) < 85:
                    color = (19,37,58,a)
                else:
                    band = (xx-split)//12 % 2
                    shade = int(24*math.cos(yy/max(h,1)*math.pi))
                    color = (max(0,107+shade+band*28), max(0,141+shade+band*25), max(0,169+shade+band*22),a)
                pixels[xx,yy] = color
        # Position circuit traces and an optical sensor inside this frame's head.
        probe = int(w*.78)
        rows = [yy for yy in range(h) if alpha.getpixel((probe,yy))]
        mid = round(sum(rows)/len(rows)) if rows else h//2
        trace = Image.new('RGBA',(w,h),(0,0,0,0))
        td = ImageDraw.Draw(trace)
        for xx in range(split+7,w-8,14):
            td.line((xx,0,xx,h), fill='#34536b',width=2)
        td.line([(split,mid),(split+19,mid),(split+25,mid-5),(w-18,mid-5)],fill='#62f4ed',width=2)
        td.line([(split+26,mid),(split+35,mid+6),(w-28,mid+6)],fill='#39accc',width=2)
        td.line((split,0,split,h),fill='#bafbf2',width=2)
        eye_x=int(w*.9)
        eye_rows=[yy for yy in range(h) if alpha.getpixel((eye_x,yy))]
        eye_y=round(sum(eye_rows)/len(eye_rows)) if eye_rows else mid
        td.rectangle((eye_x-4,eye_y-4,eye_x+4,eye_y+3),fill='#102439')
        glow=round(195+50*(.5+.5*math.sin(phase*2)))
        td.rectangle((eye_x-2,eye_y-2,eye_x+2,eye_y+1),fill=(90,glow,245,255))
        td.point((eye_x,eye_y-1),fill='#ecffff')
        trace.putalpha(ImageChops.multiply(trace.getchannel('A'),robot_mask))
        metal.alpha_composite(trace)
        return metal
    if config['theme'] != 'teal':
        import colorsys
        shift = {'midnight': 0.10, 'violet': 0.27}[config['theme']]
        data=[]
        for red,green,blue in base.getdata():
            hue,sat,val=colorsys.rgb_to_hsv(red/255,green/255,blue/255)
            red,green,blue=colorsys.hsv_to_rgb((hue+shift)%1,sat,val)
            data.append((round(red*255),round(green*255),round(blue*255)))
        base.putdata(data)
    frames=[]
    fish = fish * 2
    durations = durations * 2
    for i,f in enumerate(fish):
        phase=2*math.pi*i/len(fish)
        frame=base.copy().convert('RGBA')
        draw=ImageDraw.Draw(frame)
        # Quiet wavelets follow the inner shore, clear of the labels and icons.
        for yy,start,end,offset in [(45,280,358,0),(45,490,570,1.7),(318,220,320,1),(318,460,555,2.2)]:
            points=[(xx,yy+2*math.sin((xx-start)*math.pi/38+phase+offset)) for xx in range(start,end+1)]
            draw.line(points,fill='#28616c',width=1)
            draw.line([(xx,yy+5+1.5*math.sin((xx-start)*math.pi/38+phase+offset)) for xx in range(start+10,end-10)],fill='#205761',width=1)
        for xx,start,end,offset in [(47,150,254,0),(752,99,195,2)]:
            points=[(xx+2*math.sin((yy-start)*math.pi/40+phase+offset),yy) for yy in range(start,end+1)]
            draw.line(points,fill='#28616c',width=1)
        # Signals move through the layers, suggesting a forward pass.
        activation = (i / len(fish) * 4) % 1
        active_layer = min(3,int(activation*4))
        for xx,yy in layers[active_layer]:
            draw.ellipse((xx-3,yy-3,xx+3,yy+3),fill='#b8fff0',outline='#61d6d4')
        for offset,points in enumerate([[(260,176),(295,176),(310,161),(353,161)],[(447,190),(485,190),(503,172),(535,172)]]):
            t=(i/len(fish)*3+offset*.5)%1
            section=min(2,int(t*3))
            frac=t*3-section
            a,b=points[section],points[section+1]
            xx=a[0]+(b[0]-a[0])*frac
            yy=a[1]+(b[1]-a[1])*frac
            draw.ellipse((xx-2,yy-2,xx+2,yy+2),fill='#8ce6e4')
        for x,y in [(304,110),(564,193),(252,251),(588,105)]:
            r=10+5*math.sin(phase+x)
            draw.arc((x-r*2,y-r*.5,x+r*2,y+r*.5),5,150,fill='#3d858b',width=1)
            draw.arc((x-r*2-6,y-r*.5-3,x+r*2+6,y+r*.5+3),190,310,fill='#246c77',width=1)
        cut=f.crop(box)
        scale=170/cut.width
        cut=cut.resize((170,round(cut.height*scale)),Image.Resampling.NEAREST)
        if config['robotic']:
            cut=cyborg(cut,phase)
        heading = -math.degrees(math.atan2(-60*math.sin(phase), 200*math.cos(phase)))
        cut=cut.rotate(heading,resample=Image.Resampling.NEAREST,expand=True)
        x=round(400+200*math.sin(phase)-cut.width/2)
        y=round(184+60*math.cos(phase)-cut.height/2)
        shadow=Image.new('RGBA',cut.size,(0,0,0,0))
        shadow.putalpha(cut.getchannel('A').point(lambda p: int(p*.16)))
        frame.alpha_composite(shadow,(x+5,y+10))
        frame.alpha_composite(cut,(x,y))
        if not frames:
            palette = frame.convert('RGB').quantize(colors=128)
        frames.append(frame.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE))
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(output_path.name + '.tmp.gif')
    try:
        frames[0].save(temporary, save_all=True, append_images=frames[1:], duration=durations,
                       loop=0, disposal=1, optimize=True)
        temporary.replace(output_path)
    finally:
        temporary.unlink(missing_ok=True)
    if still_path:
        Path(still_path).parent.mkdir(parents=True, exist_ok=True)
        frames[0].convert('RGB').save(still_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Transparent GIF generated by git-koi")
    parser.add_argument("--output", default="assets/pond.gif")
    parser.add_argument("--config", help="Optional JSON configuration file")
    parser.add_argument("--still", help="Optional still PNG output")
    args = parser.parse_args()
    try:
        output = render_pond(args.input, args.output, load_config(args.config), args.still)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(f"Created {output}")


if __name__ == "__main__":
    main()
