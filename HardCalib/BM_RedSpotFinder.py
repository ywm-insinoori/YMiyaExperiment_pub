from psychopy import visual, core, monitors
from psychopy.hardware.keyboard import Keyboard
from psychopy.tools.monitorunittools import cm2deg

import numpy as np

mymoni = monitors.Monitor('Blackmagic',width=15.8,distance=279)
mymoni.setSizePix([1920,1080])

mymoni.setDistance(33.3)

win = visual.Window(monitor=mymoni,winType='pyglet',allowGUI=False,screen=1,fullscr=True,color=[-1,-1,-1],units='cm',multiSample=True,numSamples=8) # size=[640,480], winType='glfw'

kb = Keyboard()

LINELENGTH_DEG = 0.5
FIXLINESTARTEND = LINELENGTH_DEG * 0.5
PROBELINESTARTEND = LINELENGTH_DEG * 0.3

DEGINC = 0.2

centerpos = [-3.2, 0.0] # BM 3.5D

fix_hline = visual.Line(win,start=(-FIXLINESTARTEND,0.0),end=(FIXLINESTARTEND,0.0),units='deg',lineWidth=0.07,color=0)
probe_hline = visual.Line(win,start=(-PROBELINESTARTEND,0.0),end=(PROBELINESTARTEND,0.0),units='deg',lineWidth=0.05,color=(-1,1,-1))

fix_vline = visual.Line(win,start=(0.0,-FIXLINESTARTEND),end=(0.0,FIXLINESTARTEND),units='deg',lineWidth=0.07,color=0)
probe_vline = visual.Line(win,start=(0.0,-PROBELINESTARTEND),end=(0.0,PROBELINESTARTEND),units='deg',lineWidth=0.05,color=(-1,1,-1))

fix_hline.units = "cm"
fix_vline.units = "cm"
probe_hline.units = "cm"
probe_vline.units = "cm"

fix_hline.pos = centerpos
fix_vline.pos = centerpos
probe_hline.pos = centerpos
probe_vline.pos = centerpos

fix_hline.units = "deg"
fix_vline.units = "deg"
probe_hline.units = "deg"
probe_vline.units = "deg"

probepos = probe_hline.pos

fix_hline.draw()
fix_vline.draw()
probe_hline.draw()
probe_vline.draw()

win.flip()

print("Press Esc to quit")

while True:
    keys = kb.waitKeys()
    if "escape" in keys:
        break
    elif "up" in keys:
        probepos[1] = probepos[1] + DEGINC
        probe_hline.pos = probepos
        probe_vline.pos = probepos
    elif "down" in keys:
        probepos[1] = probepos[1] - DEGINC
        probe_hline.pos = probepos
        probe_vline.pos = probepos 
    elif "right" in keys:
        probepos[0] = probepos[0] + DEGINC
        probe_hline.pos = probepos
        probe_vline.pos = probepos
    elif "left" in keys:
        probepos[0] = probepos[0] - DEGINC
        probe_hline.pos = probepos
        probe_vline.pos = probepos
    elif "space" in keys:
        probe_hline.units = "cm"
        poscm = probe_hline.pos
        probe_hline.units = "deg"
        relposcm = poscm - centerpos
        print(f"Probe: [{relposcm[0]}, {relposcm[1]}] cm relative to the fixation cross")
        relposdeg = [cm2deg(relposcm[0], mymoni), cm2deg(relposcm[1], mymoni)]
        print(f"Probe: [{relposdeg[0]}, {relposdeg[1]}] deg relative to the fixation cross")
    else:
        pass
    fix_hline.draw()
    fix_vline.draw()
    probe_hline.draw()
    probe_vline.draw()

    win.flip()

win.close()
core.quit()