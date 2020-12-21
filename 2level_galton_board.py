#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:14:07 2020

@author: alex
"""
import pygame as pg
from random import randrange
import pymunk.pygame_util
import time

pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 1200, 1000
HEIGHT2 = HEIGHT//2

FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = -1, 5000
ball_mass, ball_radius = 0.4, 4
segment_thickness = 2
ball_number = 500

a, b, c, d = 0, 20, 17, 20
x1, x2, x3, x4 = a, WIDTH // 2 - c, WIDTH // 2 + c, WIDTH - a
y1, y2, y3, y4 = b, HEIGHT2 // 4 - d, HEIGHT2 // 4, HEIGHT2 // 2 - 3.85 * b ###     y5, HEIGHT2 - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (a, HEIGHT2), (WIDTH, HEIGHT2)


def create_ball(space):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = randrange(x1, x4), randrange(-y1, y1)
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.2
    ball_shape.friction = 0.2
    space.add(ball_body, ball_shape)
    return ball_body


def create_ball_2(space, bx, by):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = bx, by
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.2
    ball_shape.friction = 0.2
    space.add(ball_body, ball_shape)
    return ball_body




def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    space.add(segment_shape)


def create_peg(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=5, offset=(x, y))
    circle_shape.color = pg.color.THECOLORS[color]
    circle_shape.elasticity = 0.05
    circle_shape.friction = 0.05
    space.add(circle_shape)


# pegs
def pegs(peg_y = y4, step = 30, rows = 10, WIDTH = WIDTH, HEIGHT=HEIGHT2):
        for i in range(rows):
            peg_x = -1.5 * step if i % 2 else -step
            for j in range(WIDTH // step + 2):
                create_peg(peg_x, peg_y, space, 'darkgray')
                if i == rows - 1:
                    create_segment((peg_x, peg_y + 50), (peg_x, HEIGHT), segment_thickness, space, 'darkgray')
                peg_x += step
            peg_y += 0.5 * step

platforms = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
for platform in platforms:
    create_segment(*platform, segment_thickness, space, 'darkgray')

dd = pymunk.Segment(space.static_body, B1, B2, 9 * segment_thickness)
dd.color = pg.color.THECOLORS['darkgray']
space.add(dd)

pegs()


L5, L6, L7, L8 = (x1,  HEIGHT2), (x1, y1 + HEIGHT2), (x2, y2 + HEIGHT2), (x2, y3 + HEIGHT2)
R5, R6, R7, R8 = (x4,  HEIGHT2), (x4, y1 + HEIGHT2), (x3, y2 + HEIGHT2), (x3, y3 + HEIGHT2)
B3, B4 = (a, HEIGHT), (WIDTH, HEIGHT)

platforms2 = (L5, L6), (L6, L7), (L7, L8), (R5, R6), (R6, R7), (R7, R8)
for platform in platforms2:
    create_segment(*platform, segment_thickness, space, 'darkgray')
create_segment(B3, B4, 2 * segment_thickness, space, 'darkgray')


pegs(peg_y = y4 + HEIGHT2 , HEIGHT=HEIGHT)



# balls
col_bal = []
for i in range(ball_number):
    if i%150 and i not in (166, 321, 485): 
        col_bal.append((234,242,243))
    elif i in (166, 321, 485):
        col_bal.append((225,45,0))
    else: 
        col_bal.append((255,0,255))
        
balls = [(col_bal[j], create_ball(space)) for j in range(ball_number)]


bb = True
bAlls = None

loop = True
while loop:
    surface.fill(pg.Color('black'))
    surface.set_alpha(50)

    for i in pg.event.get():
        if i.type == pg.QUIT:
             loop = False #exit()    #
    balls_up = 0        
    if bAlls and bb :
        BALLS2 = []
        for b in  bAlls:  
            #BALLS2.append( (b.color, create_ball_2(space, b.x, b.y)) )
            if b.y < HEIGHT2 - 205 :
                balls_up += 1
                
       
        if balls_up == 0:
                time.sleep(2)
                bb = False
                

                #pg.init()
                surface = pg.display.set_mode(RES)
               
                draw_options = pymunk.pygame_util.DrawOptions(surface)
                
                space = pymunk.Space()
                space.gravity = -1, 8000
                
                for platform in platforms:
                    create_segment(*platform, segment_thickness, space, 'darkgray')

                for platform in platforms2:
                    create_segment(*platform, segment_thickness, space, 'darkgray')
                create_segment(B3, B4, 2 * segment_thickness, space, 'darkgray')
                
                pegs()
                pegs(peg_y = y4 + HEIGHT2 , HEIGHT=HEIGHT)
                
                
                for j, b in  enumerate(bAlls):  
                       BALLS2.append( (balls[j][0], create_ball_2(space, b.x, b.y)) )
                
                                
    space.step(1 / FPS)
    space.debug_draw(draw_options)

    # [pg.draw.circle(surface, color, ball.position, ball_radius) for color, ball in balls]
    if bb: ###
        bAlls = [pg.draw.circle(surface, color, (int(ball.position[0]), int(ball.position[1])),
                    ball_radius) for color, ball in balls]
    #"""
    else: ############
    
        [pg.draw.circle(surface, color, (int(ball.position[0]), int(ball.position[1])),
                    ball_radius) for color, ball in BALLS2]
    #"""
    
    
    pg.display.flip()
    clock.tick(FPS)
    #loop = False
    
