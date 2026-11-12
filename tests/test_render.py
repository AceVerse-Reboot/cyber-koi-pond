import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image,ImageDraw

spec=importlib.util.spec_from_file_location('pond',Path(__file__).parents[1]/'scripts/render_pond.py')
pond=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pond)

class RenderTests(unittest.TestCase):
    def test_config_rejects_invalid_options(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'config.json'
            for value in ({'theme':'unknown'},{'robotic':'yes'},{'unexpected':True}):
                path.write_text(json.dumps(value))
                with self.assertRaises(ValueError):pond.load_config(path)

    def test_empty_fish_keeps_existing_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'empty.gif';output=Path(folder)/'output.gif'
            Image.new('RGBA',(20,20),(0,0,0,0)).save(source,transparency=0)
            output.write_bytes(b'previous output')
            with self.assertRaises(ValueError):pond.render_pond(source,output)
            self.assertEqual(output.read_bytes(),b'previous output')

    def test_render_is_opaque_looping_gif(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'fish.gif';output=Path(folder)/'pond.gif'
            frames=[]
            for k in range(4):
                image=Image.new('RGBA',(64,32),(0,0,0,0))
                ImageDraw.Draw(image).ellipse((10,9+k,53,22+k),fill=(240,160,60,255))
                frames.append(image)
            frames[0].save(source,save_all=True,append_images=frames[1:],duration=80,loop=0,disposal=2)
            pond.render_pond(source,output,{'title':'TEST POND','robotic':False})
            with Image.open(output) as image:
                self.assertEqual(image.size,(800,360))
                self.assertEqual(image.info['loop'],0)
                self.assertGreater(image.n_frames,1)
                for k in range(image.n_frames):
                    image.seek(k)
                    self.assertEqual(image.convert('RGBA').getchannel('A').getextrema(),(255,255))

    def test_lapping_koi_stays_on_the_pond_oval(self):
        # git-koi's cruising koi laps its own frame; the pond must keep only its pose.
        import math
        shape=[(16,0),(10,-6),(0,-7),(-10,-4),(-20,-1),(-26,-1),(-26,1),(-20,1),(-10,4),(0,7),(10,6)]
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'fish.gif';output=Path(folder)/'pond.gif'
            frames=[]
            for k in range(40):
                angle=-math.pi/2+2*math.pi*k/40
                heading=angle+math.pi/2
                cx,cy=128+80*math.cos(angle),128+80*math.sin(angle)
                points=[(cx+x*math.cos(heading)-y*math.sin(heading),
                         cy+x*math.sin(heading)+y*math.cos(heading)) for x,y in shape]
                image=Image.new('RGBA',(256,256),(0,0,0,0))
                ImageDraw.Draw(image).polygon(points,fill=(255,128,0,255))
                frames.append(image)
            frames[0].save(source,save_all=True,append_images=frames[1:],duration=70,loop=0,disposal=2)
            pond.render_pond(source,output,{'robotic':False})
            with Image.open(output) as image:
                count=image.n_frames
                for k in range(count):
                    image.seek(k)
                    pixels=image.convert('RGB').load()
                    hits=[(x,y) for x in range(800) for y in range(360)
                          if pixels[x,y][0]>220 and 90<pixels[x,y][1]<170 and pixels[x,y][2]<60]
                    self.assertTrue(hits,f'koi missing in frame {k}')
                    mx=sum(p[0] for p in hits)/len(hits);my=sum(p[1] for p in hits)/len(hits)
                    phase=2*math.pi*k/count
                    self.assertLess(math.hypot(mx-(400+200*math.sin(phase)),my-(184+60*math.cos(phase))),12,
                                    f'koi left the oval in frame {k}')

if __name__=='__main__':unittest.main()
