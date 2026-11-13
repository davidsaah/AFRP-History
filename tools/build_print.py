#!/usr/bin/env python3
"""Print edition of The Roots of Ramallah (v79).

Reads the finished phone/desktop book, out/AFRP_The_One_Line_v5.html, and
writes two files:

  out/Roots_of_Ramallah_print.html   the book set for 6 x 9 inch pages with
                                     Paged.js (vendored in tools/vendor/)
  out/Roots_of_Ramallah_6x9.pdf      that file rendered by Chromium

The text and facts of the book are not touched. This script only:
  * builds a title page and a contents page with page numbers,
  * sets running heads (book title on the verso, chapter on the recto) and folios,
  * starts each chapter on a right-hand page, with its photograph where one is held,
  * keeps figures, tables and evidence boxes whole,
  * embeds every photograph held in img/ as a compressed data URI,
  * hides the screen-only controls (Chapters button, evidence toggles, lightbox,
    progress bar, next-chapter links, swipe hints).

Photographs linked from tile.loc.gov are not embedded, because they cannot be
downloaded from the build machine. Each prints as a captioned frame that says so.
Run `python3 tools/build_print.py --html-only` to skip the PDF.
"""
import base64
import io
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'out', 'AFRP_The_One_Line_v5.html')
OUT_HTML = os.path.join(ROOT, 'out', 'Roots_of_Ramallah_print.html')
OUT_PDF = os.path.join(ROOT, 'out', 'Roots_of_Ramallah_6x9.pdf')
PAGED = os.path.join(ROOT, 'tools', 'vendor', 'paged.polyfill.min.js')

MAX_PX = 1000      # about 3.5 inches at 280 dpi; photos print no wider than the text block
JPEG_Q = 68

PRINT_CSS = r"""
/* ---- v79 print edition (tools/build_print.py) ---- */
@page{size:6in 9in;margin:0.72in 0.6in 0.78in 0.82in;
  @bottom-center{content:none}}
@page :left{margin-left:0.6in;margin-right:0.82in;
  @top-left{content:counter(page);font:9pt "Times New Roman",Times,"Liberation Serif",serif;color:#5C574D;vertical-align:bottom;padding-bottom:10pt}
  @top-center{content:"The Roots of Ramallah";font:italic 9pt "Times New Roman",Times,"Liberation Serif",serif;color:#5C574D;vertical-align:bottom;padding-bottom:10pt}}
@page :right{margin-left:0.82in;margin-right:0.6in;
  @top-center{content:string(chap, first-except);font:italic 9pt "Times New Roman",Times,"Liberation Serif",serif;color:#5C574D;vertical-align:bottom;padding-bottom:10pt}
  @top-right{content:counter(page);font:9pt "Times New Roman",Times,"Liberation Serif",serif;color:#5C574D;vertical-align:bottom;padding-bottom:10pt}}
@page :blank{@top-left{content:none}@top-center{content:none}@top-right{content:none}}
@page front{@top-left{content:none}@top-center{content:none}@top-right{content:none}}
@page :first{@top-left{content:none}@top-center{content:none}@top-right{content:none}}

html,body{background:#fff!important}
body{font:10.4pt/1.42 "Times New Roman",Times,"Liberation Serif",serif;color:#1A1A1A;
  hyphens:auto;-webkit-hyphens:auto;orphans:3;widows:3}
.wrap{max-width:none!important;margin:0!important;padding:0!important}
p{margin:0 0 .55em}
a{color:inherit;text-decoration:none}
sup.cn a{color:#007a3d}
.pbar,.tocbtn,#toc,.evtoggle,.nextch,.lb,.backto,.updated,.mastrow,.mastrule,.rule-gold,
.masthead>.wrap>h1,.masthead>.wrap>.sub,.masthead>.wrap>.byline{display:none!important}
.masthead{background:none!important;border:0!important;padding:0!important}
.evfold>.evbody{display:block!important}
.fignum::after{content:none!important}

/* title page and its verso */
.tp{page:front;break-after:right;height:7.4in;display:flex;flex-direction:column;align-items:center;
  justify-content:space-between;text-align:center;padding-top:.25in}
.tp .tps{font-variant:small-caps;letter-spacing:.14em;color:#9a6324;font-size:10pt}
.tp h1{font-size:30pt;line-height:1.1;margin:.18in 0 .08in;color:#004A26;font-weight:700}
.tp .tpsub{font-size:13pt;font-style:italic;margin:0}
.tp img{width:2.6in;height:auto;margin:.2in auto}
.tp .tpby{font-size:12pt;margin:0}
.tp .tped{font-size:9.5pt;color:#5C574D;margin:.06in 0 0}
.tp .tprule{width:1.2in;border:0;border-top:1.5px solid #007a3d;margin:.12in auto}
.tpv{page:front;break-after:right;font-size:9pt;color:#46423B;padding-top:4.2in}
.tpv p{margin:0 0 .6em}
.tpv .sub{font-size:9pt!important}

/* contents */
.ptoc{page:front;break-after:right}
.ptoc h2{font-size:18pt;color:#004A26;margin:.1in 0 .25in;font-weight:700}
.ptoc ol{list-style:none;margin:0;padding:0}
.ptoc li{margin:0 0 .07in;font-size:10.2pt;line-height:1.25}
.ptoc li.pt{margin-top:.12in;font-variant:small-caps;letter-spacing:.1em;color:#9a6324;font-size:9pt}
.ptoc a{display:flex;align-items:baseline}
.ptoc .tn{width:.34in;flex:none;color:#007a3d;font-weight:700}
.ptoc .tt{flex:1}
.ptoc .td{display:block;font-size:8.6pt;color:#5C574D;font-style:italic}
.ptoc a::after{content:target-counter(attr(href), page);flex:none;padding-left:.12in;color:#1A1A1A}

/* front matter */
.front{max-width:none!important;margin:0!important;break-before:right}
.front h3{font-size:14pt;color:#004A26;margin:0 0 .12in;break-after:avoid}
.front h3+p.ded{font-style:italic}
.front figure.frontis{display:none}
.front .howto{break-before:page}

/* chapters: right-hand opening, photo, band */
.erahead{break-before:right;margin:0!important;padding:0!important}
h2.eraband,#refs{break-before:right}
.opener{position:relative;aspect-ratio:auto!important;height:3.55in;margin:0 0 0!important;border-radius:0!important;overflow:hidden;break-inside:avoid;background:#004A26}
.opener img{width:100%;height:100%;object-fit:cover;opacity:1!important;filter:none!important}
.opener .opnum{font-size:44pt!important;bottom:.06in!important;left:.18in!important;right:auto!important}
.eraband{margin:0 0 .16in!important;padding:.2in .22in!important;border-radius:0!important;break-inside:avoid}
.erahead .eraband{margin-bottom:0!important}
.eraband .ek{font-size:8pt!important}
.eraband h2,h2.eraband{font-size:17pt!important;line-height:1.18!important}
.eraband .es{font-size:9.6pt!important;line-height:1.4!important}
.eraband .edates{font-size:10pt!important}
.erahead:not(:has(.opener)) .eraband{padding-top:1.1in!important}
.linkat{padding:.1in .16in!important;border-radius:0!important;font-size:8.6pt;break-inside:avoid;margin-bottom:.2in!important}
.linkat svg{max-height:2.1in}

/* timeline: on paper each entry opens with its date line (grid layouts do not split well across pages) */
.chron::before,.entry::before,.sect::before{display:none!important}
.entry{display:block!important;margin:0 0 .2in!important}
.ewhen{display:flex!important;flex-wrap:wrap;align-items:baseline;gap:.08in;text-align:left!important;
  font-size:9pt;margin:0 0 .03in;padding:0!important;break-after:avoid}
.ewhen *{position:static!important}
.ebody{width:auto!important;max-width:none!important}
.ewhen .g{font-size:6.6pt!important;padding:1px 3px!important;white-space:normal}
.ebody h3{font-size:11.6pt!important;break-after:avoid;margin-bottom:.05in!important}
.sect{padding:0!important;margin:.25in 0 .14in!important;break-after:avoid}
.scholars,.wwsdk{margin:.18in 0!important;padding:.1in .14in!important}
.scholars li{break-inside:avoid}
.wwsdk{break-inside:avoid}
.pullq{break-inside:avoid;margin:.18in 0 .2in!important;font-size:12pt!important}

/* evidence half: a distinct panel */
.evfold{margin:.12in 0 0}
.evbody{border-top:1.5px solid #007a3d;padding-top:.06in}

/* figures, photos, tables kept whole and scaled to the page */
figure,.photo,.fix,.note blockquote,blockquote,.ntwrap.keepwhole,table.keepwhole{break-inside:avoid}
figure{margin:.16in 0!important;padding:0!important;max-width:100%!important;border-radius:0!important}
.figwrap{padding:0!important;overflow:visible!important}
.figwrap svg{width:100%!important;min-width:0!important;height:auto!important;max-height:6.4in}
.fignum,.figtitle{break-after:avoid}
.photo{padding:0!important}
.photo img{max-height:4.6in;width:auto!important;max-width:100%!important;margin:0 auto;display:block}
figcaption{font-size:8.4pt!important;line-height:1.35!important}
.noimg{border:1px solid #DCD6C9;background:#FCFAF5;color:#5C574D;font-size:8.4pt;font-style:italic;
  padding:.18in .16in;text-align:center}
.ntwrap{overflow:visible!important}
table{font-size:8.4pt!important}
tr{break-inside:avoid}
thead{display:table-header-group}
h2,h3,h4{break-after:avoid}
.rh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);string-set:chap content(text)}

/* bibliography and notes */
article{break-inside:avoid}
.notes{font-size:8.6pt;line-height:1.36}
.notes li{margin-bottom:.06in}
footer.end{font-size:8.6pt;color:#5C574D;margin-top:.3in}
"""


def embed(src, cache={}):
    """Return a JPEG data URI for an image under img/, resized and compressed."""
    if src in cache:
        return cache[src]
    from PIL import Image
    path = os.path.normpath(os.path.join(ROOT, 'out', src))
    if not os.path.exists(path):
        cache[src] = None
        return None
    im = Image.open(path)
    im = im.convert('L' if im.mode in ('L', 'LA', '1') else 'RGB')
    if max(im.size) > MAX_PX:
        im.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=JPEG_Q, optimize=True, progressive=True)
    uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    cache[src] = uri
    return uri


def strip_media_print(css):
    """Drop the screen book's own @media print blocks; the print edition sets its own rules."""
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


def text(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def build_html():
    h = open(SRC, encoding='utf-8').read()

    # scripts out (the screen reader's JS is not wanted on paper)
    h = re.sub(r'<script\b.*?</script>', '', h, flags=re.S)
    # the book's print rules out, ours in
    h = re.sub(r'<style>(.*?)</style>',
               lambda m: '<style>' + strip_media_print(m.group(1)) + '</style>', h, count=1, flags=re.S)
    h = h.replace('</style>', PRINT_CSS + '</style>', 1)

    # screen-only controls
    h = re.sub(r'<button class="evtoggle".*?</button>', '', h, flags=re.S)
    h = re.sub(r'<a class="nextch".*?</a>', '', h, flags=re.S)
    h = re.sub(r'<a class="tocbtn"[^>]*>.*?</a>', '', h, flags=re.S)

    # openers: keep only photos held in img/
    def opener(m):
        return m.group(0) if m.group(1).startswith('../img/') else ''
    h = re.sub(r'<div class="opener"><img src="([^"]+)"[^>]*><span class="opnum">\d+</span></div>', opener, h)

    # photographs: embed local ones, mark the unreachable ones
    missing = []

    def img(m):
        tag, src = m.group(0), m.group(1)
        if src.startswith('data:'):
            return tag
        if src.startswith('../img/'):
            uri = embed(src)
            if uri:
                tag = tag.replace(src, uri).replace(' loading="lazy"', '')
                return re.sub(r'\s+onerror="[^"]*"', '', tag)
        missing.append(src)
        return ('<div class="noimg">This photograph is held online by the Library of Congress and is not '
                'embedded in this draft.</div>')
    h = re.sub(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*>', img, h)

    # small tables are kept whole; long ones break between rows
    def keep(m):
        return m.group(0).replace('class="ntwrap"', 'class="ntwrap keepwhole"', 1) \
            if m.group(0).count('<tr') <= 14 else m.group(0)
    h = re.sub(r'<div class="ntwrap">.*?</table>', keep, h, flags=re.S)

    # running-head strings and contents entries
    toc = []
    for m in re.finditer(r'<div class="erahead" id="(ch\d+)">.*?<div class="ek">([^<]*)</div><h2>(.*?)</h2>', h, flags=re.S):
        cid, ek, h2 = m.groups()
        dm = re.search(r'<span class="edates">(.*?)</span>', h2)
        title = text(re.sub(r'<span class="edates">.*?</span>', '', h2))
        num = cid[2:] if ek.upper().startswith('CHAPTER') else ''
        toc.append((cid, num, title, text(dm.group(1)) if dm else ''))
    h = re.sub(r'(<div class="erahead" id="ch\d+">.*?<h2>)(.*?)(<span class="edates">|</h2>)',
               lambda m: m.group(1) + '<span class="rh">%s</span>' % text(m.group(2)) + m.group(2) + m.group(3),
               h, flags=re.S)

    back = []
    for m in re.finditer(r'<h2 id="(app[A-Z])" class="eraband"[^>]*><div class="ek">([^<]*)</div>(.*?)<div class="es">', h, flags=re.S):
        back.append((m.group(1), m.group(2), text(m.group(3))))
    h = re.sub(r'(<h2 id="app[A-Z]" class="eraband"[^>]*><div class="ek">[^<]*</div>)(.*?)(<div class="es">)',
               lambda m: m.group(1) + '<span class="rh">%s</span>' % text(m.group(2)) + m.group(2) + m.group(3),
               h, flags=re.S)
    h = h.replace('<div class="eraband"><div class="ek">Notes</div><h2>References</h2>',
                  '<div class="eraband" id="refs"><div class="ek">Notes</div>'
                  '<h2><span class="rh">References</span>References</h2>', 1)
    back.append(('refs', 'Notes', 'References'))

    # title page, its verso, contents
    mh = re.search(r'<header class="masthead"><div class="wrap">(.*?)<div class="front">', h, flags=re.S).group(1)
    h1 = text(re.search(r'<h1>(.*?)</h1>', mh, flags=re.S).group(1))
    subs = re.findall(r'<p class="sub">(.*?)</p>', mh, flags=re.S)
    byline = re.search(r'<p class="byline">(.*?)</p>', mh, flags=re.S).group(1)
    series = re.search(r'<span class="l">(.*?)</span>', mh, flags=re.S).group(1)
    edition = re.search(r'<span class="r">(.*?)</span>', mh, flags=re.S).group(1)
    updated = re.search(r'<p class="updated">(.*?)</p>', mh, flags=re.S).group(1)
    fm = re.search(r'<figure class="frontis"><img src="([^"]+)"', h)
    frontis = '<img src="%s" alt="">' % fm.group(1) if fm else ''
    edition_short = edition.split('&middot;')[-1].strip()
    title_page = (
        '<section class="tp"><div><div class="tps">%s</div><h1>%s</h1><p class="tpsub">%s</p></div>%s'
        '<div><hr class="tprule"><p class="tpby">%s</p><p class="tped">%s &middot; %s</p></div></section>'
        % (series, h1, text(subs[0]), frontis, byline, edition_short[:1].upper() + edition_short[1:], updated))
    verso = '<section class="tpv">%s</section>' % ''.join(
        re.findall(r'<p class="(?:sub|credit|meta)">.*?</p>', mh, flags=re.S)[1:])
    words = {'1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five', '6': 'Six', '7': 'Seven',
             '8': 'Eight', '9': 'Nine', '10': 'Ten', '11': 'Eleven', '12': 'Twelve'}
    li = []
    for cid, num, title, dates in toc:
        li.append('<li><a href="#%s"><span class="tn">%s</span><span class="tt">%s%s</span></a></li>'
                  % (cid, num, title, '<span class="td">%s</span>' % dates if dates else ''))
    li.append('<li class="pt">Appendices and notes</li>')
    for aid, ek, title in back:
        li.append('<li><a href="#%s"><span class="tn"></span><span class="tt">%s</span></a></li>' % (aid, title))
    contents = '<section class="ptoc"><h2>Contents</h2><ol>%s</ol></section>' % ''.join(li)
    h = h.replace('<header class="masthead">', title_page + verso + contents + '<header class="masthead">', 1)

    # Paged.js, inline so the file stands alone
    paged = open(PAGED, encoding='utf-8').read()
    h = h.replace('</head>', '<script>window.PagedConfig={auto:true,after:function(f){window.__pagedDone=f.total||true;}};</script>'
                  '<script>%s</script></head>' % paged, 1)
    h = h.replace('<meta name="viewport" content="width=device-width,initial-scale=1">', '', 1)
    open(OUT_HTML, 'w', encoding='utf-8').write(h)
    return h, missing, toc, back


def render_pdf():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    with sync_playwright() as p:
        # PRINT_CHROMIUM names a Chrome/Chromium binary when Playwright's own is not installed
        exe = os.environ.get('PRINT_CHROMIUM')
        b = p.chromium.launch(**({'executable_path': exe} if exe else {}))
        pg = b.new_page(viewport={'width': 1200, 'height': 900})
        pg.set_default_timeout(40 * 60 * 1000)
        pg.goto('file://' + OUT_HTML)
        pg.wait_for_function('window.__pagedDone', polling=2000, timeout=40 * 60 * 1000)
        n = pg.evaluate('document.querySelectorAll(".pagedjs_page").length')
        pg.pdf(path=OUT_PDF, prefer_css_page_size=True, print_background=True)
        b.close()
    return n, time.time() - t0


if __name__ == '__main__':
    h, missing, toc, back = build_html()
    print('print html: %s (%d bytes); %d chapters, %d back sections; %d photos not embedded'
          % (OUT_HTML, os.path.getsize(OUT_HTML), len(toc), len(back), len(missing)))
    if '--html-only' not in sys.argv:
        n, secs = render_pdf()
        print('pdf: %s, %d pages, %d bytes, %.0f s' % (OUT_PDF, n, os.path.getsize(OUT_PDF), secs))
