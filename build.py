#!/usr/bin/env python3
"""Builds guide.html (Letter) and slides.html (16:9) for The Sauna Hat Guide.

The temperature table is read from ../dataset/sauna_traditions.csv so the guide
and the dataset always agree. Render to PDF with:  node render.js
"""
import csv
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://diveluxsaunahat.com"
TOOLS = "https://diveluxsaunahat.com/pages/sauna-tools"
TITLE = "The Sauna Hat Guide: Why Heat Rises and What to Wear on Your Head"
DESC = ("A plain-language guide to sauna hats: why the air near the ceiling is hottest, how wool felt "
        "insulates, how to choose, wear and care for a hat, sauna etiquette, and typical temperatures by sauna type.")

# ---------------------------------------------------------------- data
with open(os.path.join(HERE, "..", "dataset", "sauna_traditions.csv"), newline="", encoding="utf-8") as f:
    ROWS = [r for r in csv.DictReader(f) if r["typical_air_temp_c_min"]]

SHORT = {"North American gym or club sauna": "North American gym sauna",
         "Bio sauna (soft sauna)": "Bio sauna (soft sauna)"}


def rng(a, b, unit=""):
    return f"{a}–{b}{unit}" if a else "—"


def temp_table(names=None, compact=False):
    out = ['<table class="temps"><thead><tr><th>Type</th><th class="n">Air, °C</th>'
           '<th class="n">Air, °F</th><th>Humidity</th>']
    if not compact:
        out.append('<th class="n">Round, min</th><th>Water on stones</th>')
    out.append("</tr></thead><tbody>")
    for r in ROWS:
        if names and r["name"] not in names:
            continue
        hum = r["typical_relative_humidity"] or "—"
        if r["typical_relative_humidity_pct_min"]:
            hum += f' ({r["typical_relative_humidity_pct_min"]}–{r["typical_relative_humidity_pct_max"]}%)'
        out.append(f'<tr><td>{html.escape(SHORT.get(r["name"], r["name"]))}</td>'
                   f'<td class="n">{rng(r["typical_air_temp_c_min"], r["typical_air_temp_c_max"])}</td>'
                   f'<td class="n">{rng(r["typical_air_temp_f_min"], r["typical_air_temp_f_max"])}</td>'
                   f'<td>{hum}</td>')
        if not compact:
            stones = {"n-a": "no stones"}.get(r["water_on_stones"], r["water_on_stones"] or "—")
            out.append(f'<td class="n">{rng(r["typical_round_minutes_min"], r["typical_round_minutes_max"])}</td>'
                       f'<td>{stones}</td>')
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


# ---------------------------------------------------------------- SVG
def strat_svg(cls="strat"):
    return f'''<svg class="{cls}" viewBox="0 0 680 400" role="img" aria-label="Cross-section of a sauna showing hotter air near the ceiling and cooler air near the floor">
<defs><clipPath id="room"><rect x="20" y="20" width="420" height="360" rx="6"/></clipPath></defs>
<g clip-path="url(#room)">
<rect x="20" y="20" width="420" height="90" fill="#f0a877"/>
<rect x="20" y="110" width="420" height="90" fill="#f5c7a0"/>
<rect x="20" y="200" width="420" height="90" fill="#f8dfc6"/>
<rect x="20" y="290" width="420" height="90" fill="#fbf1e5"/>
<!-- benches -->
<rect x="300" y="238" width="140" height="142" fill="#c99b6c"/>
<rect x="215" y="306" width="85" height="74" fill="#c99b6c"/>
<path d="M300 238H440M215 306H300M300 238V306" stroke="#1b1512" stroke-width="2" fill="none"/>
<path d="M300 258H440M215 326H300" stroke="#7a4e2d" stroke-width="1.2" fill="none" opacity=".7"/>
<!-- stove -->
<rect x="52" y="312" width="78" height="68" rx="4" fill="#2a1b13"/>
<g fill="#6f655c" stroke="#1b1512" stroke-width="1.5">
<circle cx="66" cy="306" r="9"/><circle cx="84" cy="302" r="10"/><circle cx="103" cy="305" r="9"/><circle cx="118" cy="308" r="7"/><circle cx="75" cy="292" r="8"/><circle cx="95" cy="289" r="8"/></g>
<g fill="none" stroke="#1b1512" stroke-width="1.6" stroke-linecap="round" opacity=".55">
<path d="M70 268c-8-12 8-18 0-30s8-18 0-30"/><path d="M90 262c-8-12 8-18 0-30s8-18 0-30s8-18 0-30"/><path d="M110 268c-8-12 8-18 0-30s8-18 0-30"/></g>
<!-- bather -->
<path d="M352 238v52a8 8 0 0 0 8 8h4a8 8 0 0 0 8-8v-52zM380 238v52a8 8 0 0 0 8 8h4a8 8 0 0 0 8-8v-52z" fill="#e9c9a8" stroke="#1b1512" stroke-width="2"/>
<path d="M346 240v-44c0-16 12-26 30-26s30 10 30 26v44z" fill="#e9c9a8" stroke="#1b1512" stroke-width="2"/>
<circle cx="376" cy="146" r="19" fill="#e9c9a8" stroke="#1b1512" stroke-width="2"/>
<path d="M349 150c3-26 12-46 27-46s24 20 27 46c-18 5-36 5-54 0z" fill="#f0762e" stroke="#1b1512" stroke-width="2" stroke-linejoin="round"/>
<circle cx="376" cy="100" r="5" fill="none" stroke="#1b1512" stroke-width="2"/>
</g>
<rect x="20" y="20" width="420" height="360" rx="6" fill="none" stroke="#1b1512" stroke-width="2.5"/>
<g stroke="#1b1512" stroke-width="1" stroke-dasharray="3 4" opacity=".6"><path d="M440 65H468M440 155H468M440 245H468M440 335H468"/></g>
<g font-family="Inter, sans-serif" fill="#1b1512">
<text x="476" y="60" font-size="15" font-weight="600">Under the ceiling</text><text x="476" y="78" font-size="15" fill="#3d332c">about 100 °C / 212 °F</text>
<text x="476" y="150" font-size="15" font-weight="600">Head height, top bench</text><text x="476" y="168" font-size="15" fill="#3d332c">about 88 °C / 190 °F</text>
<text x="476" y="240" font-size="15" font-weight="600">Bench level</text><text x="476" y="258" font-size="15" fill="#3d332c">about 71 °C / 160 °F</text>
<text x="476" y="330" font-size="15" font-weight="600">Floor</text><text x="476" y="348" font-size="15" fill="#3d332c">about 40 °C / 105 °F</text>
</g></svg>'''


def felt_svg():
    import random
    rnd = random.Random(7)
    fibers = []
    for _ in range(230):
        x, y = rnd.uniform(250, 390), rnd.uniform(24, 166)
        a, b = rnd.uniform(-26, 26), rnd.uniform(-22, 22)
        c, d = rnd.uniform(-18, 18), rnd.uniform(-18, 18)
        fibers.append(f"M{x:.0f} {y:.0f}q{c:.0f} {d:.0f} {a:.0f} {b:.0f}")
    waves = "".join(f'<path d="M40 {y}c14-10 28 10 42 0s28 10 42 0 28 10 42 0 28 10 42 0h14m-9-7 9 7-9 7"/>' for y in (58, 95, 132))
    thin = "".join(f'<path d="M420 {y}h46m-7-6 7 6-7 6"/>' for y in (76, 114))
    return f"""<svg class="felt" viewBox="0 14 640 162" role="img" aria-label="Diagram: hot air on one side, a layer of wool felt with trapped air in the middle, the head on the other side">
<rect x="0" y="16" width="240" height="158" fill="#f5c7a0"/><rect x="400" y="16" width="240" height="158" fill="#fbf1e5"/>
<rect x="240" y="16" width="160" height="158" fill="#b9b4ac"/>
<clipPath id="fc"><rect x="240" y="16" width="160" height="158"/></clipPath>
<path clip-path="url(#fc)" d="{''.join(fibers)}" fill="none" stroke="#3d332c" stroke-width="1.1" opacity=".75"/>
<path d="M240 16V174M400 16V174" stroke="#1b1512" stroke-width="2.5"/>
<g fill="none" stroke="#1b1512" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{waves}</g>
<g fill="none" stroke="#1b1512" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" opacity=".7">{thin}</g>
<g font-family="Inter, sans-serif" font-size="13" fill="#1b1512">
<text x="14" y="36" font-weight="600">Hot room air</text>
<text x="490" y="90" font-weight="600">Your head</text><text x="490" y="108" fill="#3d332c">Less heat gets</text><text x="490" y="124" fill="#3d332c">through, more slowly</text>
</g></svg>"""


BELL_SVG = '''<svg viewBox="0 0 200 170" role="img" aria-label="Bell-shaped sauna hat silhouette"><circle cx="100" cy="17" r="9" fill="none" stroke="#1b1512" stroke-width="4"/><path d="M22 152C30 96 58 26 100 26s70 70 78 126c-52 10-104 10-156 0z" fill="#8f8a83" stroke="#1b1512" stroke-width="3" stroke-linejoin="round"/><path d="M100 28V158" stroke="#1b1512" stroke-width="1.5" stroke-dasharray="4 5" opacity=".5"/></svg>'''
BUCKET_SVG = '''<svg viewBox="0 0 200 170" role="img" aria-label="Bucket-shaped sauna hat silhouette with a brim"><path d="M58 50c28-7 56-7 84 0l12 62H46z" fill="#8f8a83" stroke="#1b1512" stroke-width="3" stroke-linejoin="round"/><path d="M46 110c36 6 72 6 108 0l28 40c-54 10-110 10-164 0z" fill="#a39e97" stroke="#1b1512" stroke-width="3" stroke-linejoin="round"/></svg>'''
FOLD_SVG = '''<svg viewBox="0 0 200 170" role="img" aria-label="Bell hat with the edge folded up"><circle cx="100" cy="17" r="9" fill="none" stroke="#1b1512" stroke-width="4"/><path d="M30 132C40 88 62 26 100 26s60 62 70 106c-46 9-94 9-140 0z" fill="#8f8a83" stroke="#1b1512" stroke-width="3" stroke-linejoin="round"/><path d="M26 136c50 10 98 10 148 0l-3-22c-48 9-94 9-142 0z" fill="#bdb8b0" stroke="#1b1512" stroke-width="3" stroke-linejoin="round"/></svg>'''

_I = 'fill="none" stroke="#1b1512" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
_NO = '<path d="M10 10L54 54" stroke="#b5411a" stroke-width="4" stroke-linecap="round"/>'
ICONS = {
    "cool": f'<svg viewBox="0 0 64 64" {_I}><path d="M8 26h48l-5 26H13z"/><path d="M4 26h56"/><path d="M18 38c4-4 8 4 12 0s8 4 12 0 4-2 6-1"/><path d="M32 6v10M27 9l10 4M37 9l-10 4"/></svg>',
    "hand": f'<svg viewBox="0 0 64 64" {_I}><path d="M8 28h48l-5 24H13z"/><path d="M4 28h56"/><path d="M24 40V16a3 3 0 0 1 6 0v12V12a3 3 0 0 1 6 0v16V15a3 3 0 0 1 6 0v17l4-5a3 3 0 0 1 5 3l-7 12"/></svg>',
    "squeeze": f'<svg viewBox="0 0 64 64" {_I}><path d="M20 46c2-16 6-28 12-28s10 12 12 28c-8 2-16 2-24 0z"/><path d="M4 34h10M10 29l5 5-5 5M60 34H50M54 29l-5 5 5 5"/><path d="M28 54v4M36 54v4"/></svg>',
    "air": f'<svg viewBox="0 0 64 64" {_I}><path d="M6 8h52"/><circle cx="32" cy="13" r="4"/><path d="M18 50c2-18 7-33 14-33s12 15 14 33c-9 2-19 2-28 0z"/><path d="M6 30c3-3 3 3 6 0M52 30c3-3 3 3 6 0M6 42c3-3 3 3 6 0M52 42c3-3 3 3 6 0"/></svg>',
    "nomachine": f'<svg viewBox="0 0 64 64" {_I}><rect x="12" y="8" width="40" height="48" rx="4"/><path d="M12 20h40"/><circle cx="32" cy="38" r="11"/><circle cx="20" cy="14" r="1.2"/>{_NO}</svg>',
    "nodryer": f'<svg viewBox="0 0 64 64" {_I}><rect x="10" y="10" width="44" height="44" rx="4"/><circle cx="32" cy="32" r="15"/><circle cx="32" cy="32" r="2.5" fill="#1b1512"/>{_NO}</svg>',
    "nohot": f'<svg viewBox="0 0 64 64" {_I}><path d="M8 34h48l-4 20H12z"/><path d="M4 34h56"/><path d="M22 26c-4-5 4-7 0-12M32 26c-4-5 4-7 0-12M42 26c-4-5 4-7 0-12"/>{_NO}</svg>',
}

CARE = [("cool", "Cool water", "Room temperature, about 20–24 °C (68–75 °F). Never warm or hot."),
        ("hand", "Hand wash only", "A little mild soap. Press the felt gently; do not scrub hard."),
        ("squeeze", "Squeeze, do not wring", "Press the water out between your palms or in a towel."),
        ("air", "Air dry", "Shape it by hand and hang it by the loop or set it over a jar.")]
CARE_NO = [("nomachine", "No washing machine"), ("nodryer", "No dryer"), ("nohot", "No warm or hot water")]

FONT_CSS = '''
@font-face{font-family:"Bricolage Grotesque";src:url("fonts/BricolageGrotesque-var.woff2") format("woff2");font-weight:400 800;font-display:block}
@font-face{font-family:"Inter";src:url("fonts/Inter-var.woff2") format("woff2");font-weight:400 700;font-display:block}
:root{--paper:#f6f3ee;--paper-2:#ede8df;--card:#fffdf9;--ink:#1b1512;--ink-2:#3d332c;--muted:#6f655c;--line:#dcd4c8;--wood:#c99b6c;--spruce:#1d5c45;--ember:#f0762e;--r:6px;
--display:"Bricolage Grotesque",system-ui,sans-serif;--body:"Inter",system-ui,sans-serif}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--paper);color:var(--ink);font-family:var(--body);-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:var(--spruce);text-decoration:underline;text-underline-offset:2px}
h1,h2,h3{font-family:var(--display);margin:0;font-variation-settings:"opsz" 48}
p{margin:0}
table.temps{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
table.temps th{font-weight:600;text-align:left;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);vertical-align:bottom}
table.temps td{border-bottom:1px solid var(--line)}
table.temps td:first-child{font-weight:600}
table.temps .n{text-align:right;white-space:nowrap}
table.temps th:nth-child(4),table.temps td:nth-child(4){padding-left:18px}
table.temps th:last-child,table.temps td:last-child{padding-left:18px}
'''

# ================================================================ GUIDE
GUIDE_CSS = FONT_CSS + '''
@page{size:8.5in 11in;margin:0}
body{font-size:11.4pt;line-height:1.56}
.page{position:relative;width:8.5in;height:11in;padding:.8in .85in .95in;overflow:hidden;page-break-after:always;break-after:page;background:var(--paper)}
.page:last-child{page-break-after:auto;break-after:auto}
.foot{position:absolute;left:.85in;right:.85in;bottom:.45in;display:flex;justify-content:space-between;font-size:8pt;color:var(--muted);border-top:1px solid var(--line);padding-top:8px}
.foot a{color:var(--muted);text-decoration:none}
.kicker{font-family:var(--display);font-weight:600;font-size:11.5pt;color:var(--muted);margin-bottom:8px}
h2{font-size:31pt;line-height:1.06;font-weight:700;letter-spacing:-.018em;margin-bottom:18px;text-wrap:balance}
h3{font-size:13.6pt;line-height:1.25;font-weight:700;margin:18px 0 5px}
.lead{font-size:14pt;line-height:1.48;color:var(--ink-2);margin-bottom:18px;max-width:34em}
p+p{margin-top:9px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:28px}

.cols4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.cols4 .card{padding:12px 13px}.cols4 b{font-family:var(--display);font-size:11.5pt;display:block;margin-bottom:3px}.cols4 p{font-size:9.6pt;line-height:1.42;color:var(--ink-2)}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px}
.note{font-size:9.3pt;line-height:1.45;color:var(--muted)}
ul{margin:6px 0 0;padding-left:1.1em}li{margin:3px 0}
ul.plain{list-style:none;padding:0}
.rule{border:0;border-top:1px solid var(--line);margin:18px 0}
strong{font-weight:600}
figure{margin:0}
figcaption{font-size:9.2pt;color:var(--muted);margin-top:6px;line-height:1.4}

/* cover */
.cover{padding:0;display:grid;grid-template-columns:1fr 2.55in;background:var(--paper)}
.cover .main{padding:.85in .5in .7in .85in;display:flex;flex-direction:column}
.cover .logo{width:1.75in;display:block}
.cover h1{font-size:60pt;line-height:.96;font-weight:800;letter-spacing:-.025em;margin-top:1.5in;font-variation-settings:"opsz" 96}
.cover .sub{font-family:var(--display);font-size:19pt;line-height:1.2;font-weight:500;color:var(--ink-2);margin-top:22px;max-width:13em}
.cover .inside{list-style:none;padding:0;margin:auto 0 0;font-size:11pt;line-height:1.4;max-width:24em}
.cover .inside li{border-top:1px solid var(--line);padding:8px 0;margin:0}
.cover .meta{margin-top:.45in;font-size:9.6pt;color:var(--ink-2);line-height:1.6}
.cover .meta a{color:var(--ink)}
.ladder{display:grid;grid-template-rows:1fr 1fr 1fr 1fr;height:11in;border-left:2px solid var(--ink)}
.ladder div{padding:22px 20px;display:flex;flex-direction:column;justify-content:flex-end;border-top:1px solid rgba(27,21,18,.25);position:relative}
.ladder div:first-child{border-top:0}
.ladder b{font-family:var(--display);font-size:30pt;font-weight:700;line-height:1;letter-spacing:-.02em}
.ladder span{font-size:9.6pt;margin-top:5px;color:var(--ink-2)}
.ladder .l1{background:#f0a877}.ladder .l2{background:#f5c7a0}.ladder .l3{background:#f8dfc6}.ladder .l4{background:#fbf1e5}
.ladder .you{position:absolute;top:22px;left:20px;display:flex;align-items:center;gap:8px;font-family:var(--display);font-weight:700;font-size:11pt;color:var(--ink)}
.ladder .you i{width:12px;height:12px;border-radius:50%;background:var(--ember);border:2px solid var(--ink);display:block}

/* contents */
.toc{list-style:none;padding:0;margin:0;font-size:11pt}
.toc li{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line);padding:9px 0;margin:0}
.toc li span:last-child{color:var(--muted);font-variant-numeric:tabular-nums}
.short{counter-reset:s;list-style:none;padding:0;margin:0}
.short li{counter-increment:s;display:grid;grid-template-columns:36px 1fr;margin:0 0 17px}
.short li::before{content:counter(s);font-family:var(--display);font-weight:700;font-size:21pt;line-height:1.05;color:var(--ink)}

svg.strat{width:100%;height:auto;display:block;margin:6px 0 4px}
svg.felt{width:100%;height:auto;display:block;border:2.5px solid var(--ink);border-radius:var(--r)}
.shapes{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:12px 0}
.shapes .card{text-align:left}.shapes svg{width:50%;display:block;margin:0 auto 8px}
.photos{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:16px}
.photos img{width:100%;aspect-ratio:1.75/1;object-fit:contain;background:#fff;border:1px solid var(--line);border-radius:var(--r);display:block}

table.mat{width:100%;border-collapse:collapse;font-size:10.4pt;line-height:1.45;margin-top:6px}
table.mat th{text-align:left;font-weight:600;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:7px 10px 7px 0;vertical-align:bottom}
table.mat td{border-bottom:1px solid var(--line);padding:12px 12px 12px 0;vertical-align:top}
table.mat td:first-child{font-weight:600;white-space:nowrap;font-size:11pt}
table.temps{font-size:10.4pt}
table.temps th{padding:8px 0;font-size:9.4pt}
table.temps td{padding:7.5px 0}
table.temps .n{padding-left:10px}
table.temps td:first-child,table.temps td:nth-child(4),table.temps th{white-space:nowrap}

.care{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:10px}
.care .card{padding:12px}
.care svg{width:54px;height:54px;display:block;margin-bottom:10px}
.care b{font-family:var(--display);font-size:12pt;display:block;line-height:1.2;margin-bottom:3px}
.care p{font-size:9.5pt;line-height:1.4;color:var(--ink-2)}
.careno{display:flex;gap:26px;margin-top:14px;align-items:center}
.careno div{display:flex;align-items:center;gap:9px;font-family:var(--display);font-weight:600;font-size:11.4pt}
.careno svg{width:42px;height:42px}
.steps{counter-reset:st;list-style:none;padding:0;margin:8px 0 0}
.steps li{counter-increment:st;display:grid;grid-template-columns:26px 1fr;margin:0 0 7px}
.steps li::before{content:counter(st) ".";font-family:var(--display);font-weight:700}

.trad{display:grid;grid-template-columns:1.55in 1fr;gap:0 18px;margin-top:4px}
.trad dt{font-family:var(--display);font-weight:700;font-size:12pt;line-height:1.3;padding:11px 0;border-top:1px solid var(--line)}
.trad dd{margin:0;padding:11px 0;border-top:1px solid var(--line);font-size:10.8pt;line-height:1.5}
.trad dt:first-of-type,.trad dd:first-of-type{border-top:2px solid var(--ink)}

.check h3{margin-top:0;border-bottom:2px solid var(--ink);padding-bottom:5px;margin-bottom:8px}
.check ul{list-style:none;padding:0;margin:0 0 24px}
.check li{display:grid;grid-template-columns:26px 1fr;margin:0 0 10px;font-size:11.2pt;line-height:1.42}
.check li::before{content:"";width:14px;height:14px;border:1.6px solid var(--ink);border-radius:3px;margin-top:3px;background:var(--card)}

.about{display:grid;grid-template-columns:1fr 2.3in;gap:30px;align-items:start}
.about img.ph{width:100%;background:#fff;border:1px solid var(--line);border-radius:var(--r);display:block}
.btn{display:inline-block;background:var(--ember);color:var(--ink);font-family:var(--display);font-weight:700;font-size:11.5pt;padding:10px 18px;border-radius:var(--r);text-decoration:none;margin-top:14px}
.fine{font-size:9.2pt;line-height:1.5;color:var(--ink-2)}
.fine h3{font-size:10.5pt;margin:0 0 4px}
'''

PAGES = []


def page(body, cls=""):
    PAGES.append((cls, body))


# 1 cover
page(f'''<div class="main">
<img class="logo" src="img/logo-dark.png" alt="DIVELUX">
<h1>The Sauna Hat Guide</h1>
<p class="sub">Why heat rises and what to wear on your head</p>
<ul class="inside"><li>How sauna heat stacks up, and why your head feels it first</li><li>Why wool felt, and why the hat is worn dry</li><li>Choosing, wearing, and washing a hat</li><li>Typical temperatures for 13 sauna types</li><li>Etiquette and a first-timer checklist</li></ul>
<div class="meta">A free guide by DIVELUX, makers of wool sauna hats<br>Version 1.0 · November 2026 · <a href="{SITE}">diveluxsaunahat.com</a></div>
</div>
<div class="ladder" aria-hidden="true">
<div class="l1"><b>212 °F</b><span>100 °C · under the ceiling</span></div>
<div class="l2"><p class="you"><i></i>Your head</p><b>190 °F</b><span>88 °C · seated on the top bench</span></div>
<div class="l3"><b>160 °F</b><span>71 °C · bench level</span></div>
<div class="l4"><b>105 °F</b><span>40 °C · floor · illustrative figures</span></div>
</div>''', "cover")

# 2 short version + contents
page('''<p class="kicker">Start here</p>
<h2>The short version</h2>
<p class="lead">A sauna is not one temperature. It is a stack of layers, and your head sits in the hottest one you can reach. A hat is the simplest way to even things out.</p>
<div class="cols" style="margin-top:22px">
<ol class="short">
<li><div><strong>Hot air rises.</strong> The air at head height on the top bench can be far hotter than the air around your feet.</div></li>
<li><div><strong>Your head heats first.</strong> It is the highest part of you, and your ears and hair take the heat with no protection.</div></li>
<li><div><strong>Wool felt insulates.</strong> Thick felt traps air between its fibers and slows the heat on its way to your scalp.</div></li>
<li><div><strong>Wear the hat dry.</strong> A dry felt hat is the insulator. Put it on before you walk into the hot room.</div></li>
<li><div><strong>Loose is good.</strong> A roomy hat leaves a layer of air around your head. If it sits too low, fold the edge up.</div></li>
<li><div><strong>Care is simple.</strong> Hand wash in cool, room-temperature water, squeeze, and air dry. No machine, no dryer.</div></li>
</ol>
<div>
<h3 style="margin-top:0;margin-bottom:6px">In this guide</h3>
<ul class="toc">
<li><span>Why the air is hottest at the top</span><span>3</span></li>
<li><span>What a sauna hat does</span><span>4</span></li>
<li><span>Hats and head wraps by tradition</span><span>5</span></li>
<li><span>Materials: why wool felt</span><span>6</span></li>
<li><span>How to choose a hat</span><span>7</span></li>
<li><span>How to wear it and care for it</span><span>8</span></li>
<li><span>Typical temperatures by sauna type</span><span>9</span></li>
<li><span>Sauna etiquette in brief</span><span>10</span></li>
<li><span>First-timer checklist</span><span>11</span></li>
<li><span>About DIVELUX and disclaimer</span><span>12</span></li>
</ul>
<p class="note" style="margin-top:14px">This guide is general information, not medical advice. If you have a health condition, are pregnant, or take medication, talk to your doctor before using a sauna.</p>
</div></div>''')

# 3 why heat rises
page(f'''<p class="kicker">The physics</p>
<h2>Why the air is hottest at the top</h2>
<p class="lead">Warm air is lighter than cool air, so it floats up and collects under the ceiling. In a closed, heated room this builds layers, a pattern called thermal stratification.</p>
<figure style="max-width:6.5in">{strat_svg()}
<figcaption>Illustrative example of a hot Finnish-style sauna, not a measurement. Real rooms vary with the stove, the ceiling height, ventilation, and how much water goes on the stones.</figcaption></figure>
<div class="cols" style="margin-top:16px">
<div><h3 style="margin-top:0">What this means on the bench</h3>
<p>Sauna benches are raised on purpose: the higher you sit, the more heat you get. Seated on the top bench, your feet rest in mild air while your head is close to the hottest layer in the room.</p>
<p>That is why people often feel "too hot" in the head and ears first, well before the rest of the body has warmed through.</p></div>
<div><h3 style="margin-top:0">What steam adds</h3>
<p>When water hits the stones, a wave of hot, humid air rolls up to the ceiling and then down over the benches. It reaches your head and shoulders first.</p>
<p>Moving down one bench is the quickest way to turn the heat down. Covering your head is the other.</p></div>
</div>''')

# 4 what a hat does
page(f'''<p class="kicker">The hat</p>
<h2>What a sauna hat does</h2>
<p class="lead">A sauna hat works like an oven mitt for your head. It does not cool you. It slows the heat on its way to your scalp, ears, and hair.</p>
<figure style="margin:4px 0 18px">{felt_svg()}<figcaption>Dry wool felt, a few millimeters thick: tangled fibers with air trapped between them. Schematic, not to scale.</figcaption></figure>
<div class="cols">
<div>
<h3 style="margin-top:4px">Felt is mostly air</h3>
<p>Wool felt is a dense mat of tangled fibers with countless tiny air pockets between them. Still air is a poor conductor of heat, so a thick layer of felt makes a good barrier between the hot room and your head.</p>
<h3>Dry is the point</h3>
<p>A sauna hat is worn dry. Dry felt holds the air that does the insulating. Keep the hat in the changing room, put it on before you enter the hot room, and hang it up to air out between visits.</p>
<h3>Hair and ears</h3>
<p>The hat covers the parts that sit highest and have the least protection: the top of the head, the tips of the ears, and your hair, which many bathers find gets dry and brittle with regular sauna heat.</p>
</div>
<div>
<div class="card">
<h3 style="margin-top:0">What it helps with</h3>
<ul><li>Keeps the head and ears from feeling scorched before the body is warm</li>
<li>Shields hair from the hottest, driest air</li>
<li>Makes the top bench and steam bursts more comfortable</li></ul>
</div>
<div class="card" style="margin-top:14px">
<h3 style="margin-top:0">What it does not do</h3>
<ul><li>It does not lower your body temperature</li>
<li>It does not make a long session safe</li>
<li>It is not a treatment for any condition</li></ul>
<p class="note" style="margin-top:8px">If you feel dizzy, sick, or unwell, leave the hot room, hat or no hat.</p>
</div>
</div></div>''')

# 5 traditions
page(f'''<p class="kicker">A little history</p>
<h2>Hats and head wraps by tradition</h2>
<p class="lead">Felt is one of the oldest textiles people make, and covering the head in the heat is an old habit wherever steam baths are hot. Customs differ from country to country.</p>
<dl class="trad">
<dt>Russian banya</dt><dd>The felt banya hat is part of the standard kit, next to the leafy whisk (venik) and a sheet or towel. The same custom is found in Ukraine, Belarus, and neighboring countries. Hats are usually bell-shaped, and novelty shapes are common.</dd>
<dt>Baltic countries</dt><dd>In the Latvian pirts and the Lithuanian pirtis, where a bath master may lead long whisking rituals, wool felt hats are widely used. Estonians have their own word for the sauna hat, saunamüts.</dd>
<dt>Finland</dt><dd>Finns call it a saunahattu. Some bathers wear one, mostly in very hot saunas, and many do not. It is a matter of personal habit.</dd>
<dt>Germany, Austria, Switzerland</dt><dd>The felt Saunahut is a common accessory, useful during an Aufguss, when a sauna master pours water on the stones and fans the hot air toward the benches with a towel.</dd>
<dt>Japan</dt><dd>Sauna hats in wool felt or cotton terry became a popular accessory with the country's recent sauna boom.</dd>
<dt>Korea</dt><dd>In a jjimjilbang, a small towel is folded into the "sheep head" shape (yangmeori), with a rolled bun over each ear. It keeps hair back and is mostly a playful custom, not heat protection.</dd>
<dt>Hammam</dt><dd>There is no hat in the hot room. After the wash, a cotton towel is often wrapped around the hair while resting.</dd>
</dl>
<p class="note" style="margin-top:14px">These notes come from our open dataset, Sauna Traditions of the World, free to download at <a href="{TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a>.</p>''')

# 6 materials
page('''<p class="kicker">Materials</p>
<h2>Why wool felt, and how the others compare</h2>
<p class="lead">Sauna hats are sold in four main materials. They are not equal in the heat.</p>
<table class="mat">
<thead><tr><th style="width:16%">Material</th><th style="width:28%">In the heat</th><th style="width:28%">With sweat and steam</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td>Wool felt</td><td>Thick and full of trapped air, so it insulates well. The traditional choice.</td><td>Wool fibers take up moisture vapor and still feel dry to the touch.</td><td>Keeps its shape. Needs gentle hand washing in cool water.</td></tr>
<tr><td>Linen</td><td>Thin and breathable. Covers the hair but insulates much less than felt.</td><td>Dries fast.</td><td>Light and easy to pack. A fair choice for mild rooms.</td></tr>
<tr><td>Cotton or terry</td><td>Thicker than linen, thinner than felt. Moderate protection.</td><td>Absorbs sweat and holds it, so it gets heavy and loses insulation.</td><td>Easy to launder. A towel over the head is the same idea.</td></tr>
<tr><td>Synthetic felt</td><td>Insulates, but does not breathe like wool.</td><td>Does not manage moisture as well; can feel clammy.</td><td>Usually the cheapest. Check the label: "felt" does not always mean wool.</td></tr>
</tbody></table>
<div class="cols" style="margin-top:22px">
<div><h3 style="margin-top:0">What to look for in wool felt</h3>
<ul><li>100% wool on the label, not a wool blend</li>
<li>Dense, even felt a few millimeters thick, with no thin spots when held to the light</li>
<li>Neat, flat seams that will not press into your forehead</li>
<li>A loop at the top for hanging it to dry</li></ul></div>
<div><h3 style="margin-top:0">If wool makes you itch</h3>
<p>Felt can feel coarse at first and softens with use. If your skin is sensitive to wool, a thin cotton cap or bandana under the hat works well, or choose linen and sit a bench lower.</p></div>
</div>''')

# 7 choose
page(f'''<p class="kicker">Choosing</p>
<h2>How to choose a hat</h2>
<p class="lead">Shape is mostly taste. Fit matters more, and looser is better than you might expect.</p>
<div class="shapes">
<div class="card">{BELL_SVG}<h3 style="margin-top:0">Bell</h3><p style="font-size:10pt">The classic shape. Tall crown with air space above the head, sides that come down over the ears.</p></div>
<div class="card">{BUCKET_SVG}<h3 style="margin-top:0">Bucket</h3><p style="font-size:10pt">Flat crown with a short brim that shades the ears, eyes, and neck. Looks like an everyday hat.</p></div>
<div class="card">{FOLD_SVG}<h3 style="margin-top:0">Too big? Fold the edge</h3><p style="font-size:10pt">Turn the edge up once to shorten the hat. The double layer adds insulation at the brow.</p></div>
</div>
<div class="cols">
<div><h3 style="margin-top:6px">A loose fit is a plus</h3>
<p>A sauna hat should rest on your head, not grip it. The gap between felt and scalp is one more layer of still air, and a roomy hat is easy to pull down over your ears when steam rolls in.</p>
<p>Most felt hats come in one size. If yours sits too low, fold the edge up.</p></div>
<div><h3 style="margin-top:6px">Quick checklist</h3>
<ul><li>Covers the top of your ears</li><li>Does not squeeze your forehead</li><li>Thick, even wool felt</li><li>Hanging loop or a shape that stands on its own</li><li>A color you can pick out on a shared hook</li></ul></div>
</div>
<div class="photos">
<figure><img src="img/hat-bell-grey.jpg" alt="Grey bell-shaped wool felt sauna hat"><figcaption>Bell hat in grey wool felt (DIVELUX).</figcaption></figure>
<figure><img src="img/hat-bucket-grey.jpg" alt="Grey bucket-shaped wool felt sauna hat with a brim"><figcaption>Bucket hat with a brim in grey wool felt (DIVELUX).</figcaption></figure>
</div>''')

# 8 wear and care
care_cards = "".join(f'<div class="card">{ICONS[k]}<b>{t}</b><p>{d}</p></div>' for k, t, d in CARE)
care_no = "".join(f'<div>{ICONS[k]}<span>{t}</span></div>' for k, t in CARE_NO)
page(f'''<p class="kicker">Using it</p>
<h2>How to wear it and care for it</h2>
<div class="cols">
<div><h3 style="margin-top:0">Wearing</h3>
<ol class="steps">
<li><div>Start with a dry hat. Put it on in the changing room, after your shower and before the hot room.</div></li>
<li><div>Pull it down to cover the tops of your ears. Long hair can be tucked up inside.</div></li>
<li><div>Keep it on for the whole round, most of all on the top bench and when water goes on the stones.</div></li>
<li><div>Take it off when you step out to cool down, and put it back on for the next round.</div></li>
</ol></div>
<div><h3 style="margin-top:0">After each visit</h3>
<p>Shake the hat out and hang it by the loop somewhere with moving air until it is fully dry. Do not leave it balled up in a gym bag.</p>
<p>Felt does not need washing after every use. Airing it out is enough most of the time. Wash it when it looks or smells like it needs it.</p></div>
</div>
<hr class="rule" style="margin:12px 0 14px">
<h3 style="margin-top:0">Washing a wool felt hat</h3>
<p>Heat and rough handling are what make wool shrink and harden. Keep both away and the hat lasts for years.</p>
<div class="care">{care_cards}</div>
<div class="careno">{care_no}</div>
<p class="note" style="margin-top:14px">Wash by hand only, in cool, room-temperature water (about 20–24 °C / 68–75 °F, never warm or hot). Squeeze the water out without wringing, reshape, and air dry away from heaters and direct sun. Do not try to shrink a felt hat to size; fold the edge instead.</p>''')

# 9 temps
page(f'''<p class="kicker">Reference</p>
<h2>Typical temperatures by sauna type</h2>
<p class="lead">Commonly quoted ranges for the air in the hot room. The lower the humidity, the higher the temperature people can sit in comfortably.</p>
{temp_table()}
<p class="note" style="margin-top:12px">Compiled reference ranges from general published descriptions, not measurements. Individual rooms vary. A dash means no figure is given. Humidity in a stove-heated sauna jumps briefly each time water goes on the stones. Some traditions, such as smoke saunas, the Latvian pirts, and the Lithuanian pirtis, are left out of this table because published figures disagree.</p>
<p class="note" style="margin-top:8px">Source: Sauna Traditions of the World, version 1.0 (DIVELUX, 2026), an open dataset with 28 traditions. Free download: <a href="{TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p>''')

# 10 etiquette
page('''<p class="kicker">Manners</p>
<h2>Sauna etiquette in brief</h2>
<p class="lead">Rules differ by country and by venue, so read the signs and follow the locals. These basics are welcome almost everywhere.</p>
<div class="cols">
<div>
<h3 style="margin-top:4px">Before you go in</h3>
<ul><li>Shower first. Everyone shares the same air and benches.</li>
<li>Check the dress code. Some saunas are swimsuit-only, some are towel-only, and many in Germany and the Nordic countries are textile-free.</li>
<li>Take off glasses, jewelry, and watches, and leave your phone outside.</li></ul>
<h3>In the hot room</h3>
<ul><li>Sit or lie on a towel so your skin does not touch the wood.</li>
<li>Open and close the door quickly to keep the heat in.</li>
<li>Ask before you pour water on the stones. Not everyone wants more steam, and some heaters are not built for it.</li>
<li>Keep your voice down. Some rooms are silent.</li></ul>
</div>
<div>
<h3 style="margin-top:4px">Sharing the space</h3>
<ul><li>Make room for people coming in, and do not block the door.</li>
<li>The top bench is the hottest. If you need less heat, move down instead of propping the door open.</li>
<li>During a guided session such as an Aufguss, come in before it starts and stay until the end if you can. Leave at once if you feel unwell.</li></ul>
<h3>Afterward</h3>
<ul><li>Rinse off before you get into a cold plunge or pool.</li>
<li>Take your towel, hat, and water bottle with you.</li>
<li>Rest and drink water before the next round.</li></ul>
</div></div>
<h3 style="margin-top:16px;margin-bottom:8px">How customs differ</h3>
<div class="cols4">
<div class="card"><b>Finland</b><p>Often nude in single-sex or family saunas, swimsuits in mixed public ones. Water on the stones is expected.</p></div>
<div class="card"><b>Germany</b><p>Textile-free and mixed. Sit on a large towel, feet included. Quiet is the norm.</p></div>
<div class="card"><b>Russian banya</b><p>Sheets or towels, felt hats, and whisks. Rounds are social, with tea in between.</p></div>
<div class="card"><b>United States</b><p>Swimsuit or towel, by venue. Many gyms do not allow water on the heater.</p></div>
</div>''')

# 11 checklist
page('''<p class="kicker">One page to print</p>
<h2>First-timer checklist</h2>
<div class="cols check" style="margin-top:20px">
<div>
<h3>Pack</h3>
<ul><li>Two towels: one to sit on, one to dry off</li><li>Wool felt sauna hat, dry</li><li>Water bottle</li><li>Sandals or flip-flops</li><li>Swimsuit, if the venue requires one</li></ul>
<h3>Before the hot room</h3>
<ul><li>Drink a glass of water</li><li>Skip alcohol and heavy meals</li><li>Remove jewelry, watch, and glasses</li><li>Shower and dry off</li><li>Put your hat on</li></ul>
<h3>In the hot room</h3>
<ul><li>Start on a lower bench</li><li>Keep the first round short: 5 to 10 minutes is plenty</li><li>Breathe slowly through your nose</li><li>Leave as soon as you feel dizzy, sick, or uncomfortable</li><li>Stand up slowly</li></ul>
</div>
<div>
<h3>Between rounds</h3>
<ul><li>Cool down: fresh air, a cool shower, or a quick plunge</li><li>Take your hat off while you cool</li><li>Sit and rest at least as long as you were in the heat</li><li>Drink water</li><li>Two or three rounds is a full session for most people</li></ul>
<h3>Afterward</h3>
<ul><li>Rinse off and cool down fully before you dress</li><li>Drink more water</li><li>Hang your hat up to air dry</li><li>Give yourself a quiet half hour</li></ul>
<div class="card" style="margin-top:4px">
<p class="note" style="color:var(--ink-2)"><strong>Not medical advice.</strong> Sauna heat is a real load on the body. If you are pregnant, have a heart or blood pressure condition, or take medication, talk to your doctor first. Children and older adults need shorter, milder sessions. Never use a sauna after drinking alcohol.</p>
</div>
</div></div>''', "")

# 12 about
page(f'''<p class="kicker">Who made this</p>
<h2>About DIVELUX</h2>
<div class="about">
<div>
<p class="lead" style="margin-bottom:10px">DIVELUX is a small family brand in Irvine, California. We make one thing: sauna hats of 100% natural wool felt.</p>
<p>Each hat is felted and stitched by hand at a partner workshop in Ukraine and shipped from the United States. The felt is 4–5 mm thick. One size, about 24 inches around, in two shapes: the classic bell and a bucket with a brim.</p>
<p>We wrote this guide because we get the same good questions every week. It is free to read, share, and reprint.</p>
<a class="btn" href="{SITE}">Visit diveluxsaunahat.com</a>
<p style="margin-top:14px">More free sauna tools and the open dataset behind the temperature table:<br><a href="{TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p>
</div>
<figure><img class="ph" src="img/hat-bell-white-blue.jpg" alt="White wool felt sauna hat with a blue edge"><figcaption>DIVELUX bell hat, white wool felt with a blue edge.</figcaption></figure>
</div>
<hr class="rule" style="margin:26px 0 18px">
<div class="cols fine">
<div><h3>Disclaimer</h3>
<p>This guide is general information for healthy adults and is not medical advice. It does not diagnose, treat, or prevent any condition. Talk to your doctor before using a sauna if you are pregnant, have a heart, blood pressure, or other health condition, or take medication. Leave the hot room right away if you feel dizzy, sick, or unwell. Temperatures and times in this guide are commonly quoted ranges, not measurements or recommendations. Always follow the rules of the facility you visit.</p></div>
<div><h3>License and citation</h3>
<p>Text and diagrams © 2026 DIVELUX, released under the Creative Commons Attribution 4.0 International license (CC BY 4.0). You may share and adapt them with credit to DIVELUX and a link to diveluxsaunahat.com. Product photographs and the DIVELUX name and logo are not covered by this license.</p>
<p style="margin-top:6px">Cite as: DIVELUX (2026). <em>The Sauna Hat Guide: Why Heat Rises and What to Wear on Your Head</em> (Version 1.0). {TOOLS}</p></div>
</div>''')


def build_guide():
    out = [f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8">
<title>{TITLE}</title>
<meta name="author" content="DIVELUX">
<meta name="description" content="{DESC}">
<meta name="keywords" content="sauna hat, wool felt, banya hat, sauna etiquette, sauna temperature, Finnish sauna, banya, heat stratification, sauna for beginners">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{GUIDE_CSS}</style></head><body>''']
    n = len(PAGES)
    for i, (cls, body) in enumerate(PAGES, 1):
        foot = "" if i == 1 else (f'<div class="foot"><span>The Sauna Hat Guide · <a href="{SITE}">DIVELUX</a></span>'
                                  f'<span>{i} / {n}</span></div>')
        tag = "main" if i == 1 else "section"
        out.append(f'<{tag} class="page {cls}">{body}{foot}</{tag}>')
    out.append("</body></html>\n")
    with open(os.path.join(HERE, "guide.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


# ================================================================ SLIDES
SLIDES_CSS = FONT_CSS + '''
@page{size:13.333in 7.5in;margin:0}
body{font-size:22pt;line-height:1.42}
.slide{position:relative;width:13.333in;height:7.5in;padding:.6in .85in .85in;overflow:hidden;display:flex;flex-direction:column;justify-content:center;page-break-after:always;break-after:page;background:var(--paper)}
.slide:last-child{page-break-after:auto;break-after:auto}
.foot{position:absolute;left:.85in;right:.85in;bottom:.32in;display:flex;justify-content:space-between;font-size:10pt;color:var(--muted)}
.foot a{color:var(--muted);text-decoration:none}
h2{font-size:50pt;line-height:1.03;font-weight:700;letter-spacing:-.022em;margin-bottom:34px;text-wrap:balance}
h3{font-size:25pt;font-weight:700;line-height:1.15;margin-bottom:10px}
.lead{font-size:27pt;line-height:1.36;color:var(--ink-2);max-width:26em}
.two{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.two.wide{grid-template-columns:.62fr 1.38fr;gap:40px}
.two.photo-r{grid-template-columns:1.25fr .75fr}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.four{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:28px 30px}
ul{margin:0;padding-left:1.1em}li{margin:10px 0}
.note{font-size:14pt;color:var(--muted);line-height:1.4}
strong{font-weight:600}
.title{padding:0;display:grid !important;grid-template-columns:1fr 3.6in}
.title .main{padding:.8in .6in .7in .85in;display:flex;flex-direction:column}
.title img.logo{width:2.1in}
.title h1{font-size:76pt;line-height:.96;font-weight:800;letter-spacing:-.025em;margin-top:.95in;font-variation-settings:"opsz" 96}
.title .sub{font-family:var(--display);font-size:25pt;font-weight:500;color:var(--ink-2);margin-top:20px}
.title .meta{margin-top:auto;font-size:13pt;color:var(--ink-2)}
.title .meta a{color:var(--ink)}
.ladder{display:grid;grid-template-rows:repeat(4,1fr);height:7.5in;border-left:2px solid var(--ink)}
.ladder div{padding:14px 22px;display:flex;flex-direction:column;justify-content:flex-end;border-top:1px solid rgba(27,21,18,.25);position:relative}
.ladder div:first-child{border-top:0}
.ladder b{font-family:var(--display);font-size:32pt;font-weight:700;line-height:1}
.ladder span{font-size:11.5pt;margin-top:4px;color:var(--ink-2)}
.ladder .l1{background:#f0a877}.ladder .l2{background:#f5c7a0}.ladder .l3{background:#f8dfc6}.ladder .l4{background:#fbf1e5}
.ladder .you{position:absolute;top:14px;left:22px;display:flex;align-items:center;gap:8px;font-family:var(--display);font-weight:700;font-size:13pt}
.ladder .you i{width:13px;height:13px;border-radius:50%;background:var(--ember);border:2px solid var(--ink);display:block}
svg.strat{width:100%;height:auto;display:block}
.shape svg{width:52%;display:block;margin:0 auto 10px}
.shape p{font-size:20pt;line-height:1.36}
.care svg{width:84px;height:84px;display:block;margin-bottom:16px}
.care p{font-size:17pt;line-height:1.36;color:var(--ink-2)}
.care h3{font-size:23pt}
.care .card{padding:24px}
.careno{display:flex;gap:56px;margin-top:34px}
.careno div{display:flex;align-items:center;gap:14px;font-family:var(--display);font-weight:600;font-size:22pt}
.careno svg{width:60px;height:60px}
table.temps{font-size:19pt}
table.temps th{padding:7px 0;font-size:15pt}
table.temps td{padding:6.5px 0}
.tight h2{margin-bottom:20px;font-size:44pt}
.tight .card{padding:22px 24px;font-size:19.5pt}
.tight li{margin:7px 0}
table.mat{width:100%;border-collapse:collapse;font-size:21pt;line-height:1.3}
table.mat th{text-align:left;font-weight:600;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:12px 14px 12px 0;font-size:17pt}
table.mat td{border-bottom:1px solid var(--line);padding:15px 24px 15px 0;vertical-align:top}
table.mat td:first-child{font-weight:600;white-space:nowrap}
.trad{display:grid;grid-template-columns:1fr 1fr;gap:0 56px;font-size:19.5pt;line-height:1.36}
.trad div{border-top:1px solid var(--line);padding:18px 0}
.trad b{font-family:var(--display);display:block;font-size:23pt;margin-bottom:2px}
.big{font-family:var(--display);font-size:110pt;font-weight:700;line-height:1.08;letter-spacing:-.02em;max-width:15em}
.btn{display:inline-block;background:var(--ember);color:var(--ink);font-family:var(--display);font-weight:700;font-size:22pt;padding:16px 30px;border-radius:var(--r);text-decoration:none;margin-top:22px}
.photo{width:100%;background:#fff;border:1px solid var(--line);border-radius:var(--r);display:block}
ol.steps{margin:0;padding-left:1.2em}ol.steps li{margin:16px 0;padding-left:6px;font-size:25pt;line-height:1.3}
'''

SL = []
SL.append(("title", f'''<div class="main"><img class="logo" src="img/logo-dark.png" alt="DIVELUX">
<h1>The Sauna Hat Guide</h1><p class="sub">Why heat rises and what to wear on your head</p>
<p class="meta">A free guide by DIVELUX, makers of wool sauna hats · <a href="{SITE}">diveluxsaunahat.com</a></p></div>
<div class="ladder" aria-hidden="true">
<div class="l1"><b>212 °F</b><span>100 °C · under the ceiling</span></div>
<div class="l2"><p class="you"><i></i>Your head</p><b>190 °F</b><span>88 °C · top bench, seated</span></div>
<div class="l3"><b>160 °F</b><span>71 °C · bench level</span></div>
<div class="l4"><b>105 °F</b><span>40 °C · floor · illustrative</span></div></div>'''))
SL.append(("", f'''<div class="two wide"><div><h2>A sauna is a stack of layers</h2>
<p class="lead" style="font-size:21pt">Warm air is lighter than cool air. It floats up and collects under the ceiling, so the room is hottest at the top and mildest at the floor.</p>
<p class="note" style="margin-top:22px">Illustrative example of a hot Finnish-style sauna, not a measurement. Real rooms vary.</p></div>
<div>{strat_svg()}</div></div>'''))
SL.append(("", '''<h2>Your head heats first</h2>
<div class="three">
<div class="card"><h3>It sits highest</h3><p>On the top bench your feet rest in mild air while your head is close to the hottest layer in the room.</p></div>
<div class="card"><h3>Steam lands there first</h3><p>Water on the stones sends hot, humid air up to the ceiling and down over your head and shoulders.</p></div>
<div class="card"><h3>Two ways to turn it down</h3><p>Move down a bench, or cover your head. A hat lets you keep your seat.</p></div>
</div>'''))
SL.append(("tight", '''<div class="two"><div><h2>What a sauna hat does</h2>
<p class="lead" style="font-size:25pt">It works like an oven mitt for your head. Wool felt is full of tiny air pockets, and still air is a poor conductor of heat.</p></div>
<div><div class="card"><h3>Helps with</h3><ul><li>Head and ears that feel scorched before the body is warm</li><li>Hair exposed to the hottest, driest air</li><li>Comfort on the top bench and during steam</li></ul></div>
<div class="card" style="margin-top:18px"><h3>Does not</h3><ul><li>Lower your body temperature</li><li>Make a long session safe</li></ul></div></div></div>'''))
SL.append(("", '''<p class="big">Wear the hat dry.</p>
<p class="lead" style="margin-top:40px;font-size:30pt">Dry felt holds the air that does the insulating. Put the hat on before you walk into the hot room, and hang it up to air out afterward.</p>'''))
SL.append(("", '''<h2>Hats and head wraps by tradition</h2>
<div class="trad">
<div><b>Russian banya</b>The felt banya hat is part of the standard kit, next to the whisk.</div>
<div><b>Germany, Austria, Switzerland</b>The felt Saunahut is a common accessory, handy during an Aufguss.</div>
<div><b>Baltic countries</b>Wool felt hats are widely used in the pirts and the pirtis.</div>
<div><b>Japan</b>Sauna hats became popular with the recent sauna boom.</div>
<div><b>Finland</b>The saunahattu: some bathers wear one, many do not.</div>
<div><b>Korea</b>A towel folded into the "sheep head" shape. A playful custom, not heat protection.</div>
</div>'''))
SL.append(("", '''<h2>Why wool felt</h2>
<table class="mat"><thead><tr><th>Material</th><th>In the heat</th><th>With sweat and steam</th></tr></thead><tbody>
<tr><td>Wool felt</td><td>Thick, full of trapped air. Insulates well.</td><td>Takes up moisture vapor and still feels dry to the touch.</td></tr>
<tr><td>Linen</td><td>Thin. Covers hair, insulates much less.</td><td>Dries fast.</td></tr>
<tr><td>Cotton or terry</td><td>Moderate protection.</td><td>Holds sweat, gets heavy, loses insulation.</td></tr>
<tr><td>Synthetic felt</td><td>Insulates, but does not breathe like wool.</td><td>Can feel clammy. Check the label.</td></tr>
</tbody></table>'''))
SL.append(("", f'''<h2>How to choose: shape and fit</h2>
<div class="three shape">
<div class="card">{BELL_SVG}<h3>Bell</h3><p>The classic. Tall crown, sides that come down over the ears.</p></div>
<div class="card">{BUCKET_SVG}<h3>Bucket</h3><p>Flat crown and a short brim that shades ears, eyes, and neck.</p></div>
<div class="card">{FOLD_SVG}<h3>Loose is a plus</h3><p>The gap is one more layer of air. Too big? Fold the edge up.</p></div>
</div>'''))
SL.append(("", '''<div class="two photo-r"><div><h2>How to wear it</h2>
<ol class="steps"><li>Start with a dry hat. Put it on before the hot room.</li><li>Pull it down over the tops of your ears.</li><li>Keep it on for the whole round.</li><li>Take it off while you cool down.</li><li>Hang it up to air dry afterward.</li></ol></div>
<div><img class="photo" src="img/hat-bell-grey.jpg" alt="Grey bell-shaped wool felt sauna hat" style="max-height:5.2in;object-fit:contain"></div></div>'''))
care_s = "".join(f'<div class="card">{ICONS[k]}<h3>{t}</h3><p>{d}</p></div>' for k, t, d in CARE)
SL.append(("", f'''<h2>Caring for a wool felt hat</h2>
<div class="four care">{care_s}</div><div class="careno">{care_no}</div>'''))
SL.append(("tight", f'''<h2>Typical temperatures by sauna type</h2>
{temp_table(names={"Finnish sauna", "Russian banya", "German Aufguss sauna", "Bio sauna (soft sauna)", "Infrared sauna", "Steam room", "Turkish hammam", "Japanese sauna"}, compact=True)}
<p class="note" style="margin-top:14px">Compiled reference ranges from general published descriptions, not measurements. Source: Sauna Traditions of the World, v1.0 (DIVELUX, 2026).</p>'''))
SL.append(("tight", '''<h2>First-timer checklist</h2>
<div class="three">
<div class="card"><h3>Before</h3><ul><li>Shower and dry off</li><li>Drink water, skip alcohol</li><li>Remove jewelry and glasses</li><li>Put on a dry hat</li></ul></div>
<div class="card"><h3>In the hot room</h3><ul><li>Sit on a towel, lower bench first</li><li>Keep the first round to 5–10 minutes</li><li>Ask before adding water to the stones</li><li>Leave if you feel dizzy or unwell</li></ul></div>
<div class="card"><h3>Between rounds</h3><ul><li>Cool down with air, a shower, or a plunge</li><li>Rest as long as you were in the heat</li><li>Drink water</li><li>Two or three rounds is plenty</li></ul></div>
</div>
<p class="note" style="margin-top:14px">General information, not medical advice. If you are pregnant, have a health condition, or take medication, talk to your doctor before using a sauna.</p>'''))
SL.append(("", f'''<div class="two photo-r"><div><h2>About DIVELUX</h2>
<p class="lead" style="font-size:24pt">A small family brand in Irvine, California. We make sauna hats of 100% natural wool felt, felted and stitched by hand and shipped from the United States.</p>
<a class="btn" href="{SITE}">Visit diveluxsaunahat.com</a>
<p style="margin-top:26px;font-size:19pt">Full guide, open dataset, and more free sauna tools:<br><a href="{TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></p>
<p class="note" style="margin-top:18px">Text and diagrams © 2026 DIVELUX, CC BY 4.0. Not medical advice.</p></div>
<div><img class="photo" src="img/hat-bucket-white-blue.jpg" alt="White bucket-shaped wool felt sauna hat with a blue edge" style="max-height:5.4in;object-fit:contain"></div></div>'''))


def build_slides():
    out = [f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8">
<title>{TITLE}</title>
<meta name="author" content="DIVELUX">
<meta name="description" content="{DESC}">
<style>{SLIDES_CSS}</style></head><body>''']
    n = len(SL)
    for i, (cls, body) in enumerate(SL, 1):
        foot = "" if i == 1 else (f'<div class="foot"><span>The Sauna Hat Guide · <a href="{SITE}">diveluxsaunahat.com</a></span>'
                                  f'<span>{i} / {n}</span></div>')
        tag = "main" if i == 1 else "section"
        out.append(f'<{tag} class="slide {cls}">{body}{foot}</{tag}>')
    out.append("</body></html>\n")
    with open(os.path.join(HERE, "slides.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


if __name__ == "__main__":
    build_guide()
    build_slides()
    print(f"guide.html: {len(PAGES)} pages; slides.html: {len(SL)} slides; temperature rows: {len(ROWS)}")
