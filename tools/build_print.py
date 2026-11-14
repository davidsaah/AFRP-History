#!/usr/bin/env python3
"""Print editions of The Roots of Ramallah (v79).

Reads the finished book, out/AFRP_The_One_Line_v5.html, and writes:

  out/Roots_of_Ramallah_print.html            the book set for 6 x 9 inch pages (Paged.js)
  out/Roots_of_Ramallah_6x9.pdf               that file rendered by Chromium
  out/Roots_of_Ramallah_Companion_print.html  the annotated bibliography and the test harness
  out/Roots_of_Ramallah_Companion_6x9.pdf

The words and facts of the book are not touched. This script only lays them out
as a book: EB Garamond (embedded), justified and hyphenated text, a full-bleed
opening page for every chapter with its numeral and epigraph, dates in the outer
margin, drop caps, quiet small-caps labels in place of coloured badges, figures
at full text width with captions below, running heads and folios, a contents page
with page numbers, endnotes, and a short Further reading drawn from the
bibliography. The bibliography and the test harness go to the companion volume.

Every photograph is embedded from img/ (Library of Congress photos from img/loc/
once they are saved there). A photograph that is not held locally is left out of
print rather than printed as an empty frame.

    python3 tools/build_print.py              # both HTML files and both PDFs
    python3 tools/build_print.py --html-only
Set PRINT_CHROMIUM to a Chrome/Chromium binary if Playwright's own is not installed.
"""
import base64
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'out', 'AFRP_The_One_Line_v5.html')
OUT = os.path.join(ROOT, 'out')
PAGED = os.path.join(ROOT, 'tools', 'vendor', 'paged.polyfill.min.js')
FONTS = os.path.join(ROOT, 'assets', 'fonts', 'eb-garamond')

MAX_PX = 1400      # 4.2 inch text block at about 330 dpi; full-bleed openers use 1800
OPENER_PX = 1800
JPEG_Q = 74

# A short shelf for the end of the main book, taken word for word from the
# annotated bibliography (each key is a phrase unique to that entry's title line).
FURTHER = [
    'ʻAzīz Shāhīn (1894–1996)',
    'New Light on Ramallah',
    'Rām Allāh al-ʻUthmānīyah',
    'Yūsuf Jurjis Qadūrah',
    'Remembering Ramallah',
    'A Pictorial History of Ramallah',
    'Nazmi al-Jubeh &amp; Khaldun Bshara',
    'Muṣṭafá Murād al-Dabbāgh',
    'Ibrāhīm Khalīl Nayrūz',
    'Yaḥyá ʻĪsá al-Farḥān',
    'Turbulent Times in Palestine',
    'Ordinary Lives',
    'Enclave Micropolis',
    'Landed Property, Palestinian Migration',
    'I Saw Ramallah',
]

SERIF = '"EB Garamond","Times New Roman",Times,"Liberation Serif",serif'

PRINT_CSS = r"""
/* ════════ v79 print edition (tools/build_print.py) ════════ */
@page{size:6in 9in;margin:0.78in 1.02in 0.82in 0.74in}
@page :left{margin-left:1.02in;margin-right:0.74in;
  @top-left{content:counter(page);font:9.5pt SERIF;color:#5C574D;vertical-align:bottom;padding-bottom:12pt}
  @top-center{content:"The Roots of Ramallah";font:italic 9.5pt SERIF;letter-spacing:.02em;color:#5C574D;vertical-align:bottom;padding-bottom:12pt}}
@page :right{margin-left:0.74in;margin-right:1.02in;
  @top-center{content:string(chap);font:italic 9.5pt SERIF;color:#5C574D;vertical-align:bottom;padding-bottom:12pt}
  @top-right{content:counter(page);font:9.5pt SERIF;color:#5C574D;vertical-align:bottom;padding-bottom:12pt}}
@page :blank{@top-left{content:none}@top-center{content:none}@top-right{content:none}}
@page front{@top-left{content:none}@top-center{content:none}@top-right{content:none}}
@page opener{margin:0;@top-left{content:none}@top-center{content:none}@top-right{content:none}}

html,body{background:#fff!important}
body{font:10.8pt/1.42 SERIF;color:#1B1A17;text-align:justify;hyphens:auto;-webkit-hyphens:auto;
  orphans:2;widows:2;font-variant-numeric:oldstyle-nums;font-kerning:normal}
.wrap{max-width:none!important;margin:0!important;padding:0!important}
p{margin:0;text-indent:0}
p+p{text-indent:1.3em}
[data-align-last-split-element='justify'] *{text-align-last:auto!important}
h1,h2,h3,h4,.ewhen,.erahead *{text-align-last:auto!important}
a{color:inherit!important;text-decoration:none!important}
sup.cn{font-size:.62em;line-height:0}
sup.cn a{color:#9A6324!important}
b,strong{font-weight:600}
.ar{font-family:"Noto Naskh Arabic","DejaVu Sans",serif}
.pbar,.tocbtn,#toc,.evtoggle,.nextch,.lb,.backto,.updated,.mastrow,.mastrule,.rule-gold,.pullq,
.masthead>.wrap>h1,.masthead>.wrap>.sub,.masthead>.wrap>.byline,.masthead>.wrap>.credit,.masthead>.wrap>.meta,
.fignum::after{display:none!important}
.masthead{background:none!important;border:0!important;padding:0!important}
.evfold>.evbody{display:block!important}
*{box-shadow:none!important;border-radius:0!important}
img{filter:none!important;mix-blend-mode:normal!important}

/* ── title page, its verso, contents ── */
.tp{page:front;break-after:page;height:7.3in;display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:.5in}
.tp .tps{font-variant:small-caps;letter-spacing:.2em;color:#9A6324;font-size:10pt;text-transform:lowercase}
.tp h1{font:500 31pt/1.08 SERIF;color:#004A26;margin:.32in 0 .14in;letter-spacing:.005em}
.tp .tpsub{font:italic 14pt/1.3 SERIF;margin:0;color:#3A3730}
.tp .tprule{width:.9in;border:0;border-top:.6pt solid #9A6324;margin:.34in auto}
.tp img{width:2.3in;height:auto;margin:.1in auto .2in;mix-blend-mode:multiply}
.tp .tpby{font:13pt/1.3 SERIF;margin:auto 0 0;letter-spacing:.02em}
.tp .tped{font:italic 10pt/1.3 SERIF;color:#5C574D;margin:.08in 0 0}
.tpv{page:front;break-after:right;font-size:9pt;line-height:1.45;color:#46423B;padding-top:4.6in;text-align:left}
.tpv p{margin:0 0 .7em;text-indent:0!important}
.tpv .sub,.tpv .credit,.tpv .meta{font-size:9pt!important;margin:0 0 .7em!important;max-width:none!important}
.ptoc{page:front;break-after:right;text-align:left}
.ptoc h2{font:500 22pt/1.1 SERIF;color:#004A26;margin:.35in 0 .32in}
.ptoc ol{list-style:none;margin:0;padding:0}
.ptoc li{margin:0 0 .085in;font-size:10.8pt;line-height:1.25}
.ptoc li.pt{margin:.22in 0 .1in;font-variant:small-caps;text-transform:lowercase;letter-spacing:.14em;color:#9A6324;font-size:10pt}
.ptoc a{display:flex;align-items:baseline}
.ptoc .tn{width:.36in;flex:none;color:#9A6324;font-variant-numeric:lining-nums}
.ptoc .tt{flex:1}
.ptoc .td{font-style:italic;color:#6B675F;font-size:9.6pt}
.ptoc .td::before{content:"  ·  ";font-style:normal}
.ptoc a::after{content:target-counter(attr(href), page);flex:none;padding-left:.15in;font-variant-numeric:oldstyle-nums}

/* ── front matter ── */
.front{max-width:none!important;margin:0!important;break-before:right}
.front h3{font:500 15pt/1.2 SERIF;color:#004A26;margin:0 0 .18in;text-align:left;break-after:avoid}
.front h3:not(:first-of-type){margin-top:.5in}
.front p.ded{font-style:italic;font-size:12pt;line-height:1.5;text-align:center;margin:1.4in .3in 0;text-indent:0!important}
.front p.ded+h3{break-before:right;margin-top:0}
.front figure.frontis{display:none}
.front .howto{break-before:page;background:none!important;border:0!important;padding:0!important;margin:0!important}
.front .howto h4{font:500 15pt/1.2 SERIF;color:#004A26;margin:0 0 .18in}

/* ── chapter opening page: full-bleed picture, numeral, title, epigraph ── */
.erahead{page:opener;break-before:right;break-after:page;margin:0!important;padding:0!important;height:9in;position:relative;text-align:left}
.erahead *,h1,h2,h3,h4,.ptoc,.backhead{text-align:left!important}
.opener{position:relative;height:4.7in;width:6in;margin:0!important;overflow:hidden;background:#fff!important;aspect-ratio:auto!important;max-height:none!important}
.opener img{width:100%;height:100%;object-fit:cover;display:block}
.opener .opnum{display:none}
/* Library of Congress scans are 1024 px: set at two-thirds of the page with white around them */
.opener.framed{width:3.9in;height:3.05in;margin:.75in auto 0 1.05in!important;overflow:visible;background:none!important}
.opener.framed img{object-fit:cover;width:100%!important;transform:none!important}
.opener.framed.stereo{width:2.9in;height:2.75in}
.opener.framed .opcap{position:static;display:block;max-width:none;text-align:left;margin-top:.07in;color:#6B675F;text-shadow:none}
.erahead:has(.opener.framed) .eraband{padding-top:.42in!important;padding-left:1.05in!important}
.erahead:has(.opener.framed) .eraband::before{font-size:44pt}
.opener .opcap{position:absolute;right:.22in;bottom:.12in;max-width:3.4in;text-align:right;
  font:italic 7.6pt/1.3 SERIF;color:#fff;text-shadow:0 0 6px rgba(0,0,0,.75)}
.erahead .eraband{background:none!important;color:#1B1A17!important;margin:0!important;padding:.36in .9in 0 .9in!important;border:0!important}
.erahead .eraband::before{content:attr(data-num);display:block;font:400 52pt/0.9 SERIF;color:#9A6324;margin:0 0 .1in;font-variant-numeric:lining-nums}
.erahead:not(:has(.opener)) .eraband{padding-top:1.7in!important}
.erahead:not(:has(.opener)) .eraband::before{font-size:110pt;color:#C9B48F;margin-bottom:.25in}
.erahead .eraband .ek{font:500 9.5pt/1 SERIF!important;font-variant:small-caps;text-transform:lowercase;letter-spacing:.24em;color:#9A6324!important;margin:0 0 .1in!important}
.erahead .eraband h2{font:500 23pt/1.1 SERIF!important;color:#004A26!important;margin:0!important;letter-spacing:0}
.erahead .eraband h2 .edates{display:block;font:italic 11.5pt/1.3 SERIF!important;color:#5C574D!important;letter-spacing:.02em;margin-top:.07in}
.erahead .eraband .es{font:italic 10.4pt/1.42 SERIF!important;color:#3A3730!important;margin-top:.16in;max-width:4.2in;text-align:left}
.erahead .eraband .es::before{display:block;content:"";width:.55in;border-top:.6pt solid #9A6324!important;margin:0 0 .16in!important}
.erahead .epigraph{margin:.24in .9in 0 1.5in!important;padding:0!important;border:0!important;background:none!important;text-align:left}
.erahead .epigraph p{font:italic 10.6pt/1.42 SERIF!important;color:#3A3730!important;text-indent:0!important}
.erahead .epigraph cite{display:block;margin-top:.06in;font:9pt/1.3 SERIF;font-style:normal;font-variant:small-caps;text-transform:lowercase;letter-spacing:.08em;color:#9A6324}
.erahead:not(:has(.opener)) .epigraph{margin-top:.5in!important}

/* "where our own line stands", now at the head of the chapter's first text page */
.linkat{background:none!important;border:0!important;border-top:.5pt solid #9A6324!important;border-bottom:.5pt solid #D8D0BF!important;
  padding:.08in 0 .06in!important;margin:0 0 .3in!important;font-size:8.6pt;line-height:1.35;break-inside:avoid;text-align:left}
.linkat .lkhead{font:500 8.4pt/1 SERIF!important;font-variant:small-caps;text-transform:lowercase;letter-spacing:.16em;color:#9A6324!important;margin-bottom:.05in}
.linkat .lkladder svg{max-height:1.5in;width:100%}
.linkat .lkladder svg.phonefig{max-height:2.4in!important;width:auto!important;max-width:100%!important;margin:0}

/* ── the running text ── */
.chron::before,.entry::before,.entry::after,.sect::before{display:none!important}
.entry{display:block!important;position:relative;margin:0 0 .17in!important;padding:0!important}
.ewhen{position:absolute!important;margin-top:.02in!important;width:.78in;padding:0!important;margin:0!important;text-align:right!important;line-height:1.15;font-size:8pt}
.pagedjs_left_page .ewhen{left:-.92in;text-align:right!important}
.pagedjs_right_page .ewhen{right:-.92in;left:auto;text-align:left!important}
.ewhen .d{display:block;font:500 9pt/1.15 SERIF!important;color:#9A6324!important;font-variant-numeric:lining-nums;hyphens:none}
.ewhen .g,.ewhen .w2{display:block!important;margin:.04in 0 0!important}
.g,.w2,.badge{background:none!important;color:#9A6324!important;padding:0!important;margin:0!important;border:0!important;
  font:7.6pt/1.2 SERIF!important;font-variant:small-caps!important;text-transform:lowercase!important;letter-spacing:.08em!important;white-space:normal}
.ebody{width:auto!important;max-width:none!important}
.ebody h3{font:600 11.6pt/1.25 SERIF!important;color:#1B1A17;margin:0 0 .05in!important;text-align:left;break-after:avoid;hyphens:none}
.note{font-size:inherit!important;max-width:none!important;color:inherit!important}
.more{margin-top:.08in}
.dropcap::first-letter{float:left;font:400 3.55em/.8 SERIF;color:#004A26;margin:.05em .06em 0 0;padding:0}
.sect{padding:0!important;margin:.34in 0 .2in!important;text-align:center;break-after:avoid}
.sect .sl{display:block;font:500 9.5pt/1 SERIF!important;font-variant:small-caps;text-transform:lowercase;letter-spacing:.24em;color:#9A6324!important;margin-bottom:.05in}
.sect .ss{display:block;font:italic 9.8pt/1.3 SERIF!important;color:#6B675F!important;border:0!important;padding:0!important}
.sect::after{content:"";display:block;width:.4in;margin:.1in auto 0;border-top:.5pt solid #9A6324}

/* the evidence half: a quiet indented section */
.evfold{margin:.2in 0 0;break-before:page}
.evbody{margin-left:.22in;font-size:10pt;line-height:1.4}
.evbody .entry{margin-bottom:.15in!important}

/* side panels */
.scholars,.wwsdk{background:none!important;border:0!important;border-left:.5pt solid #9A6324!important;
  margin:.28in 0 .28in .22in!important;padding:.02in 0 .02in .16in!important;font-size:9.4pt;line-height:1.38;text-align:left}
.scholars h4,.wwsdk h4{font:500 9.5pt/1.2 SERIF!important;font-variant:small-caps;text-transform:lowercase;letter-spacing:.16em;color:#9A6324!important;margin:0 0 .08in!important}
.scholars ul{margin:0;padding:0;list-style:none}
.scholars li{margin:0 0 .07in;break-inside:avoid}
.scholars .sw{font-weight:600}
.wwsdk{break-inside:avoid}

/* quotations: large italic, set off with white space */
blockquote{background:none!important;border:0!important;margin:.22in .3in .22in .3in!important;padding:0!important;
  font:italic 11.6pt/1.42 SERIF!important;color:#2E2B26;max-width:none!important;text-align:left;break-inside:avoid}
blockquote b{font-weight:500}
blockquote .cite{display:block;margin-top:.07in;font:8.6pt/1.3 SERIF;font-style:normal;font-variant:small-caps;text-transform:lowercase;letter-spacing:.06em;color:#9A6324}
.fix{background:none!important;border:0!important;border-top:.5pt solid #9A6324!important;border-bottom:.5pt solid #9A6324!important;
  padding:.08in 0!important;margin:.2in 0!important;break-inside:avoid;font-size:9.8pt}
.fixgrid{display:block!important}
.fixgrid>div{display:block!important;width:auto!important;margin:0 0 .07in!important;padding:0!important;border:0!important;background:none!important;text-align:left}
.fix .fl{display:block;font-variant:small-caps;text-transform:lowercase;letter-spacing:.1em;color:#9A6324;font-size:8.6pt}
.fixhead{font-variant:small-caps;text-transform:lowercase;letter-spacing:.12em;color:#9A6324!important;background:none!important;padding:0!important}

/* figures and photographs: full text width, captions below */
figure{display:block!important;margin:.26in 0!important;padding:0!important;border:0!important;background:none!important;
  break-inside:avoid;max-width:100%!important;text-align:left}
figure .figwrap{order:1;padding:0!important;overflow:visible!important;background:none!important;border:0!important}
figure .fignum{order:2;margin:.08in 0 0!important;font:500 8.4pt/1.2 SERIF!important;font-variant:small-caps;text-transform:lowercase;
  letter-spacing:.16em;color:#9A6324!important;background:none!important;border:0!important;padding:0!important}
figure .fignum::before{display:none!important}
figure .figtitle{order:3;font:italic 10.4pt/1.3 SERIF!important;color:#1B1A17!important;margin:.02in 0 .04in!important;padding:0!important}
figure figcaption{order:4;font:8.6pt/1.38 SERIF!important;color:#46423B!important;padding:0!important;margin:0!important;border:0!important;background:none!important}
figure figcaption .src{display:block;margin-top:.04in;font-style:italic;color:#6B675F!important;font-size:8pt}
figure figcaption .made{font-weight:500!important}
.figwrap img.mapimg{display:block;width:100%;height:auto;max-height:6.7in;object-fit:contain}
.figwrap svg{width:100%!important;min-width:0!important;height:auto!important;max-height:6.7in}
figure.photo img{order:1;display:block;width:auto!important;max-width:100%!important;height:auto;max-height:2.55in!important;object-fit:contain;margin:0 0 .08in!important;border:0!important}
figure.photo.srcpage img{max-height:5.4in!important}
figure.photo figcaption{order:2}
figure.wide .figwrap svg{max-height:6.9in}
/* tall phone-first charts: capped so the chart and its caption share one page */
.figwrap svg.phonefig{max-height:5.3in!important;width:auto!important;max-width:100%!important;display:block;margin:0 auto}

/* tables */
.ntwrap{border:0!important;background:none!important;overflow:visible!important;margin:.2in 0!important}
.ntwrap.keepwhole{break-inside:avoid}
.nthead{background:none!important;color:#9A6324!important;font:500 9pt/1.2 SERIF!important;font-variant:small-caps;text-transform:lowercase;letter-spacing:.12em;
  padding:0 0 .05in!important;border:0!important;border-bottom:.5pt solid #9A6324!important}
table{font-size:8.6pt!important;line-height:1.3;border-collapse:collapse;text-align:left;width:100%}
th{font-weight:500;font-variant:small-caps;text-transform:lowercase;letter-spacing:.06em;color:#5C574D;background:none!important;border:0!important;border-bottom:.5pt solid #9A6324!important}
td{background:none!important;border:0!important;border-bottom:.4pt solid #E2DACA!important;vertical-align:top}
tr{break-inside:avoid}
thead{display:table-header-group}
.tfoot{font-size:8pt;color:#6B675F;font-style:italic}
h2,h3,h4{break-after:avoid;hyphens:none}
.rh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);string-set:chap content(text)}

/* ── back matter ── */
.backhead{break-before:right;margin:0 0 .3in;padding:.9in 0 0;text-align:left}
.backhead .ek{font:500 9.5pt/1 SERIF;font-variant:small-caps;text-transform:lowercase;letter-spacing:.24em;color:#9A6324;margin:0 0 .1in}
.backhead h2{font:500 21pt/1.12 SERIF;color:#004A26;margin:0}
.backhead .es{font:italic 10pt/1.4 SERIF;color:#46423B;margin-top:.14in}
.backhead .es::before{display:block;content:"";width:.55in;border-top:.6pt solid #9A6324;margin:0 0 .14in}
.notes{font-size:8.7pt;line-height:1.36;text-align:left}
.notes ol{padding-left:.28in;margin:0}
.notes li{margin-bottom:.05in}
.notes code,code{font-size:7.6pt;background:none!important;border:0!important;padding:0!important}
.further{font-size:9.6pt;line-height:1.38;text-align:left}
.further p.intro{font-style:italic;margin:0 0 .2in}
.further ul{list-style:none;margin:0;padding:0}
.further li{margin:0 0 .11in;padding-left:.2in;text-indent:-.2in}
.further .imp{display:inline;color:#5C574D;font-style:italic}
footer.end{font-size:8.6pt;color:#6B675F;margin-top:.4in;text-align:center}
footer.end p{text-indent:0!important}

/* chart appendix and companion: plain, ruled */
.appx,.testsec,.howto{background:none!important;border:0!important}
.howto{padding:0!important;margin:0 0 .2in!important}
article{break-inside:avoid;background:none!important;border:0!important;border-bottom:.4pt solid #E2DACA!important;
  padding:.08in 0 .1in!important;margin:0!important;font-size:9.4pt;line-height:1.38;text-align:left}
article .t{font-weight:600;display:block}
article .imp{font-style:italic;color:#5C574D;font-size:9pt}
article .acc{font-size:8.4pt;color:#5C574D}
article .star{color:#9A6324}
h2.keep,h2.parthead{font:500 14pt/1.2 SERIF!important;color:#004A26!important;margin:.3in 0 .12in!important;background:none!important;border:0!important;padding:0!important;text-align:left}
h2.parthead{break-before:page;font-size:17pt!important}
h2.parthead .pnum{display:block;font:500 9.5pt/1 SERIF;font-variant:small-caps;text-transform:lowercase;letter-spacing:.24em;color:#9A6324;margin-bottom:.1in}
.secnote,.partnote{font-style:italic;font-size:9.4pt;color:#46423B;text-align:left}
nav{font-size:9pt}
""".replace('SERIF', SERIF)


def embed(src, px=MAX_PX, crop=None, cache={}):
    """A JPEG data URI for an image under img/, resized and compressed.
    crop='opener' trims the black glass-negative border of a Library of Congress scan;
    crop='stereo' also keeps only the left frame of a stereograph."""
    key = (src, px, crop)
    if key in cache:
        return cache[key]
    from PIL import Image
    path = os.path.normpath(os.path.join(OUT, src))
    if not os.path.exists(path):
        cache[key] = None
        return None
    im = Image.open(path)
    im = im.convert('L' if im.mode in ('L', 'LA', '1') else 'RGB')
    if crop:
        w, h = im.size
        if crop == 'stereo':
            im = im.crop((0, 0, w // 2, h))
            w, h = im.size
        dx, dy = int(w * .055), int(h * .06)
        im = im.crop((dx, dy, w - dx, h - dy))
    if max(im.size) > px:
        im.thumbnail((px, px), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=JPEG_Q, optimize=True, progressive=True)
    cache[key] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    return cache[key]


def font_faces():
    """EB Garamond, embedded, so the PDF never falls back to another face."""
    css = open(os.path.join(FONTS, 'eb-garamond.css'), encoding='utf-8').read()

    def sub(m):
        data = base64.b64encode(open(os.path.join(FONTS, m.group(1)), 'rb').read()).decode()
        return 'url(data:font/woff2;base64,%s)' % data
    return re.sub(r'url\(([^)]+\.woff2)\)', sub, css)


def strip_media_print(css):
    out, i = [], 0
    for m in re.finditer(r'@media\s+print\s*\{', css):
        if m.start() < i:
            continue
        out.append(css[i:m.start()])
        depth, j = 1, m.end()
        while depth and j < len(css):
            depth += {'{': 1, '}': -1}.get(css[j], 0)
            j += 1
        i = j
    out.append(css[i:])
    return ''.join(out)


def block_end(h, start, tag='div'):
    """Index just past the element that opens at start."""
    depth = 0
    for m in re.compile(r'<%s\b|</%s>' % (tag, tag)).finditer(h, start):
        depth += -1 if m.group(0).startswith('</') else 1
        if depth == 0:
            return m.end()
    return len(h)


def text(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


WORDS = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve']


def prepare(h):
    """Everything both volumes share: scripts out, print CSS in, images embedded."""
    h = re.sub(r'<script\b.*?</script>', '', h, flags=re.S)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
    from phone_maps import strip as strip_phone_maps
    h = strip_phone_maps(h)        # v82: print keeps the full map plates
    h = re.sub(r'<link[^>]+fonts\.googleapis[^>]*>', '', h)
    h = re.sub(r'<style>(.*?)</style>', lambda m: '<style>' + strip_media_print(m.group(1)) + '</style>',
               h, count=1, flags=re.S)
    h = h.replace('</style>', font_faces() + PRINT_CSS + '</style>', 1)
    h = h.replace('<meta name="viewport" content="width=device-width,initial-scale=1">', '', 1)
    h = re.sub(r'<button class="evtoggle".*?</button>', '', h, flags=re.S)
    h = re.sub(r'<a class="nextch".*?</a>', '', h, flags=re.S)
    h = re.sub(r'<a class="tocbtn"[^>]*>.*?</a>', '', h, flags=re.S)

    # openers: full-bleed, larger file; dropped when the photo is not held locally
    def opener(m):
        src = m.group(1)
        is_loc = '/img/loc/' in src
        crop = ('stereo' if 'stereo' in m.group(0)[:40] else 'opener') if is_loc else None
        uri = embed(src, OPENER_PX, crop) if src.startswith('../img/') else None
        if not uri:
            return ''
        out = m.group(0).replace(src, uri)
        return re.sub(r'<div class="opener', '<div class="opener framed', out, count=1) if is_loc else out
    h = re.sub(r'<div class="opener(?: stereo)?"><img src="([^"]+)".*?</span></div>', opener, h)
    h = re.sub(r'(<div class="opener[^"]*"><img [^>]*?)\s+onerror="[^"]*"', r'\1', h)

    # photographs: embedded, or left out of print entirely
    dropped = []

    def photo(m):
        src = m.group(2)
        uri = embed(src) if src.startswith('../img/') else None
        if not uri:
            dropped.append(src)
            return ''
        return m.group(0).replace(src, uri).replace(' loading="lazy"', '')
    h = re.sub(r'<figure class="photo[^"]*"[^>]*>(<img [^>]*?src="([^"]+)"[^>]*>).*?</figure>', photo, h, flags=re.S)

    def img(m):
        src = m.group(1)
        if src.startswith('data:'):
            return m.group(0)
        uri = embed(src) if src.startswith('../img/') else None
        if not uri:
            dropped.append(src)
            return ''
        return m.group(0).replace(src, uri).replace(' loading="lazy"', '')
    h = re.sub(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', img, h)

    h = rasterize_maps(h)

    # figure number and title move under the picture, as a caption (block layout: Paged.js
    # does not split flex boxes reliably)
    out, pos = [], 0
    for m in re.finditer(r'<figure[^>]*>(<div class="fignum">.*?</div>)(<div class="figtitle">.*?</div>)(?=<div class="figwrap">)', h, flags=re.S):
        fw = m.end()
        fe = block_end(h, fw)
        out.append(h[pos:m.start()] + m.group(0)[:m.start(1) - m.start()] + h[fw:fe] + m.group(1) + m.group(2))
        pos = fe
    out.append(h[pos:])
    h = ''.join(out)

    # the margin date travels with its entry's heading: move it inside the entry body
    h = re.sub(r'(<div class="entry[^"]*">)(<div class="ewhen">.*?</div>)(<div class="ebody">)',
               r'\1\3\2', h, flags=re.S)

    # wide maps get a little more height
    h = re.sub(r'<figure>(<div class="fignum">)', r'<figure class="wide">\1', h)

    # small tables kept whole
    h = re.sub(r'<div class="ntwrap">.*?</table>',
               lambda m: m.group(0).replace('class="ntwrap"', 'class="ntwrap keepwhole"', 1)
               if m.group(0).count('<tr') <= 14 else m.group(0), h, flags=re.S)
    return h, dropped


def rasterize_maps(h):
    """Terrain maps carry a hillshade raster under semi-transparent vector layers, which
    Chromium's PDF writer flattens into huge lossless images. Render each such map once,
    at print resolution, to a JPEG instead: the page looks the same and the PDF is a
    fraction of the size."""
    from PIL import Image
    from playwright.sync_api import sync_playwright
    svgs = [m for m in re.finditer(r'<svg\b[^>]*>.*?</svg>', h, flags=re.S) if '<image' in m.group(0)]
    if not svgs:
        return h
    out, pos = [], 0
    with sync_playwright() as p:
        exe = os.environ.get('PRINT_CHROMIUM')
        b = p.chromium.launch(**({'executable_path': exe} if exe else {}))
        pg = b.new_page(viewport={'width': 1400, 'height': 1000}, device_scale_factor=1)
        for m in svgs:
            svg = m.group(0)
            vb = re.search(r'viewBox="([\d.\s-]+)"', svg)
            w, hh = (float(x) for x in vb.group(1).split()[2:4]) if vb else (860, 600)
            px_w = 1400
            px_h = int(round(px_w * hh / w))
            pg.set_viewport_size({'width': px_w, 'height': px_h})
            pg.set_content('<html><body style="margin:0;background:#fff">%s</body></html>'
                           % re.sub(r'<svg\b', '<svg style="display:block;width:%dpx;height:%dpx"' % (px_w, px_h), svg, count=1))
            png = pg.screenshot(clip={'x': 0, 'y': 0, 'width': px_w, 'height': px_h})
            im = Image.open(io.BytesIO(png)).convert('RGB')
            buf = io.BytesIO()
            im.save(buf, 'JPEG', quality=84, optimize=True, progressive=True)
            label = re.search(r'aria-label="([^"]*)"', svg)
            out.append(h[pos:m.start()])
            out.append('<img class="mapimg" alt="%s" src="data:image/jpeg;base64,%s">'
                       % (label.group(1) if label else '', base64.b64encode(buf.getvalue()).decode()))
            pos = m.end()
        b.close()
    out.append(h[pos:])
    return ''.join(out)


def paged(h):
    js = open(PAGED, encoding='utf-8').read()
    return h.replace('</head>', '<script>window.PagedConfig={auto:true,after:function(f){window.__pagedDone=f.total||true;}};'
                     '</script><script>%s</script></head>' % js, 1)


def build_main(h, bib, harness):
    toc = []
    # chapters: numeral for the opening page, running-head string, the link block after the opener
    out, pos = [], 0
    for m in re.finditer(r'<div class="erahead" id="(ch\d+)">', h):
        cid = m.group(1)
        e = block_end(h, m.start())
        blk = h[m.start():e]
        ek = re.search(r'<div class="ek">([^<]*)</div>', blk).group(1)
        h2 = re.search(r'<h2>(.*?)</h2>', blk, flags=re.S).group(1)
        dm = re.search(r'<span class="edates">(.*?)</span>', h2)
        title = text(re.sub(r'<span class="edates">.*?</span>', '', h2))
        num = cid[2:] if ek.upper().startswith('CHAPTER') else ''
        toc.append((cid, num, title, text(dm.group(1)) if dm else ''))
        blk = blk.replace('<div class="eraband">', '<div class="eraband" data-num="%s">' % num, 1)
        blk = blk.replace('<h2>', '<h2><span class="rh">%s</span>' % title, 1)
        la = blk.find('<div class="linkat">')
        link = ''
        if la > 0:
            le = block_end(blk, la)
            link, blk = blk[la:le], blk[:la] + blk[le:]
        out.append(h[pos:m.start()] + blk + link)
        pos = e
    out.append(h[pos:])
    h = ''.join(out)

    # cut the bibliography and the test harness out to the companion
    a, c = h.find('<h2 id="appA"'), h.find('<h2 id="appC"')
    h = h[:a] + h[c:]
    b, r = h.find('<h2 id="appB"'), h.find('<div class="eraband"><div class="ek">Notes</div>')
    h = h[:b] + h[r:]

    # the chart appendix and the notes get plain book headings
    mc = re.search(r'<h2 id="appC" class="eraband"[^>]*><div class="ek">([^<]*)</div>(.*?)<div class="es">(.*?)</div></h2>', h, flags=re.S)
    chart_title = text(mc.group(2))
    h = h[:mc.start()] + ('<div class="backhead" id="appC"><div class="ek">%s</div><h2><span class="rh">%s</span>%s</h2>'
                          '<div class="es">%s</div></div>' % (mc.group(1), chart_title, mc.group(2), mc.group(3))) + h[mc.end():]
    further = further_reading(bib)
    h = h.replace('<div class="eraband"><div class="ek">Notes</div><h2>References</h2><div class="es">',
                  further + '<div class="backhead" id="refs"><div class="ek">Notes</div><h2><span class="rh">References</span>References</h2><div class="es">', 1)
    back = [('appC', chart_title), ('further', 'Further reading'), ('refs', 'References')]

    # title page, verso, contents
    mh = re.search(r'<header class="masthead"><div class="wrap">(.*?)<div class="front">', h, flags=re.S).group(1)
    h1 = text(re.search(r'<h1>(.*?)</h1>', mh, flags=re.S).group(1))
    subs = re.findall(r'<p class="sub">(.*?)</p>', mh, flags=re.S)
    byline = re.search(r'<p class="byline">(.*?)</p>', mh, flags=re.S).group(1)
    series = re.search(r'<span class="l">(.*?)</span>', mh, flags=re.S).group(1)
    edition = re.search(r'<span class="r">(.*?)</span>', mh, flags=re.S).group(1).split('&middot;')[-1].strip()
    updated = re.search(r'<p class="updated">(.*?)</p>', mh, flags=re.S).group(1)
    fm = re.search(r'<figure class="frontis"><img src="([^"]+)"', h)
    tp = ('<section class="tp"><div class="tps">%s</div><h1>%s</h1><p class="tpsub">%s</p><hr class="tprule">%s'
          '<p class="tpby">%s</p><p class="tped">%s &middot; %s</p></section>'
          % (series, h1, text(subs[0]), '<img src="%s" alt="">' % fm.group(1) if fm else '',
             byline, edition[:1].upper() + edition[1:], updated))
    verso = '<section class="tpv">%s<p>The annotated bibliography and the test harness are printed in the companion volume.</p></section>' % ''.join(
        re.findall(r'<p class="(?:sub|credit|meta)">.*?</p>', mh, flags=re.S)[1:])
    li = ['<li><a href="#%s"><span class="tn">%s</span><span class="tt">%s%s</span></a></li>'
          % (cid, num, title, '<span class="td">%s</span>' % d if d else '') for cid, num, title, d in toc]
    li.append('<li class="pt">At the back</li>')
    li += ['<li><a href="#%s"><span class="tn"></span><span class="tt">%s</span></a></li>' % (i, t) for i, t in back]
    contents = '<section class="ptoc"><h2>Contents</h2><ol>%s</ol></section>' % ''.join(li)
    h = h.replace('<header class="masthead">', tp + verso + contents + '<header class="masthead">', 1)
    return paged(h), toc, back


def further_reading(bib):
    arts = re.findall(r'<article[^>]*>(.*?)</article>', bib, flags=re.S)
    items, seen = [], set()
    for key in FURTHER:
        for a in arts:
            t = re.search(r'<span class="t">(.*?)</span>\s*<div class="imp">(.*?)</div>', a, flags=re.S)
            if t and key in t.group(1) and key not in seen:
                seen.add(key)
                title = re.sub(r'<span class="star">★</span>\s*', '', t.group(1)).strip()
                items.append('<li>%s. <span class="imp">%s</span></li>' % (title.rstrip('.'), t.group(2).strip()))
                break
    return ('<div class="backhead" id="further"><div class="ek">Further reading</div><h2><span class="rh">Further reading</span>'
            'A short shelf</h2></div><div class="further"><p class="intro">Fifteen books and articles to start with, from the '
            'annotated bibliography. The bibliography is printed in full, with what each work says and where to find it, '
            'in the companion volume.</p><ul>%s</ul></div>' % ''.join(items))


def build_companion(head, bib, harness, mh_series, h1):
    def plain(seg, sid):
        return re.sub(r'<h2 id="(app[AB])" class="eraband"[^>]*><div class="ek">([^<]*)</div>(.*?)<div class="es">(.*?)</div></h2>',
                      lambda m: '<div class="backhead" id="%s"><div class="ek">%s</div><h2><span class="rh">%s</span>%s</h2>'
                      '<div class="es">%s</div></div>' % (m.group(1), m.group(2), text(m.group(3)), m.group(3), m.group(4)),
                      seg, count=1, flags=re.S)
    bib, harness = plain(bib, 'appA'), plain(harness, 'appB')
    tA = text(re.search(r'id="appA">.*?<h2>(.*?)</h2>', bib, flags=re.S).group(1))
    tB = text(re.search(r'id="appB">.*?<h2>(.*?)</h2>', harness, flags=re.S).group(1))
    tp = ('<section class="tp"><div class="tps">%s</div><h1>%s</h1><p class="tpsub">Companion volume</p><hr class="tprule">'
          '<p class="tpsub" style="font-size:11.5pt">The annotated bibliography and the test harness</p></section>'
          '<section class="tpv"><p>This companion holds the two long reference sections of <i>The Roots of Ramallah</i>. '
          'The notes, a short list of further reading and the book itself are in the main volume.</p></section>'
          % (mh_series, h1))
    toc = ('<section class="ptoc"><h2>Contents</h2><ol><li><a href="#appA"><span class="tn"></span><span class="tt">%s</span></a></li>'
           '<li><a href="#appB"><span class="tn"></span><span class="tt">%s</span></a></li></ol></section>'
           % (tA[:len(tA) // 2] if tA[:len(tA) // 2] * 2 == tA else tA, tB[:len(tB) // 2] if tB[:len(tB) // 2] * 2 == tB else tB))
    return paged(head + '<body>' + tp + toc + '<main><div class="wrap">' + bib + harness + '</div></main></body></html>')


def render(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    with sync_playwright() as p:
        exe = os.environ.get('PRINT_CHROMIUM')
        b = p.chromium.launch(**({'executable_path': exe} if exe else {}))
        pg = b.new_page(viewport={'width': 1200, 'height': 900})
        pg.set_default_timeout(40 * 60 * 1000)
        pg.goto('file://' + html_path)
        pg.wait_for_function('window.__pagedDone', polling=2000, timeout=40 * 60 * 1000)
        n = pg.evaluate('document.querySelectorAll(".pagedjs_page").length')
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        b.close()
    return n, time.time() - t0


def main():
    src = open(SRC, encoding='utf-8').read()
    h, dropped = prepare(src)
    bib = h[h.find('<h2 id="appA"'):h.find('<h2 id="appC"')]
    harness = h[h.find('<h2 id="appB"'):h.find('<div class="eraband"><div class="ek">Notes</div>')]
    head = h[:h.find('<body')]
    mh = re.search(r'<header class="masthead"><div class="wrap">(.*?)<div class="front">', h, flags=re.S).group(1)
    series = re.search(r'<span class="l">(.*?)</span>', mh, flags=re.S).group(1)
    h1 = text(re.search(r'<h1>(.*?)</h1>', mh, flags=re.S).group(1))

    main_html, toc, back = build_main(h, bib, harness)
    comp_html = build_companion(head, bib, harness, series, h1)
    files = []
    for name, doc in (('Roots_of_Ramallah', main_html), ('Roots_of_Ramallah_Companion', comp_html)):
        hp = os.path.join(OUT, name + '_print.html')
        open(hp, 'w', encoding='utf-8').write(doc)
        files.append((hp, os.path.join(OUT, name + '_6x9.pdf')))
        print('%s: %d bytes' % (hp, os.path.getsize(hp)))
    print('%d chapters; %d photographs left out of print (not held in img/)' % (len(toc), len(set(dropped))))
    for s in sorted(set(dropped)):
        print('   not embedded:', s)
    if '--html-only' not in sys.argv:
        for hp, pp in files:
            n, secs = render(hp, pp)
            print('%s: %d pages, %d bytes, %.0f s' % (pp, n, os.path.getsize(pp), secs))


if __name__ == '__main__':
    main()
