# -*- coding: utf-8 -*- python3
"""
GREAT PLAGUE DEATH TRACKER
Created on Mon Nov 11 02:39:06 2019

@author: Antiochian

The gameplan:
    - Manually transcribe each parish's death count in a text file of format "totaldeaths plaguedeaths\n"
    - Generate polygon vertex coordinates of each parish as a .txt file using ShapeJ "points" and "measure" tools
    - Automatically convert these text files to polygon objects in pygame to be coloured
    - iterate over all 51 weeks and colour each parish accordingly
    - Make parish a different colour of red for number of deaths (option to normalise with population of parish?)
    - include total mortality counter on bottom of screen as some kind of neat graph perhaps
"""

import pygame
import sys,os
#color data
rivercolor = (88,110,117)
bgcolor = (7,54,66)
lifecolor = (133,153,0,255)
lifecolor = (0,0,0,255)
deathcolor = (255,0,0,255)

#this FPS is NOT the same FPS the animation runs at, its just to make inputs feel snappy
FPS = 30
animspeed = 1.7 #weeks/second

scale = 1
xscale = scale
yscale = scale

pygame.init()
Nx,Ny = 1000,654
mapsize = (1000,674)
(Nx,Ny) = Nx,Ny
window = pygame.display.set_mode( (Nx,Ny) )
deathlayer = pygame.Surface( (Nx,Ny), pygame.SRCALPHA ) 
maplayer = pygame.image.load('trans_map.png')
maplayer = pygame.transform.smoothscale(maplayer, (int(mapsize[0]*scale),int(mapsize[1]*scale)))
parishdict = {}
namelist = []
class Parish:
    def __init__(self,name):
        self.name = name #eg: St Aldates
        self.shape = import_shape('shapes/'+name)   #eg: [ (10,20) , (10,30) , (15,42) ]
        self.deathlist = import_deaths('deaths/'+name)  #eg: [[0,0],[1,0],[3,2],[56,49], ...] each death by plague (total deaths?)
        #self.size = some sort of shoelace algorithm? #possibly might be used for normalising data?
        
def import_shape(URL):
    #reads given file path and outputs a 2-dimensional list of polygon vertex coordinates
    file = open(URL).read().splitlines()
    points = []
    for count in range(1,len(file)):
        points.append(list(map(float,file[count].split('\t')))[5:])
    for index in range(len(points)):
        points[index][0],points[index][1] = int(points[index][0]*xscale), int(points[index][1]*yscale)
    return points

def import_deaths(URL='testname.txt'):
    #imports file as list of strings for each line
    deathlist = open(URL).read().splitlines()
    for count in range(len(deathlist)):
        deathlist[count] = list(map(int,deathlist[count].split(' ')))
    #BE CAREFUL there might be a memory leak here?
    return deathlist

def create_parishes():
    deathfiles = os.listdir('deaths')
    shapefiles = os.listdir('shapes')
#    if any(deathfiles != shapefiles): #check all files are named properly
#        raise Exception("Filename Mismatch!")
    for parishname in deathfiles:
        parishdict[parishname[:-4]] = Parish(parishname)
        namelist.append(parishname[:-4])
    return

def draw_river():
    rivershape = import_shape('rivershape.txt')
    pygame.draw.polygon(window, rivercolor, rivershape)
    return

def draw_deaths(weekno):
    #draw polygons for each parish
    deathlayer.fill((0,0,0,0))
    for name in namelist:
        dR,dG,dB = deathcolor[0] - lifecolor[0], deathcolor[1] - lifecolor[1], deathcolor[2] - lifecolor[2]
        intensityfrac = parishdict[name].deathlist[weekno][0] /maxdeaths #based on no. of deaths
        shade = (int(lifecolor[0]+dR*intensityfrac), int(lifecolor[1]+dG*intensityfrac),int(lifecolor[2]+dB*intensityfrac), 255)
        pygame.draw.polygon(deathlayer, shade, parishdict[name].shape)
    window.blit(deathlayer, (0,0))
    window.blit(maplayer, (0,0)) #put map overtop
    pygame.display.update()
    return

clock = pygame.time.Clock()
window.fill(bgcolor)
deathlayer.fill((0,0,0,0))
create_parishes()

maxdeaths = int(max(parishdict[namelist[0]].deathlist)[0]) #normalise
totalweeks = len(parishdict[namelist[0]].deathlist)
weekno = 0
framecount = 0
draw_river()
while True: #main simulation loop
    clock.tick(FPS)
    framecount += 1
    if weekno < totalweeks and framecount % 17 == 0: #modulo to make animation FPS seperate from actual program FPS
        draw_deaths(weekno) 
        weekno += 1   
    
    for event in pygame.event.get(): #detect events
        if event.type == pygame.QUIT: #detect attempted exit
            pygame.quit()
            sys.exit()      #these 2 optional lines fix a hangup bug in IDLE  
        if  pygame.key.get_pressed()[114]: #R to reset
            weekno = 0
            framecout = 0






