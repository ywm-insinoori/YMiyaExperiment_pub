from psychopy.visual import Rect, Circle

class LandoltC:
    def __init__(self, gappx, pwin, ori='right', centerpos=[0,0], brightness=1):
        self.gappx = gappx
        self.ori = ori
        self.pwin = pwin
        self.centerpos = centerpos
        self.brightness = brightness

        self.Ocirc = Circle(win=pwin,units='pix',radius=2.5*self.gappx,fillColor=brightness,lineWidth=0,edges=128)
        self.Ocirc.pos = self.centerpos
        self.Icirc = Circle(win=pwin,units='pix',radius=1.5*self.gappx,fillColor=-1,lineWidth=0,edges=128)
        self.Icirc.pos = self.centerpos
        self.gaprect = Rect(win=pwin,units='pix',size=[2.5*self.gappx,self.gappx],lineColor=-1,lineWidth=0,fillColor=-1)
        self.gaprect.pos = [self.centerpos[0]+1.25*self.gappx, self.centerpos[1]]

        self.setOri(ori=self.ori)

        # self.Ocirc.draw()
        # self.Icirc.draw()
        # self.gaprect.draw()

    def setOri(self, ori='right'):
        self.ori = ori
        if self.ori == 'right':
            self.gaprect.ori = 0
            self.gaprect.pos = [self.centerpos[0]+1.25*self.gappx, self.centerpos[1]]
        elif self.ori == 'left':
            self.gaprect.ori = 0
            self.gaprect.pos = [self.centerpos[0]-1.25*self.gappx, self.centerpos[1]]
        elif self.ori == 'up':
            self.gaprect.ori = 90
            self.gaprect.pos = [self.centerpos[0], self.centerpos[1]+1.25*self.gappx]
        elif self.ori == 'down':
            self.gaprect.ori = 90
            self.gaprect.pos = [self.centerpos[0], self.centerpos[1]-1.25*self.gappx]
        else:
            print('Error: select LandoltC orientation from \'right\',\'left\',\'up\', or \'down\'')
    
    def setSize(self, newgappx):
        self.gappx = newgappx
        self.Ocirc.radius = 2.5*self.gappx
        self.Icirc.radius = 1.5*self.gappx
        self.gaprect.size = [2.5*self.gappx,self.gappx]
        self.setOri(ori=self.ori) # Because the position of the gaprect should change
    
    def setCenterPos(self, newcenter):
        self.Ocirc.pos = [self.Ocirc.pos[0] - self.centerpos[0] + newcenter[0], self.Ocirc.pos[1] - self.centerpos[1] + newcenter[1]]
        self.Icirc.pos = [self.Icirc.pos[0] - self.centerpos[0] + newcenter[0], self.Icirc.pos[1] - self.centerpos[1] + newcenter[1]]
        self.gaprect.pos = [self.gaprect.pos[0] - self.centerpos[0] + newcenter[0], self.gaprect.pos[1] - self.centerpos[1] + newcenter[1]]
        self.centerpos = newcenter
    
    def setBrightness(self, newbrightness):
        self.Ocirc.fillColor = newbrightness
        self.brightness = newbrightness

    def draw(self):
        self.Ocirc.draw()
        self.Icirc.draw()
        self.gaprect.draw()