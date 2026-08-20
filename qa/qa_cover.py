import asyncio, json
from playwright.async_api import async_playwright
import os, pathlib
ROOT = pathlib.Path(os.environ.get('AFRP_ROOT') or pathlib.Path(__file__).resolve().parents[1])
BOOK = (ROOT / 'out' / 'AFRP_The_One_Line_v5.html').as_uri()

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':1000})
        await pg.goto(BOOK); await pg.wait_for_timeout(1600)
        r=await pg.evaluate("""()=>{
          const out=[];
          document.querySelectorAll('figure svg').forEach((svg,fi)=>{
            const kids=[...svg.querySelectorAll('*')];
            const texts=[];
            kids.forEach((el,idx)=>{ if(el.tagName==='text'){ try{const b=el.getBBox(); if((el.textContent||'').trim()) texts.push({idx,b,s:el.textContent.trim()});}catch(e){} } });
            kids.forEach((el,idx)=>{
              const tag=el.tagName;
              if(!['circle','rect','path','ellipse','polygon'].includes(tag)) return;
              const fill=(el.getAttribute('fill')||getComputedStyle(el).fill||'').toLowerCase();
              if(!fill||fill==='none'||fill==='transparent') return;
              const op=parseFloat(el.getAttribute('opacity')||'1');
              if(op<0.55) return;
              let bb; try{bb=el.getBBox()}catch(e){return}
              if(bb.width>260||bb.height>260) return;   // background plates
              texts.forEach(t=>{
                if(t.idx>idx) return;                    // only shapes painted AFTER the text
                const cx=t.b.x+t.b.width/2, cy=t.b.y+t.b.height/2;
                if(cx>bb.x+1&&cx<bb.x+bb.width-1&&cy>bb.y+1&&cy<bb.y+bb.height-1)
                  out.push({fig:fi+1,text:t.s.slice(0,40),over:tag,fill});
              });
            });
          });
          const seen=new Set(),u=[];out.forEach(o=>{const k=JSON.stringify(o);if(!seen.has(k)){seen.add(k);u.push(o)}});
          return u;}""")
        print(json.dumps(r,ensure_ascii=False,indent=1) if r else 'CLEAN — no text painted over by a later opaque shape')
        await b.close()
asyncio.run(main())
