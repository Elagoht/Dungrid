#!/usr/bin/python3
import random
import pygame
import pygame.key
import pygame.time
import pygame.image
import pygame.display
from json import loads
from pygame import font
from pygame import mixer
import os
pygame.init()
font.init()
GUIFONT=pygame.font.Font(os.path.join("assets","pixelFont.ttf"),8)
#region Global Variables
gameRun=True
crsX=0
crsY=0
aCrsX=0
aCrsY=0 
select=0
act=0
turn=0
lastSelected=None
actList=[[],[]]
LANGUAGES={
    0:"English",
    1:"Turkce",
    2:"Osmanlica"
}
settings=loads(open(os.path.join("settings.json"),encoding="UTF-8").read())
lang=settings["lang"]
lanText=loads(open(os.path.join("language.json"),encoding="UTF-8").read())
langS=LANGUAGES[lang]
lanText=lanText[langS]
namesModified=lanText["namelist"]
planLog=[]
#region Language Packs
#endregion
#region Asset Loading
icoGame=pygame.image.load(os.path.join("icon.png"))
bgBlackGrass=pygame.image.load(os.path.join("assets","background.png"))
bgGrid=pygame.image.load(os.path.join("assets","grid.png"))
sprGridSelection=pygame.image.load(os.path.join("assets","crs.png"))
sprGridSelected=pygame.image.load(os.path.join("assets","crsOk.png"))
sprGridActionSelect=pygame.image.load(os.path.join("assets","actCrs.png"))
sprGridActionSelectRange=pygame.image.load(os.path.join("assets","actCrsRange.png"))
sprGridActionSelectSup=pygame.image.load(os.path.join("assets","actCrsSup.png"))
sprGridActionSelectSupRange=pygame.image.load(os.path.join("assets","actCrsSupRange.png"))
    #region Actions
actMoveLeft=pygame.image.load(os.path.join("assets","arrowLeft.png"))
actMoveRight=pygame.image.load(os.path.join("assets","arrowRight.png"))
actMoveUp=pygame.image.load(os.path.join("assets","arrowUp.png"))
actMoveDown=pygame.image.load(os.path.join("assets","arrowDown.png"))
actWizard=pygame.image.load(os.path.join("assets","actWizard.png"))
actSupport=pygame.image.load(os.path.join("assets","actSupport.png"))
actWarrior=pygame.image.load(os.path.join("assets","actWarrior.png"))
actArcher=pygame.image.load(os.path.join("assets","actArcher.png"))
actDefense=pygame.image.load(os.path.join("assets","actDefense.png"))
actMove=pygame.image.load(os.path.join("assets","actMove.png"))
actSpecials=pygame.image.load(os.path.join("assets","actSpecials.png"))
    #endregion
sprLvlBadge1=pygame.image.load(os.path.join("assets","lvl1.png"))
sprLvlBadge2=pygame.image.load(os.path.join("assets","lvl2.png"))
sprLvlBadge3=pygame.image.load(os.path.join("assets","lvl3.png"))
    #region Lvl 1
sprNull=pygame.Surface((1,1));sprNull.set_colorkey((0,0,0))
sprArcher0m=pygame.image.load(os.path.join("assets","archer0m.png"))
sprWarrior0m=pygame.image.load(os.path.join("assets","warrior0m.png"))
sprWizard0m=pygame.image.load(os.path.join("assets","wizard0m.png"))
sprSupport0m=pygame.image.load(os.path.join("assets","support0m.png"))
sprArcher0f=pygame.image.load(os.path.join("assets","archer0f.png"))
sprWarrior0f=pygame.image.load(os.path.join("assets","warrior0f.png"))
sprWizard0f=pygame.image.load(os.path.join("assets","wizard0f.png"))
sprSupport0f=pygame.image.load(os.path.join("assets","support0f.png"))
    #endregion
mixer.music.load(os.path.join("assets","bitstep.ogg"))
sfxMenuOk=mixer.Sound(os.path.join("assets","menuOk.ogg"))
sfxMenuMove=mixer.Sound(os.path.join("assets","menuMove.ogg"))
sfxMenuNo=mixer.Sound(os.path.join("assets","menuNo.ogg"))
#endregion
#region CONSTANTS
WINW=480
WINH=270
if settings["debug"]: settings["fullscreen"]=False
if settings["fullscreen"]:
    WIN=pygame.display.set_mode((WINW,WINH),pygame.SCALED|pygame.NOFRAME|pygame.FULLSCREEN)
else:
    WIN=pygame.display.set_mode((WINW,WINH),pygame.SCALED)#|pygame.NOFRAME|pygame.FULLSCREEN)
FPS=30
UNITS=[{
    0:sprNull,
    1:sprArcher0m,
    2:sprWarrior0m,
    3:sprWizard0m,
    4:sprSupport0m
    #5:sprArcher1,
    #6:sprWarrior2,
    #7:sprWizard3,
    #8:sprSupport4
    },{
    0:sprNull,
    1:sprArcher0f,
    2:sprWarrior0f,
    3:sprWizard0f,
    4:sprSupport0f
    #5:sprArcher1,
    #6:sprWarrior2,
    #7:sprWizard3,
    #8:sprSupport4,
    }
]
CLASSES={
    1:lanText["car"],
    2:lanText["cwr"],
    3:lanText["cwz"],
    4:lanText["csp"]
}
ACTS={
    0:actSupport,
    1:actArcher,
    2:actWarrior,
    3:actWizard
}
CURSOR={
    0:sprGridSelection,
    1:sprGridSelected,
    2:sprGridActionSelect,
    3:sprGridActionSelectSup,
    4:sprGridActionSelectRange
}
ACTTYPES={
    "None":sprNull,
    "aMoveRight":actMoveRight,
    "aMoveUp":actMoveUp,
    "aMoveLeft":actMoveLeft,
    "aMoveDown":actMoveDown,
    "aAttack":actWarrior,
    "aDefense":actDefense
}
LVLBADGES={
    1:sprLvlBadge1,
    2:sprLvlBadge2,
    3:sprLvlBadge3,
}
#region Draw Functions
class unit():
    def __init__(self,x:int=0,y:int=0,side:int=0,gender:int=-1,specials:list=[],health:int=10,unitClass:int=0,spr:pygame.Surface=sprNull,isAttacked:bool=False,isDefenced:bool=False,lvl:int=1,actShape:list=[[0,0,0],[0,1,0],[0,0,0]]):
        self.unitClass=unitClass
        if gender==-1: self.gender=random.randrange(0,2)
        else: self.gender=gender
        self.health=health
        self.specials=specials
        self.side=side
        self.color=[(30,150,30),(150,30,30)][self.side]
        self.x=x
        self.y=y
        self.isAttacked=isAttacked
        self.isDefenced=isDefenced
        self.lvl=lvl
        shapes=[[[[0,1,0],[0,0,1],[0,1,0]],
                 [[0,0,0],[1,1,1],[0,0,0]],
                 [[1,0,0],[0,0,1],[1,0,0]],
                 [[1,0,0],[0,1,0],[1,0,0]]],
                [[[0,1,0],[1,0,1],[0,1,0]],
                 [[0,1,1],[0,0,0],[0,1,1]],
                 [[1,0,1],[0,0,0],[1,0,1]],
                 [[1,0,0],[1,0,1],[1,0,0]]],
                [[[0,1,0],[1,1,1],[0,1,0]],
                 [[1,1,0],[1,0,0],[1,1,0]],
                 [[1,0,1],[0,1,0],[1,0,1]],
                 [[0,1,1],[1,0,1],[1,1,0]]]]
        if self.unitClass>0:
            self.actShape=shapes[self.lvl-1][self.unitClass-1]
        else: self.actShape=actShape
        self.name=""
        self.setName("")
    def setName(self,name:str):
        self.spr=UNITS[self.gender][self.unitClass].copy()
        self.spr.blit(LVLBADGES[self.lvl],(0,20))
        if self.unitClass!=0:
            if name=="":
                self.name=namesModified[self.gender].pop(random.randrange(0,len(namesModified[self.gender])))
            else: self.name=name.capitalize()[:7]
            self.nameShadow=GUIFONT.render(self.name,1,(44,44,44))
            self.nameString=GUIFONT.render(self.name,1,self.color)
            self.spr.blit(self.nameShadow,(self.spr.get_rect().center[0]-self.nameString.get_rect().center[0],1))
            self.spr.blit(self.nameString,(self.spr.get_rect().center[0]-self.nameString.get_rect().center[0],0))
    def move(self,direction,x=-1,y=-1,noLog:bool=False):
        global crsX,crsY
        if x<0: x=crsX
        if y<0: y=crsY
        if direction in [">",0,"right","Right","r"]:
            if self.x<len(grid[0])-1:
                self.x+=1
                if noLog==False:
                    actList[turn].append([ACTTYPES["aMoveRight"],x,y,grid[turn][x][y],"rgh"])
                    planLog.append(self.name+lanText["rgh"])
                grid[turn][x+1][y].x-=1
                grid[turn][x][y],grid[turn][x+1][y]=grid[turn][x+1][y],grid[turn][x][y]
                x+=1
                mixer.Sound.play(sfxMenuOk)
                crsY=y%len(grid[0][0])
                crsX=x%len(grid[0])
                return True
            else:
                mixer.Sound.play(sfxMenuNo)
                return False
        if direction in ["^",1,"up","Up","u"]:
            if self.y>0:
                self.y-=1
                if noLog==False:
                    actList[turn].append([ACTTYPES["aMoveUp"],x,y,grid[turn][x][y],"up"])
                    planLog.append(self.name+lanText["up"])
                grid[turn][x][y-1].y+=1
                grid[turn][x][y],grid[turn][x][y-1]=grid[turn][x][y-1],grid[turn][x][y]
                y-=1
                mixer.Sound.play(sfxMenuOk)
                crsY=y%len(grid[0][0])
                crsX=x%len(grid[0])
                return True
            else:
                mixer.Sound.play(sfxMenuNo)
                return False
        if direction in ["<",2,"left","Left","l"]:
            if self.x>0:
                self.x-=1
                if noLog==False:
                    actList[turn].append([ACTTYPES["aMoveLeft"],x,y,grid[turn][x][y],"lft"])
                    planLog.append(self.name+lanText["lft"])
                grid[turn][x-1][y].x+=1
                grid[turn][x][y],grid[turn][x-1][y]=grid[turn][x-1][y],grid[turn][x][y]
                x-=1
                crsY=y%len(grid[0][0])
                crsX=x%len(grid[0])
                mixer.Sound.play(sfxMenuOk)
                return True
            else:
                mixer.Sound.play(sfxMenuNo)
                return False
        if direction in ["v",3,"down","Down","d"]:
            if self.y<len(grid[0][0])-1:
                self.y+=1
                if noLog==False:
                    actList[turn].append([ACTTYPES["aMoveDown"],x,y,grid[turn][x][y],"dwn"])
                    planLog.append(self.name+lanText["dwn"])
                grid[turn][x][y+1].y-=1
                grid[turn][x][y],grid[turn][x][y+1]=grid[turn][x][y+1],grid[turn][x][y]
                y+=1
                crsY=y%len(grid[0][0])
                crsX=x%len(grid[0])
                mixer.Sound.play(sfxMenuOk)
                return True
            else:
                mixer.Sound.play(sfxMenuNo)
                return False
    def die(self):
        self.unitClass=0
        self.spr=sprNull
selectedUnit=unit()
grid=[[[unit() for i in range(5)] for i in range(5)] for i in range(2)]
for s in range(2):
    for x in range(5):
            grid[s][x][x]=unit(x,x,s,unitClass=x%4+1,lvl=x%3+1)
def drawWindow():
    global crsX, crsY, select, selectedUnit
    WIN.blit(bgBlackGrass,(0,0))
    WIN.blit(bgGrid,(10,10))
    WIN.blit(bgGrid,(WINW-176,10))
    for s in range(len(grid)):
        for x in range(len(grid[0])):
            for y in range(len(grid[s][x])):
                WIN.blit(grid[s][x][y].spr,((1 if s==0 else -1)*(17+x*31)+s*452,17+y*31))
    if select==3:
        for row in range(len(lastSelected[0].actShape)):
            for cell in range(len(lastSelected[0].actShape[0])):
                if lastSelected[0].actShape[row][::-1][cell]:
                    if not (crsX==0 and cell==0) and not (crsY==0 and row==0) and not (crsY==len(grid[turn][0])-1 and row==len(lastSelected[0].actShape)-1) and not (crsX==len(grid[turn])-1 and cell==len(lastSelected[0].actShape[0])-1):
                        WIN.blit(sprGridActionSelectSupRange,(((cell-1)*31+crsX*31+10,crsY*31+10+(row-1)*31)))
    if select in [0,1,3]:
        WIN.blit(CURSOR[int(select)],(crsX*31+10,crsY*31+10))
    if select==2:
        for row in range(len(lastSelected[0].actShape)):
            for cell in range(len(lastSelected[0].actShape[0])):
                if lastSelected[0].actShape[row][::-1][cell]:
                    if not (crsX==0 and cell==0) and not (crsY==0 and row==0) and not (crsY==len(grid[turn][0])-1 and row==len(lastSelected[0].actShape)-1) and not (crsX==len(grid[turn])-1 and cell==len(lastSelected[0].actShape[0])-1):
                        WIN.blit(sprGridActionSelectRange,(((428-crsX*31)-(cell-1)*31,crsY*31+10+(row-1)*31)))
        WIN.blit(CURSOR[int(select)],(428-crsX*31,crsY*31+10))
    if select==1:
        if act==0:
            if lastSelected[0].isDefenced==False: WIN.blit(actDefense,(crsX*31+27-17,crsY*31+26))
            if lastSelected[0].isAttacked==False: WIN.blit(ACTS[selectedUnit.unitClass%len(ACTS)],(crsX*31+27,crsY*31+26-17))
            WIN.blit(actMove,(crsX*31+27,crsY*31+26+17))
            WIN.blit(actSpecials,(crsX*31+27+17,crsY*31+26))
        if act==1:
            if selectedUnit.x<len(grid[0])-1: WIN.blit(actMoveRight,(crsX*31+27+17,crsY*31+27))
            if selectedUnit.x>0: WIN.blit(actMoveLeft,(crsX*31+27-17,crsY*31+27))
            if selectedUnit.y<len(grid[0][0])-1: WIN.blit(actMoveDown,(crsX*31+27,crsY*31+27+17))
            if selectedUnit.y>0: WIN.blit(actMoveUp,(crsX*31+27,crsY*31+27-17))
    for i in range(len(actList[turn])):
        WIN.blit(actList[turn][i][0],(10,WINH-65+(i+1)*10))
    for i in range(len(planLog)):
        planLogs=GUIFONT.render(planLog[:5][i],0,(255,255,255))
        WIN.blit(planLogs,(20,WINH-65+(i+1)*10))
    if selectedUnit.unitClass!=0:
        selectedUnitData=[
            lanText["nme"]+selectedUnit.name,
            lanText["cls"]+CLASSES[selectedUnit.unitClass],
            lanText["hlt"]+str(selectedUnit.health),
            lanText["crd"]+f"({selectedUnit.x},{selectedUnit.y})",
            lanText["sex"]+[lanText["man"],lanText["wmn"]][selectedUnit.gender],
        ]
        for i in range(len(selectedUnitData)):
            selectedUnitInfo=GUIFONT.render(selectedUnitData[i],0,(255,255,255))
            WIN.blit(selectedUnitInfo,(WINW/2-selectedUnitInfo.get_rect().center[0],WINH/2-selectedUnitInfo.get_rect().center[1]*len(selectedUnitData)+i*9))
    pygame.display.update()
#endregion
#region Control Functions
def isCursorMoved(event):
    if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT or event.key==pygame.K_DOWN or event.key==pygame.K_UP:
        return True
    else: return False
def cursorMovement(event):
    global crsX,crsY,select,lastSelected
    if select in [0,2,3]:
        crsX+=(-1 if select==2 else 1)*(int(event.key==pygame.K_RIGHT)-int(event.key==pygame.K_LEFT))
        crsY+=int(event.key==pygame.K_DOWN)-int(event.key==pygame.K_UP)
        if isCursorMoved(event): mixer.Sound.play(sfxMenuMove)
    crsX=crsX%len(grid[0])
    crsY=crsY%len(grid[0][0])
    if event.key==pygame.K_SPACE:
        if grid[turn][crsX][crsY].unitClass>0:
            if len(actList[turn])<5:
                if select==0:
                    mixer.Sound.play(sfxMenuOk)
                    select=1
                    lastSelected=[selectedUnit,selectedUnit.x,selectedUnit.y]
                elif select==1: select=0
            else: mixer.Sound.play(sfxMenuNo)
        elif select==0: mixer.Sound.play(sfxMenuNo)
def unDo():
    global select
    data=actList[turn][-1][1:]
    xx=data[0]
    yy=data[1]
    obj=data[2]
    act=data[3]
    del planLog[-1]
    del actList[turn][-1]
    if act=="rgh": grid[turn][xx+1][yy].move("<",xx+1,yy,noLog=1)
    if act=="up" : grid[turn][xx][yy-1].move("v",xx,yy-1,noLog=1)
    if act=="lft": grid[turn][xx-1][yy].move(">",xx-1,yy,noLog=1)
    if act=="dwn": grid[turn][xx][yy+1].move("^",xx,yy+1,noLog=1)
    if act=="atk": grid[turn][xx][yy].isAttacked=False
    if act=="ahl": grid[turn][xx][yy].isAttacked=False
    if act=="dfc": grid[turn][xx][yy].isDefenced=False
    print(grid[turn][xx][yy].name)
    select=0
def actionSelection(event):
    global act,select,selectedUnit,lastSelected
    if select==1:
        if len(actList[turn])<5 and act==0:
            if event.key==pygame.K_w:
                if lastSelected[0].isAttacked==False:
                    if selectedUnit.unitClass!=4: select=2
                    else: select=3
                    mixer.Sound.play(sfxMenuOk)
                else: mixer.Sound.play(sfxMenuNo)
            elif event.key==pygame.K_a:
                if lastSelected[0].isDefenced==False:
                    actList[turn].append([ACTTYPES["aDefense"],lastSelected[1],lastSelected[2],grid[turn][crsX][crsY],"dfc"])
                    planLog.append(selectedUnit.name+lanText["dfc"])
                    lastSelected[0].isDefenced=True
                    mixer.Sound.play(sfxMenuOk)
                    select=0
                else: mixer.Sound.play(sfxMenuNo)
            elif event.key==pygame.K_s:
                mixer.Sound.play(sfxMenuOk)
                act=1
            elif event.key==pygame.K_d:
                selectedUnit.die()
                select=0
        if act==1:
            if event.key==pygame.K_UP:
                if selectedUnit.move("^"): select=0
            if event.key==pygame.K_DOWN:
                if selectedUnit.move("v"): select=0
            if event.key==pygame.K_LEFT:
                if selectedUnit.move("<"): select=0
            if event.key==pygame.K_RIGHT:
                if selectedUnit.move(">"): select=0
    if select==2:
        if event.key==pygame.K_SPACE:
            planLog.append(lastSelected[0].name+lanText["atk"].format(chr(len(grid[turn])-crsX+64)+str(crsY+1)))
            actList[turn].append([ACTS[lastSelected[0].unitClass%len(ACTS)],lastSelected[1],lastSelected[2],grid[turn][crsX][crsY],"atk"])
            lastSelected[0].isAttacked=True
            select=0
    if select==3:
        if event.key==pygame.K_SPACE:
                planLog.append(lastSelected[0].name+lanText["ahl"].format(chr(len(grid[turn])-crsX+64)+str(crsY+1)))
                actList[turn].append([ACTS[lastSelected[0].unitClass%len(ACTS)],lastSelected[1],lastSelected[2],grid[turn][crsX][crsY],"ahl"])
                lastSelected[0].isAttacked=True
                select=0
    if event.key==pygame.K_BACKSPACE and len(actList[turn])>0: unDo()
    if event.key==pygame.K_SPACE: act=0
#endregion#region Game Managament Functions
def gameQuit(reason="No Reason"):
    print("Quit Reason:",reason)
    global gameRun
    gameRun=False
#endregion
#region Game Loop
def gameLoop():
    global gameRun,selectedUnit
    clock=pygame.time.Clock()
    clock.tick(FPS)
    while gameRun:
        #region Event Loop
        selectedUnit=grid[turn][crsX][crsY]
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameRun=False
            keysPressed=pygame.key.get_pressed()
            if event.type==pygame.KEYDOWN:
                cursorMovement(event)
                actionSelection(event)
                if event.key==pygame.K_F4:
                    if keysPressed[pygame.K_LALT]:
                        gameQuit("\"Alt+F4\" shortcut pressed.")
        #endregion
        #region Function Calls
        drawWindow()
        #endregion
#endregion
#region Run Game
if __name__=="__main__":
    pygame.init()
    pygame.display.set_icon(icoGame)
    pygame.display.set_caption("Dungrid - A Grid Based Roguelike Dungen Game - Also Try Sudo Mice!")
    mixer.music.play(-1)
    mixer.music.set_volume(.5)
    gameLoop()
    pygame.quit()
#endregion