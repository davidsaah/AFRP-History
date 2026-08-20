import asyncio, json
from playwright.async_api import async_playwright
import os, pathlib
ROOT = pathlib.Path(os.environ.get('AFRP_ROOT') or pathlib.Path(__file__).resolve().parents[1])
BOOK = (ROOT / 'out' / 'AFRP_The_One_Line_v5.html').as_uri()

P=BOOK
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        errs=[]
        for w in (1280,900,420):
            pg=await b.new_page(viewport={'width':w,'height':1000})
            pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            await pg.goto(P); await pg.wait_for_timeout(1200)
            ov=await pg.evaluate("()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,h:document.body.scrollHeight})")
            print(f'{w}px  scrollWidth={ov["sw"]} client={ov["cw"]} overflow={ov["sw"]-ov["cw"]}  docHeight={ov["h"]}')
            if w==1280:
                bad=await pg.evaluate("""()=>{
                  const out=[];
                  document.querySelectorAll('figure svg').forEach((svg,i)=>{
                    const t=[...svg.querySelectorAll('text')];
                    const bx=t.map(e=>{try{const b=e.getBBox();return {b,s:(e.textContent||'').trim()}}catch(e){return null}}).filter(Boolean).filter(o=>o.s);
                    for(let a=0;a<bx.length;a++)for(let c=a+1;c<bx.length;c++){
                      const A=bx[a].b,B=bx[c].b;
                      const ox=Math.min(A.x+A.width,B.x+B.width)-Math.max(A.x,B.x);
                      const oy=Math.min(A.y+A.height,B.y+B.height)-Math.max(A.y,B.y);
                      if(ox>2.5&&oy>2.5){out.push({fig:i+1,a:bx[a].s,b:bx[c].s});}
                    }
                  });
                  return out.slice(0,25);}""")
                print('  text overlaps:', 'CLEAN' if not bad else json.dumps(bad,ensure_ascii=False)[:1500])
                links=await pg.evaluate("""()=>{const ids=new Set([...document.querySelectorAll('[id]')].map(e=>e.id));
                  return [...document.querySelectorAll('a[href^=\"#\"]')].map(a=>a.getAttribute('href').slice(1)).filter(h=>h&&!ids.has(h));}""")
                print('  broken anchors:', 'none' if not links else links[:20])
            await pg.close()
        print('page errors:', 'none' if not errs else errs[:5])
        await b.close()
asyncio.run(main())
