from __future__ import annotations
import contextlib, functools, http.server, os, shutil, threading
from pathlib import Path
from urllib.parse import quote


def browser_executable():
    return (os.environ.get("CHROME_PATH") or shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome") or shutil.which("google-chrome-stable"))


def launch_chromium(playwright, headless=True):
    kwargs={"headless": headless}
    exe=browser_executable()
    if exe: kwargs["executable_path"]=exe
    return playwright.chromium.launch(**kwargs)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


@contextlib.contextmanager
def serve_directory(directory: Path):
    directory=Path(directory).resolve()
    handler=functools.partial(QuietHandler, directory=str(directory))
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/"
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)


@contextlib.contextmanager
def serve_file(path: Path):
    path=Path(path).resolve()
    with serve_directory(path.parent) as base:
        yield base + quote(path.name)
