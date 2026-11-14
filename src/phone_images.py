"""v86: pictures that can be read on a phone.

Runs after reader.py, on the finished page.

1. Every picture in a figure opens full size on a tap, with zoom buttons and
   pinch (the v79 viewer only took the drawn plates).
2. On a phone the pictures run the full width of the screen.
3. Captions upright, a size larger, with a darker source line. A long caption
   keeps its first sentence; the rest folds under "more" on a phone.
4. The sixteen document scans show a close-up of the lines that matter, with
   "What it says" typed out under them; the four old maps show the part around
   Ramallah. The whole page or map is one tap away.

strip() takes the close-ups, the typed panels and the "more" buttons back out,
so the printed and family editions keep the full plates as before.
"""
import html as _html
import re

MARK = '<!-- phone_images:v86 -->'
PZ_A, PZ_B = '<!--pz-->', '<!--/pz-->'


def ar(s):
    return '<span class="ar" dir="rtl" lang="ar">%s</span>' % s


# figure -> (close-up label, [(kind, text)]) ; kind: 'o' original, 'e' English, 'n' note
# Transcriptions are what the scan clearly shows; [?] marks an uncertain reading.
# English is the book's own translation, from the caption.
SCANS = {
    '6.3': ('Close-up of the boxed words', [
        ('o', '<i lang="la">… prope viam regalem, qua vaditur Ramelie …</i>'),
        ('e', '“… by which one goes to Ramallah …”'),
    ]),
    '7.4': ('Close-up of the first line, in two halves', [
        ('o', ar('ويعرف اهالي رام الله ان راشداً الحداد واخاه صبره هما اول من سكن هذه المدينة')),
        ('e', '“The people of Ramallah know that Rāshid al-Ḥaddād and his brother Ṣabra were the first to live in this town.”'),
    ]),
    '7.8': ('Close-up of the two boxed entries', [
        ('o', '<i>Karye-i Ramallah tābiʿ-i m. tamāmen. Hāsıl maʿa rüsūm 2905</i>'),
        ('e', 'The whole village, endowed to the shrine of Abraham at Hebron, yielding 2,905 akçe with its dues.'),
        ('o', '<i>Deyr-i Nasārā der-karye-i Ramallah tābiʿ-i m. 71 neferen, fī 80, 5680</i>'),
        ('e', 'The Christians of Ramallah, seventy-one persons at 80 akçe each, 5,680 akçe.'),
    ]),
    '7.11': ('Close-up of the head of the register and the note below it', [
        ('o', '“Register 289: The 36 families temporarily living in Beit Jala during the census of 1553-54 (961 Hijri). Columns 79 and 80 of Register 289.”'),
        ('o', '“The 1553 census of Beit Jala includes the above 36 families. Nine years later, in the 1562 census, these families were no longer living in Beit Jala, but had moved to Ramallah.”'),
        ('n', 'Shaheen’s printed notes on the page. The Ottoman entries themselves are not typed out here.'),
    ]),
    '8.5': ('Close-up of the first four lines', [
        ('o', '<i lang="de">Rechts liessen wir das Dorf Taréndy liegen, von welchem weiter rechts Râm-Allah, ein beträchtliches Dorf, grösstentheils von griechischen Christen bewohnt, liegen blieb, welches man aber vom Wege nicht sieht.</i>'),
        ('e', '“On our right we left the village of Taréndy, and further right of it Râm-Allah, a considerable village, inhabited mostly by Greek Christians, which cannot be seen from the road.”'),
    ]),
    '9.1': ('Close-up of the last lines of the page', [
        ('o', '“The present inhabitants of Jufna are all Christians; they number only forty-two taxable men; which gives a population …”'),
        ('n', 'The sentence runs on to the next page.'),
    ]),
    '9.2': ('Close-up of the paragraph on Ramallah', [
        ('o', '<i lang="fr">Ce bourg compte environ deux mille habitants, appartenant presque tous à la religion grecque schismatique. Ils y ont élevé, il y a dix-huit ans, une église, construite en partie avec les restes d’une ancienne église du Kharbet et-Thireh.</i>'),
        ('e', '“This town has about two thousand inhabitants, almost all belonging to the Greek Orthodox religion. Eighteen years ago they built a church there, constructed partly with the remains of an ancient church at Kharbet et-Thireh.”'),
    ]),
    '9.13': ('Close-up of the handwritten agreement', [
        ('o', '“An agreement dated June 15, 1896 whereby Ibrahim Daoud Harb lends Daoud Ya’coub Harb seven French gold “liras” without interest for one-and-one-half years. The names of the witnesses to the agreement appear at the bottom.”'),
        ('n', 'Shaheen’s printed note under the document. The handwritten Arabic is not typed out here.'),
    ]),
    '10.14': ('Close-up of the opening of the letter, turned to read', [
        ('n', 'A letter in Arabic handwriting. It is not typed out here; tap for the whole letter.'),
    ]),
    '10.16': ('Close-up of the masthead', [
        ('o', ar('مرآة الشرق') + ' · <span lang="en">MERAAT AL-SHARK</span>'),
        ('o', ar('جريدة عربية سياسية حرة تصدر مرة في الاسبوع موقتاً')),
        ('e', '“A free Arabic political newspaper, appearing once a week for the present.”'),
        ('o', ar('صاحب امتياز الجريدة ومحررها بولس شحادة')),
        ('e', 'Its licence-holder and editor, Boulos Shehadeh.'),
    ]),
    '10.19': ('Close-up of the certificate', [
        ('o', 'TRANS-JORDAN FRONTIER FORCE · CERTIFICATE OF DISCHARGE.<br>'
              'Serial No. 3904 · Regtl. No. 2581 · Rank: Corporal<br>'
              'Name: Elias Nasrallah Oudeh.<br>'
              'Branch of Service and nature of Employment: Base W/T Sigs. [?] · W/T Operator.<br>'
              'Date of Enlistment: 4th Oct. 1938.<br>'
              'Date of Discharge: 27th Dec. 1943.<br>'
              'Reason for Discharge: Termination of Contract<br>'
              'Character: Good'),
    ]),
    '10.21': ('Close-up of the paragraph on district 2', [
        ('o', '“Messrs Yousef Jiries Kaddoura, Khalil Salem Salah, Jamil Jiries Totah, Jalil Daoud Harb and Hanna Salem Jaber '
              'have been nominated for Electoral District, No.2. As the number of nominees for this district is five, whereas the '
              'number required is four, the election of the four candidates out of the five nominees for district No.2 will take '
              'place on Monday, 15th. April, in the premises of the Municipality from 9.00 a.m. to 1.00 p.m. and from 2.00 to 6.00 p.m.”'),
    ]),
    '10.22': ('Close-up of item 13, the result', [
        ('o', ar('١٣) كانت نتيجة التصويت كما يلي :')),
        ('e', '“The result of the vote was as follows”:'),
        ('o', ar('جميل طوطح ٢٥٥ صوت · يوسف قدوره ٢٣٦ · خليل صلاح ٢٢٢ · جليل حرب ٢١٥ · حنا جابر ١٥٤')),
        ('e', 'Jamīl Ṭūṭaḥ 255 votes, Yūsuf Qaddūra 236, Khalīl Ṣalāḥ 222, Jalīl Ḥarb 215, Ḥannā Jābir 154.'),
    ]),
    '10.23': ('Close-up of the head of the ballot and the five names', [
        ('o', 'BALLOT PAPER.<br>Electoral District: No.2, the Hadadeh.<br>'
              'Election: Held on Monday, 15th. April, 1946.<br>No. of candidates required: Four.<br>'
              'NOMINEES: 1. Yousef Jiries Kaddoura. 2. Khalil Salem Salah. 3. Jamil Jiries Totah. 4. Jalil Daoud Harb. 5. Hanna Salem Jaber.'),
    ]),
    '11.1': ('Close-up of the permit', [
        ('o', 'Palestine Railways (Ports Authority) · PORT MANAGER’S OFFICE, HAIFA<br>'
              'PERMANENT PERMIT · To enter the area of HAIFA PORT<br>'
              'Date: 19.4.1948 [?]<br>'
              'Name of holder: Mr. Harb N. Harb [?]<br>'
              'Occupation: Clerk Grade III<br>'
              'Employed by: Port Manager – Haifa'),
        ('o', '“The permit allowing Mr. Harb Harb to enter the port of Haifa, where he was employed as a Clerk, Grade III. The permit was issued April 19, 1948.”'),
        ('n', 'The permit is in English, Hebrew and Arabic; the English is typed out here, with Shaheen’s printed note under it.'),
    ]),
    '12.8': ('Close-up of the headline', [
        ('o', ar('اجراء أول عملية قسطرة للقلب في مستشفى رام الله الحكومي')),
        ('e', '“The first heart catheterisation in the Ramallah government hospital.”'),
        ('o', ar('الشريف : انجاز حقيقي سيوفر مبالغ كبيرة')),
        ('n', 'The line above the headline is not translated in the book.'),
    ]),
}

MAPS = {
    '6.4': 'Detail: Jerusalem and the land of the tribe of Benjamin, where Ramallah lies',
    '7.5': 'Detail: from Ramallah down to al-Karak',
    '8.4': 'Detail: “Rammula”, beside Gibeon and Jerusalem',
    '9.14': 'Detail: Râm Allah and el Bîreh',
}

CSS = r'''
/* v86: pictures that read on a phone */
figure img{cursor:zoom-in}
.pzc{display:none}
.pzsay{margin:12px 18px 18px;padding:12px 16px;background:#FBF7EE;border-left:3px solid #9A6324;text-align:left}
.pzsay .pzk{font:500 .86rem/1.2 "EB Garamond",Georgia,serif;font-variant:small-caps;text-transform:lowercase;letter-spacing:.12em;color:#7A4E1C;margin:0 0 6px}
.pzsay p{margin:0 0 8px;font:400 1.02rem/1.5 "EB Garamond",Georgia,serif;color:#1A1915}
.pzsay p.pe{color:#3D3A35}
.pzsay p.pn{font-size:.9rem;color:#5C574D}
.pzsay p:last-child{margin-bottom:0}
.pzsay .ar{font-size:1.18rem;line-height:1.8}
.cmb{display:none}
.lbz{position:absolute;top:6px;right:96px;display:flex;gap:6px}
.lbz button{background:#fff;color:#1A1915;border:0;border-radius:18px;font:600 1.05rem/1 "EB Garamond",Georgia,serif;width:36px;height:34px;padding:0}
.lb.lbi .lbt{right:190px}
.lb.lbi .lbin>img{background:#fff;margin:0 auto;max-width:none;height:auto;display:block}
@media screen and (max-width:760px){
  /* v86: an entry that holds a picture is always laid out, so it never comes up blank */
  .entry:has(figure){content-visibility:visible!important}
  figure.photo,figure.frontis{overflow:visible}
  figure.photo>img,figure.frontis>img,figure.photo .pzc img{display:block;max-width:none!important;
    width:calc(100% + var(--bl,0px) + var(--br,0px))!important;margin-left:calc(-1 * var(--bl,0px))!important;height:auto}
  figure.pz>img{display:none!important}
  figure.pz>.pzc{display:block;position:relative;margin:0}
  .pzc .pzh{display:block;margin:6px 0 0;font:italic .9rem/1.3 "EB Garamond",Georgia,serif;color:#5C574D}
  .pzc .pzh::after{content:" · tap for the whole page";font-style:normal;color:#7A4E1C}
  figure.pzmap .pzc .pzh::after{content:" · tap for the whole map"}
  figcaption{font-style:normal!important;font-size:1.02rem!important;line-height:1.5!important;color:#2B2924!important;text-align:left!important;padding:8px 0 6px!important}
  figcaption .src{display:block;margin-top:6px;font-size:.88rem!important;line-height:1.45;color:#5C4A2E!important;opacity:1!important}
  .pzsay{margin:12px 0 6px}
  figcaption .cm{display:none}
  figcaption.open .cm{display:inline}
  .cmb{display:inline;background:none;border:0;padding:0 0 0 4px;color:#007A3D;font:italic 1rem/1.5 "EB Garamond",Georgia,serif;cursor:pointer}
  figcaption.open .cmb{display:none}
}
@media print{.pzc,.pzsay,.cmb,.lbz{display:none!important}figure.pz>img{display:block!important}}
'''

JS = r'''
(function(){
  var root=document.documentElement;
  function bleed(){
    var f=[].find.call(document.querySelectorAll('.more figure.photo'),function(x){return x.offsetWidth>0;});
    if(!f||!window.matchMedia('(max-width:760px)').matches){root.style.removeProperty('--bl');root.style.removeProperty('--br');return;}
    var r=f.getBoundingClientRect(),vw=root.clientWidth;
    root.style.setProperty('--bl',Math.max(0,Math.round(r.left))+'px');
    root.style.setProperty('--br',Math.max(0,Math.round(vw-r.right))+'px');
  }
  bleed();window.addEventListener('resize',bleed);window.addEventListener('load',bleed);
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.evtoggle'))setTimeout(bleed,30);});

  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.cmb');if(!b)return;
    b.parentNode.classList.add('open');e.stopPropagation();
  });

  var lb=document.createElement('div');lb.className='lb lbi';
  lb.innerHTML='<div class="lbt"></div><div class="lbz"><button type="button" data-z="-1" aria-label="Smaller">−</button><button type="button" data-z="1" aria-label="Larger">+</button></div><button class="lbx" type="button">Close</button><div class="lbin"></div>';
  document.body.appendChild(lb);
  var inner=lb.querySelector('.lbin'),img=null,z=1,Z=[1,1.6,2.5,4];
  function fit(){var cw=inner.clientWidth;return Math.min(cw,img&&img.naturalWidth||cw);}
  function setz(nz,cx,cy){
    if(!img)return;nz=Math.max(0,Math.min(Z.length-1,nz));
    var ow=img.offsetWidth||1,sx=(inner.scrollLeft+(cx||inner.clientWidth/2))/ow,sy=(inner.scrollTop+(cy||inner.clientHeight/2))/(img.offsetHeight||1);
    z=nz;img.style.width=Math.round(fit()*Z[z])+'px';
    inner.scrollLeft=sx*img.offsetWidth-(cx||inner.clientWidth/2);inner.scrollTop=sy*img.offsetHeight-(cy||inner.clientHeight/2);
  }
  function close(){lb.classList.remove('on');inner.innerHTML='';img=null;root.style.overflow='';}
  lb.querySelector('.lbx').addEventListener('click',close);
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('on'))close();});
  lb.querySelectorAll('.lbz button').forEach(function(b){b.addEventListener('click',function(){setz(z+(+b.dataset.z));});});
  inner.addEventListener('dblclick',function(e){var r=inner.getBoundingClientRect();setz(z<Z.length-1?z+1:0,e.clientX-r.left,e.clientY-r.top);});
  document.addEventListener('click',function(e){
    var t=e.target;if(!t.closest)return;
    var fig=t.closest('figure');if(!fig||t.closest('a')||t.closest('.cmb')||t.closest('.lb'))return;
    if(!(t.tagName==='IMG'||t.closest('.pzc')))return;
    var full=fig.querySelector(':scope>img:not(.pzcrop)')||fig.querySelector('img:not(.pzcrop)');if(!full)return;
    e.preventDefault();e.stopPropagation();
    img=new Image();img.alt=full.alt||'';img.src=full.dataset.full||full.currentSrc||full.src;
    inner.innerHTML='';inner.appendChild(img);z=0;
    var k=(fig.getAttribute('data-k')||'').split(' · ')[0];
    lb.querySelector('.lbt').textContent=k||'';
    lb.classList.add('on');root.style.overflow='hidden';
    function go(){setz(0);inner.scrollTop=0;inner.scrollLeft=0;}
    if(img.complete)go();else img.onload=go;
  },true);
})();
'''


def _num(fig_open):
    m = re.search(r'data-k="Figure ([0-9.]+) ·', fig_open)
    return m.group(1) if m else None


def _say(num):
    label, rows = SCANS[num]
    cls = {'o': 'po', 'e': 'pe', 'n': 'pn'}
    ps = ''.join('<p class="%s">%s</p>' % (cls[k], t) for k, t in rows)
    return '%s<div class="pzsay"><div class="pzk">What it says</div>%s</div>%s' % (PZ_A, ps, PZ_B)


def _crop(num, label):
    src = '../img/crops/fig%s.jpg' % num.replace('.', '_')
    return ('%s<div class="pzc"><img class="pzcrop" src="%s" alt="%s" loading="lazy" decoding="async">'
            '<span class="pzh">%s</span></div>%s' % (PZ_A, src, _html.escape(label, quote=True), label, PZ_B))


def _split_caption(cap):
    """Keep the first sentence; fold the rest of the caption text (not the source)."""
    i = cap.find('<span class="src">')
    body, src = (cap[:i], cap[i:]) if i >= 0 else (cap, '')
    plain = re.sub(r'<[^>]+>', '', body)
    if len(plain) < 230 or 'class="cm"' in body:
        return cap
    for m in re.finditer(r'[.”!?](?=\s+[A-Z“‘ʿ(])', body):
        cut = m.end()
        head = body[:cut]
        if len(re.sub(r'<[^>]+>', '', head)) < 50:
            continue
        # not inside a tag or an open element
        if head.count('<') != head.count('>'):
            continue
        opens = len(re.findall(r'<(?!/|br|img)[a-z][^>]*>', head))
        closes = len(re.findall(r'</[a-z]+>', head))
        if opens != closes:
            continue
        rest = body[cut:]
        if len(re.sub(r'<[^>]+>', '', rest).strip()) < 40:
            return cap
        return head + '<span class="cm">' + rest + '</span><button class="cmb" type="button">more</button>' + src
    return cap


def apply(h):
    if MARK in h:
        return h
    counts = {'scans': 0, 'maps': 0, 'split': 0}

    def fig(m):
        whole = m.group(0)
        open_tag = m.group(1)
        num = _num(open_tag)
        out = whole
        # caption split (all figures)
        def cap(cm):
            new = _split_caption(cm.group(2))
            if new != cm.group(2):
                counts['split'] += 1
            return cm.group(1) + new + cm.group(3)
        out = re.sub(r'(<figcaption>)(.*?)(</figcaption>)', cap, out, count=1, flags=re.S)
        if num in SCANS or num in MAPS:
            is_map = num in MAPS
            label = MAPS[num] if is_map else SCANS[num][0]
            cls = 'pz pzmap' if is_map else 'pz'
            out = re.sub(r'^<figure class="([^"]*)"', lambda c: '<figure class="%s %s"' % (c.group(1), cls), out, count=1)
            out = out.replace('<img ', _crop(num, label) + '<img ', 1)
            if not is_map:
                out = out.replace('</figure>', _say(num) + '</figure>', 1)
                counts['scans'] += 1
            else:
                counts['maps'] += 1
        return out

    h = re.sub(r'(<figure\b[^>]*>).*?</figure>', fig, h, flags=re.S)
    h = h.replace('</style>', CSS + '</style>', 1)
    h = h.replace('</body>', '<script>' + JS + '</script>' + MARK + '</body>', 1)
    apply.counts = counts
    return h


def strip(h):
    """Print and the family edition: full plates, no close-ups, no buttons."""
    h = re.sub(re.escape(PZ_A) + r'.*?' + re.escape(PZ_B), '', h, flags=re.S)
    h = re.sub(r'<button class="cmb"[^>]*>.*?</button>', '', h, flags=re.S)
    h = h.replace('<span class="cm">', '<span>')
    return h
