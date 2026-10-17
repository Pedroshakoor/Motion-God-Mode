import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from init_project import init
from validate_project import validate

class TestMotionGodMode(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'sample'
        init(self.path,'product',10,'9:16',60)

    def tearDown(self): self.temp.cleanup()

    def test_scaffold_valid(self):
        self.assertTrue(validate(self.path)['passed'])

    def test_exact_frame_coverage(self):
        t=self._timeline()
        t['scenes'][1]['start']+=1
        self._write(t)
        self.assertFalse(validate(self.path)['passed'])
        self.assertTrue(any('gap/overlap' in s for s in validate(self.path)['errors']))

    def test_end_frame_required(self):
        t=self._timeline(); t['scenes'][-1]['end']-=1; self._write(t)
        self.assertFalse(validate(self.path)['passed'])

    def test_facts_must_be_verified(self):
        t=self._timeline(); t['scenes'][0]['claims']=['f-1'];self._write(t)
        (self.path/'facts.json').write_text(json.dumps({'facts':[{'id':'f-1','claim':'Fake','status':'unverified','source':'url','evidence':'text','verified_at':'2026-10-17'}]}))
        self.assertFalse(validate(self.path)['passed'])

    def test_verified_fact_ok(self):
        t=self._timeline();t['scenes'][0]['claims']=['f-1'];self._write(t)
        (self.path/'facts.json').write_text(json.dumps({'facts':[{'id':'f-1','claim':'Verified statement','status':'verified','source':'https://example.com','evidence':'Exact support','verified_at':'2026-10-17'}]}))
        self.assertTrue(validate(self.path)['passed'])

    def test_audio_cue_range(self):
        t=self._timeline();t['audio_cues']=[{'frame':t['duration_frames'],'event':'hit'}];self._write(t)
        self.assertFalse(validate(self.path)['passed'])

    def _timeline(self):return json.loads((self.path/'timeline.json').read_text())
    def _write(self,t):(self.path/'timeline.json').write_text(json.dumps(t))

if __name__ == '__main__':unittest.main()
