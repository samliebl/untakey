import numpy as np, sys, time
from PIL import Image
import potrace
S="/private/tmp/claude-501/-Users-samliebl-Code/6a285366-f6e5-4fa8-b4f8-81bbd007a045"
im=Image.open(f"{S}/images/3.webp").convert("RGBA")
a=np.array(im).astype(float); al=a[:,:,3]/255
R,B=a[:,:,0],a[:,:,2]
gold=np.clip((R-B)/200,0,1)         # 1 for gold, ~0 for dark brown
cov_gold=al*gold; cov_dark=al*(1-gold)
UP=3
def trace(cov,name):
    ys,xs=np.where(cov>0.05); x0,x1,y0,y1=xs.min()-6,xs.max()+7,ys.min()-6,ys.max()+7
    c=cov[y0:y1,x0:x1]
    big=Image.fromarray((c*255).astype("uint8")).resize(((x1-x0)*UP,(y1-y0)*UP),Image.BICUBIC)
    m=np.array(big)>127
    t=time.time()
    bm=potrace.Bitmap(~m)
    pl=bm.trace(turdsize=40,turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,alphamax=1.0,opticurve=True,opttolerance=0.6)
    print(name,"traced",time.time()-t,"s",len(pl),"paths",flush=True)
    d=[]
    f=lambda p:f"{x0+p.x/UP:.2f},{y0+p.y/UP:.2f}"
    for cv in pl:
        d.append(f"M{f(cv.start_point)}")
        for s in cv.segments:
            if s.is_corner: d.append(f"L{f(s.c)}L{f(s.end_point)}")
            else: d.append(f"C{f(s.c1)} {f(s.c2)} {f(s.end_point)}")
        d.append("Z")
    return " ".join(d)
dk=trace(cov_dark,"dark"); gd=trace(cov_gold,"gold")
w,h=im.size
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><path fill="#2e2a24" fill-rule="evenodd" d="{dk}"/><path fill="#f9c70a" fill-rule="evenodd" d="{gd}"/></svg>'
open(f"{S}/scratchpad/wordmark-traced.svg","w").write(svg); print("done",len(svg))
