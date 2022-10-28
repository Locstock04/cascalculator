
"""
To-do
  ‣Add more blocks
  ‣Show more info on pause menu, such as
      save slot, controls, number of blocks
  ‣Save and load selected block
  ‣Move between maps
  ‣When sand falls diagonal, check if the block
      above needs to fall down
  ‣3 water falling diagnol left due to sand tvrns
      to 2 water
  ‣Make blocks get IDs automatically
"""
#================================
from math import *
from ti_draw import *
from ti_system import *
#================================
#3,2,6,53,106,159,318 
#2,4,53,106,212
screenWidth=318
screenHeight=212
px=10
py=10
cp=-px
rp=-py
slc=1
slcm = 0
slcs = 0
saveSlot="1"
saveSlots=("1","2","3","4")

keysLeft = {"left","4","a"}
keysRight ={"right","6","d"}
keysLeftLeft = {"square","**"}
keysRightRight ={"*","/"}
keysUp ={"up","8","w"}
keysDown ={"down","2","s"}
keysUpUp ={"upup","."}
keysDownDown ={"downdown","k"}
keysPlace ={"center","5"}
keysAntiClock={"AntiClock","7"}
keysClock={"Clock","9"}
keysSave={"Save","scratchpad", 'o'}
keysLoad={"Load","tab"}
keysClear={"Clear","u"}
keysRefresh={"Refresh","n","enter"}
keysSaveSlot1={"SaveSlot1","y"}
keysSaveSlot2={"SaveSlot2","z"}
keysPause={"pause","p","menu"}

class Mats:
  instances = []
  def __init__(self,a=[-1],u=[0],d=3,c1=(0,0,0),c2=(0,0,0),c3=(0,0,0)):
    # a is set of active IDs
    # u is set of unactive IDs
    # d is density
    # c are tuples for colours
    self.__class__.instances.append(self)
    self.a=a
    self.u=u
    self.d=d
    self.c1=c1
    self.c2=c2
    self.c3=c3

menuBG=Mats([-5],[0],100,(40,40,40))
debugR=Mats([-4],[],-1,(255,0,0))
debugG=Mats([-3],[],-1,(0,255,0))
debugB=Mats([-2],[],-1,(0,0,255))
air=Mats([-1],[0],0,(210,220,255))
sand=Mats([2,1],[7],3,(246,237,90))
waterR=Mats([4,3],[8],2,(82,102,200))
waterL=Mats([6,5],[9],2,(70,140,255))
stone=Mats([11,10],[12],5,(150,150,150))
wood=Mats([13,14],[15],1,(155,100,20),)
void=Mats([16,17,18],[],99,(250,220,200))
bedrock=Mats([19,20],[21],90,(100,120,150))

# ua is a set of all unactives
ua={0}
for i in Mats.instances:
  for j in i.u:
    ua.add(j)

#Block IDs
get={}
for i in Mats.instances:
  for j in (i.a+i.u):
    get[j]=i

# placable blocks
plc = {
  1: 1,
  2: 3,
  3: 5,
  4: 10,
  5: 13,
  6: 16,
  7: 19}
# placable blocks names
plcn ={
  1: "Sand",
  2: "Water (Right)",
  3: "Water (Left)",
  4: "Stone",
  5: "Wood",
  6: "Void",
  7: "Bedrock"}

# Return a list with each list containing a list
def CreateMatrix(x,y):
  return x*[y*[0]]

def rep(x,y,n,map=0):
  global scrn
  global menu
  if (map==0):
    temp = list(scrn[x])
    temp[y] = n
    scrn[x] = temp
  elif(map==1):
    temp = list(menu[x])
    temp[y] = n
    menu[x] = temp
  else:
    temp = list(map[x])
    temp[y] = n
    map[x] = temp
    return map

def repr(r,n):
  global scrn
  for i in range(0,len(scrn)):
    rep(i,r,n)

def chk(x,y,l=1):
  if(l!=1):
    try:
      temp = list(l[x])
      return temp[y]
    except:
      return -5
  else:
    try:
      temp = list(scrn[x])
      return temp[y]
    except:
      return -5

def Save():
  tmp = [px,py]
  for r in scrn:
    for c in r:
      tmp.append(c)
  store_list("map"+saveSlot,tmp)

def Load():
  global scrn
  tmp=recall_list("map"+saveSlot)
  tmpx=tmp.pop(0)
  tmpy=tmp.pop(0)
  tmps=CreateMatrix(ceil(screenWidth/tmpx),ceil(screenHeight/tmpy))
  rp=-1
  for r in tmps:
    rp+=1
    cp=-1
    for c in r:
      cp+=1
      tmps=list(rep(rp,cp,tmp[cp+rp*ceil(screenHeight/tmpy)],tmps))
  scrn=list(tmps)

def UpdateInput(k):
  if k in keysLoad:
    Load()
  elif k in keysSave:
    Save()
  elif k in keysClear:
    FillBlank()
  elif k in keysRefresh:
    UpdateAllDisplay()

def UpdateData(k):
  global scrn
  global slc
  global saveSlot
  global pause
  if(pause):
    UpdateAllDisplay()
    pause=False
  for cc in range(0,len(scrn)):
    for rr in range(0,len(scrn[cc])):
      cr=chk(cc,rr)
      if (chk(cc,rr) in ua):
        continue
      if (cr in {-2,-3,-4}):
        rep(cc,rr,cr-1)
        cr-=1
        if cr==-5: rep(cc,rr,-2)
        # Controls
        if k in keysLeft:
          if (cc==0): rep(len(scrn)-1,rr,-5)
          else: rep(cc-1,rr,cr)
          rep(cc,rr,-1)
        elif k in keysRight:
          if (cc<len(scrn)-1): rep(cc+1,rr,-5)
          else: rep(0,rr,-5)
          rep(cc,rr,-1)
        if k in keysLeftLeft:
          if (cc in {0,1}): rep(len(scrn)-1,rr,chk(cc,rr))
          else: rep(cc-2,rr,chk(cc,rr))
          rep(cc,rr,-1)
        elif k in keysRightRight:
          if cc+1<len(scrn)-1: rep(cc+2,rr,-5)
          else: rep((-len(scrn)+cc),rr,-5)
          rep(cc,rr,-1)
        elif k in keysDownDown:
          if (get[chk(cc,rr+1)].d < get[-5].d):
            rep(cc,rr+1,-5)
            rep(cc,rr,-1)
        elif k in keysUpUp:
          if (get[chk(cc,rr-1)].d < get[-5].d):
            rep(cc,rr-1,-4)
            rep(cc,rr,-1)

        elif k in keysPlace:
          rep(cc,rr+1,get[plc[slc]].a[0])
        elif k in keysDown:
          rep(cc,rr+1,get[plc[slc]].a[0])
          if (cc!=0):
            rep(cc-1,rr+1,get[plc[slc]].a[0])
          if(cc!=len(scrn)-1):
            rep(cc+1,rr+1,get[plc[slc]].a[0])
        elif k in keysUp:
          repr(rr+1,get[plc[slc]].a[0])

        elif k in keysAntiClock:
          slc-=1
          if (slc==0): slc=len(plc)
        elif k in keysClock:
          if (slc==len(plc)): slc=0
          slc+=1
      # Rep lag blocks
      elif (cr==2): rep(cc,rr,1)
      elif (cr==4): rep(cc,rr,3)
      elif (cr==6): rep(cc,rr,5)
      elif (cr==-1): rep(cc,rr,0)
      elif (cr==-5): rep(cc,rr,-4)
      elif (cr==11): rep(cc,rr,10)
      elif (cr==13): rep(cc,rr,14)
      elif (cr==17): rep(cc,rr,16)
      elif (cr==19): rep(cc,rr,20)
      elif (cr==20): rep(cc,rr,21)
    # Logic blocks
      #Water
      elif (cr==3):
        if (get[chk(cc,rr+1)].d < get[cr].d):
          rep(cc,rr,get[chk(cc,rr+1)].a[0])
          rep(cc,rr+1,4)
        elif (chk(cc+1,rr)in{0,-1}):
          rep(cc+1,rr,4)
          rep(cc,rr,-1)
        elif ((get[chk(cc+1,rr)].d <= get[cr].d) and (chk(cc+1,rr) not in {-1,0}) and (chk(cc+2,rr) in {0,-1}) and (cc+2<len(scrn))):
          rep(cc+2,rr,get[chk(cc+1,rr)].a[0])
          rep(cc+1,rr,get[cr].a[0])
          rep(cc,rr,-1)
          rep(cc-1,rr-1,get[chk(cc-1,rr-1)].a[0])
        elif ((chk(cc-1,rr) in {0,-1}) and (cc!=0)):
          rep(cc,rr,6)
        elif ((get[chk(cc-1,rr)].d <= get[cr].d) and (chk(cc-1,rr) not in {-1,0}) and (chk(cc-2,rr) in {0,-1}) and (cc>1)):
          rep(cc,rr,5)
        else: rep(cc,rr,8)

      elif (cr ==5):
        if (get[chk(cc,rr+1)].d < get[cr].d):
          rep(cc,rr,get[chk(cc,rr+1)].a[0])
          rep(cc,rr+1,6)
        elif (chk(cc-1,rr)in{0,-1}):
          rep(cc-1,rr,6)
          rep(cc,rr,-1)
        elif ((get[chk(cc-1,rr)].d <= get[cr].d) and (chk(cc-2,rr) in {0,-1})):
          rep(cc-2,rr,get[chk(cc-1,rr)].a[0])
          rep(cc-1,rr,cr)
          rep(cc,rr,-1)
          if(cc<len(scrn)-1):
            rep(cc+1,rr-1,get[chk(cc+1,rr-1)].a[0])
        elif ((chk(cc+1,rr) in {0,-1}) and (cc!=len(scrn)-1)):
          rep(cc,rr,4)
        elif ((get[chk(cc+1,rr)].d <= get[cr].d) and (chk(cc+1,rr) not in {-1,0}) and (chk(cc+2,rr) in {0,-1}) and (cc+2<len(scrn))):
          rep(cc,rr,3)
        else:
          rep(cc,rr,9)
      elif(cr==10):
        if (chk(cc,rr+1)>-2 and (rr<len(scrn[0])-1)):
          if (get[chk(cc,rr+1)].d<stone.d):
            rep(cc,rr,get[chk(cc,rr+1)].a[0])
            rep(cc,rr+1,11)
          else:
            rep(cc,rr,12)
        else:
          rep(cc,rr,12)

      elif(cr==14):
        if (chk(cc,rr+1)>-2 and (rr<len(scrn[0])-1)):
          if (get[chk(cc,rr+1)].d<wood.d):
            rep(cc,rr,get[chk(cc,rr+1)].a[0])
            rep(cc,rr+1,13)
            rep(cc,rr-1,get[chk(cc,rr-1)].a[0])
          else:
            rep(cc,rr,15)
        else:
          rep(cc,rr,15)

      elif(cr==16):
        if(chk(cc,rr+1)in{0,1}):
          rep(cc,rr+1,17)
          rep(cc,rr,-1)
        elif(get[chk(cc,rr+1)].d<get[cr].d):
          rep(cc,rr+1,18)
          rep(cc,rr,-1)
        else:
          rep(cc,rr,-1)
          if(get[chk(cc+1,rr+1)].d<get[cr].d):
            rep(cc+1,rr+1,get[chk(cc+1,rr+1)].a[0])
          if(get[chk(cc-1,rr+1)].d<get[cr].d):
            rep(cc-1,rr+1,get[chk(cc-1,rr+1)].a[0])
      elif(cr==18):
#        rep(cc,rr+1,-1)
        if(get[chk(cc+1,rr)].d<get[cr].d):
          rep(cc+1,rr,get[chk(cc+1,rr)].a[0])
        if(get[chk(cc-1,rr)].d<get[cr].d):
          rep(cc-1,rr,get[chk(cc-1,rr)].a[0])
#        print(get[chk(cc-1,rr+1)].d,get[cr].d)
        rep(cc,rr,-1)

      elif (cr==1):
        if ((get[chk(cc,rr+1)].d<sand.d)):
          rep(cc,rr,get[chk(cc,rr+1)].a[0])
          rep(cc,rr+1,2)
        elif (chk(cc+1,rr+1)==0):
          rep(cc+1,rr+1,2)
          rep(cc,rr,-1)
#            UpdateNear(cc,rr,3)
        elif (chk(cc-1,rr+1)==0):
          rep(cc-1,rr+1,2)
          rep(cc,rr,-1)
#            UpdateNear(cc,rr,3)
        else:
          rep(cc,rr,7)

def FillBlank():
  set_color(255,255,255)
  fill_rect(0,0,screenWidth,screenHeight)

def UpdateAllDisplay(scaleX=px,scaleY=py,shiftX=-1,shiftY=-6):
  global scrn
  global cp
  global rp
  cp=-scaleX
  rp=-10
  set_color(air.c1)
  fill_rect(shiftX,shiftY-8,32*scaleX,(scaleY*22+(abs(shiftY)%scaleY)))
  for c in range(0,len(scrn)):
    cp+=scaleX
    for r in range(0,len(scrn[c])):
      cnt=1
      rp+=scaleY
      cr=chk(c,r)
      if cr in {-1,0}: continue
      while ((chk(c,r+1)==cr)and not r >= len(scrn[c])):
        cnt+=1
        r+=1
      set_color(get[cr].c1)
      fill_rect(cp+shiftX,rp+shiftY,scaleX,scaleY*cnt)
    rp=-py

def UpdateMenu(k):
  global menu
  global cp
  global rp
  global pause
  global slc
  global slcm
  global slcs
  global saveSlot

  # run on first frame of pause
  if (pause):
    pause = False
    set_color(40,40,40)
    fill_rect(0,0,400,400)
    set_color(250,250,250)
    for i in range(len(saveSlots)):
      draw_text(20*4*i-1,80,"Save slot "+saveSlots[i])
  cp=-px
  rp=-py
  if (slcm==0):
    if (k in keysAntiClock or k in keysLeft):
      slc-=1
      if (slc==0):
        slc=len(plc)
    elif (k in keysClock or k in keysRight):
      if (slc==len(plc)):      slc=0
      slc+=1
  elif slcm==1:
    if (k in keysClock or k in keysRight):
       slcs+=1
       if (slcs==len(saveSlots)): slcs=0
       saveSlot=saveSlots[slcs]
    elif (k in keysAntiClock or k in keysLeft):
       slcs-=1
       if (slcs==-1): slcs=len(saveSlots)-1
       saveSlot=saveSlots[slcs]
    elif (k in keysLoad or k in keysRefresh):
      Load()
      UpdateAllDisplay(2,2,slcs*20*4,110)
  if k in keysDown:
    slcm = slcm +1
    if (slcm==2): slcm=0
  elif k in keysUp:
    slcm -= 1
    if slcm==-1: slcm=1
  for i in range(len(plc)):
    if(i==slc-1 and slcm==0):
      rep(((i*2)+1),2,-4,1)
      rep(((i*2)+1),0,-4,1)
    else:
      rep(((i*2)+1),2,-5,1)
      rep(((i*2)+1),0,-5,1)
    rep(((i*2)+1),1,plc[i+1],1)
    rep(((i*2)),1,-5,1)
  for i in range(len(plc),16-len(plc)):
    rep(((i+len(plc)-1)+1),1,-5,1)
  for i in range(15): rep(i,4,-5,1)
  rep(0,0,-5,1)
  rep(2,0,-5,1)
  rep(4,0,-5,1)
  for i in range(len(saveSlots)):
    if(i==slcs):
      rep(((i*4)+1),4,-3,1)
      if(slcm==1):
        rep(((i*4)+2),4,-4,1)
        rep((i*4),4,-4,1)
    else: rep(((i*4)+1),4,-1,1)
  for c in range(0,len(menu)):
    cp+=px
    for r in range(0,len(menu[c])):
      rp+=py
      if (chk(c,r,menu)!=0):
        set_color(get[chk(c,r,menu)].c1)
        fill_rect(cp*2,rp*2,px*2,py*2)
        rep(c,r,0,1)
    rp=-py
  set_color(250,250,250)
  draw_text(5,20,str(slc)+": "+plcn[slc])
  set_color(get[chk(c,r,menu)].c1)

def UpdateDisplay():
  global scrn
  global cp
  global rp
  offX=-1
  offY=-6
  cp=-px+offX
  rp=-py+offY
  for c in range(0,len(scrn)):
    cp+=px
    for r in range(0,len(scrn[c])):
      rp+=py
      cr=scrn[c][r]
      if (cr not in ua):
        set_color(get[cr].c1)
        fill_rect(cp,rp,px,py)
    rp=-py+offY

#clear_history()

set_color(air.c1)
fill_rect(0,0,screenWidth,screenHeight)

scrn = CreateMatrix(ceil(screenWidth/px),ceil(screenHeight/py))
menu = CreateMatrix(ceil(screenWidth/(px*2)),ceil(screenHeight/(py*2)))
rep(0,0,-2)

pause=False
paused=False
while True:
  #use_buffer()
  k = get_key()
#  if len(k)>0:print(k)
  if(k in keysPause):
    pause=True
    paused=not paused
  if(not paused):
    UpdateInput(k)
    UpdateData(k)
    UpdateDisplay()
  else:
    UpdateMenu(k)
  paint_buffer()
