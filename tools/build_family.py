#!/usr/bin/env python3
"""The family edition of The Roots of Ramallah (v81).

Reads the finished book, out/AFRP_The_One_Line_v5.html, and writes:

  out/Roots_of_Ramallah_Family_print.html   the family edition set for 6 x 9 inch pages (Paged.js)
  out/Roots_of_Ramallah_Family_6x9.pdf      that file rendered by Chromium

The family edition is the story half of every chapter, word for word, with the
evidence taken away: no evidence halves, no tables, no note numbers, no evidence
labels, no correction boxes and no reading lists. Nothing is rewritten and
nothing is added except headings and the editions note on the title verso.
What it adds is pictures and shape:

  * a timeline of the whole story at the front, from the chapter titles and dates;
  * at the head of each chapter, a timeline of that chapter's entries;
  * at the end of each chapter, a photo essay of every photograph the full book
    prints for that era, in the story or in the evidence;
  * three family panels, built from passages and figures of the full book:
    the Saah, the five sons, and the emigrants.

It shares the design, the type and the image handling of tools/build_print.py.

    python3 tools/build_family.py              # HTML and PDF
    python3 tools/build_family.py --html-only
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_print as bp  # noqa: E402

OUT = bp.OUT
SERIF = bp.SERIF

FAMILY_CSS = r"""
/* ════════ v81 family edition (tools/build_family.py) ════════ */
body{font-size:10.9pt;line-height:1.43}
@page :left{@top-center{content:"The Roots of Ramallah · Family edition"}}
.tp .tped{margin-top:.12in}
.tpv{padding-top:4.2in}

/* the story at a glance */
.glance{break-before:right;text-align:left}
.glance h2{font:500 22pt/1.1 SERIF;color:#004A26;margin:.35in 0 .08in}
.glance .gs{font:italic 10.4pt/1.4 SERIF;color:#46423B;margin:0 0 .3in}
.glance ol{list-style:none;margin:0;padding:0 0 0 .3in;border-left:1.2pt solid #9A6324;position:relative}
.glance li{position:relative;margin:0 0 .17in;break-inside:avoid}
.glance li::before{content:"";position:absolute;left:-.365in;top:.05in;width:.11in;height:.11in;border-radius:50%!important;background:#007A3D}
.glance li.clos::before{background:#9A6324}
.glance .gd{display:block;font:500 9pt/1.2 SERIF;color:#9A6324;font-variant-numeric:lining-nums;letter-spacing:.03em}
.glance .gt{display:block;font:600 11.2pt/1.25 SERIF;color:#1B1A17}
.glance .ge{display:block;font:italic 9.6pt/1.35 SERIF;color:#46423B;margin-top:.02in}
.glance .gn{color:#9A6324;font-weight:500;margin-right:.08in}

/* this chapter at a glance */
.chtl{break-inside:avoid;margin:0 0 .32in;padding:.1in 0 .06in;border-top:.5pt solid #9A6324;border-bottom:.5pt solid #D8D0BF;text-align:left}
.chtl .chh{font:500 8.6pt/1 SERIF;font-variant:small-caps;text-transform:lowercase;letter-spacing:.18em;color:#9A6324;margin:0 0 .09in}
.chtl ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1.05in 1fr;column-gap:.12in;row-gap:.045in}
.chtl li{display:contents}
.chtl .cd{font:500 8.8pt/1.3 SERIF;color:#9A6324;text-align:right;font-variant-numeric:lining-nums;position:relative;padding-right:.1in;border-right:1pt solid #007A3D}
.chtl .ct{font:9.8pt/1.3 SERIF;color:#1B1A17}

/* the story with nothing in the margin but the date */
.ewhen .g,.ewhen .w2{display:none!important}

/* photo essay */
.essay{break-before:page;text-align:left}
.essay .eh{margin:0 0 .22in;padding:.05in 0 0}
.essay .eh .ek{font:500 9pt/1 SERIF;font-variant:small-caps;text-transform:lowercase;letter-spacing:.24em;color:#9A6324;margin:0 0 .06in}
.essay .eh h3{font:500 17pt/1.15 SERIF;color:#004A26;margin:0}
.essay .prow{break-inside:avoid;font-size:0;line-height:0;margin:0 0 .2in}
.essay figure.photo{display:inline-block!important;vertical-align:top;width:48.5%!important;margin:0!important;break-inside:avoid;font-size:8pt;line-height:1.3}
.essay figure.photo.lft{margin-right:3%!important}
.essay figure.photo.wide2{width:100%!important;margin-right:0!important}
.essay figure.photo img{max-height:2.2in!important;max-width:100%!important;margin:0 0 .06in!important}
.essay figure.photo.wide2 img{max-height:3.3in!important}
.essay figure.photo figcaption{font-size:7.9pt!important;line-height:1.32!important}
.essay figure.photo figcaption .src{font-size:7.2pt!important}
/* no blank versos in the family edition */
.erahead{break-before:page!important}
.tpv,.ptoc{break-after:page!important}
.glance{break-before:page!important}

/* family panels */
.fam{break-inside:avoid;background:#F7F2E8!important;border-top:1.4pt solid #007A3D!important;padding:.14in .18in .12in!important;
  margin:.3in 0!important;font-size:9.8pt;line-height:1.42;text-align:left}
.fam .fk{font:500 8.4pt/1 SERIF;font-variant:small-caps;text-transform:lowercase;letter-spacing:.2em;color:#007A3D;margin:0 0 .05in}
.fam h4{font:500 14pt/1.15 SERIF;color:#004A26;margin:0 0 .1in}
.fam p{text-indent:0!important;margin:0 0 .07in}
.fam ul{margin:0;padding:0;list-style:none}
.fam li{margin:0 0 .07in;padding-left:.16in;text-indent:-.16in}
.fam li::before{content:"·";color:#9A6324;font-weight:700;display:inline-block;width:.16in;text-indent:0}
.fam figure{margin:.12in 0 0!important}
.fam figure .figwrap svg{max-height:4.4in!important;width:auto!important;max-width:100%!important;margin:0 auto!important;display:block}
.fam figure figcaption{font-size:8pt!important}
.fam.long{break-inside:auto}
.fam.withfig{break-before:page}

/* the close of each chapter */
.wwsdk{margin-top:.34in!important}
.endnote{font-size:9pt;color:#5C574D;font-style:italic;text-align:left}
""".replace('SERIF', SERIF)

# The Saah panel: sentences of the full book, quoted as they stand there (the build
# checks that each one is in the book, word for word).
SAAH = [
    '“The Al-Saah family were builders and among the first forced into labor.”',
    'When the work was done, the Saah builders escaped.',
    '“Construction was the domain of the Saah clan.”',
    'The first to go abroad was Hanna Ibrahim Saah, in 1858, to Constantinople.',
    'In 1885 Ibrāhīm al-Saah brought petrol lanterns from Jerusalem to light his house, and the village came to look; Cadora had the story from Sheikh Ḥannā al-Zaʿrūr.',
    'In 1940 Yūsuf Jiryis al-Saah opened a large furniture factory in Washington, D.C., making tables, chairs and cupboards.',
    'She became “the Qaddoura mother,” her children “the children of Qaddoura,” and the family was known as the Qaddūras instead of Saah.',
]


def strip_story(s):
    """Remove the apparatus from a stretch of story: note numbers, evidence labels,
    tables, correction boxes, Drive notes and the "where our line stands" box."""
    s = re.sub(r'<sup class="cn">.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<span class="(?:g|w2[^"]*|badge[^"]*)"[^>]*>.*?</span>', '', s, flags=re.S)
    for cls in ('fix', 'caution', 'linkat', 'ntwrap', 'drivenote', 'scholars', 'secnote', 'sect'):
        while True:
            m = re.search(r'<div class="%s[ "]' % cls, s)
            if not m:
                break
            s = s[:m.start()] + s[bp.block_end(s, m.start()):]
    s = re.sub(r'<p class="drivenote">.*?</p>', '', s, flags=re.S)
    return s


def pull_photos(seg, keep_srcpages=False):
    """Every photograph in seg, in order, and seg without them."""
    photos = []

    def take(m):
        if 'srcpage' in m.group(1) and not keep_srcpages:
            return ''
        photos.append(m.group(0))
        return ''
    rest = re.sub(r'<figure class="(photo[^"]*)"[^>]*>.*?</figure>', take, seg, flags=re.S)
    return photos, rest


KEEP_FIGS = ('Rāshid’s five sons', 'Ramallah people in the United States')


def drop_figures(seg, kinds, keep=()):
    """Drop drawn figures of the given kinds (Table, Diagram ...), keeping the rest."""
    out, pos = [], 0
    for m in re.finditer(r'<figure(?: class="wide")?>', seg):
        if m.start() < pos:
            continue
        e = seg.find('</figure>', m.end()) + len('</figure>')
        fig = seg[m.start():e]
        k = re.search(r'<div class="fignum">[^<]*·\s*([A-Za-z ]+)</div>', fig)
        if k and k.group(1).strip() in kinds and not any(x in fig for x in keep):
            out.append(seg[pos:m.start()])
            pos = e
    out.append(seg[pos:])
    return ''.join(out)


def saah_panel(h):
    t = bp.text(re.sub(r'<sup class="cn">.*?</sup>', '', h, flags=re.S))
    missing = [x for x in SAAH if x not in t]
    assert not missing, 'Saah panel sentences not in the book: %r' % missing
    church = ('At the inauguration of [the church in] 1852 … “the builders of the church were from the Al-Saah family.”'
              if '“the builders of the church were from the Al-Saah family”' in t else None)
    items = SAAH[:3] + ([church] if church else []) + SAAH[3:]
    return ('<aside class="fam" id="fam-saah"><div class="fk">The family</div><h4>The Saah</h4>'
            '<ul>%s</ul></aside>' % ''.join('<li>%s</li>' % x for x in items))


def wrap_panel(seg, start_pat, title, lead, end_pat=None, keep=''):
    """Turn the passage that begins at start_pat into a family panel."""
    m = re.search(start_pat, seg, flags=re.S)
    if not m:
        print('   family panel not found:', title)
        return seg
    if end_pat:
        e = re.search(end_pat, seg[m.start():], flags=re.S)
        end = m.start() + e.end()
    else:
        end = seg.find('</figure>', m.start()) + len('</figure>')
    body = seg[m.start():end]
    keep = (keep + ' withfig') if '<figure' in body else keep
    panel = ('<aside class="fam %s"><div class="fk">The family</div><h4>%s</h4>%s%s</aside>'
             % (keep, title, '<p>%s</p>' % lead if lead else '', body))
    return seg[:m.start()] + panel + seg[end:]


def chapter_timeline(story):
    rows = []
    for m in re.finditer(r'<div class="entry[^"]*"><div class="ebody">(?:<div class="ewhen">(.*?)</div>)?<h3>(.*?)</h3>', story, flags=re.S):
        d = re.search(r'<span class="d">(.*?)</span>', m.group(1) or '')
        rows.append('<li><span class="cd">%s</span><span class="ct">%s</span></li>' % (bp.text(d.group(1)) if d else '', bp.text(m.group(2))))
    if len(rows) < 2:
        return ''
    return '<div class="chtl"><div class="chh">In this chapter</div><ol>%s</ol></div>' % ''.join(rows)


def essay(photos, cid, title, num):
    if not photos:
        return ''
    seen, figs = set(), []
    for f in photos:
        src = re.search(r'<img [^>]*?src="([^"]{0,200})', f).group(1)
        if src in seen:
            continue
        seen.add(src)
        f = re.sub(r'<sup class="cn">.*?</sup>', '', f, flags=re.S)
        f = re.sub(r' data-k="[^"]*"', '', f, count=1)
        figs.append(f)
    odd = len(figs) % 2
    for i in range(len(figs)):
        if odd and i == 0:
            cls = 'wide2'
        else:
            cls = 'lft' if (i - odd) % 2 == 0 else 'rgt'
        figs[i] = figs[i].replace('<figure class="photo', '<figure class="photo %s' % cls, 1)
    rows, i = [], 0
    if odd:
        rows.append(figs[0])
        i = 1
    while i < len(figs):
        rows.append(''.join(figs[i:i + 2]))
        i += 2
    figs = ['<div class="prow">%s</div>' % r for r in rows]
    return ('<section class="essay" id="%s-essay"><div class="eh"><div class="ek">%s</div><h3>%s</h3></div>%s</section>'
            % (cid, 'Chapter %s in pictures' % num if num else 'In pictures', title, ''.join(figs)))


def build(h):
    # masthead facts, for the title page
    mh = re.search(r'<header class="masthead"><div class="wrap">(.*?)<div class="front">', h, flags=re.S).group(1)
    h1 = bp.text(re.search(r'<h1>(.*?)</h1>', mh, flags=re.S).group(1))
    subs = re.findall(r'<p class="sub">(.*?)</p>', mh, flags=re.S)
    byline = re.search(r'<p class="byline">(.*?)</p>', mh, flags=re.S).group(1)
    series = re.search(r'<span class="l">(.*?)</span>', mh, flags=re.S).group(1)
    updated = re.search(r'<p class="updated">(.*?)</p>', mh, flags=re.S).group(1)
    fm = re.search(r'<figure class="frontis"><img src="([^"]+)"', h)
    head = h[:h.find('<body')]
    dedication = re.search(r'<p class="ded">.*?</p>', h, flags=re.S).group(0)

    starts = [m.start() for m in re.finditer(r'<div class="erahead" id="', h)]
    end_all = h.find('<h2 id="appA"')
    chapters, toc, glance = [], [], []
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else end_all
        ch = h[s:e]
        cid = re.search(r'id="([^"]+)"', ch).group(1)
        he = bp.block_end(ch, 0)
        headblk, body = ch[:he], ch[he:]
        ek = re.search(r'<div class="ek">([^<]*)</div>', headblk).group(1)
        h2 = re.search(r'<h2>(.*?)</h2>', headblk, flags=re.S).group(1)
        dm = re.search(r'<span class="edates">(.*?)</span>', h2)
        title = bp.text(re.sub(r'<span class="edates">.*?</span>', '', h2))
        es = re.search(r'<div class="es">(.*?)</div>', headblk, flags=re.S)
        num = cid[2:] if ek.upper().startswith('CHAPTER') else ''
        dates = bp.text(dm.group(1)) if dm else ''
        toc.append((cid, num, title, dates))
        glance.append('<li class="%s"><span class="gd">%s</span><span class="gt"><span class="gn">%s</span>%s</span><span class="ge">%s</span></li>'
                      % ('' if num else 'clos', dates, num, title, bp.text(es.group(1)) if es else ''))

        # the opening page, as in the print book, without the line ladder
        la = headblk.find('<div class="linkat">')
        if la > 0:
            headblk = headblk[:la] + headblk[bp.block_end(headblk, la):]
        headblk = headblk.replace('<div class="eraband">', '<div class="eraband" data-num="%s">' % num, 1)
        headblk = headblk.replace('<h2>', '<h2><span class="rh">%s</span>' % title, 1)

        ev = body.find('<div class="evfold"')
        story, evidence = (body[:ev], body[ev:]) if ev > 0 else (body, '')
        close = ''
        for which in ('evidence', 'story'):
            seg = evidence if which == 'evidence' else story
            w = seg.find('<div class="wwsdk">')
            if w >= 0:
                close = seg[w:bp.block_end(seg, w)]
                if which == 'story':
                    story = story[:w] + story[bp.block_end(story, w):]
                break
        photos_s, story = pull_photos(story)
        photos_e, _ = pull_photos(evidence)
        story = strip_story(story)
        story = drop_figures(story, {'Table', 'Diagram', 'Chart'}, keep=KEEP_FIGS)
        close = strip_story(close)

        # family panels, where their passages stand in the story
        if cid == 'ch8':
            story = wrap_panel(story, r'<figure(?: class="wide")?><div class="figwrap"><svg[^>]*aria-label="Rāshid’s five sons',
                               'The five sons', '')
            story += saah_panel(h)
        if cid == 'ch10':
            fm_ = re.search(r'<figure(?: class="wide")?><div class="figwrap"><svg[^>]*aria-label="Ramallah people in the United States.*?</figure>',
                            evidence, flags=re.S)
            story = wrap_panel(story, r'<p>Leaving has its own family tree', 'The emigrants',
                               '', keep='long', end_pat=r'ever\s+since\.</p>')
            if fm_:
                i = story.find('</aside>', story.find('<h4>The emigrants</h4>')) + len('</aside>')
                story = (story[:i] + '<aside class="fam withfig"><div class="fk">The family</div><h4>The emigrants, counted</h4>%s</aside>'
                         % fm_.group(0) + story[i:])
            else:
                print('   emigration chart not found')
        chapters.append(headblk + chapter_timeline(story) + story + close
                        + essay(photos_s + photos_e, cid, title, num))

    # front matter
    tp = ('<section class="tp"><div class="tps">%s</div><h1>%s</h1><p class="tpsub">%s</p><hr class="tprule">%s'
          '<p class="tpby">%s</p><p class="tped">Family edition &middot; %s</p></section>'
          % (series, h1, bp.text(subs[0]), '<img src="%s" alt="">' % fm.group(1) if fm else '', byline, updated))
    verso = ('<section class="tpv"><p>This family edition is the story of <i>The Roots of Ramallah</i>, '
             'chapter by chapter, in the words of the full edition, with its photographs gathered after each chapter. '
             'The full edition prints, beside every date, the evidence: the sources, the notes, the tables and how '
             'each record is read. Every fact in this book is there, with its source.</p>%s</section>'
             % ''.join(re.findall(r'<p class="(?:credit|meta)">.*?</p>', mh, flags=re.S)))
    li = ['<li><a href="#%s"><span class="tn">%s</span><span class="tt">%s%s</span></a></li>'
          % (cid, num, title, '<span class="td">%s</span>' % d if d else '') for cid, num, title, d in toc]
    contents = ('<section class="ptoc"><h2>Contents</h2><ol><li><a href="#glance"><span class="tn"></span>'
                '<span class="tt">The story at a glance</span></a></li>%s</ol></section>' % ''.join(li))
    ded = '<section class="front"><p class="ded">%s</p></section>' % re.sub(r'</?p[^>]*>', '', dedication)
    glance_s = ('<section class="glance" id="glance"><h2>The story at a glance</h2>'
                '<p class="gs">Twelve chapters, from the first villages on the ridge to the town and its people today.</p>'
                '<ol>%s</ol></section>' % ''.join(glance))
    # no blank versos: a family edition opens chapters on the next page, left or right
    head = (head.replace('.erahead{page:opener;break-before:right;', '.erahead{page:opener;break-before:page;')
                .replace('break-after:right', 'break-after:page')
                .replace('.front{max-width:none!important;margin:0!important;break-before:right}',
                         '.front{max-width:none!important;margin:0!important;break-before:page}'))
    doc = (head.replace('</style>', FAMILY_CSS + '</style>', 1) + '<body>' + tp + verso + contents + ded + glance_s
           + '<main><div class="wrap">' + ''.join(chapters)
           + '<footer class="end"><p>The Roots of Ramallah &middot; Family edition &middot; %s</p></footer>' % updated
           + '</div></main></body></html>')
    return bp.paged(doc), toc


def main():
    src = open(bp.SRC, encoding='utf-8').read()
    h, dropped = bp.prepare(src)
    doc, toc = build(h)
    hp = os.path.join(OUT, 'Roots_of_Ramallah_Family_print.html')
    pp = os.path.join(OUT, 'Roots_of_Ramallah_Family_6x9.pdf')
    open(hp, 'w', encoding='utf-8').write(doc)
    print('%s: %d bytes, %d chapters' % (hp, os.path.getsize(hp), len(toc)))
    if '--html-only' not in sys.argv:
        n, secs = bp.render(hp, pp)
        print('%s: %d pages, %d bytes, %.0f s' % (pp, n, os.path.getsize(pp), secs))


if __name__ == '__main__':
    main()
