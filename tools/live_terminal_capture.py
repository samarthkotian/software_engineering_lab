"""Stream the actual local test runner into an xterm browser terminal.

Start with Python from the lab testing environment. The browser is a passive
terminal display; all test commands start here, not from browser input.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import importlib.util
import json
import shutil
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parents[1] / 'live_terminal_control'
WORK.mkdir(exist_ok=True)
SCREEN = {'text': '', 'revision': 0}
LOCK = threading.Lock()
ORIGINAL_STDOUT = sys.stdout


class Stream:
    def write(self, value):
        with LOCK:
            if '\033[2J\033[H' in value:
                SCREEN['text'] = ''
                value = value.split('\033[2J\033[H')[-1]
            SCREEN['text'] += value
            SCREEN['revision'] += 1
        return len(value)

    def flush(self):
        pass


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORK), **kwargs)

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == '/screen.json':
            with LOCK:
                payload = json.dumps(SCREEN).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(payload)
        else:
            super().do_GET()


def run_tests():
    spec = importlib.util.spec_from_file_location('capture_runner', ROOT/'tools/capture_terminal_evidence.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.CONTROL = WORK
    runner.BEFORE = WORK / 'original_lab7'
    runner.BEFORE.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'lab7/original/salon_booking.py', runner.BEFORE/'salon_booking.py')
    shutil.copy2(ROOT/'lab7/test_processor.py', runner.BEFORE/'test_processor.py')
    sys.stdout = Stream()
    try:
        runner.main()
    except Exception:
        import traceback
        with LOCK:
            SCREEN['text'] += traceback.format_exc()
            SCREEN['revision'] += 1
        (WORK/'error.ready').write_text('error')
    finally:
        sys.stdout = ORIGINAL_STDOUT


PAGE = '''<!doctype html><html><head><meta charset="utf-8">
<title>SE Lab - Live Terminal</title>
<link rel="stylesheet" href="xterm.css">
<style>body{margin:0;background:#101820;color:#e8eef2;font:16px Segoe UI}
header{padding:14px 22px;background:#1c2b38;border-bottom:1px solid #456}
header b{font-size:20px} header span{float:right;color:#8dd6e8}
#terminal{padding:18px 22px} footer{padding:10px 22px;color:#9daeba;font-size:13px}
</style></head><body><header><b>Software Engineering - Live Test Terminal</b>
<span>Local test runner | xterm.js</span></header><div id="terminal"></div>
<footer>Live process output from the assigned Salon Booking application. No output is simulated.</footer>
<script src="xterm.js"></script><script>
const terminal = new Terminal({cols:126,rows:43,fontFamily:'Consolas, monospace',fontSize:16,
 theme:{background:'#101820',foreground:'#e8eef2'},cursorBlink:false,disableStdin:true,
 scrollback:2000,convertEol:true});
terminal.open(document.getElementById('terminal'));
let revision=-1;
async function refresh(){try{const state=await(await fetch('/screen.json')).json();
if(state.revision!==revision){revision=state.revision; terminal.reset(); terminal.write(state.text);}}
catch(error){} setTimeout(refresh,250);} refresh();
</script></body></html>'''


if __name__ == '__main__':
    (WORK/'index.html').write_text(PAGE, encoding='utf-8')
    server = ThreadingHTTPServer(('127.0.0.1',8766), Handler)
    print('Live terminal at http://127.0.0.1:8766', flush=True)
    threading.Thread(target=run_tests,daemon=True).start()
    server.serve_forever()
