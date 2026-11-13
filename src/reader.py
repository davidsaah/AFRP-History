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
import re
import sys

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

CSS = r'''
/* ═══════════ v79: the phone reader ═══════════ */
.pbar{height:2px}
.opener{position:relative;margin:0;border-radius:12px 12px 0 0;overflow:hidden;background:#1A1915;
  aspect-ratio:16/7;max-height:340px}
.opener img{display:block;width:100%;height:100%;object-fit:cover;opacity:.88;filter:grayscale(.15) contrast(1.02)}
.opener .opnum{position:absolute;left:24px;bottom:6px;font:700 5.6rem/1 "Times New Roman",Times,serif;
  color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.45);letter-spacing:-.02em}
.opener .opcred{position:absolute;right:10px;bottom:8px;font:italic .7rem/1.2 "Times New Roman",Times,serif;
  color:rgba(255,255,255,.85);max-width:60%;text-align:right;text-shadow:0 1px 4px rgba(0,0,0,.6)}
.opener+.eraband{border-top-left-radius:0;border-top-right-radius:0}
.eraband h2 .edates{display:block;font-size:.62em;font-weight:400;letter-spacing:.06em;margin-top:6px;opacity:.9}
.pullq{position:relative;z-index:1;margin:6px 0 30px;padding:4px 0 4px 122px}
.pullq p{margin:0;font:italic 400 1.62rem/1.32 "Times New Roman",Times,serif;color:#9A6324;max-width:30em}
.pullq p::before{content:"“";display:block;font:700 3.2rem/0.6 "Times New Roman",Times,serif;color:#9A6324;opacity:.5;margin-bottom:6px}
.pullq .pqby{display:block;margin-top:10px;font-size:.82rem;letter-spacing:.14em;text-transform:uppercase;color:#6B6760}
.evtoggle{display:none}
.nextch{display:flex;flex-direction:column;align-items:flex-end;gap:4px;margin:26px 0 48px;padding:16px 20px;
  border-top:2px solid #007A3D;border-bottom:1px solid #D9D4C8;color:#004A26;text-decoration:none}
.nextch .nk{font:700 .72rem/1 "Times New Roman",Times,serif;letter-spacing:.22em;text-transform:uppercase;color:#9A6324}
.nextch .nt{font:700 1.2rem/1.3 "Times New Roman",Times,serif}
.nextch .nt::after{content:" →"}
.figzoom{display:none}
.lb{position:fixed;inset:0;z-index:100;background:rgba(26,25,21,.92);display:none}
.lb.on{display:block}
.lb .lbin{position:absolute;inset:44px 0 0 0;overflow:auto;-webkit-overflow-scrolling:touch;touch-action:pan-x pan-y pinch-zoom}
.lb .lbin>*{display:block;background:#fff;margin:0 auto;width:1100px;max-width:none;height:auto}
.lb .lbin img{width:auto;max-width:none}
.lb .lbx{position:absolute;top:6px;right:10px;background:#fff;color:#1A1915;border:0;border-radius:18px;
  font:700 .8rem/1 "Times New Roman",Times,serif;letter-spacing:.1em;text-transform:uppercase;padding:10px 14px}
.lb .lbt{position:absolute;top:14px;left:14px;right:100px;color:#fff;font:700 .9rem/1.2 "Times New Roman",Times,serif;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:760px){
  .opener{aspect-ratio:4/3;border-radius:10px 10px 0 0}
  .opener .opnum{font-size:4.4rem;left:16px}
  .pullq{padding-left:18px;margin:4px 0 24px}
  .pullq p{font-size:1.38rem}
  /* plates fit the screen; a tap opens them full size */
  .figwrap{overflow:visible;padding:6px 0 10px}
  .figwrap svg{width:100%;min-width:0;max-width:100%}
  .fignum::after{content:"tap to enlarge"}
  .figwrap{cursor:zoom-in}
  .linkat .lkladder svg{width:100%;min-width:0}
}
@media (max-width:700px){
  .evtoggle{display:flex;align-items:center;justify-content:space-between;width:100%;margin:24px 0 18px;
    padding:14px 18px;background:#F7F4EE;border:1px solid #D9D4C8;border-left:4px solid #007A3D;border-radius:8px;
    font:700 1rem/1.3 "Times New Roman",Times,serif;color:#004A26;text-align:left;cursor:pointer}
  .evtoggle small{display:block;font-weight:400;font-size:.82rem;color:#6B6760;margin-top:3px}
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

        # 2. pull quote as the chapter's epigraph, under "The story"
        if cid in PULL:
            q, by = PULL[cid]
            st = re.search(r'<div class="sect"><span class="sl">The story</span>.*?</div>', ch)
            if st:
                aside = '<aside class="pullq"><p>%s</p>%s</aside>' % (
                    _html.escape(q, quote=False),
                    ('<span class="pqby">%s</span>' % _html.escape(by, quote=False)) if by else '')
                ch = ch[:st.end()] + aside + ch[st.end():]

        # 3. the opener: a photograph from this chapter, a big numeral, the dates on their own line
        story_end = ch.find('<div class="evfold">')
        story = ch[:story_end if story_end > 0 else len(ch)]
        # prefer a photo held in the repo (../img/), so the opener never shows an empty box
        ph = (re.search(r'<figure class="photo"><img src="(\.\./img/[^"]+)" alt="([^"]*)"', story)
              or re.search(r'<figure class="photo"><img src="(\.\./img/[^"]+)" alt="([^"]*)"', ch)
              or re.search(r'<figure class="photo"><img src="([^"]+)" alt="([^"]*)"', story))
        m = re.match(r'(<div class="erahead" id="%s">)(<div class="eraband">)' % cid, ch)
        if m:
            opener = ''
            if ph and 1 <= num <= 12:
                opener = ('<div class="opener"><img src="%s" alt="" loading="lazy" decoding="async" onerror="this.parentNode.style.display=\'none\'">'
                          '<span class="opnum">%d</span></div>' % (ph.group(1), num))
            ch = m.group(1) + opener + m.group(2) + ch[m.end():]
        ch = re.sub(r'(<div class="eraband"><div class="ek">[^<]*</div><h2>)(.*?) &middot; (.*?)(</h2>)',
                    r'\1\2<span class="edates">\3</span>\4', ch, count=1)

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
