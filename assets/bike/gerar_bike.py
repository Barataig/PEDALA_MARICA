from PIL import Image
import math
W,H=32,20
def frame(f):
    g=[[0]*W for _ in range(H)]
    def p(x,y,c):
        if 0<=x<W and 0<=y<H: g[y][x]=c
    def pts(a,b):
        n=max(abs(b[0]-a[0]),abs(b[1]-a[1]),1)
        return [(round(a[0]+(b[0]-a[0])*i/n),round(a[1]+(b[1]-a[1])*i/n)) for i in range(n+1)]
    def wheel(cx,cy,rot):
        for y in range(-7,8):
            for x in range(-7,8):
                d=math.hypot(x,y)
                if 4.5<=d<=5.7: p(cx+x,cy+y,1)
                elif d<4.5 and False: p(cx+x,cy+y,4)
        for k in range(2):
            a=rot+k*math.pi/2
            for t in pts((round(cx-4*math.cos(a)),round(cy-4*math.sin(a))),(round(cx+4*math.cos(a)),round(cy+4*math.sin(a)))): p(*t,3)
        p(cx,cy,1)
    r=0 if f==0 else math.pi/4
    wheel(7,13,r); wheel(24,13,r)
    def thick(segs):
        S=set()
        for a,b in segs: S|=set(pts(a,b))
        for x,y in S:
            for dx in(-1,0,1):
                for dy in(-1,0,1):
                    if g[y+dy][x+dx] in(0,4,3) or True:
                        if (x+dx,y+dy) not in S and 0<=x+dx<W and 0<=y+dy<H and g[y+dy][x+dx]!=2: g[y+dy][x+dx]=1
        for x,y in S: p(x,y,2)
    # rear fender
    for x in range(2,12):
        for y in range(5,8):
            if (x-7)**2/26+(y-8)**2/10<=1: p(x,y,2)
    for x in range(2,12): p(x,5 if False else 4,0)
    for t in [(x,y) for x in range(2,12) for y in range(4,9)]:
        pass
    thick([((7,13),(14,14)),((14,14),(10,5)),((14,14),(17,11)),((17,11),(21,8)),((21,8),(24,13)),((21,8),(21,4)),((21,4),(24,3))])
    # fender label
    for x in range(5,10):
        for y in range(5,8): p(x,y,4)
    p(6,6,2);p(7,6,2);p(8,6,2)
    # seat
    for x in range(7,13): p(x,3,1); 
    for x in range(8,12): p(x,4,1)
    for x in range(8,12): p(x,3,1)
    # basket
    for y in range(4,9):
        for x in range(23,30): p(x,y,2)
    for x in range(23,30): p(x,4,1); p(x,8,1)
    for y in range(4,9): p(23,y,1); p(29,y,1)
    p(25,5,4);p(26,5,4);p(27,5,4);p(25,6,4);p(26,6,4);p(27,6,4)
    p(25,6,2)
    # pedal
    if f==0:
        for x in(13,14,15): p(x,17,1)
        p(14,16,1);p(14,15,1)
    else:
        for x in(13,14,15): p(x,11 if False else 12,1)
        p(14,13,1)
    for x in range(3,29): 
        if g[19][x]==0: p(x,19,3)
    return g
pal_col={1:(34,22,30),2:(222,36,44),3:(150,150,160),4:(252,252,252)}
pal_gb={1:(15,56,15),2:(48,98,48),3:(139,172,15),4:(155,188,15)}
def render(frames,pal,name,bg):
    im=Image.new("RGBA",(W*len(frames),H),(0,0,0,0))
    for i,g in enumerate(frames):
        for y in range(H):
            for x in range(W):
                if g[y][x]: im.putpixel((i*W+x,y),pal[g[y][x]]+(255,))
    im.save(name+".png")
    big=im.resize((im.width*14,im.height*14),Image.NEAREST)
    b=Image.new("RGBA",big.size,bg+(255,)); b.alpha_composite(big); b.save(name+"_preview.png")
fs=[frame(0),frame(1)]
render(fs,pal_col,"bike_color",(248,248,232))
render(fs,pal_gb,"bike_gameboy",(155,188,15))
