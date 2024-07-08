from numpy import power, linspace
from psychopy import core, visual, monitors
from psychopy.hardware.keyboard import Keyboard

def LUT(input, gamma):
    # input has to be in [-1,1]
    normalizedinput = (input+1)/2 # Not this is [0,1]
    normalizedoutput = power(normalizedinput, 1/gamma)
    return normalizedoutput * 2 - 1

VDIST = 33.3
BMGAMMA = 3

moni_bm = monitors.Monitor('Blackmagic',width=15.8,distance=279)
moni_bm.setSizePix([1920,1080])
moni_bm.setDistance(VDIST)

win = visual.Window(monitor=moni_bm, winType='pyglet', allowGUI=False,screen=1,fullscr=True,color=[-1,-1,-1],units='cm')
core.wait(0.5)

kb=Keyboard()

inputcol = linspace(-1,1,8)
idx = 0

ctrRect = visual.Rect(win=win, units='cm', size=[4,4], lineWidth=0, fillColor=LUT(inputcol[idx],BMGAMMA))
ctrRect.draw()
win.flip()
print("Draw and flip done")

while True:
    keys = kb.waitKeys()
    if "space" in keys:
        break
    else:
        if "up" in keys:
            idx += 1
        elif "down" in keys:
            idx -= 1
        else:
            pass

        if idx > (len(inputcol)-1):
            idx = (len(inputcol)-1)
        elif idx < 0:
            idx = 0
        else:
            pass
        ctrRect.fillColor = LUT(inputcol[idx],BMGAMMA)
        ctrRect.draw()
        win.flip()

win.close()
core.quit()