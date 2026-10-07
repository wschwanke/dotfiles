#!/usr/bin/env python3
"""Scroll the focused herdr pane by half a viewport. Usage: herdr-halfpage.py up|down"""
import json, os, socket, sys

sock = os.environ.get("HERDR_SOCKET_PATH", os.path.expanduser("~/.config/herdr/herdr.sock"))


def call(method, params):
    s = socket.socket(socket.AF_UNIX)
    s.connect(sock)
    s.sendall((json.dumps({"id": "halfpage", "method": method, "params": params}) + "\n").encode())
    buf = b""
    while not buf.endswith(b"\n"):
        chunk = s.recv(65536)
        if not chunk:
            break
        buf += chunk
    s.close()
    return json.loads(buf)["result"]


direction = sys.argv[1] if len(sys.argv) > 1 else "up"
pane = call("pane.current", {})["pane"]
sc = pane["scroll"]
step = max(1, sc["viewport_rows"] // 2)
off = sc["offset_from_bottom"] + (step if direction == "up" else -step)
off = min(max(off, 0), sc["max_offset_from_bottom"])
call("pane.scroll", {"pane_id": pane["pane_id"], "offset_from_bottom": off})
