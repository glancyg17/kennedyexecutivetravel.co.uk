#!/usr/bin/env python3
"""
16-seater visibility switch for kennedyexecutivetravel.co.uk

    python3 tools/16-seater/toggle.py status   # report current state (changes nothing)
    python3 tools/16-seater/toggle.py hide     # remove 16-seater details from the public pages
    python3 tools/16-seater/toggle.py show     # restore them (once the licence is in place)

What it touches: DISPLAY content only (page copy, fleet cards, airport price rows,
meta description, llms.txt). It does NOT touch the booking forms/dropdowns or the
dispatch app - those still accept "Mini Bus 15-16 Seater" bookings.

How it works: tools/16-seater/store.json holds, for each edit, the exact "show" text
and its "hide" replacement. `hide` swaps show -> hide; `show` swaps hide -> show.
Pure removals leave a tiny anchor comment (<!--@opt:id-->) so they can be restored
in the right place. Edits are made in the real HTML, so nothing is left in page source.

Safety: all-or-nothing. If any entry is in an unexpected state, nothing is written.
Run from anywhere; paths are resolved relative to the repo root.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
entries = json.loads((HERE / "store.json").read_text(encoding="utf-8"))["entries"]


def entry_state(text, e):
    """Return 'shown', 'hidden' or None (unrecognised) for one entry in the given file text."""
    has_show = e["show"] in text
    # a pure-removal hide marker is unique; a replacement hide text may be a normal string
    has_hide = e["hide"] in text
    if has_show and not has_hide:
        return "shown"
    if has_hide and not has_show:
        return "hidden"
    return None


def status():
    texts, states = {}, {}
    for e in entries:
        texts.setdefault(e["file"], (ROOT / e["file"]).read_text(encoding="utf-8"))
    for e in entries:
        t = texts[e["file"]]
        # Manchester/Liverpool rows share identical text: count-aware check
        if e["id"] in ("ap-manchester", "ap-liverpool"):
            same = e["show"]
            marker_m, marker_l = "<!--@opt:ap-manchester-->", "<!--@opt:ap-liverpool-->"
            n_show = t.count(same)
            hidden_here = (marker_m if e["id"] == "ap-manchester" else marker_l) in t
            # shown if its marker is absent and a row for it still exists
            other_marker = marker_l if e["id"] == "ap-manchester" else marker_m
            if hidden_here:
                states[e["id"]] = "hidden"
            else:
                expected_rows = 1 if other_marker in t else 2
                states[e["id"]] = "shown" if n_show == expected_rows else None
        else:
            states[e["id"]] = entry_state(t, e)
    return texts, states


def apply(mode):
    texts, states = status()
    want_from = "shown" if mode == "hide" else "hidden"
    want_to = "hidden" if mode == "hide" else "shown"
    bad = [i for i, s in states.items() if s is None]
    if bad:
        sys.exit(f"ABORTED - unrecognised state (files edited by hand?): {', '.join(bad)}\nNothing was changed.")
    todo = [e for e in entries if states[e["id"]] == want_from]
    if not todo:
        print(f"Already {want_to}. Nothing to do.")
        return
    new = dict(texts)
    for e in todo:  # entries are stored in file order, so identical rows resolve correctly
        src, dst = (e["show"], e["hide"]) if mode == "hide" else (e["hide"], e["show"])
        if new[e["file"]].count(src) < 1:
            sys.exit(f"ABORTED - cannot find text for {e['id']}. Nothing was changed.")
        new[e["file"]] = new[e["file"]].replace(src, dst, 1)
    for f, t in new.items():
        if t != texts[f]:
            (ROOT / f).write_text(t, encoding="utf-8", newline="")
    print(f"Done: 16-seater details are now {want_to.upper()} ({len(todo)} edits across "
          f"{len({e['file'] for e in todo})} files).")


def main():
    cmd = (sys.argv[1] if len(sys.argv) > 1 else "status").lower()
    if cmd == "status":
        _, states = status()
        vals = set(states.values())
        overall = "HIDDEN" if vals == {"hidden"} else "SHOWN" if vals == {"shown"} else "MIXED/UNKNOWN"
        print(f"16-seater details: {overall}")
        for e in entries:
            print(f"  {states[e['id']] or 'UNRECOGNISED':<13} {e['file']:<28} {e['id']}")
    elif cmd in ("hide", "show"):
        apply(cmd)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
