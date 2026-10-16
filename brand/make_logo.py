import math,sys
INK="#2e2a24"; FACE="#38332d"; LEG="#27231e"
def sub(a,b): return [a[k]-b[k] for k in range(3)]
def dot(a,b): return sum(a[k]*b[k] for k in range(3))
def cross(a,b): return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a): l=math.sqrt(dot(a,a)); return [x/l for x in a]
C=[5.6,-4.2,5.2]; T=[1.2,.5,.1]
f=norm(sub(T,C)); R=norm(cross(f,[0,0,1])); U=cross(R,f); FOC=1000
def proj(p):
    v=sub(p,C); x,y,z=dot(v,R),dot(v,U),dot(v,f); return (FOC*x/z,-FOC*y/z)
H=.55; I=.1; keys=[0,1.12,2.24]; CELL=700; PADX=60
allp=[proj([X+a,b,c]) for X in keys for a in(0,1) for b in(0,1) for c in(0,H)]
minx=min(p[0] for p in allp);maxx=max(p[0] for p in allp);miny=min(p[1] for p in allp);maxy=max(p[1] for p in allp)
sc=(CELL-2*PADX)/(maxx-minx); ox=PADX-minx*sc-30; oy=(CELL-(maxy-miny)*sc)/2-miny*sc+30
def P(p): x,y=proj(p); return (x*sc+ox,y*sc+oy)
def pts(l): return " ".join(f"{x:.1f},{y:.1f}" for x,y in l)
SW=5.5
PAL={'beige':("#e6dfd0","#c9bfab","#aea48f","#d8d0be"),'gold':("#ffd21f","#ffc20a","#f0a000","#fbc815")}
def rpath(pl,rad):
    # pl: list of (pt, rounded) closed
    n=len(pl); d=""
    for k in range(n):
        (p,rd)=pl[k]; a=pl[k-1][0]; b=pl[(k+1)%n][0]
        if not rd:
            d+=("M" if k==0 else "L")+f"{p[0]:.1f},{p[1]:.1f} "; continue
        def toward(q,r_):
            dx,dy=q[0]-p[0],q[1]-p[1]; l=math.hypot(dx,dy); t=min(r_,l/2)/l; return (p[0]+dx*t,p[1]+dy*t)
        rr=rd if rd>1 else rad; s=toward(a,rr); e=toward(b,rr)
        d+=("M" if k==0 else "L")+f"{s[0]:.1f},{s[1]:.1f} Q{p[0]:.1f},{p[1]:.1f} {e[0]:.1f},{e[1]:.1f} "
    return d+"Z"
def build(D):
    def zs(x): t=(x-.5)/(.5-I); return H-D*(1-t*t)
    N=48
    def curveY(y,x0,x1): return [(x0+(x1-x0)*k/N,y,zs(x0+(x1-x0)*k/N)) for k in range(N+1)]
    def uscale(X,Y,Z):
        a=P([X,Y,Z]);b=P([X+.1,Y,Z]);c=P([X,Y+.1,Z]); return (math.dist(a,b)+math.dist(a,c))*5
    def stroke(world,cx,y,w,col,X0):
        dens=[]
        for (u1,v1),(u2,v2) in zip(world,world[1:]):
            for k in range(8): t=k/8; dens.append((u1+(u2-u1)*t,v1+(v2-v1)*t))
        dens.append(world[-1])
        l=[P([X0+cx+u,y+v,zs(cx+u)]) for u,v in dens]
        s=uscale(X0+cx,y,H)*w
        return f'<polyline points="{pts(l)}" fill="none" stroke="{col}" stroke-width="{s:.2f}" stroke-linecap="round" stroke-linejoin="round"/>'
    def dotp(X0,cx,y,r,col):
        l=[P([X0+cx+r*math.cos(t),y+r*math.sin(t),zs(cx+r*math.cos(t))]) for t in [k*math.pi/8 for k in range(16)]]
        return f'<polygon points="{pts(l)}" fill="{col}"/>'
    def curve(a,b,c,n=14): return [((1-t)**2*a[0]+2*(1-t)*t*b[0]+t*t*c[0],(1-t)**2*a[1]+2*(1-t)*t*b[1]+t*t*c[1]) for t in [k/n for k in range(n+1)]]
    def legend(kind,X0):
        cx=.35; up=.66; lo=.34; o=[]
        if kind==';': lo=.4
        if kind=='L': return stroke([(-.07,.08),(-.07,-.08),(.07,-.08)],cx,up,.032,LEG,X0)
        if kind==';':
            o+= [dotp(X0,cx,up+.05,.021,LEG),dotp(X0,cx,up-.05,.021,LEG),dotp(X0,cx,lo+.05,.021,LEG),stroke([(0,-.03),(-.022,-.07)],cx,lo,.024,LEG,X0)]
            return "".join(o)
        for dx in(-.055,.055): o.append(stroke([(dx+.012,.06),(dx-.012,-.04)],cx,up,.032,FACE,X0))
        o.append(stroke(curve((-.1,.03),(0,-.065),(.1,.03)),cx,lo,.032,FACE,X0)); return "".join(o)
    def star4(x,y,r,k,fill,sw,rot=0):
        a=[(0,-r),(r,0),(0,r),(-r,0)]; c=[(k*r,-k*r),(k*r,k*r),(-k*r,k*r),(-k*r,-k*r)]
        pp=[(0,-r)]; d=f"M0,{-r:.1f} "
        for i in range(4):
            e=a[(i+1)%4]; d+=f"Q{c[i][0]:.1f},{c[i][1]:.1f} {e[0]:.1f},{e[1]:.1f} "
        return f'<path d="{d}Z" transform="translate({x:.1f},{y:.1f}) rotate({rot})" fill="{fill}" stroke="{INK if sw else "none"}" stroke-width="{sw}" stroke-linejoin="round"/>'
    def sparkle(x,y,r):
        s=star4(x,y,r*.62,.16,"#ffe36a",0,45)+star4(x,y,r,.2,"#fff4b8",1.8)+star4(x,y,r*.4,.2,"#ffffff",0)
        for dx,dy,rr in((r*.95,-r*.75,3.2),(r*.9,r*.55,2.2),(-r*.85,-r*.8,2.4)):
            s+=f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="{rr}" fill="#fff4b8" stroke="{INK}" stroke-width="1.2"/>'
        return s
    cid=[0]
    def key(kind,X0,leg,spark=False):
        top,fr,rt,sh=PAL[kind]; i=I; p=lambda x,y,z:P([X0+x,y,z]); pw=lambda q:P([X0+q[0],q[1],q[2]])
        cid[0]+=1; k=f"c{D}{cid[0]}"
        fc=[pw(q) for q in curveY(i,i,1-i)]; bc=[pw(q) for q in curveY(1-i,1-i,i)]
        sil=[(p(0,0,0),1),(fc[0],1),(bc[-1],1)]+[(q,0) for q in bc[::-1][1:-1]][::-1]
        # silhouette: p0 -> front-left top -> back-left top -> back curve to back-right -> right back base -> right front base
        JR=3.5
        sil=[(p(0,0,0),1),(fc[0],JR),(bc[-1],1)]+[(q,0) for q in bc[1:-1][::-1]]+[(bc[0],JR),(p(1,1,0),1),(p(1,0,0),JR)]
        def apex(k,rad=JR):
            n=len(sil); p_,_=sil[k]; a_=sil[k-1][0]; b_=sil[(k+1)%n][0]
            def tw(q):
                dx,dy=q[0]-p_[0],q[1]-p_[1]; l=math.hypot(dx,dy); t=min(rad,l/2)/l; return (p_[0]+dx*t,p_[1]+dy*t)
            s_=tw(a_); e_=tw(b_); return (.25*s_[0]+.5*p_[0]+.25*e_[0],.25*s_[1]+.5*p_[1]+.25*e_[1])
        iF=1; iBR=len(sil)-3; iFB=len(sil)-1
        fcE=[apex(iF)]+fc[1:]
        rtE=[p(1-i,i,H),apex(iBR)]
        vtE=[apex(iFB),p(1-i,i,H)]
        o=[f'<clipPath id="{k}"><path d="{rpath(sil,9)}"/></clipPath><g clip-path="url(#{k})">']
        o.append(f'<polygon points="{pts([p(0,0,0),vtE[0],fc[-1]]+fc[:0:-1]+[fcE[0]])}" fill="{fr}"/>')
        o.append(f'<polygon points="{pts([vtE[0],p(1,1,0),rtE[1],p(1-i,i,H)])}" fill="{rt}"/>')
        o.append(f'<polygon points="{pts(fcE+[rtE[1]]+bc[1:])}" fill="{top}"/>')
        if D>0:
            inner=[pw(q) for q in curveY(1-i-.16,1-i,i)]
            o.append(f'<polygon points="{pts(bc+inner[::-1])}" fill="{sh}" opacity=".75"/>')
        if kind=='gold':
            gl="#fff8c4"
            o.append(f'<polygon points="{pts([p(.66,.84,H),p(.84,.84,H),p(.66,.66,H)])}" fill="{gl}"/>')
            o.append(f'<polygon points="{pts([p(.86,.8,H),p(.86,.7,H),p(.76,.6,H),p(.76,.7,H)])}" fill="{gl}" opacity=".8"/>')
            o.append(f'<polygon points="{pts([p(.12,0,.05),p(.2,0,.05),p(.21,i*.7,H-.05),p(.14,i*.7,H-.05)])}" fill="{gl}" opacity=".85"/>')
        e=lambda l:f'<polyline points="{pts(l)}" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"/>'
        o+= [e(fcE),e(rtE),e(vtE)]
        o.append(f'<circle cx="{p(1-i,i,H)[0]:.1f}" cy="{p(1-i,i,H)[1]:.1f}" r="{SW/2:.2f}" fill="{INK}"/>')
        o.append(legend(leg,X0)); o.append('</g>')
        o.append(f'<path d="{rpath(sil,9)}" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
        s="\n".join(o)
        if spark:
            vx,vy=max([p(1-i,i,H),p(1-i,1-i,H)],key=lambda q:q[0]); r=50; bx,by=vx+r*.42,vy-r*.1
            s+="\n"+sparkle(bx,by,r)+"\n"+sparkle(bx+r*.72,by-r*.9,r*.3)
        return s
    return "\n".join([key('beige',keys[0],'L'),key('beige',keys[1],';'),key('gold',keys[2],"'")])
bgs=[("#ffffff",0),("#ffffff",.06),("#2e2a24",0),("#2e2a24",.06)]
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CELL*2} {CELL*2}" width="{CELL*2}" height="{CELL*2}">']
for n,(bg,D) in enumerate(bgs):
    x=(n%2)*CELL;y=(n//2)*CELL
    o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" fill="{bg}"/><g transform="translate({x},{y})">{build(D)}</g>')
o.append('</svg>'); open('sheet8.svg','w').write("\n".join(o))
open('keys8-flat.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CELL} {CELL}" width="{CELL}" height="{CELL}">{build(0)}</svg>')
open('keys8-scoop.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CELL} {CELL}" width="{CELL}" height="{CELL}">{build(.06)}</svg>')
