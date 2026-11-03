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

if __name__=='__main__':unittest.main()
