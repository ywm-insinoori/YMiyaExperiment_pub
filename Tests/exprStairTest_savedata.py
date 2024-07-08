import random
from datetime import datetime
import numpy as np
import pandas as pd

from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB','sounddevice','pyo','pygame']
from psychopy import core, visual, gui
from psychopy.hardware.keyboard import Keyboard
from psychopy import logging

from LandoltC import LandoltC

def getRealTimeStampAndStoreToDataFrame(df,rowidx,colname):
    d = datetime.now()
    df.loc[rowidx,colname] = d.strftime('%Y-%m-%d-%H-%M-%S-%f')

def generateFilename(dlgdat, type:str):
    myd = datetime.now()
    if dlgdat[1] == 'real':
        disptypesfx = dlgdat[1] + str(dlgdat[2].replace(' ',''))
    else:
        disptypesfx = dlgdat[1]

    if type == 'trial':
        typestr = 'trialdata'
    elif type == 'log':
        typestr = 'log'
    else:
        return None
    return 'LFacm-v0-' + typestr + myd.strftime('-%Y-%m-%d-%H-%M-%S-%f') + '-Subj{:02}-'.format(int(dlgdat[0])) + disptypesfx + f'-Delay{dlgdat[3]}ms'

realdistsdpts = {'0.0 D':None, '0.3 D':279.0, '0.5 D':200.0, '1.0 D':101.0, '1.5 D':64.6, '2.0 D':50.0, '2.5 D':40.0, '3.0 D':32.5, '3.5 D':27.6} # Keys=str indicating (rough) dioptric distances, Vals = float indicating metric distance in cm

dlg = gui.Dlg(title='Stair Expr Test')
dlg.addText('Participant info')
dlg.addField('* ID:')
dlg.addText('Session info')
dlg.addField('Display type:', choices=["LF","real"], initial="real")
dlg.addField('Target distance (real):', initial="0.0D", choices=list(realdistsdpts.keys()))
dlg.addField('FrontSurfer interval [ms]:',160)
ok_data = dlg.show()
if dlg.OK:
    if not ok_data[0]:
        print('Participant ID not filled')
        core.quit()
    print(f'Starting experiment for Participant {ok_data[0]}. Display type: {ok_data[1]}.')
    if ok_data[1] == "real":
        if ok_data[2] == '0.0 D':
            print('Real target, but the distance inproperly picked.')
            core.quit()
        print(f'Real target distance: {ok_data[2]}')
        print(f'FrontSurfer computation interval of {ok_data[3]} ms')
else:
    print('User cancelled')
    core.quit()

print(generateFilename(ok_data,'trial'))
thislog = logging.LogFile(generateFilename(ok_data,'log')+'.log', level=logging.INFO, filemode='w')
# print(type(thislog)) # LogFile class. thislog.write() can be used? See the source code. 

NTRIAL = 10
stimAngRes_deg = np.flip(np.linspace(start=0.6,stop=1.08,num=4))

resdat = pd.DataFrame(0, index=list(range(NTRIAL)), columns=['trial_SN','disptype','imgdepth','stimsize_AR','stim_ori','time_stimonset','time_resp','iscorrect'])
resdat['disptype'] = ok_data[1]
resdat = resdat.astype({'trial_SN': 'int','imgdepth': 'str','stimsize_AR':'float','stim_ori':'str','time_stimonset':'str','time_resp':'str','iscorrect':'bool'})
# print(resdat.dtypes)

win = visual.Window([800,600],units='pix',color=-1)
kb = Keyboard()
core.wait(0.5)

LandCgapsize_px = 20
myLandC = LandoltC(gappx=LandCgapsize_px,ori='right',pwin=win,brightness=0.5,centerpos=[0,100])

idx = 0
resdat.loc[:,'imgdepth'] = ok_data[2]
for itrial in range(NTRIAL):
    resdat.loc[itrial,'trial_SN'] = itrial

    thisAR = stimAngRes_deg[idx]
    myLandC.setSize(LandCgapsize_px*thisAR)
    resdat.loc[itrial,'stimsize_AR'] = thisAR
    
    thisori = random.choice(['right','left','up','down'])
    resdat.loc[itrial,'stim_ori'] = thisori
    myLandC.setOri(thisori)

    win.callOnFlip(getRealTimeStampAndStoreToDataFrame,resdat,itrial,'time_stimonset')
    myLandC.draw()
    win.flip()

    allkeys = kb.waitKeys()
    resdat.loc[itrial,'time_resp'] = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    if thisori in allkeys:
        thisResp = True
        # if len(allkeys) == 1:
        #     print('KeyPress.rt: '+str(allkeys[0].rt))
        #     print('KeyPress.tDown: ' + str(allkeys[0].tDown))
    else:
        thisResp = False
    resdat.loc[itrial,'iscorrect'] = thisResp

    # if respstr == thisori:
    if thisResp:
        idx += 1
    else:
        idx -= 1
    
    if idx < 0:
        idx = 0
    elif idx > (len(stimAngRes_deg)-1):
        idx = 3
    else:
        pass

print(resdat[['stimsize_AR','stim_ori','time_stimonset','time_resp','iscorrect']])
print(resdat.time_stimonset)

resdat.to_csv(generateFilename(ok_data,'trial')+'.csv')

win.close()
core.quit()