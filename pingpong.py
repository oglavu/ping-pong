import pygame as pg
import time
from random import randint
from threading import Thread
from os import path

Path = path.dirname(path.abspath(__file__))

pg.init()

run=True
new_round_pause = True
main_menu = True
first_time = True

powerup = False
is_pause = False
winning = False

#importing images
icon = pg.image.load(path.join(Path,"images","icon.ico"))
active_btn = pg.image.load(path.join(Path,"images","active_btn.png"))
trofej = pg.image.load(path.join(Path,"images","trofej.png"))

a_online = pg.image.load(path.join(Path,"images","a_online.png"))
p_online = pg.image.load(path.join(Path,"images","p_online.png"))

a_mm = pg.image.load(path.join(Path,"images","a_mm.png"))
p_mm = pg.image.load(path.join(Path,"images","p_mm.png"))

a_re = pg.image.load(path.join(Path,"images","a_re.png"))
p_re = pg.image.load(path.join(Path,"images","p_re.png"))

a_single = pg.image.load(path.join(Path,"images","a_single.png"))
p_single = pg.image.load(path.join(Path,"images","p_single.png"))

a_multi = pg.image.load(path.join(Path,"images","a_multi.png"))
p_multi = pg.image.load(path.join(Path,"images","p_multi.png"))

active_p = pg.image.load(path.join(Path,"images","active_p.png"))
passive_p = pg.image.load(path.join(Path,"images","passive_p.png"))

active_wall = pg.image.load(path.join(Path,"images","active_wall.png"))
passive_wall = pg.image.load(path.join(Path,"images","passive_wall.png"))

active_big = pg.image.load(path.join(Path,"images","active_big.png"))
passive_big = pg.image.load(path.join(Path,"images","passive_big.png"))

active_slow = pg.image.load(path.join(Path,"images","active_slowness.png"))
passive_slow = pg.image.load(path.join(Path,"images","passive_slowness.png"))


HEIGHT,WIDTH = 480,940
R_HEIGHT,R_WIDTH = 100,20
P_WIDTH = 150
RADIUS=10
LINE_WIDTH=5
DISTANCE = 70
FPS=60

#fonts
FONT=pg.font.SysFont("comicsansms",45)
BIGGER_FONT = pg.font.SysFont("comicsansms",55)
press = pg.font.SysFont("comicsansms",30)
welcome = pg.font.SysFont("comicsansms",130)

win = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("PING PONG")
pg.display.set_icon(icon)

#colours
white = (255,255,255)
black = (0,0,0)

#velocities of rackets by x,y axis
difficulty=1
previous_diff = difficulty
vel_1,vel_2 = 6,6
vel_x,vel_y = randint(1,4),randint(1,4)

#text rendering
PING = welcome.render("PING PONG",1,white)
win1 = press.render("PLAYER 1 HAS WON!",1,white)
win2 = press.render("PLAYER 2 HAS WON!",1,white)
bili = press.render("nisam bili gej brate",1,white)

#timer
time_="00:00"
clock = FONT.render(time_,1,black)

def hardening():
    global difficulty, time_
    secounds,minuts = 0,0
    difficulty = 1
    while run:
        if new_round_pause:
            secounds,minuts = 0,0
            difficulty = 1
            time.sleep(2)
            
        while is_pause:
            pass
        while winning:
            secounds,minuts = 0,0
        
        time.sleep(0.9)
        secounds +=1
        
        if secounds<10:
            secound="0"+str(secounds)
        elif secounds<60:
            secound=str(secounds)
        else:
            secounds=0
            secound="00"
            minuts +=1
            
        if minuts<10:
            minut="0"+str(minuts)
        elif minutes<60:
            minut=str(minuts)

        if secounds == 30:
            difficulty *= 2
        elif secounds == 0 and minuts == 1:
            difficulty = int(difficulty*1.5)

        time_=minut+":"+secound

timer = Thread(target = hardening)
timer.start()

class Ball:
    def __init__(self,x,y,radius,vel_x,vel_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel_x = vel_x
        self.vel_y = vel_y
    def draw(self,x,y,radius,win):
        pg.draw.circle(win,black,(x,y),radius)

class Racket:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.height = height
    def draw(self,win,x,y,width,height):
        pg.draw.rect(win,black,(x,y,width,height))

class Button:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
    def blitting(self,win,x,y,image):
        win.blit((image),(x,y))
    def isOver(self,pos):
        if self.x < pos[0] < self.x + self.image.get_size()[0] and self.y < pos[1] < self.y + self.image.get_size()[1]:
            return True
        else:
            return False
        
#Classes
pause_btn = Button(WIDTH//2-active_btn.get_size()[0]//2,HEIGHT//2-active_btn.get_size()[1]//2,active_p)

dugme_r1_1 = Button(20,30,active_wall)
dugme_r1_2 = Button(20,60+active_btn.get_size()[1],active_big)
dugme_r1_3 = Button(20,90+2*active_btn.get_size()[1],active_slow)

dugme_r2_1 = Button(20+WIDTH-P_WIDTH,30,active_wall)
dugme_r2_2 = Button(20+WIDTH-P_WIDTH,60+active_btn.get_size()[1],active_big)
dugme_r2_3 = Button(20+WIDTH-P_WIDTH,90+2*active_btn.get_size()[1],active_slow)

single_btn = Button((WIDTH-a_single.get_size()[0])//2,PING.get_size()[1]+20,a_single)
multi_btn = Button((WIDTH-a_multi.get_size()[0])//2,single_btn.y+20+single_btn.image.get_height(),a_multi)
online_btn = Button((WIDTH-a_online.get_size()[0])//2,multi_btn.y+20+multi_btn.image.get_height(),a_online)

mm_btn = Button(WIDTH//2+10,20+30+trofej.get_height()+win1.get_height(),a_mm)
re_btn = Button(WIDTH//2-10-a_re.get_width(),20+30+trofej.get_height()+win1.get_height(),a_re)


lopta=Ball(WIDTH//2,HEIGHT//2,RADIUS,vel_x,vel_y)
reket1=Racket(10+P_WIDTH,(HEIGHT-R_HEIGHT)//2,R_WIDTH,R_HEIGHT)
reket2=Racket(WIDTH-R_WIDTH-P_WIDTH-10,(HEIGHT-R_HEIGHT)//2,R_WIDTH,R_HEIGHT)

#pause menu
def pause():
    global is_pause, t
    tx = time.time()
    is_pause = True
    run = True
    fade(0,151,1)
        
    while run: #waiting for pause end
        fps.tick(FPS)
        pos = pg.mouse.get_pos()
        Redraw(win)
        
        pause_surf = pg.Surface((WIDTH,HEIGHT))
        pause_surf.fill(black)
        pause_surf.set_alpha(150)
        win.blit((pause_surf),(0,0))
        
        pause_btn.blitting(win,pause_btn.x,pause_btn.y,pause_btn.image)

        press_r = press.render("Press R to resume",1,white)
        win.blit((press_r),((WIDTH-press_r.get_size()[0])//2,(HEIGHT+active_btn.get_size()[1])//2+10))
        
        if pause_btn.isOver(pos): # image changing
            pause_btn.image = passive_p
        else:
            pause_btn.image = active_p

        for event in pg.event.get(): #event collector
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    run = False
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
            elif event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if pause_btn.isOver(pos):
                    run = False
        
        pg.display.update()
        
    fade(151,0,-1)

    ty = time.time()
    t= ty-tx
    is_pause = False

def main_screen(win):
    win.fill(black)

    win.blit((PING),((WIDTH-PING.get_size()[0])//2,20))
    win.blit((single_btn.image),(single_btn.x,single_btn.y))
    win.blit((multi_btn.image),(multi_btn.x,multi_btn.y))
    win.blit((online_btn.image),(online_btn.x,online_btn.y))

def powerup_activator():
    global used_powerups,t1,powerup
    dugme_r1_1.image = active_wall
    dugme_r2_1.image = active_wall

    dugme_r1_2.image = active_big
    dugme_r2_2.image = active_big

    dugme_r1_3.image = active_slow
    dugme_r2_3.image = active_slow

    used_powerups =[6]
    t0 = time.time()-20
    powerup = False

    Redraw(win)
    pg.display.update()

#online
def online():
    pass

def single():
    single_game = True
    
    surf = pg.Surface((WIDTH,HEIGHT))
    surf.fill(black)
    for alpha in range(0,300):
        surf.set_alpha(alpha)
        win.fill(black)

        win.blit((PING),((WIDTH-PING.get_size()[0])//2,20))
        win.blit((single_btn.image),(single_btn.x,single_btn.y))
        win.blit((multi_btn.image),(multi_btn.x,multi_btn.y))
        win.blit((online_btn.image),(online_btn.x,online_btn.y))
        win.blit((surf),(0,0))
        pg.display.update()
        pg.time.delay(5)

    for alpha in range(300,0,-1):
        surf.set_alpha(alpha)
        win.blit((bili),((WIDTH-bili.get_width())//2,(HEIGHT-bili.get_height())//2))
        win.blit((mm_btn.image),((WIDTH-mm_btn.image.get_width())//2,HEIGHT//2+mm_btn.image.get_height()+30))
        win.blit((surf),(0,0))
        pg.display.update()
        pg.time.delay(5)
        
    while single_game:
        pos = pg.mouse.get_pos()
        fps.tick(FPS)
        win.fill(black)
        if mm_btn.isOver(pos):
            mm_btn.image = p_mm
        else:
            mm_btn.image = a_mm
        win.blit((bili),(WIDTH//2-bili.get_width()//2,HEIGHT//2-bili.get_height()//2))
        win.blit((mm_btn.image),((WIDTH-mm_btn.image.get_width())//2,HEIGHT//2+mm_btn.image.get_height()+30))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                winning = False
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if mm_btn.isOver(pos):
                    single_game = False
                    main_screen = True
                    first_time = True
                
        pg.display.update()

def won():
    global winning,main_menu,score1,score2,first_time,new_round_pause
    global wall_1_list,wall_2_list,big_1_list,big_2_list,slow_1_list,slow_2_list #globals for powerups
    global vel_x,vel_y
    fade(0,151,1)
    winning = True
    while winning:
        pos = pg.mouse.get_pos()
        Redraw(win)
        pause_surf = pg.Surface((WIDTH,HEIGHT))
        pause_surf.fill(black)
        pause_surf.set_alpha(150)
        win.blit((pause_surf),(0,0))

        re_btn.blitting(win,re_btn.x,re_btn.y,re_btn.image)
        mm_btn.blitting(win,mm_btn.x,mm_btn.y,mm_btn.image)
        win.blit((trofej),(WIDTH//2-trofej.get_width()//2,30))

        if score1 == 5:
            win.blit((win1),(WIDTH//2-win1.get_width()//2,trofej.get_height()+30))
        elif score2 == 5:
            win.blit((win1),(WIDTH//2-win1.get_width()//2,trofej.get_height()+30))

        if re_btn.isOver(pos):
            re_btn.image = p_re
        else:
            re_btn.image = a_re

        if mm_btn.isOver(pos):
            mm_btn.image = p_mm
        else:
            mm_btn.image = a_mm
            

        for event in pg.event.get():
            if event.type == pg.QUIT:
                winning = False
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if mm_btn.isOver(pos):
                    main_menu = True
                    winning = False
                    first_time = True
                    new_round_pause = True
                    
                    wall_1_list = [False]
                    wall_2_list = [False]

                    big_1_list = [False]
                    big_2_list = [False]

                    slow_1_list = [False]
                    slow_2_list = [False]
                    
                    powerup_activator()
                    score1,score2 = 0,0
                elif re_btn.isOver(pos):
                    winning = False
                    new_round_pause = True

                    wall_1_list = [False]
                    wall_2_list = [False]
                    
                    big_1_list = [False]
                    big_2_list = [False]

                    slow_1_list = [False]
                    slow_2_list = [False]
                    
                    powerup_activator()
                    score1,score2 = 0,0
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
        pg.display.update()
    fade(151,301,1)
        

def wall_draw():
    if wall_1_list[-1]:
        pg.draw.rect(win,black,(reket1.x+R_WIDTH+DISTANCE,0,R_WIDTH,HEIGHT))
    if wall_2_list[-1]:
        pg.draw.rect(win,black,(reket2.x-R_WIDTH-DISTANCE,0,R_WIDTH,HEIGHT))

def fade(a,b,c):
    fade_surf = pg.Surface((WIDTH,HEIGHT))
    fade_surf.fill(black)
    for alpha in range(a,b,c):
        fade_surf.set_alpha(alpha)
        Redraw(win)
        win.blit((fade_surf),(0,0))
        pg.display.update()
        pg.time.delay(5)


def move(x,y,vel_x,vel_y):
    lopta.x = x+vel_x
    lopta.y = y+vel_y
    

def Redraw(win):
    win.fill(white)
    lopta.draw(lopta.x,lopta.y,lopta.radius,win)
    win.blit((score),((WIDTH-score.get_width())//2,10))

    pg.draw.rect(win,white,(0,0,P_WIDTH,HEIGHT))
    pg.draw.rect(win,white,(WIDTH-P_WIDTH,0,P_WIDTH,HEIGHT))
    
    clock = FONT.render(time_,1,black)
    win.blit((clock),((WIDTH-clock.get_width())//2,HEIGHT-clock.get_height()-10))

    reket1.draw(win,reket1.x,reket1.y,R_WIDTH,reket1.height)
    reket2.draw(win,reket2.x,reket2.y,R_WIDTH,reket2.height)

    #walls
    pg.draw.line(win,black,[0,0],[WIDTH,0],LINE_WIDTH)
    pg.draw.line(win,black,[0,HEIGHT],[WIDTH,HEIGHT],LINE_WIDTH)

    #powerup wall
    wall_draw()

    #lines
    pg.draw.line(win,black,[P_WIDTH,0],[P_WIDTH,HEIGHT],LINE_WIDTH) #left goal
    pg.draw.line(win,black,[WIDTH-P_WIDTH,0],[WIDTH-P_WIDTH,HEIGHT],LINE_WIDTH)#right goal
    pg.draw.line(win,black,[WIDTH//2,0],[WIDTH//2,HEIGHT]) #mid line

    #buttons
    for button in powerups_list:
        button.blitting(win,button.x,button.y,button.image)
        
    #pg.draw.line(win,black,[0,240],[640,240])

#event lists
event_1_up = [False]
event_1_down = [False]
event_2_up = [False]
event_2_down = [False]
used_powerups = [6]

#powerup list
wall_1_list = [False]
wall_2_list = [False]

big_1_list = [False]
big_2_list = [False]

slow_1_list = [False]
slow_2_list = [False]

powerups_list = [dugme_r1_1,dugme_r1_2,dugme_r1_3,dugme_r2_1,dugme_r2_2,dugme_r2_3]

score1 = 0
score2 = 0
t1 = time.time()
t = 0

fps = pg.time.Clock()


while run:
    fps.tick(FPS)
    score = FONT.render((str(score1)+":"+str(score2)),1,black)
    pos = pg.mouse.get_pos()
    
    while main_menu:
        pos = pg.mouse.get_pos()
        if first_time:
            surf = pg.Surface((WIDTH,HEIGHT))
            surf.fill(black)
            for alpha in range(300,0,-1):
                surf.set_alpha(alpha)
                main_screen(win)
                win.blit((surf),(0,0))
                pg.display.update()
                pg.time.delay(5)
            first_time = False
        
        if single_btn.isOver(pos):
            single_btn.image = p_single
        else:
            single_btn.image = a_single
        
        if multi_btn.isOver(pos):
            multi_btn.image = p_multi
        else:
            multi_btn.image = a_multi
        
        if online_btn.isOver(pos):
            online_btn.image = p_online
        else:
            online_btn.image = a_online

        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
            elif event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if single_btn.isOver(pos):
                    single()
                elif multi_btn.isOver(pos):
                    main_menu = False
                elif online_btn.isOver(pos):
                    single()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()

        main_screen(win)

        pg.display.update()

    
    if new_round_pause:
        fade(300,0,-1)
        
        #preparing for next round... :/
        Redraw(win)
        ready = FONT.render("3",1,white)
        ready_ = BIGGER_FONT.render("3",1,black)
        win.blit((ready_),((WIDTH-ready_.get_width())//2,(HEIGHT-ready_.get_height())//2))
        win.blit((ready),((WIDTH-ready.get_width())//2,(HEIGHT-ready.get_height())//2))
        pg.display.update()

        time.sleep(0.9)
        Redraw(win)
        steady = FONT.render("2",1,white)
        steady_ = BIGGER_FONT.render("2",1,black)
        win.blit((steady_),((WIDTH-steady_.get_width())//2,(HEIGHT-steady_.get_height())//2))
        win.blit((steady),((WIDTH-steady.get_width())//2,(HEIGHT-steady.get_height())//2))
        pg.display.update()

        time.sleep(0.9)
        Redraw(win)
        go = FONT.render("1",1,white)
        go_ = BIGGER_FONT.render("1",1,black)
        win.blit((go_),((WIDTH-go_.get_width())//2,(HEIGHT-go_.get_height())//2))
        win.blit((go),((WIDTH-go.get_width())//2,(HEIGHT-go.get_height())//2))
        pg.display.update()

        time.sleep(0.9)
        Redraw(win)
        gogo = FONT.render("GO",1,white)
        gogo_ = BIGGER_FONT.render("GO",1,black)
        win.blit((gogo_),((WIDTH-gogo_.get_width())//2,(HEIGHT-gogo_.get_height())//2))
        win.blit((gogo),((WIDTH-gogo.get_width())//2,(HEIGHT-gogo.get_height())//2))
        pg.display.update()
        time.sleep(0.25)

        vel_x,vel_y = randint(1,4),randint(1,4)
        lopta.vel_x,lopta.vel_y = vel_x,vel_y

        new_round_pause = False

    #collision of walls and ball
    if lopta.y+lopta.radius >= HEIGHT:
        vel_y = -vel_y
    elif lopta.y-lopta.radius <= 0:
        vel_y = -vel_y

    #collision of ball and summoned walls
    t1 = time.time()
    if wall_1_list[-1]:
        if lopta.x-lopta.radius <= reket1.x+DISTANCE+2*R_WIDTH and t1-t_wall_1 <= 15+t:
            vel_x = -vel_x
        elif t1-t_wall_1 > 15+t:
            wall_1_list.append(False)
    if wall_2_list[-1]:
        if lopta.x+lopta.radius >= reket2.x-DISTANCE-R_WIDTH and t1-t_wall_2 <= 15+t:
            vel_x = -vel_x
        elif t1-t_wall_2 > 15+t:
            wall_2_list.append(False)



    #collision of rackets and ball
    if lopta.x > P_WIDTH and lopta.x < WIDTH-P_WIDTH:
        if lopta.x- lopta.radius <= reket1.x+R_WIDTH and reket1.y<lopta.y<(reket1.y+reket1.height):
            vel_x = -vel_x
        if lopta.x+lopta.radius >= reket2.x and reket2.y<lopta.y<(reket2.y+reket2.height):
            vel_x = -vel_x
    else:
        #new round
        if lopta.x <= P_WIDTH:
            score2 +=1
        elif lopta.x >= WIDTH-P_WIDTH:
            score1 +=1
        
        if score1 == 5 or score2 == 5:
            score = FONT.render((str(score1)+":"+str(score2)),1,black)
            Redraw(win)
            pg.display.update()
            won()
            
        else:
            t=0
            fade(0,300,1)

            if difficulty == 2:
                vel_x,vel_y = vel_x//2,vel_y//2
                lopta.vel_x,lopta.vel_y = vel_x,vel_y
                difficulty = 1
                previous_diff = 1

            elif difficulty == 3:
                vel_x,vel_y = vel_x//3,vel_y//3
                lopta.vel_x,lopta.vel_y = vel_x,vel_y
                difficulty = 1
                previous_diff = 1

            new_round_pause = True
            
        lopta.x,lopta.y = WIDTH//2,HEIGHT//2
        reket1.x,reket1.y = 10+P_WIDTH,(HEIGHT-R_HEIGHT)//2
        reket2.x,reket2.y = WIDTH-R_WIDTH-P_WIDTH-10,(HEIGHT-R_HEIGHT)//2
            

    #collision of rackets and walls
    if reket1.y <= 0:
        reket1.y = 0
    elif reket1.y+reket1.height >= HEIGHT:
        reket1.y = HEIGHT-reket1.height
    
    if reket2.y <= 0:
        reket2.y = 0
    elif reket2.y+reket2.height >= HEIGHT:
        reket2.y = HEIGHT-reket2.height

    #big racket and slowness powerups
    if big_1_list[-1]:
        if reket1.height != 3*R_HEIGHT and t1-t_big_1 < 15+t:
            reket1.height = 3*R_HEIGHT
        elif t1-t_big_1 >= 15+t:
            reket1.height = R_HEIGHT
            big_1_list.append(False)

    if big_2_list[-1]:
        if reket2.height != 3*R_HEIGHT and t1-t_big_2 < 15+t:
            reket2.height = 3*R_HEIGHT
        elif t1-t_big_2 >= 15+t:
            reket2.height = R_HEIGHT
            big_2_list.append(False)

    if slow_1_list[-1]:
        if abs(lopta.vel_x) == abs(vel_x) and abs(lopta.vel_y) == abs(vel_y) and t1-t_slow_1 < 15+t:
            if vel_x != 1:
                vel_x = vel_x//2
            if vel_y != 1:
                vel_y = vel_y//2
        elif t1-t_slow_1 >= 15+t:
            if vel_x > 0:
                vel_x = lopta.vel_x
            else:
                vel_x = -lopta.vel_x

            if vel_y > 0:
                vel_y = lopta.vel_x
            else:
                vel_y = -lopta.vel_x
            slow_1_list.append(False)

    if slow_2_list[-1]:
        if abs(lopta.vel_x) == abs(vel_x) and abs(lopta.vel_y) == abs(vel_y) and t1-t_slow_2 < 15+t:
            if vel_x != 1:
                vel_x = vel_x//2
            if vel_y != 1:
                vel_y = vel_y//2
        elif t1-t_slow_2 >= 15+t:
            if vel_x > 0:
                vel_x = lopta.vel_x
            else:
                vel_x = -lopta.vel_x

            if vel_y > 0:
                vel_y = lopta.vel_x
            else:
                vel_y = -lopta.vel_x
                
            slow_2_list.append(False)


    #event collector
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run=False
            pg.quit()
            
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run=False
                timer.join()
                pg.quit()

            #movement collector 
            if event.key == pg.K_w:
                event_1_up.append(True)
            elif event.key == pg.K_s:
                event_1_down.append(True)
            elif event.key == pg.K_UP:
                event_2_up.append(True)
            elif event.key == pg.K_DOWN:
                event_2_down.append(True)

            #power ups collecting
            #racket1
            elif event.key == pg.K_e:
                if not True in wall_1_list:
                    dugme_r1_1.image = passive_wall
                    wall_1_list.append(True)
                    if reket1.x+DISTANCE+2*R_WIDTH>=lopta.x>DISTANCE+reket1.x+R_WIDTH:
                        lopta.x,lopta.y = WIDTH//2,HEIGHT//2
                    t_wall_1 = time.time()
            elif event.key == pg.K_r:
                if not True in big_1_list:
                    dugme_r1_2.image = passive_big
                    big_1_list.append(True)
                    t_big_1 = time.time()
            elif event.key == pg.K_t:
                if not True in slow_1_list:
                    dugme_r1_3.image = passive_slow
                    slow_1_list.append(True)
                    t_slow_1 = time.time()
            #racket2
            elif event.key == pg.K_b:
                if "b" not in used_powerups:
                    if not True in wall_2_list:
                        dugme_r2_1.image = passive_wall
                        wall_2_list.append(True)
                        if reket2.x-DISTANCE >= lopta.x > reket2.x-DISTANCE-R_WIDTH:
                            lopta.x,lopta.y = WIDTH//2,HEIGHT//2
                        t_wall_2 = time.time()
            elif event.key == pg.K_n:
                if not True in big_2_list:
                    dugme_r2_2.image = passive_big
                    big_2_list.append(True)
                    t_big_2 = time.time()
            elif event.key == pg.K_m:
                if not True in slow_2_list:
                    dugme_r2_3.image = passive_slow
                    slow_2_list.append(True)
                    t_slow_2 = time.time()
            elif event.key == pg.K_p:
                pause()

        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                event_1_up.append(False)
            elif event.key == pg.K_s:
                event_1_down.append(False)
            elif event.key == pg.K_UP:
                event_2_up.append(False)
            elif event.key == pg.K_DOWN:
                event_2_down.append(False)
                
    #moving
    if difficulty != previous_diff:
        vel_x,vel_y = int(vel_x*difficulty),int(vel_y*difficulty)
        lopta.vel_x,lopta.vel_y = int(lopta.vel_x*difficulty),int(lopta.vel_y*difficulty)
        previous_diff = difficulty
    
    move(lopta.x,lopta.y,vel_x,vel_y)
    
    if event_1_up[-1]:
        reket1.y = reket1.y - vel_1
    elif event_1_down[-1]:
        reket1.y = reket1.y + vel_1
    if event_2_up[-1]:
        reket2.y = reket2.y - vel_2
    elif event_2_down[-1]:
        reket2.y = reket2.y + vel_2


    Redraw(win)
    
    pg.display.update()


