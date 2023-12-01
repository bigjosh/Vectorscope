# A little slideshow you can customize
## Images need to be in true color / jpg
## Example conversion: convert Death_Star.jpg -resize 240x240 -type TrueColor thats_no_moon.jpg

import screennorm
import keyboardcb
import keyleds
import vectoros
import timer
import gc
import asyncio
from vos_state import vos_state
import colors


screen=screennorm.ScreenNorm()   # get the screen



current_slide=0   # current slide
exit_flag=False   # don't exit
tid=None          # timer ID
timer_rate=100    # timer rate (ticks; see vos_launch.py for multiplier)
pauseflag=False   # pause slide show

# comamnds for slides
TEXT=0
IMAGE=1
BACKGROUND=2
TEXTXY=3

slides=[
        [ IMAGE, "r1.jpg" ],
        [ IMAGE, "r2.jpg" ],
        [ IMAGE, "r3.jpg" ],
        [ IMAGE, "r4.jpg" ],
        [ IMAGE, "r5.jpg" ],
        [ IMAGE, "r6.jpg" ],
        [ IMAGE, "r7.jpg" ],
        [ IMAGE, "r8.jpg" ],
        [ IMAGE, "r9.jpg" ],
        [ IMAGE, "r10.jpg" ],
        [ IMAGE, "r11.jpg" ],
        [ IMAGE, "r12.jpg" ],
        [ IMAGE, "r13.jpg" ],
        [ IMAGE, "r14.jpg" ],
        [ IMAGE, "r15.jpg" ],
        [ IMAGE, "r16.jpg" ],
        [ IMAGE, "r17.jpg" ],
        [ IMAGE, "r18.jpg" ],
        [ IMAGE, "r19.jpg" ],

        [ IMAGE, "r20.jpg" ],
        [ IMAGE, "r21.jpg" ],
        [ IMAGE, "r22.jpg" ],
        [ IMAGE, "r23.jpg" ],
        [ IMAGE, "r24.jpg" ],
        [ IMAGE, "r25.jpg" ],
        [ IMAGE, "r26.jpg" ],
        [ IMAGE, "r27.jpg" ],
        [ IMAGE, "r28.jpg" ],
        [ IMAGE, "r29.jpg" ],

        [ IMAGE, "r30.jpg" ],
        [ IMAGE, "r31.jpg" ],
        [ IMAGE, "r32.jpg" ],
        [ IMAGE, "r33.jpg" ],
        [ IMAGE, "r34.jpg" ],
        [ IMAGE, "r35.jpg" ],
        [ IMAGE, "r36.jpg" ],
        
       ]

# if you change the timeout we have to kill the old timer and make a new one
def update_timer():
    global tid, timer_rate
    timer.Timer.remove_timer(tid)
    tid=timer.Timer.add_timer(timer_rate,next)  # change over

# get next slide
def next():
    global current_slide, TEXT, IMAGE
    bkflag=False
    if pauseflag:
        return  # nothing doing
    cmdlist=slides[current_slide]
    if cmdlist[0]==IMAGE or cmdlist[0]==BACKGROUND:
        print(cmdlist[1])
        screen.jpg(cmdlist[1])
    if cmdlist[0]==BACKGROUND:
        bkflag=True
        current_slide+=1
        if current_slide>=len(slides):
            current_slide=0
        cmdlist=slides[current_slide]   #assume next one will be TEXT
    if cmdlist[0]==TEXT:
        x=40
        y=40
    if cmdlist[0]==TEXTXY:
        x=cmdlist[1]
        y=cmdlist[2]
        cmdlist[0]=TEXT
        del cmdlist[1:3]
        
    if cmdlist[0]==TEXT:
        if bkflag==False:
            screen.clear(cmdlist[2])
        for txt in cmdlist[3:]:
            screen.text(x,y,txt,cmdlist[1], cmdlist[2])
            y+=30
    current_slide+=1   # advance slide
    if current_slide>=len(slides):
        current_slide=0   # or recycle




# Joystick
# Up is delay up, Down is delay down
# Right is next, and Left toggles the pause flag
def joycb(key):
    global timer_rate, pauseflag
    if (key==keyleds.JOY_UP):
        timer_rate+=10
        if timer_rate>200:
            timer_rate=200
        update_timer()
    if (key==keyleds.JOY_DN):
        timer_rate-=10
        if timer_rate<=0:
            timer_rate=1
        update_timer()
    if (key==keyleds.JOY_RT):
        oldpause=pauseflag
        update_timer()    # reset timer for next auto-next
        pauseflag=False   # make sure it redraws
        next()
        pauseflag=oldpause
    if (key==keyleds.JOY_LF):
        pauseflag=not pauseflag



    
def menu(key):						# menu -bail out
    global exit_flag
    exit_flag=True





async def vos_main():
    global exit_flag, current_slide, tid, timer_rate
    current_slide=0
    # we treat the joystick like any other key here
    keys=keyboardcb.KeyboardCB({keyleds.KEY_MENU: menu, keyleds.JOY_UP: joycb, keyleds.JOY_DN: joycb, keyleds.JOY_RT: joycb, keyleds.JOY_LF: joycb})
    tid=timer.Timer.add_timer(timer_rate,next)
    # prime it
    next()
    # do nothing... everything is on keyboard and timer
    while exit_flag==False:
        await asyncio.sleep_ms(500)
# stop listening for keys
    keys.detach()
    timer.Timer.remove_timer(tid)
    exit_flag=False  # next time

    vos_state.show_menu=True  # tell menu to wake up
    


if __name__=="__main__":
    import vectoros
    vectoros.run()

