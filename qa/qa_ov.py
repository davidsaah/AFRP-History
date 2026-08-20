import asyncio,json
from playwright.async_api import async_playwright
import os, pathlib
ROOT = pathlib.Path(os.environ.get('AFRP_ROOT') or pathlib.Path(__file__).resolve().parents[1])
BOOK = (ROOT / 'out' / 'AFRP_The_One_Line_v5.html').as_uri()

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':1000})
        await pg.goto(BOOK); await pg.wait_for_timeout(1500)
        bad=await pg.evaluate("""()=>{const out=[];
          document.querySelectorAll('figure svg').forEach((svg,i)=>{
            const bx=[...svg.querySelectorAll('text')].map(e=>{try{const b=e.getBBox();return{b,s:(e.textContent||'').trim()}}catch(x){return null}}).filter(o=>o&&o.s);
            for(let a=0;a<bx.length;a++)for(let c=a+1;c<bx.length;c++){
              if(bx[a].s===bx[c].s) continue;
              const A=bx[a].b,B=bx[c].b;
              const ox=Math.min(A.x+A.width,B.x+B.width)-Math.max(A.x,B.x);
              const oy=Math.min(A.y+A.height,B.y+B.height)-Math.max(A.y,B.y);
              if(ox>2.5&&oy>2.5)out.push({fig:i+1,a:bx[a].s,b:bx[c].s,ox:Math.round(ox),oy:Math.round(oy),ax:Math.round(A.x),ay:Math.round(A.y),bx:Math.round(B.x),by:Math.round(B.y)});
            }});
          const seen=new Set(),u=[];out.forEach(o=>{const k=o.fig+'|'+o.a+'|'+o.b;if(!seen.has(k)){seen.add(k);u.push(o)}});return u;}""")
        print(json.dumps(bad,ensure_ascii=False,indent=1))
        await b.close()
asyncio.run(main())
