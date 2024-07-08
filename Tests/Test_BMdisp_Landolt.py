import random
import sys
import numpy as np

from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB','sounddevice','pyo','pygame']
from psychopy import core, visual, monitors, sound, gui
from psychopy.tools.monitorunittools import deg2pix, cm2pix
from psychopy.constants import FINISHED
from psychopy.hardware.keyboard import Keyboard

from LandoltC import LandoltC

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
   print(ok_data)
else:
   print('User cancelled')
   core.quit()

isLRflipped = False

if ok_data[1] == 'LF':
   print('LF mode was chosen. Exiting')
   sys.exit()
else:
   realvdist = realdistsdpts[ok_data[2]] # Viewing distance chosen (in cm)
   if ok_data[2] == '1.5 D':
      stimpos = [1.6, 0.0]
   elif (ok_data[2] == '0.5 D') or (ok_data[2] == '0.3 D'):
      stimpos = [0.0, 0.0]
      isLRflipped = True
   elif (ok_data[2] == '1.0 D'): 
      stimpos = [0.55, 0.0]
      isLRflipped = True
   else:
      stimpos = [-3.2, 0.0]

realLandCbrightness = 0.2

NTRIAL = 5

stimSizeLogMAR = np.flip(np.linspace(start=0.6,stop=1.08,num=4)) # LogMAR
stimSizeARdeg = 10.0 ** stimSizeLogMAR / 60 # Angle of resolution = gap size *in deg*

moni_bm = monitors.Monitor('Blackmagic',width=15.8,distance=279)
moni_bm.setSizePix([1920,1080])
moni_bm.setDistance(realvdist)

# Sound setup 
s_Cnotes = sound.Sound('.\sound\Shuttle-96bpm-06Cnotes-01.wav', name='Cnotes', volume=0.1)
s_Asc = sound.Sound('.\sound\Shuttle-96bpm-02ascending-01.wav', name='Ascending', volume=0.05)
s_Desc = sound.Sound('.\sound\Shuttle-96bpm-04descending-01.wav', name='Descending', volume=0.1)

isASC = True

win = visual.Window(monitor=moni_bm, winType='pyglet', allowGUI=False,screen=1,fullscr=True,color=[-1,-1,-1],units='cm')
core.wait(0.5)

kb = Keyboard()

# Initialize the stimulus (LandoltC)
idx = 0
Land_gapdeg = stimSizeARdeg[idx] # deg

myLandC = LandoltC(gappx = deg2pix(Land_gapdeg, moni_bm),ori='right',pwin=win,brightness=realLandCbrightness,centerpos=[cm2pix(stimpos[0], moni_bm),cm2pix(stimpos[1], moni_bm)])

for itrial in range(NTRIAL):
   myLandC.setSize(deg2pix(stimSizeARdeg[idx], moni_bm))
   thisori = random.choice(['right','left','up','down'])
   if isLRflipped:
      if thisori == 'right':
         corrans = 'left'
      elif thisori == 'left':
         corrans = 'right'
      else:
         corrans = thisori
   myLandC.setOri(thisori)
   myLandC.draw()
   win.flip()

   if isASC:
      s_Asc.play()
   else:
      s_Desc.play()
   core.wait(5.7)
   while True:
      if isASC and (s_Asc.status == FINISHED):
         break
      elif (not isASC) and (s_Desc.status == FINISHED):
         break
      else:
         core.wait(0.1)
   isASC = not isASC

   kb.clearEvents()
   s_Cnotes.play()

   keys = kb.waitKeys()
   # if keys == None:
   #    print('No response. quitting')
   #    sys.exit()

   thisResp = None
   if corrans in keys:
      thisResp = 1
   elif 's' in keys:
      break
   else:
      thisResp = 0

   if thisResp:
      idx += 1
      # TODO: Record a correct response
   else:
      idx -= 1
      # TODO: Record an incorrect response
   if idx < 0:
      idx = 0
   elif idx > (len(stimSizeARdeg) - 1):
      idx = len(stimSizeARdeg) -1
   else:
      pass

win.close()
core.quit()