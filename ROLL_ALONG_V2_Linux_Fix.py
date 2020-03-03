#!/usr/bin/env python
# coding: utf-8

# In[1]:

#Author: Daniel Kulik

import random, os, glob, time, sys
import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

HEIGHT = 650
WIDTH = 1200

radius = 10
running = False
paused = False

rt_change = False

x = 10
y = 10
maze = []
streamers_x = []
streamers_y = []
skill = 8
runs = 0
current = 0
volume = 0.15

cursor = 0
blank = False
silent = False
schoice = 0
cx1 = 35
cx2 = 20
cy1 = 110
cy2 = 95

FONT1 = pygame.font.SysFont("comicsansms", 35)
FONT2 = pygame.font.SysFont("arial", 25)
FONT3 = pygame.font.SysFont("timesnewroman", 30)

try:
    folder =  os.path.abspath(os.path.join(__file__, "../"))
except:
    folder = os.path.join(os.path.dirname(sys.argv[0]), "")
    
gsfold = os.path.join(folder, 'Game_Stats/')

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Roll Along!")

def get_platform():
    platforms = {
        'linux' : 'Linux',
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows',
        'mysys' : 'Windows/MSYS2',
        'cygwin' : 'Windows/Cygwin',
        'os2' : 'OS/2',
        'os2emx' : 'OS/2 EMX',
        'riscos' : 'RiscOS',
        'atheos' : 'AtheOS',
        'freebsd7' : 'FreeBSD 7',
        'freebsd8' : 'FreeBSD 8',
        'freebsdN' : 'FreeBSD N',
        'openbsd6' : 'OpenBSD 6' 
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

platform = get_platform()
if (platform=='Linux') or (platform=='OS X'):
    rm_music = True
    import webbrowser, subprocess
    try:
        import psutil
    except:
        try:
            subprocess.call([sys.executable, "-m", "pip3", "install", "--user", 'psutil'])
            import psutil
        except:
            subprocess.call([sys.executable, "-m", "pip", "install", "--user", 'psutil'])
            import psutil
    if (platform=='Linux'):
        try:
        
            import gi
            gi.require_version('Wnck','3.0')
            from gi.repository import Wnck
        except:
            print("Please install software using 'sudo apt-get install python3-gi gir1.2-wnck-3.0' or other install method for these packages")
    else:
        print("Manually minimize default music player if opened with f-key")
else:
    rm_music = False

def alt_player(p,wait,songs,loaded,load):
    
    tic = time.time()
    
    load_new = p.io_counters()

    if load_new[1]>=(load+2):
        r = 1
    else:
        r = 0

    load = load_new[1]
    loaded.append(r)
    
    if (len(loaded)>10):
    
        loaded.pop(0)

        if (sum(loaded)<1):
            
            songs = random.sample(songs,len(songs))

            try:
                p.terminate()
            except:
                pass
            
            for i in range(len(songs)):
                webbrowser.open(str(songs[i]))
            finder = []

            loaded.append(1)
            loaded.append(1)
            time.sleep(0.5)

            for proc in psutil.process_iter(['pid', 'name']):
                finder.append(proc.info)

            open_ls = finder[-(len(songs)-1):]

            for i in range(len(open_ls)):
                d = open_ls[i]
                pid = d['pid']
                p = psutil.Process(pid)
                usage = p.cpu_percent(interval=0.3)
                if usage>=1:
                    break
            try:
                screen=Wnck.Screen.get_default()
                screen.force_update()
                windows=screen.get_windows() 
                for w in windows:
                    if str(w.get_name()).endswith(('.mp3', 'wav', 'ogg')):
                        w.minimize()
            except:
                pass

    toc = time.time()
    rest = toc-tic
    wait_new = int(wait - rest*2000)
    if wait_new<0:
        wait_new = 0   
    return p,wait_new,loaded,load,songs
    
def speed_test():

    if not os.path.isdir(gsfold):
        os.makedirs(gsfold)

    if os.path.isfile(gsfold + 'Speed.txt'):
        speed = open(gsfold + "Speed.txt","r")

    else:
        speed = open(gsfold + "Speed.txt","w+")
        tic = time.time()
        test1 = []
        for i in range(5000000):
            test1.append('x')

        toc = time.time()
        guage = toc-tic
        speed.write(str(guage))

    latency = speed.read()
    try:
        wait = int(-10*float(latency)+35)
    except:
        latency = guage
        wait = int(-10*float(latency)+35)
        
    return wait

wait = speed_test()
wait_new = wait

def background():

    global bground

    bground = []
    bfold = os.path.join(folder, 'Background/')

    if not os.path.isdir(bfold):
        os.makedirs(bfold)

    extensions = [ "jpg", "jpeg", "png", "bmp", "gif" ]
    try:
        for extension in extensions:
            for backg in glob.glob(bfold + "*." + extension):
                bground.append(backg)
    
        back = random.randint(0,len(bground)-1)
        bg = pygame.image.load(str(bground[back]))
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        return bg
    
    except:
        pass
try:
    bg = background()
    if bg == None:
        wait = int(wait*1.4 + 4.8)
except:
    wait = int(wait*1.4 + 4.8)

def music(schoice):

    global songs
    
    if (schoice == 0) or (schoice==len(songs)):

        songs = []
        
        mfold = os.path.join(folder, 'Music/')

        if not os.path.isdir(mfold):
            os.makedirs(mfold)

        extensions = [ "mp3", "wav", "ogg"]

        for extension in extensions:
            for tune in glob.glob(mfold + "*." + extension):
                songs.append(tune)

        songs = random.sample(songs,len(songs))
        
    pygame.mixer.music.load(str(songs[schoice]))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume)

try:
    music(schoice)
except:
    pass

def HScore():
        
    if os.path.isfile(gsfold + 'HScore.txt'):
        Hi_score = open(gsfold + "HScore.txt","r")
        current = Hi_score.read()
        Hi_score.close()

    else:
        Hi_score = open(gsfold + "HScore.txt","w+")
        Hi_score.write(str(runs))
        current = str(runs)
        Hi_score.close()

    return current

current = HScore()

def HFile(current):
    
    if runs>=int(current):
        Hi_score = open(gsfold + "HScore.txt","w+")
        Hi_score.write(str(runs))
        current = str(runs)
        Hi_score.close()
        
    return current

def Start_Maze():
    
    for rows in range(random.randint(20,30)):

        t = (random.randint(20,WIDTH-30)) #position of columns    
        n = (random.randint(10,HEIGHT-10)) #center of column postions
        v = random.randint(20,150) #size of columns
        
        for stacks in range(25):
    
            maze.append(t)
            maze.append(random.randint(n-v,n+v))

def Draw_Maze():
    
    for i in range(len(maze)-1):
        if (i % 2) == 0:
            pygame.draw.rect(win, (80,30,30), (maze[i], maze[i+1], radius, radius))
           
def Draw_circle(x,y):
    pygame.draw.circle(win, (255,0,0), (int(x), int(y)), radius)
      
def move(items):
    for item in items:
        item[0] += item[2]
        item[1] += item[3]
    
def removeUseless_x(items):
    for item in items:
        if item[1] > HEIGHT:
            items.remove(item)
            
def removeUseless_y(items):
    for item in items:
        if item[0] < 25:
            items.remove(item)
           
def Draw_streamers():
    
    num_s = 1
    xvals = set()
    yvals = set()
    
    ticker = random.randint(4,skill)
    attack = random.randint(0,3)
    
    if (ticker>=(random.randint(5,10))) & (attack>0): 
        while len(xvals) < num_s:
            pos = random.randint(40, WIDTH-15)
            xvals.add(pos)
   
        DY = random.randint(6,11)
        for val in xvals:
            streamers_x.append([val,0,0,DY])
        
    for item in streamers_x:        
        pygame.draw.circle(win, (50, 30, 150),(item[0], item[1]), 4)
        
    if (ticker>=(random.randint(5,10))) & (attack==0): 
        while len(yvals) < num_s:
            pos = random.randint(10, HEIGHT)
            yvals.add(pos)
            
        DX = random.randint(6,11)
        for val in yvals:
            streamers_y.append([WIDTH,val,-DX,0])
        
    for item in streamers_y:        
        pygame.draw.circle(win, (50, 30, 150),(item[0], item[1]), 4)
        
    move(streamers_x)
    move(streamers_y)
    removeUseless_x(streamers_x)
    removeUseless_y(streamers_y)
  
def Lose():
    
    for itemx in streamers_x:
        s = abs(x-itemx[0])
        t = abs(y-itemx[1])
        if (s<=13) & (t<=13):
            running = False
            return running
        
    for itemy in streamers_y:
        s = abs(x-itemy[0])
        t = abs(y-itemy[1])
        if (s<=13) & (t<=13):
            running = False
            return running
  
    else:
        running = True
        return running

def winning():

    pygame.draw.rect(win, (0, 128, 0), (WIDTH-40 , 12, 3.5*radius, 2.5*radius),1)
    nr_wins = FONT2.render(str(runs), True, (0, 128, 0))
    if runs<10:
        win.blit(nr_wins, (WIDTH-22 , 10))
    elif runs<100:
        win.blit(nr_wins, (WIDTH-30 , 10))
    else:
        win.blit(nr_wins, (WIDTH-40 , 10))
        
def redrawGameWindow():
    
    try:
        if not blank:
            win.blit(bg, [0, 0])
        else:
            win.fill((0,0,0))
    except:
        win.fill((0,0,0))
        
    Draw_circle(x,y) 
    Draw_Maze()
    Draw_streamers()
    winning()
            
    pygame.display.flip()
    
run = True
while run:

    if running:
    
        for event in pygame.event.get():
            pass

        if event.type == pygame.QUIT:
            try:
                p.terminate()
            except:
                pass
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_SPACE):

                paused = not paused

                while paused:
                    
                    try:
                        try:
                            pygame.mixer.music.pause()
                        except:
                            p.suspend()
                    except:
                        pass
                    
                    pygame.time.delay(300)
                    
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.type == pygame.KEYDOWN:

                            if (event.key == pygame.K_SPACE):
                                
                                try:
                                    try:
                                         pygame.mixer.music.unpause()
                                    except:
                                        p.resume()
                                         
                                except:
                                    pass

                                paused = not paused

            if (event.key == pygame.K_w) or (event.key == pygame.K_UP) & (y>=15):
            
                yes = True
                for i in range(len(maze)-1): 
                     if (i % 2) == 0:
                        s = abs(x-maze[i])
                        t = abs((y-14)-maze[i+1])
                        if (s<=10) & (t<=10):
                            yes = False
                            break
            
                if yes:    
                    y = y - 14
                
            if (event.key == pygame.K_s) or (event.key == pygame.K_DOWN) & (y<=HEIGHT-15):
            
                yes = True
                for i in range(len(maze)-1):
                    if (i % 2) == 0:
                        s = abs(x-maze[i])
                        t = abs((y+14)-maze[i+1])
                        if (s<=10) & (t<=10):
                            yes = False
                            break
                    
                if yes:    
                    y = y + 14
                   
            if (event.key == pygame.K_a) or (event.key == pygame.K_LEFT) & (x>=15):
            
                yes = True
                for i in range(len(maze)-1): 
                     if (i % 2) == 0:
                        s = abs((x-14)-maze[i])
                        t = abs(y-maze[i+1])
                        if (s<=10) & (t<=10):
                            yes = False
                            break
                if yes:
                    x = x - 14
                
            if (event.key == pygame.K_d) or (event.key == pygame.K_RIGHT):

                if x>=(WIDTH-7):
                    x = 10
                    y = 10
                    maze = []
                    streamers_x = []
                    streamers_y = []
                    runs += 1
                    pygame.time.delay(200)
                    Start_Maze()
                    current = HFile(current)
                
                yes = True
                for i in range(len(maze)-1): 
                   if (i % 2) == 0:
                        s = abs((x+14)-maze[i])
                        t = abs(y-maze[i+1])
                        if (s<=10) & (t<=10):
                            yes = False
                            break
                
                if yes:    
                    x = x + 14
       
        running = Lose()

        try:
            try:

                if (pygame.mixer.music.get_busy() == False) & (not silent):
                    try:
                        schoice +=1
                        if schoice==(len(songs)):
                            schoice = 0
                        music(schoice)
                    except:
                        pass

            except:

                p,wait_new,loaded,load,songs = alt_player(p,wait,songs,loaded,load)
                    
        except:
            pass

            
        redrawGameWindow()

    else:

        try:
            if not blank:
                win.blit(bg, (0, 0))
            else:
                win.fill((0,0,0))
        except:
            win.fill((0,0,0))

        start = FONT1.render("Play", True, (0, 128, 0))
        settings = FONT1.render("Settings", True, (0, 128, 0))
        leave = FONT1.render("Exit", True, (0, 128, 0))
        high_score = FONT2.render("Best Run: " + current, True, (0, 128, 0))
        cursor_txt1 = FONT3.render(">", True, (50, 30, 150))
        cursor_txt2 = FONT3.render("_", True, (50, 30, 150))
        
        win.blit(start, (55, 100))
        win.blit(settings, (55, 170))
        win.blit(leave, (55, 240))
        win.blit(high_score, (WIDTH-170, 20))
        win.blit(cursor_txt1, (cx1, cy1))
        win.blit(cursor_txt2, (cx2, cy2))
        

        if (rm_music):
            lnx = FONT1.render("Game CPU Usage May Be High, Press f-key To Fix", True, (0, 128, 0))
            win.blit(lnx, (55, HEIGHT-75))
        
        if skill==6:
            easy = FONT2.render("Skill: Easy", True, (0, 128, 0))
            win.blit(easy, (WIDTH-170, 50))
            
        if skill==8:
            moderate = FONT2.render("Skill: Moderate", True, (0, 128, 0))
            win.blit(moderate, (WIDTH-170, 50))
            
        if skill==10:
            hard = FONT2.render("Skill: Hard", True, (0, 128, 0))
            win.blit(hard, (WIDTH-170, 50))
        
        pygame.display.flip()

        try:
            try:

                if (pygame.mixer.music.get_busy() == False) & (not silent):
                    try:
                        schoice +=1
                        if schoice==(len(songs)):
                            schoice = 0
                        music(schoice)
                    except:
                        pass

            except:
                p,wait_new,loaded,load,songs = alt_player(p,wait,songs,loaded,load)   
        except:
            pass

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    p.terminate()
                except:
                    pass
                
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_f):
                    try:
                        pygame.mixer.quit()
                        rm_music = False
                    except:
                        pass
                    
                    try:
                        for i in range(len(songs)):
                            webbrowser.open(str(songs[i]))
                    except:
                        pass
                        
                    try:
                        finder = []
                        time.sleep(0.3)
                        for proc in psutil.process_iter(['pid', 'name']):
                            finder.append(proc.info)

                        open_ls = finder[-(len(songs)-1):]

                        for i in range(len(open_ls)):
                            d = open_ls[i]
                            pid = d['pid']
                            p = psutil.Process(pid)
                            usage = p.cpu_percent(interval=0.3)
                            if usage>=2:
                                break

                        try:
                            screen=Wnck.Screen.get_default()
                            screen.force_update()
                            windows=screen.get_windows() 
                            for w in windows:
                                if str(w.get_name()).endswith(('.mp3', 'wav', 'ogg')):
                                    w.minimize()
                        except:
                            pass

                        load = p.io_counters()
                        rt_change = True
                        load = load[1]
                        loaded = []
                        loaded.append(load)
                    except:
                        pass
                
                if (event.key == pygame.K_RETURN)  & (cursor==0):
                    
                    running = True
                    x = 10
                    y = 10
                    maze = []
                    streamers_x = []
                    streamers_y = []
                    runs = 0
                    Start_Maze()

                if (event.key == pygame.K_RETURN)  & (cursor==2):

                    try:
                        p.terminate()
                    except:
                        pass
                    pygame.quit()
                    sys.exit()

                if (event.key == pygame.K_RETURN)  & (cursor==1):

                    settings = True
                    cursor = 0
                    cy1 = 110
                    cy2 = 95

                    while settings:
                        
                        try:
                            if not blank:
                                win.blit(bg, (0, 0))
                            else:
                                win.fill((0,0,0))    
                        except:
                            win.fill((0,0,0))

                        Audio = FONT1.render("Audio", True, (0, 128, 0))
                        Display = FONT1.render("Display", True, (0, 128, 0))
                        Difficulty = FONT1.render("Difficulty", True, (0, 128, 0))
                        Hremove = FONT1.render("Reset High Score", True, (0, 128, 0))
                        MM = FONT1.render("Return To Main Menu", True, (0, 128, 0))
                        cursor_txt3 = FONT3.render(">", True, (50, 30, 150))
                        cursor_txt4 = FONT3.render("_", True, (50, 30, 150))
                        xcom = FONT1.render("r- to remove;  i- to insert;  e- easy;  m- moderate;  h- hard", True, (0, 128, 0))
                        high_score = FONT2.render("Best Run: " + current, True, (0, 128, 0))
                        
                        if (len(songs)>0) & (not silent):
                            Volume = FONT1.render(str(int(volume*200)) + "%  +- to adjust", True, (0, 128, 0))
                        elif (len(songs)>0) & (silent):
                            Volume = FONT1.render("Music Removed", True, (0, 128, 0))
                        else:
                            Volume = FONT1.render("No Music In Folder", True, (0, 128, 0))
                            
                        if len(bground)==0:
                            Background = FONT1.render("No Images in Folder",True,(0,128,0))
                        elif blank:
                            Background = FONT1.render("Background Removed",True,(0,128,0))
                            
                            
                        win.blit(Audio, (55, 100))
                        win.blit(Display, (55, 170))
                        win.blit(Difficulty, (55, 240))
                        win.blit(Hremove, (55, 310))
                        win.blit(MM, (55, 380))
                        win.blit(cursor_txt3, (cx1, cy1))
                        win.blit(cursor_txt4, (cx2, cy2))
                        win.blit(xcom, (55, HEIGHT-75))
                        win.blit(high_score, (WIDTH-170, 20))
                        
                        if cursor==0:
                            win.blit(Volume, (300, 100))

                        if (cursor==1) & ((len(bground)==0) or blank):
                            win.blit(Background,(300,170))
                        
                        if skill==6:
                            easy = FONT2.render("Skill: Easy", True, (0, 128, 0))
                            win.blit(easy, (WIDTH-170, 50))
                            
                        if skill==8:
                            moderate = FONT2.render("Skill: Moderate", True, (0, 128, 0))
                            win.blit(moderate, (WIDTH-170, 50))
                            
                        if skill==10:
                            hard = FONT2.render("Skill: Hard", True, (0, 128, 0))
                            win.blit(hard, (WIDTH-170, 50))
                            
                        
                        pygame.display.flip()

                        for event in pygame.event.get():
                            
                            if event.type == pygame.QUIT:
                                try:
                                    p.terminate()
                                except:
                                    pass
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.KEYDOWN:

                                if (cursor==0):

                                    if (event.key == pygame.K_r):
                                        try:
                                            pygame.mixer.music.stop()  
                                        except:
                                            pass
                                        try:
                                            p.terminate()
                                        except:
                                            pass
                                        silent = True
                                        volume = 0.0
                                        
                                    if (event.key == pygame.K_i):
                                        if not rt_change:
                                            try:
                                                pygame.mixer.init()
                                            except:
                                                pass
                                        
                                            if volume==0.0:
                                                volume = 0.15
                                            try:
                                                schoice+=1
                                                if schoice==(len(songs)):
                                                    schoice = 0
                                                music(schoice)
                                                silent = False
                                            except:
                                                pass

                                        else:
                                            try:
                                                
                                                songs = random.sample(songs,len(songs))
                                                    
                                                try:
                                                    p.terminate()
                                                except:
                                                    pass
                                                for i in range(len(songs)):
                                                    webbrowser.open(str(songs[i]))
                                                
                                                finder = []
                                                loaded.append(1)
                                                loaded.append(1)
                                                time.sleep(0.5)
                                                for proc in psutil.process_iter(['pid', 'name']):
                                                    finder.append(proc.info)

                                                open_ls = finder[-(len(songs)-1):]

                                                for i in range(len(open_ls)):
                                                    d = open_ls[i]
                                                    pid = d['pid']
                                                    p = psutil.Process(pid)
                                                    usage = p.cpu_percent(interval=0.3)
                                                    if usage>=1:
                                                        break
                                                try:
                                                    screen=Wnck.Screen.get_default()
                                                    screen.force_update()
                                                    windows=screen.get_windows() 
                                                    for w in windows:
                                                        if str(w.get_name()).endswith(('.mp3', 'wav', 'ogg')):
                                                            w.minimize()
                                                except:
                                                    pass

                                                load = p.io_counters()
                                                load = load[1]
                                                loaded = []
                                                loaded.append(load)
                                                silent = False
                                            except:
                                                pass
     
                                    if (event.unicode == "+") & (volume<=0.5):
                                        try:
                                            volume += 0.025
                                            pygame.mixer.music.set_volume(volume)
                                        except:
                                            pass
                                        
                                    if (event.unicode == "-") & (volume>0.0025):
                                        try:
                                            volume -= 0.025
                                            pygame.mixer.music.set_volume(volume)
                                        except:
                                            pass
                                              
                                if (cursor==1):
                                    
                                    if (event.key == pygame.K_r):
                                        
                                        win.fill((0,0,0))
                                        pygame.display.update()
                                        wait = speed_test()
                                        wait = int(wait*1.4 + 4.8)
                                        blank = True
                                        
                                    if (event.key == pygame.K_i):
                                        
                                        bg = background()
                                        blank = False
                                        wait = speed_test()

                                if (cursor==2):

                                    if (event.key == pygame.K_e):
                                        skill = 6

                                    if (event.key == pygame.K_m):
                                        skill = 8

                                    if (event.key == pygame.K_h):
                                        skill = 10

                                if (event.key == pygame.K_r) & (cursor==3):
                                    current = '0'
                                    Hi_score = open(gsfold + "HScore.txt","w+")
                                    Hi_score.write(current)
                                    Hi_score.close()
                                              
                                if (event.key == pygame.K_RETURN)  & (cursor==4): 

                                    settings = False                      
                                              
                                if (event.key == pygame.K_DOWN) & (cursor<4):

                                    cursor += 1
                                    cy1 += 70
                                    cy2 += 70

                                if (event.key == pygame.K_UP) & (cursor>0):
                                    
                                    cursor -= 1
                                    cy1 -= 70
                                    cy2 -= 70

                        pygame.time.delay(wait)

                    cursor = 0
                    cy1 = 110
                    cy2 = 95
                    
                if (event.key == pygame.K_DOWN) & (cursor<2):
                    
                    cursor += 1
                    cy1 += 70
                    cy2 += 70

                if (event.key == pygame.K_UP) & (cursor>0):
                    
                    cursor -= 1
                    cy1 -= 70
                    cy2 -= 70

    if not rt_change:
        pygame.time.wait(wait)
    else:
        pygame.time.wait(wait_new)

pygame.quit()
sys.exit()


# In[ ]:




