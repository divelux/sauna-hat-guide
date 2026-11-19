#!/usr/bin/env python3
"""Adds PDF metadata and writes the final guide.pdf / slides.pdf from the raw Chromium output."""
import os
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = "The Sauna Hat Guide: Why Heat Rises and What to Wear on Your Head"
META = {
    "/Author": "DIVELUX",
    "/Creator": "DIVELUX (https://diveluxsaunahat.com)",
    "/Subject": ("A plain-language guide to sauna hats: heat stratification in the sauna, wool felt as insulation, "
                 "choosing, wearing and caring for a hat, etiquette, and typical temperatures by sauna type."),
    "/Keywords": ("sauna hat, wool felt sauna hat, banya hat, sauna etiquette, sauna temperature, Finnish sauna, "
                  "Russian banya, heat stratification, sauna for beginners, DIVELUX"),
    "/CreationDate": "D:20261119000000Z",
    "/ModDate": "D:20261119000000Z",
}

for raw, out, title in [("guide-raw.pdf", "guide.pdf", TITLE),
                        ("slides-raw.pdf", "slides.pdf", TITLE + " (Slides)")]:
    r = PdfReader(os.path.join(HERE, raw))
    w = PdfWriter(clone_from=r)
    w.add_metadata({**META, "/Title": title})
    w.compress_identical_objects()
    with open(os.path.join(HERE, out), "wb") as f:
        w.write(f)
    os.remove(os.path.join(HERE, raw))
    print(out, len(r.pages), "pages", os.path.getsize(os.path.join(HERE, out)) // 1024, "KB")
