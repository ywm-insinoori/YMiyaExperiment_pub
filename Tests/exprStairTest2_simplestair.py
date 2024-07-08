from psychopy import core, visual, gui, event, data
import numpy as np
import random
from LandoltC import LandoltC

# mydate = data.getDateStr()
# print(mydate)

NTRIAL = 10

dlg = gui.Dlg(title='Stair Expr Test')
dlg.addText('Participant info')
dlg.addField('* ID:')
dlg.addText('Session info')
dlg.addField('Display type:', choices=["LF","real"])
dlg.addField('Target distance (real):', initial="0.0D", choices=["0.0D","0.3D","0.5D","1.0D","1.5D","2.0D","2.5D","3.0D","3.5D"])
dlg.addField('FrontSurfer interval [ms]:',160)
#ok_data = dlg.show()
#if dlg.OK:
#    print(ok_data)
#else:
#    print('User cancelled')
#    core.quit()

stimAngRes_deg = np.flip(np.linspace(start=0.6,stop=1.08,num=4))
print(stimAngRes_deg)

win = visual.Window([800,600],units='pix',color=-1)

core.wait(5)

LandCgapsize_px = 20

myLandC = LandoltC(gappx=LandCgapsize_px,ori='right',pwin=win,brightness=0.5,centerpos=[0,100])

idx = 0
for itrial in range(NTRIAL):
    myLandC.setSize(LandCgapsize_px*stimAngRes_deg[idx])
    thisori = random.choice(['right','left','up','down'])
    myLandC.setOri(thisori)
    myLandC.draw()
    win.flip()

    thisResp = None
    while thisResp == None:
        allkeys = event.waitKeys()
        for thiskey in allkeys:
            if thiskey == thisori:
                thisResp = 1
            else:
                thisResp = 0
        event.clearEvents()
    
    # respstr = input('ENTER THE SIDE OF GAP (right, left, up, or down) >')
    # respstr = thisori

    # if respstr == thisori:
    if thisResp:
        idx += 1
        # TODO: Record a correct response
    else:
        idx -= 1
        # TODO: Record an incorrect response
    
    if idx < 0:
        idx = 0
    elif idx > (len(stimAngRes_deg)-1):
        idx = 3
    else:
        pass

core.wait(1)

# myLandC.setSize(10)
# myLandC.setOri('up')
# myLandC.setBrightness(0.9)
# myLandC.setCenterPos([-100,0])
# myLandC.draw()
# win.flip()

# core.wait(1)

core.quit()