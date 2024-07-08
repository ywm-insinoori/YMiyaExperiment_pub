from psychopy import core, visual, gui, data, logging, event
import numpy as np
import random

expInfo = {'Participant':0, 'Disptype':"real", 'Distance':"0.0D"}
expInfo['dateStr'] = data.getDateStr()

dlg = gui.Dlg(title='Stair Expr Test')
dlg.addText('Participant info')
dlg.addField('ID:')
dlg.addText('Session info')
dlg.addField('Display type:', choices=["LF","real"])
dlg.addField('Target distance (real):', initial="0.0D", choices=["0.0D","0.3D","0.5D","1.0D","1.5D","2.0D","2.5D","3.0D","3.5D"])
dlg.addField('FrontSurfer interval [ms]:',160)
ok_data = dlg.show()
if dlg.OK:
    print(ok_data)
else:
    print('User cancelled')
    core.quit()

staircase = data.StairHandler(startVal = 1.08, stepType = 'lin', stepSizes=0.16, nUp=1, nDown=2, nTrials=5, nReversals=0, applyInitialRule=True, minVal=0.6, maxVal=1.08)

win = visual.Window([800,600],units='pix')

tgt = visual.GratingStim(win, sf=0.05, size=100, mask='gauss', ori=90)

for thisIncrement in staircase:
    orientation = 90
    tgt.ori = orientation
    tgt.size = 100*thisIncrement
    tgt.draw()
    win.flip()
    core.wait(0.5)
    thisResp = None
    print(thisIncrement)
    while thisResp==None:
        allKeys = event.waitKeys()
        for thiskey in allKeys:
            if thiskey == 'left':
                if orientation==90: thisResp=1
                else: thisResp=-1
            elif thiskey == 'up':
                if orientation==0: thisResp=1
                else: thisResp=-1
            elif thiskey in ['q','escape']:
                core.quit()
        event.clearEvents()
    staircase.addResponse(thisResp)
    core.wait(1)

core.quit()