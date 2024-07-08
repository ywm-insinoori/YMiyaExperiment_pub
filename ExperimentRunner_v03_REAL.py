# Experiment runner for real target observation VERSION 3
# Update from Version 2
# - Duration of stimulus (5 sec to 3 sec) and change of tones file
# - Stimulus size steps from 5 to 4, number of trials for one sequence 10 to 8

import random
from datetime import datetime
import numpy as np
import pandas as pd
import winsound

from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB','sounddevice','pyo','pygame']
from psychopy import core, monitors, visual, gui, sound
from psychopy.tools.monitorunittools import deg2pix, cm2pix
from psychopy.constants import FINISHED
from psychopy.hardware.keyboard import Keyboard

from LandoltC import LandoltC

def getRealTimeStampAndStoreToDataFrame(df,rowidx,colname):
    d = datetime.now()
    df.at[rowidx,colname] = d.strftime('%Y-%m-%d-%H-%M-%S-%f')

def generateFilename(subjID:str,tgtdist:str):
    myd = datetime.now()
    return 'LFacm-v3-REAL-trialdata-' + 'Subj{:02}-'.format(int(subjID)) + tgtdist + myd.strftime('-%Y-%m-%d-%H-%M-%S-%f') 

def LUT(input, gamma):
    # input has to be in [-1,1]
    normalizedinput = (input+1)/2 # Not this is [0,1]
    
    normalizedoutput = np.power(normalizedinput, 1/gamma)
    return normalizedoutput * 2 - 1

realdistsdpts = {'0.0 D':None, '0.3 D':279.0, '0.5 D':200.0, '1.0 D':101.0, '1.5 D':64.6, '2.0 D':50.0, '2.5 D':40.0, '3.0 D':32.5, '3.5 D':27.6} # Keys=str indicating (rough) dioptric distances, Vals = float indicating metric distance in cm

dlg = gui.Dlg(title='LF accommodation experiment (v3): real target')
dlg.addText('Participant info')
dlg.addField('* ID:')
dlg.addText('Session info')
dlg.addText('Target type: REAL')
dlg.addField('Target distance:', initial="0.0D", choices=list(realdistsdpts.keys()))
dlgdat = dlg.show()

if dlg.OK:
    if not dlgdat[0]:
        print('PARTICIPANT ID NOT FILLED')
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        core.quit()
    print(f'Starting LF accommodation experiment for Participant {dlgdat[0]}.')
    if dlgdat[1] == '0.0 D':
        print('TARGET DISTANCE NOT PROPERLY SELECTED')
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        core.quit()
    print(f'REAL TARGET DISTANCE: {dlgdat[1]}')
else:
    print('USER CANCELLED')
    core.quit()

NTRIAL = 12
NSIZESTEPS = 4
STIMBRIGHTNESS = 0.765 # 0.765 for equalizing brightness to EOS viewing conditions

thisfilename = generateFilename(dlgdat[0],dlgdat[1].replace(' ',''))
print(thisfilename)

resdat = pd.DataFrame(0, index=list(range(NTRIAL)), 
                      columns=['trial_SN',
                               'disptype',
                               'imgdepth',
                               'stimsize_AR_arcmin',
                               'stim_ori',
                               'time_stimonset',
                               'time_resp',
                               'iscorrect'])
resdat['disptype'] = 'REAL'
resdat['imgdepth'] = dlgdat[1].replace(' ','')
resdat = resdat.astype({'trial_SN':'int',
                        'stimsize_AR_arcmin':'float',
                        'stim_ori':'str',
                        'time_stimonset':'str',
                        'time_resp':'str',
                        'iscorrect':'bool'})

vdist = realdistsdpts[dlgdat[1]] # Viewing distance chosen (in cm)
isLRflipped = False
if dlgdat[1] == '1.5 D':
      stimpos = [1.6, 0.0]
elif (dlgdat[1] == '0.5 D') or (dlgdat[1] == '0.3 D'):
    stimpos = [0.0, 0.0]
    isLRflipped = True
    print('0.5D or 0.3D selected. LR flipped.')
elif (dlgdat[1] == '1.0 D'): 
    stimpos = [0.55, 0.0]
    isLRflipped = True
else:
    stimpos = [-3.2, 0.0]

stimSizeLogMAR = np.flip(np.linspace(start=0.48,stop=1.08,num=NSIZESTEPS)) # LogMAR
stimSizeARdeg = 10.0 ** stimSizeLogMAR / 60 # Angle of resolution = gap size *in deg*

# PsychoPy monitor, sound, window and keyboard setup
moni_bm = monitors.Monitor('Blackmagic',width=15.8,distance=279)
moni_bm.setSizePix([1920,1080])
moni_bm.setDistance(vdist)
print(f'Viewing distance set: {vdist} cm')
BMGAMMA = 3

s_Cnotes = sound.Sound('.\sound\Shuttle-96bpm-06Cnotes-01.wav', name='Cnotes', volume=0.2)
s_Asc = sound.Sound('.\sound\Shuttle-160bpm-02ascending-01.wav', name='Ascending', volume=0.1)
s_Desc = sound.Sound('.\sound\Shuttle-160bpm-04descending-01.wav', name='Descending', volume=0.1)
s_Mark = sound.Sound('.\sound\Shuttle-96bpm-01mark-01.wav', name='Mark', volume=0.8)
s_End = sound.Sound('.\sound\Shuttle-96bpm-03arpeggioH-01.wav', name='SessionEnd', volume=0.8)
isASC = True

win = visual.Window(monitor=moni_bm, winType='pyglet', allowGUI=False,screen=1,fullscr=True,color=[-1,-1,-1],units='cm')
core.wait(0.5)

kb = Keyboard()

# Initialize the stimulus
stimidx = 0
Land_gapdeg = stimSizeARdeg[stimidx] # deg
myLandC = LandoltC(gappx = deg2pix(Land_gapdeg, moni_bm),
                   ori='right',
                   pwin=win,
                   brightness=LUT(STIMBRIGHTNESS,BMGAMMA),
                   centerpos=[cm2pix(stimpos[0], moni_bm),cm2pix(stimpos[1], moni_bm)])

abortsession = False

print('LF display session start')
print('Press S for session abortion')
s_Mark.play()
core.wait(1.8)
while True:
    if s_Mark.status == FINISHED:
        break
    else:
        core.wait(0.1)
kb.waitKeys()

for itrial in range(NTRIAL):
    resdat.at[itrial,'trial_SN'] = itrial+1

    thisAR_deg = stimSizeARdeg[stimidx]
    myLandC.setSize(deg2pix(thisAR_deg, moni_bm))
    resdat.at[itrial,'stimsize_AR_arcmin'] = thisAR_deg * 60

    thisori = random.choice(['right','left','up','down'])

    myLandC.setOri(thisori)
    if isLRflipped:
      if thisori == 'right':
         corrans = 'left'
      elif thisori == 'left':
         corrans = 'right'
      else:
         corrans = thisori
    else:
      corrans = thisori
    resdat.at[itrial,'stim_ori'] = corrans
    win.callOnFlip(getRealTimeStampAndStoreToDataFrame,resdat,itrial,'time_stimonset')
    myLandC.draw()
    win.flip()

    if isASC:
        s_Asc.play()
    else:
        s_Desc.play()
    core.wait(3.4)
    while True:
        if isASC and (s_Asc.status == FINISHED):
            break
        elif (not isASC) and (s_Desc.status == FINISHED):
            break
        else:
            core.wait(0.1)
            print('WAITING FOR TONE END')
    isASC = not isASC
    kb.clearEvents()
    s_Cnotes.play()

    allkeys = kb.waitKeys()
    resdat.at[itrial,'time_resp'] = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    s_Cnotes.stop()
    if corrans in allkeys:
        thisResp = True
    elif 's' in allkeys:
        # Confirmation
        print('S pressed for session abortion. Really want to abort session? Press Y to abort anyway, other keys to continue')
        keys = kb.waitKeys()
        if 'y' in keys:
            abortsession = True
            break
        else:
            continue
    else:
        thisResp = False
    resdat.at[itrial,'iscorrect'] = thisResp

    if thisResp:
        stimidx += 1
    else:
        stimidx -= 1
    
    if stimidx < 0:
        stimidx = 0
    elif stimidx > (len(stimSizeARdeg)-1):
        stimidx = (len(stimSizeARdeg)-1)
    else:
        pass
if abortsession:
    print("SESSION ABORTED")
    thisfilename = 'SESSION_ABORTED-' + thisfilename

s_End.play()

resdat.to_csv('.\\exprdata\\' + thisfilename + '.csv',index=False)

core.wait(1.5)

win.close()
core.quit()