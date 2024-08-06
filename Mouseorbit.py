import mouse
import pyautogui
import keyboard
import tkinter as tk
import time
import random
import math
import win32gui
import win32con
import win32api


stopstartkey = 'PgUp'
quitkey = 'End'
screen_width, screen_height = pyautogui.size()
centerx = screen_width / 2
centery = screen_height / 2
bounce = 0.95
x, y = mouse.get_position()
CanPressQ = True
Running = True
Runall = True
deltaTime = 0
gettime = time.perf_counter()
xmomentum = 0
ymomentum = 0
movex = 0
movey = 0
max_move_speed = 1000
countXmomentumthisframe = False
countYmomentumthisframe = False
friction = 0.04 #Must be between 0 and 1, higher means more friction 0 is no friction
slow = 13 #controls how much the mouse movement effects the momentum, 1 doesn't slow down its speed at all
pull = 1 #put negative for it to push away from the center, controls the speed it moves toward the center
dynamicpull = False #controls weather or not the distence you are from the center effects the pull
havemomentum = True #controls if the mouse will be slippery
havepull = False #disables or inables the pull towarards the center
keepOrbit = True #restors the lost pull momentum from slow to keep orbit going
centerpull = 0 #changes how much the center is pulled towards the mouse, set to 0 to disable
dynamiccenterpull = False
drawline = True
screenwrap = True #makes the mouse loop around the screen rather than bounce (not reccomended if pull is enabled)

def draw_dot(x, y):
    hdc = win32gui.GetDC(0)
    pen = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(255, 30, 30))  # Reduced the pen width
    win32gui.SelectObject(hdc, pen)
    win32gui.SetPixel(hdc, int(x), int(y), win32api.RGB(255, 30, 30))  # Set a pixel at (x, y)
    win32gui.DeleteObject(pen)
    win32gui.ReleaseDC(0, hdc)

def draw_rope(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    red = min(int(distance/5), 255)
    green = min(255 - int(distance/7), 255)
    color = win32api.RGB(red, green, 0)
    hdc = win32gui.GetDC(0)
    pen = win32gui.CreatePen(win32con.PS_SOLID, 1, color)
    win32gui.SelectObject(hdc, pen)
    win32gui.MoveToEx(hdc, int(x1), int(y1))
    win32gui.LineTo(hdc, int(x2), int(y2))
    win32gui.DeleteObject(pen)
    win32gui.ReleaseDC(0, hdc)




while Runall:
    deltaTime = (time.perf_counter() - gettime)
    gettime = time.perf_counter()
    
    if keyboard.is_pressed(quitkey):
        Runall = False
        
    if Running == True:
        if keyboard.is_pressed(stopstartkey):
            if CanPressQ == True:
                Running = False
                CanPressQ = False
        else:
            CanPressQ = True
        
        x_prev, y_prev = x, y 
        x, y = mouse.get_position()
        
        xmomentum += (((x - x_prev - round(xmomentum))/slow) + (round(movex)-round(movex)/slow)*havepull*keepOrbit)*countXmomentumthisframe
        ymomentum += (((y - y_prev - round(ymomentum))/slow) + (round(movey)-round(movey)/slow)*havepull*keepOrbit)*countYmomentumthisframe
        
        if not countXmomentumthisframe:
            countXmomentumthisframe = True
        if not countYmomentumthisframe:
            countYmomentumthisframe = True
        
        xmomentum *= 1-friction
        ymomentum *= 1-friction
        
        if dynamicpull:
            dx = centerx - x
            dy = centery - y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                speed = pull * deltaTime
                movex = dx / distance * min(speed * distance, max_move_speed)
                movey = dy / distance * min(speed * distance, max_move_speed)
            else:
                movey = 0
                movex = 0
            if centerpull != 0:
                if dynamiccenterpull:
                    dx = x - centerx
                    dy = y - centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > 0:
                        speed = centerpull * deltaTime
                        centerx += dx / distance * min(speed * distance, max_move_speed)
                        centery += dy / distance * min(speed * distance, max_move_speed)
                    else:
                        movey = 0
                        movex = 0
                else:
                    dx = x - centerx
                    dy = y - centery
                    angle = math.atan2(dy, dx) + math.pi

                    centerx += centerpull * -math.cos(angle)
                    centery += centerpull * -math.sin(angle)
            
        else:
            dx = centerx - x
            dy = centery - y
            angle = math.atan2(dy, dx) + math.pi

            movex = pull * -math.cos(angle)
            movey = pull * -math.sin(angle)
            if centerpull != 0:
                if dynamiccenterpull:
                    dx = x - centerx
                    dy = y - centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > 0:
                        speed = centerpull * deltaTime
                        centerx += dx / distance * min(speed * distance, max_move_speed)
                        centery += dy / distance * min(speed * distance, max_move_speed)
                    else:
                        movey = 0
                        movex = 0
                else:
                    dx = x - centerx
                    dy = y - centery
                    angle = math.atan2(dy, dx) + math.pi

                    centerx += centerpull * -math.cos(angle)
                    centery += centerpull * -math.sin(angle)
            
        
        mouse.move(x + round(xmomentum)*havemomentum + round(movex)*havepull, y + round(ymomentum)*havemomentum + round(movey)*havepull)
        tempx, tempy = mouse.get_position()
        if tempx >= screen_width-1 or tempx <= 0:
            if not screenwrap:
                xmomentum *= -bounce
                mouse.move(x , y)
            else:
                if tempx >= screen_width-1:
                    mouse.move(9 , y)
                else:
                    mouse.move(screen_width-10 , y)
                countXmomentumthisframe = False
        if tempy >= screen_height-1 or tempy <= 0:
            if not screenwrap:
                ymomentum *= -bounce
                mouse.move(x , y)
            else:
                if tempy >= screen_height-1:
                    mouse.move(x , 1)
                else:
                    mouse.move(x , screen_height-2)
                countYmomentumthisframe = False
        if centerx > screen_width or centerx < 0:
            centerx = screen_width / 2
        if centery > screen_height or centery <= 0:
            centery = screen_height / 2
                
        if drawline and havepull:
            draw_rope(x, y, centerx, centery)
            
    else:
        screen_width, screen_height = pyautogui.size()
        centerx = screen_width / 2
        centery = screen_height / 2
        x, y = mouse.get_position()
        if keyboard.is_pressed(stopstartkey):
            if CanPressQ == True:
                Running = True
                CanPressQ = False
        else:
            CanPressQ = True
    time.sleep(0.01)
