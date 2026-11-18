# -*- coding: utf-8 -*-
"""v108: the desktop reading layout (David, 18 Nov 2026: "the desktop view is hard to read, the mobile version is great").

Only for screens 1000 px and wider; the phone layout and the print editions are untouched.
- One centred reading column of about 66 letters, at 20 px, in darker ink.
- The dates and grades in a slim rail on the left; figures a little wider than the text.
- From 1240 px: footnotes set beside their paragraph in the right margin (sidenotes), as in a printed book.
- From 1500 px: the chapter list stays in view at the left edge.
Runs last, from src/restyle.py, so its rules come after every other style on the page.
"""

CSS = r"""
<style id="desktop-v108">
@media screen and (min-width:1000px){
  html body{font-size:18px;background:#FFFDF8}
  body .wrap{max-width:760px}
  body .ebody .note,body .ebody p,body .ebody li{font-size:1.15rem;line-height:1.62;color:#24211C;max-width:none}
  body .ebody .note b{color:#111}
  body .ebody h3{font-size:1.55rem;line-height:1.25}
  body figcaption{font-size:1rem!important;line-height:1.5!important;color:#3A3730!important}
  body figcaption .src{font-size:.9rem!important}
  body .ctxbox,body .record,body .sfyouth{font-size:1rem!important;line-height:1.55!important}
  body .wwsdk p{font-size:1.06rem}
  body sup.cn{font-size:.62em}
  body .figwrap svg{max-width:100%}
  body .ewhen .d{font-size:1.05rem!important}
}
@media screen and (min-width:1240px){
  body .wrap{max-width:1010px;padding-right:340px!important;box-sizing:border-box}
  body .wrap .wrap{max-width:none;padding-right:0!important;margin-right:0!important}
  body .masthead .wrap,body header .wrap{padding-right:0!important;max-width:760px}
  body .ebody figure{margin-right:-240px!important;clear:right}
  body .sn{float:right;clear:right;width:280px;margin:4px -340px 12px 22px;padding-left:12px;border-left:2px solid #E2D6BE;
           font-size:.78rem;line-height:1.45;color:#5A554C;font-style:normal;font-weight:400;text-indent:0;max-width:none!important}
  body .sn b.snn{color:#007A3D;font-weight:700;margin-right:4px}
}
@media screen and (min-width:1600px){
  body .dtoc{display:block}
}
.dtoc{display:none;position:fixed;left:22px;top:90px;width:210px;max-height:calc(100vh - 120px);overflow:auto;
      font:15px/1.35 "EB Garamond","Times New Roman",serif;z-index:20}
.dtoc .dk{font-variant:small-caps;letter-spacing:.14em;color:#9A6324;margin:0 0 8px}
.dtoc a{display:block;color:#5A554C;text-decoration:none;padding:4px 0 4px 10px;border-left:2px solid #E2D6BE}
.dtoc a small{display:block;font-size:12px;color:#9A6324;letter-spacing:.03em}
.dtoc a:hover{color:#004A26}
.dtoc a.on{color:#004A26;border-left-color:#007A3D;font-weight:600}
@media print{.dtoc,.sn{display:none!important}}
</style>
"""

JS = r"""
<script id="desktop-v108-js">
(function(){
  if(!window.matchMedia) return;
  var wide=window.matchMedia('screen and (min-width:1240px)');
  var done=false;
  function sidenotes(){
    if(done||!wide.matches) return; done=true;
    document.querySelectorAll('.ebody sup.cn a').forEach(function(a){
      var id=(a.getAttribute('href')||'').slice(1), li=document.getElementById(id);
      if(!li) return;
      var host=a.closest('p,.note,li,figcaption,td');
      if(!host||host.closest('table,figure,.ctxbox,.record,.linkat')) return;
      var s=document.createElement('span'); s.className='sn';
      var t=li.cloneNode(true); t.querySelectorAll('.backto').forEach(function(x){x.remove()});
      s.innerHTML='<b class="snn">'+a.textContent+'</b>'+t.innerHTML;
      // keep a paragraph's notes in reading order: each goes after the last one placed
      var last=host._snLast; host.insertBefore(s,last?last.nextSibling:host.firstChild); host._snLast=s;
    });
  }
  sidenotes(); wide.addEventListener&&wide.addEventListener('change',sidenotes);
  // the chapter list at the left edge, from the book's own contents
  var toc=document.querySelectorAll('#toc li a'); if(!toc.length) return;
  var nav=document.createElement('nav'); nav.className='dtoc'; nav.setAttribute('aria-label','Chapters');
  nav.innerHTML='<div class="dk">chapters</div>';
  var links=[];
  toc.forEach(function(a){var b=document.createElement('a'); b.href=a.getAttribute('href');
    var c=a.querySelector('.cnum'), t=a.querySelector('.ctit');
    var g=t&&t.querySelector('.cgen'), tt=t?t.cloneNode(true):null; if(tt){var gg=tt.querySelector('.cgen'); if(gg) gg.remove();}
    b.textContent=(c?c.textContent.replace(/^Chapter /,'')+' · ':'')+(tt?tt.textContent:a.textContent);
    if(g){var sm=document.createElement('small'); sm.textContent=g.textContent; b.appendChild(sm);} nav.appendChild(b); links.push(b);});
  document.body.appendChild(nav);
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
      links.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+e.target.id)});}})},{rootMargin:'0px 0px -70% 0px'});
    links.forEach(function(l){var el=document.querySelector(l.getAttribute('href')); if(el) io.observe(el);});
  }
})();
</script>
"""


CALM = '/* the phone: a calm page, more white, fewer boxes */'
SKIP = ('body{font-size', '.wrap{padding', '.opener{', '.opener .opnum', '.fignum::after', '.figwrap{', '.figwrap svg', '.linkat .lkladder svg')


def _calm(html):
    """The phone's calm page (src/build_v5.py), reused for the desktop: no rail, no badges, no boxes."""
    i = html.find(CALM)
    if i < 0:
        return ''
    a = html.index('{', i) + 1
    b = html.index('\n}\n', a)
    lines, keep, skip = html[a:b].split('\n'), [], False
    for ln in lines:
        st = ln.strip()
        if skip:
            skip = not st.endswith('}')
            continue
        if any(st.startswith(x) for x in SKIP):
            skip = not st.endswith('}')
            continue
        keep.append(ln)
    return '<style id="desktop-calm-v108">@media screen and (min-width:1000px){' + '\n'.join(keep) + '\n}</style>'


def apply(html):
    if 'id="desktop-v108"' in html:
        return html
    k = html.rfind('</body>')
    return html[:k] + _calm(html) + CSS + JS + html[k:]
