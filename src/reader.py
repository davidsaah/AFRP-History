# -*- coding: utf-8 -*-
"""v79: the phone reader.

Runs last, on the finished HTML (after restyle). It does not change a word of
the book; it changes how the book is held on a small screen.

  * Each chapter opens with a photograph already in that chapter, a large
    chapter numeral and the era dates set on their own line.
  * One pull quote per chapter, taken from a quotation already in the chapter's
    story, set as an epigraph under "The story".
  * On screens up to 700px the evidence half of each chapter (the evidence
    entries and "What the scholars say") folds under "Show the evidence". The
    story and "What we still don't know" stay open. Wider screens and print see
    the book as before.
  * Plates fit the screen; a tap opens the plate full size in a pannable,
    pinch-zoomable view. The sideways swipe is retired on phones.
  * A "Next chapter" link closes every chapter. The existing reading-progress
    bar is kept and thinned.

Idempotent: a page that already carries the reader is left alone.

    python src/reader.py out/AFRP_The_One_Line_v5.html
"""
import html as _html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARK = '<!-- reader:v79 -->'

WORDS = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Eleven', 'Twelve']

# One quotation per chapter, each already printed in that chapter's story.
# Attribution only where the book itself names the speaker beside the words.
PULL = {
    'ch1': ('Behold, I alone am cultivating in the city of Shunama …',
            'Biridiya of Megiddo to the king of Egypt, Amarna letter EA 365'),
    'ch2': ('There was for Sabaʾ, in their dwelling-place, a sign: two gardens, '
            'on the right hand and on the left.', 'Qurʾān 34:15'),
    'ch3': ('… went thence unto a country near to the wilderness, into a city called '
            'Ephraim, and there continued with his disciples.', 'John 11:54'),
    'ch4': ('… the dignity of king, a thing which among the Romans had never before '
            'been done.', 'Procopius, on al-Ḥārith ibn Jabala'),
    'ch6': ('One hamlet of ours … near the royal road by which one goes to Ramelie.',
            'The charter of 1186'),
    'ch7': ('The little tribe of Ḥaddādīn is made up of a number of families, '
            'exclusively Christian.', 'Dissard, Revue Biblique, 1905'),
    'ch8': ('Ramallah became a prosperous town and attracted other families. '
            'The influx began about 1750.', None),
    'ch9': ('Eighty percent of the land is now uncultivated. The generations that '
            'worked the land have passed away and, alas, the land too is passing away.',
            'Shāhīn, 1982'),
    'ch10': ('Till 1902 there had been no government rule in the villages and small '
             'towns of Palestine.', 'Shāhīn'),
    'ch11': ('The future looked grim and the morale of the people was at its lowest ebb.',
             'Shāhīn, of 1951–52'),
    'ch12': ('The five lions represented the five Ramallah families who viewed '
             'themselves as the city’s ‘original’ inhabitants.', None),
}

# The opener photograph of each chapter: a different picture from the chapter's own era.
# First choice first; a Library of Congress photo is used only once it is saved in img/loc/.
OPENER = {
    'ch1': ['05506v.jpg', '04114v.jpg'],
    'ch2': ['22915v.jpg'],
    'ch3': ['22165v.jpg', '01719v.jpg'],
    'ch4': ['05329v.jpg'],
    'ch5': ['03718v.jpg'],
    'ch6': ['vesconte_c1320.jpg', 'bireh_church_1881.jpg'],
    'ch7': ['06951v.jpg', 'p012_1.jpg'],
    'ch8': ['p038_1.jpg'],
    'ch9': ['p238_1.jpg', 'bireh_khan_1881.jpg'],
    'ch10': ['p172_1.jpg', '01047v.jpg'],
    'ch11': ['p228_1.jpg'],
    'ch12': ['p162_2.jpg'],
}

# Matson stereographs: two near-identical frames side by side. Openers show the left frame.
STEREO = {'01047v.jpg', '01719v.jpg', '04114v.jpg', '05506v.jpg'}

LOC = re.compile(r'https://tile\.loc\.gov/storage-services/service/pnp/[a-z]+/\d+/(\w+\.jpg)')


def localize_loc(h):
    """Point Library of Congress photos at img/loc/<name> once a copy is saved there."""
    def sub(m):
        name = m.group(1)
        return '../img/loc/' + name if os.path.exists(os.path.join(ROOT, 'img', 'loc', name)) else m.group(0)
    return LOC.sub(sub, h)


def _photo(h, names):
    """The first photograph in the book whose file name is in names, if it can be shown."""
    for name in names:
        m = re.search(r'<figure class="photo[^"]*"[^>]*><img src="([^"]*/%s)" alt="([^"]*)"' % re.escape(name), h)
        if m and (m.group(1).startswith('../img/')):
            return m.group(1), m.group(2)
    return None


CSS = r'''
/* ═══════════ v79: the reader ═══════════ */
@font-face{font-family:"EB Garamond";font-style:normal;font-weight:400 800;font-display:swap;
  src:url(../assets/fonts/eb-garamond/EBGaramond-normal-latin-ext.woff2) format("woff2");
  unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"EB Garamond";font-style:normal;font-weight:400 800;font-display:swap;
  src:url(../assets/fonts/eb-garamond/EBGaramond-normal-latin.woff2) format("woff2");
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"EB Garamond";font-style:italic;font-weight:400 800;font-display:swap;
  src:url(../assets/fonts/eb-garamond/EBGaramond-italic-latin-ext.woff2) format("woff2");
  unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"EB Garamond";font-style:italic;font-weight:400 800;font-display:swap;
  src:url(../assets/fonts/eb-garamond/EBGaramond-italic-latin.woff2) format("woff2");
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
body,.eraband h2,.ebody h3,blockquote,figure,figcaption{font-family:"EB Garamond","Times New Roman",Times,serif}
.pbar{height:2px}
.pullq{display:none}
.opener{position:relative;margin:0;overflow:hidden;background:#1A1915;aspect-ratio:16/7;max-height:380px;border-radius:12px 12px 0 0}
.opener img{display:block;width:100%;height:100%;object-fit:cover}
.opener.stereo img{width:200%;max-width:none;object-position:left center}
.opener .opnum{position:absolute;left:24px;bottom:2px;font:500 6rem/1 "EB Garamond",Georgia,serif;
  color:#fff;text-shadow:0 2px 18px rgba(0,0,0,.5)}
.opener .opcap{position:absolute;right:12px;bottom:8px;max-width:55%;text-align:right;
  font:italic .74rem/1.25 "EB Garamond",Georgia,serif;color:rgba(255,255,255,.9);text-shadow:0 1px 4px rgba(0,0,0,.7)}
.opener+.eraband{border-top-left-radius:0;border-top-right-radius:0}
.eraband h2 .edates{display:block;font-size:.6em;font-weight:400;letter-spacing:.06em;margin-top:6px;opacity:.9}
.epigraph{margin:26px 0 30px 122px;padding:0;border:0;background:none;max-width:30em}
.epigraph p{margin:0;font:italic 400 1.42rem/1.38 "EB Garamond",Georgia,serif;color:#5C4A2E}
.epigraph cite{display:block;margin-top:8px;font-style:normal;font-variant:small-caps;letter-spacing:.06em;color:#9A6324}
.dropcap::first-letter{float:left;font:500 3.6em/.82 "EB Garamond",Georgia,serif;color:#004A26;margin:.06em .08em 0 0}
.evtoggle{display:none}
.nextch{display:block;margin:34px 0 56px;padding:18px 0 0;border-top:1px solid #9A6324;color:#004A26;text-decoration:none;text-align:right}
.nextch .nk{display:block;font-variant:small-caps;letter-spacing:.12em;color:#9A6324;font-size:.95rem}
.nextch .nt{display:block;font-size:1.3rem;margin-top:2px}
.nextch .nt::after{content:" →"}
.lb{position:fixed;inset:0;z-index:100;background:rgba(26,25,21,.92);display:none}
.lb.on{display:block}
.lb .lbin{position:absolute;inset:44px 0 0 0;overflow:auto;-webkit-overflow-scrolling:touch;touch-action:pan-x pan-y pinch-zoom}
.lb .lbin>*{display:block;background:#fff;margin:0 auto;width:1100px;max-width:none;height:auto}
.lb .lbx{position:absolute;top:6px;right:10px;background:#fff;color:#1A1915;border:0;border-radius:18px;
  font:600 .9rem/1 "EB Garamond",Georgia,serif;letter-spacing:.08em;padding:10px 14px}
.lb .lbt{position:absolute;top:14px;left:14px;right:100px;color:#fff;font:600 1rem/1.2 "EB Garamond",Georgia,serif;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

/* the phone: a calm page, more white, fewer boxes */
@media (max-width:760px){
  body{font-size:19px;line-height:1.6;background:#FFFDF8}
  .wrap{padding:0 22px}
  .chron::before,.entry::before,.sect::before{display:none!important}
  .entry{display:block!important;margin:0 0 38px!important}
  .ewhen{display:flex!important;flex-wrap:wrap;align-items:baseline;gap:4px 12px;text-align:left!important;padding:0!important;margin:0 0 4px}
  .ewhen .d{display:inline!important;font-size:1rem!important;font-weight:600!important;color:#9A6324!important}
  .g,.ewhen .g,.w2,.badge{background:none!important;color:#9A6324!important;padding:0!important;margin:0!important;border:0!important;
    border-radius:0!important;font:500 .86rem/1.3 "EB Garamond",Georgia,serif!important;font-variant:small-caps!important;
    text-transform:lowercase!important;letter-spacing:.07em!important}
  .ebody h3{font-size:1.32rem;font-weight:600;color:#1A1A1A}
  .sect{padding:0!important;margin:52px 0 22px!important}
  .sl{font:500 .9rem/1 "EB Garamond",Georgia,serif;font-variant:small-caps;text-transform:lowercase;letter-spacing:.14em;color:#9A6324}
  .ss{border-bottom:1px solid #E8E2D5}
  .erahead{margin-top:56px}
  .opener{aspect-ratio:4/3;max-height:none;border-radius:0;margin:0 -22px}
  .opener .opnum{font-size:5.2rem;left:18px}
  .erahead .eraband,.eraband{background:none!important;color:#1A1A1A!important;border-radius:0!important;padding:24px 0 0!important;margin:0!important;box-shadow:none!important}
  .eraband .ek{color:#9A6324!important;font:500 .9rem/1 "EB Garamond",Georgia,serif;font-variant:small-caps;text-transform:lowercase;letter-spacing:.16em}
  .eraband h2{color:#004A26!important;font-size:2rem!important;font-weight:600;line-height:1.15}
  .eraband h2 .edates{color:#5C574D;opacity:1}
  .eraband .es{color:#46423B!important;font-size:1.06rem}
  .eraband .es::before{width:56px!important;border-top:1px solid #007A3D!important;margin:14px 0 12px!important}
  .epigraph{margin:26px 0 8px!important}
  .epigraph p{font-size:1.28rem}
  .linkat{background:none!important;border:0!important;border-top:1px solid #E4DCCB!important;border-bottom:1px solid #E4DCCB!important;
    border-radius:0!important;padding:16px 0!important;margin:26px 0 0!important}
  .scholars,.wwsdk{background:none!important;border:0!important;border-top:1px solid #9A6324!important;border-radius:0!important;
    padding:18px 0 4px!important;margin:40px 0 30px!important}
  .scholars h4,.wwsdk h4,.howto h4{font:500 .95rem/1.2 "EB Garamond",Georgia,serif!important;font-variant:small-caps;text-transform:lowercase;letter-spacing:.12em}
  blockquote{background:none!important;border:0!important;border-left:1px solid #9A6324!important;border-radius:0!important;
    padding:2px 0 2px 18px!important;margin:24px 0!important;font-style:italic;font-size:1.06rem}
  blockquote .cite{font-style:normal}
  .fix{background:none!important;border:0!important;border-top:1px solid #A85210!important;border-bottom:1px solid #E8D9BE!important;
    border-radius:0!important;padding:14px 0!important}
  .ntwrap{border:0!important;border-top:1px solid #DCD6C9!important;border-radius:0!important;background:none!important}
  .howto,.contents,.note .box{background:none!important;border:0!important;border-radius:0!important}
  .contents{border-top:1px solid #DCD6C9!important;padding:16px 0!important}
  figure{border-top:1px solid #DCD6C9!important;border-bottom:0!important;background:none!important;margin:34px 0!important}
  .photo{padding:0!important}
  .figwrap{overflow:visible;padding:6px 0 10px;cursor:zoom-in}
  .figwrap svg{width:100%;min-width:0;max-width:100%}
  .fignum::after{content:"tap to enlarge";font-style:italic;letter-spacing:0;text-transform:none}
  .linkat .lkladder svg{width:100%;min-width:0}
}
@media (max-width:700px){
  .evtoggle{display:flex;align-items:center;justify-content:space-between;width:100%;margin:40px 0 18px;
    padding:14px 0;background:none;border:0;border-top:1px solid #007A3D;border-bottom:1px solid #E4DCCB;border-radius:0;
    font:500 1.12rem/1.3 "EB Garamond",Georgia,serif;color:#004A26;text-align:left;cursor:pointer}
  .evtoggle small{display:block;font-size:.88rem;color:#6B6760;margin-top:2px;font-style:italic}
  .evtoggle::after{content:"+";font-size:1.5rem;line-height:1;color:#007A3D;margin-left:12px}
  .evfold.open>.evtoggle::after{content:"−"}
  .evfold:not(.open)>.evbody{display:none}
}
@media print{
  .evtoggle,.nextch,.lb,.pbar{display:none!important}
  .evfold>.evbody{display:block!important}
}
'''

JS = r'''
(function(){
  var mq=window.matchMedia('(max-width:700px)');
  function openFor(el){
    while(el&&el!==document.body){
      if(el.classList&&el.classList.contains('evfold')&&!el.classList.contains('open')){el.classList.add('open');}
      el=el.parentNode;}
  }
  function goHash(h,ev){
    if(!h||h.length<2)return;
    var t=document.getElementById(decodeURIComponent(h.slice(1)));
    if(!t)return;
    var f=t.closest&&t.closest('.evfold:not(.open)');
    if(f){openFor(t);if(ev)ev.preventDefault();t.scrollIntoView();history.replaceState(null,'',h);}
  }
  document.querySelectorAll('.evtoggle').forEach(function(b){
    b.addEventListener('click',function(){
      var f=b.parentNode;var on=f.classList.toggle('open');
      b.setAttribute('aria-expanded',on?'true':'false');
      b.querySelector('span').firstChild.nodeValue=on?'Hide the evidence':'Show the evidence';
    });
  });
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="#"]');
    if(a&&mq.matches)goHash(a.getAttribute('href'),e);
  });
  window.addEventListener('hashchange',function(){if(mq.matches)goHash(location.hash);});
  if(location.hash&&mq.matches)setTimeout(function(){goHash(location.hash);},50);

  /* tap a plate to see it full size */
  var lb=document.createElement('div');lb.className='lb';
  lb.innerHTML='<div class="lbt"></div><button class="lbx" type="button">Close</button><div class="lbin"></div>';
  document.body.appendChild(lb);
  var inner=lb.querySelector('.lbin');
  function close(){lb.classList.remove('on');inner.innerHTML='';document.documentElement.style.overflow='';}
  lb.querySelector('.lbx').addEventListener('click',close);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
  document.addEventListener('click',function(e){
    if(!window.matchMedia('(max-width:760px)').matches)return;
    var w=e.target.closest&&e.target.closest('.figwrap');
    if(!w||e.target.closest('a'))return;
    var svg=w.querySelector('svg');if(!svg)return;
    var c=svg.cloneNode(true);c.removeAttribute('width');c.style.width='1100px';
    inner.innerHTML='';inner.appendChild(c);
    var fig=w.closest('figure');var t=fig&&fig.querySelector('.figtitle');
    lb.querySelector('.lbt').textContent=t?t.textContent:'';
    lb.classList.add('on');document.documentElement.style.overflow='hidden';
    inner.scrollLeft=(c.scrollWidth-inner.clientWidth)/2;
  });

  /* fold the evidence on a phone, open on a wider screen */
  function sync(){document.querySelectorAll('.evfold').forEach(function(f){
    if(!mq.matches){f.classList.add('open');}
    else if(!f.dataset.touched){f.classList.remove('open');}
  });}
  document.querySelectorAll('.evtoggle').forEach(function(b){b.addEventListener('click',function(){b.parentNode.dataset.touched='1';});});
  if(mq.addEventListener)mq.addEventListener('change',sync);
  sync();
})();
'''


def _depth_ok(fragment):
    """True when every div opened in the fragment is closed in it."""
    opens = len(re.findall(r'<div\b', fragment))
    closes = len(re.findall(r'</div>', fragment))
    return opens == closes


def _chapter_bounds(h):
    starts = [(m.start(), m.group(1)) for m in re.finditer(r'<div class="erahead" id="(ch\d+)"', h)]
    out = []
    for k, (a, cid) in enumerate(starts):
        b = starts[k + 1][0] if k + 1 < len(starts) else None
        out.append((a, b, cid))
    return out


def _titles(h):
    t = {}
    for m in re.finditer(r'<div class="erahead" id="(ch\d+)"><div class="eraband"><div class="ek">([^<]*)</div><h2>(.*?)</h2>', h):
        t[m.group(1)] = (m.group(2), m.group(3))
    return t


def reader(h):
    if MARK in h:
        return h
    h = localize_loc(h)
    titles = _titles(h)
    ids = [c for _, _, c in _chapter_bounds(h)]

    # Work chapter by chapter from the end, so earlier offsets stay valid.
    for a, b, cid in reversed(_chapter_bounds(h)):
        end = b if b is not None else _chapter_end(h, a)
        ch = h[a:end]
        num = int(cid[2:])

        # 1. fold the evidence half (evidence sect up to "What we still don't know")
        ev = ch.find('<div class="sect"><span class="sl">The evidence')
        ww = ch.find('<div class="wwsdk">')
        if ev > 0:
            stop = ww if ww > ev else len(ch)
            body = ch[ev:stop]
            if _depth_ok(body):
                n_entries = body.count('class="entry')
                label = ('<button class="evtoggle" type="button" aria-expanded="false"><span>Show the evidence'
                         '<small>%d %s for this chapter</small></span></button>' % (n_entries, 'source and reading' if n_entries == 1 else 'sources and readings'))
                ch = ch[:ev] + '<div class="evfold">' + label + '<div class="evbody">' + body + '</div></div>' + ch[stop:]

        # 2. the opener: a picture from the chapter's own era, a big numeral, the dates on
        #    their own line, and an epigraph from a source quoted in the chapter
        m = re.match(r'(<div class="erahead" id="%s">)(<div class="eraband">.*?</div></div>)' % cid, ch, flags=re.S)
        if m:
            opener = ''
            ph = _photo(h, OPENER.get(cid, []))
            if ph and 1 <= num <= 12:
                cap = re.split(r'(?<=[.!?])\s', ph[1], maxsplit=1)[0]
                opener = ('<div class="opener%s"><img src="%s" alt="" decoding="async" '
                          'onerror="this.parentNode.style.display=\'none\'"><span class="opnum">%d</span>'
                          '<span class="opcap">%s</span></div>' % (' stereo' if ph[0].split('/')[-1] in STEREO else '',
                                                              ph[0], num, cap))
            epi = ''
            if cid in PULL:
                q, by = PULL[cid]
                epi = '<blockquote class="epigraph"><p>%s</p>%s</blockquote>' % (
                    _html.escape(q, quote=False),
                    ('<cite>%s</cite>' % _html.escape(by, quote=False)) if by else '')
            ch = m.group(1) + opener + m.group(2) + epi + ch[m.end():]
        ch = re.sub(r'(<div class="eraband"><div class="ek">[^<]*</div><h2>)(.*?) &middot; (.*?)(</h2>)',
                    r'\1\2<span class="edates">\3</span>\4', ch, count=1)

        # 3. a drop cap on the first paragraph of the story
        st = ch.find('<div class="sect"><span class="sl">The story')
        if st > 0:
            pm = re.compile(r'<div class="ebody">(?:<h3>.*?</h3>)?\s*<(div class="note"|p)>').search(ch, st)
            fold = ch.find('<div class="evfold">')
            if pm and (fold < 0 or pm.start() < fold):
                tag = pm.group(1)
                new = '<div class="note dropcap">' if tag.startswith('div') else '<p class="dropcap">'
                ch = ch[:pm.end() - len(tag) - 2] + new + ch[pm.end():]

        # 4. next chapter link at the end of this chapter
        k = ids.index(cid)
        if k + 1 < len(ids):
            nxt = ids[k + 1]
            ek, t2 = titles.get(nxt, ('', ''))
            t2 = t2.split(' &middot; ')[0]
            ch = ch + ('<a class="nextch" href="#%s"><span class="nk">Next · %s</span>'
                       '<span class="nt">%s</span></a>' % (nxt, ek.title(), t2))
        h = h[:a] + ch + h[end:]

    h = h.replace('</style>', CSS + '</style>', 1)
    h = h.replace('</body>', '<script>' + JS + '</script>' + MARK + '</body>', 1)
    return h


def _chapter_end(h, a):
    """The last chapter runs to the end of its 'what we still don't know' box."""
    w = h.find('<div class="wwsdk">', a)
    if w < 0:
        return a
    # close the wwsdk div: count nested divs from w
    depth = 0
    for m in re.finditer(r'<div\b|</div>', h[w:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            return w + m.end()
    return a


if __name__ == '__main__':
    p = sys.argv[1]
    s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8', newline='\n').write(reader(s))
