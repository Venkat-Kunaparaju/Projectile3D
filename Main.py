from direct.showbase.ShowBase import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from math import *

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.set_var()
        
    def loadModels(self):
        self.scene = self.loader.loadModel("env.egg")
        
        self.scene.reparentTo(self.render)
        self.scene.setScale(40)
        self.ball = self.loader.loadModel("bowlingBall.egg")
        self.ball.reparentTo(self.render)
        self.ball.setPosHprScale(-20,.1,self.height, 0, 0 ,0,  2.5, 2.5, 2.5)
        self.box = self.loader.loadModel("box.egg")
        self.box.reparentTo(self.render)
        self.box.setPosHprScale(-31,.1, 0, 0, 0, 0, 10,10,self.height-1)
        self.box.setColor(0,1,0,1)
       
        
        
    def load_text(self):
        self.update()
        self.text = OnscreenText(text = self.output, pos = (1, .9), scale =.1)
        self.intial = OnscreenText(text = f"Velocity: {round(self.velocity*10, 2)}m/s\nHeight: {round(self.height*10, 2)}m", pos=(0,.9), scale = .1)
    def rotate(self, task):
        self.rotate = self.ball.hprInterval(1, LVector3(180, 180, 180))
        self.rotate.loop()
        self.update()
        self.text.setText(self.output)
        return Task.cont
    def update(self):
        self.output = f"X: {round((self.ball.getX() + 20) * 10,2)}m \nY: {abs(round((self.ball.getZ()) * 10,2))}m \nTime: {round(self.time,2)}s"                                
    def fall(self):
        self.Fall = ProjectileInterval(self.ball, startPos = Point3(-20,.1,self.height), startVel = Point3(self.velocity, 0 , 0),  duration = self.duration, gravityMult = 0.030625 )
        i = LerpFunc(self.time_up, fromData = 0, toData = self.duration, duration = self.duration)
        self.FallSeq = Sequence(Parallel(self.Fall,i), Wait(2))
        self.FallSeq.loop()
    def time_up(self, t):
        self.time = t
        self.update()
    def set_var(self):
        self.entry = DirectEntry(text = "", scale=.1, command=self.set_velocity,
        initialText="Enter Velocity in m/s (between 1 and 50): ", numLines = 1, pos=LVecBase3f(-1,0), focusInCommand = self.clear_text, width = 20)
        self.entry2 = DirectEntry(text = "", scale=.1, command=self.set_height,
        initialText="Enter Height in m (between 1 and 250): ", numLines = 1, pos=LVecBase3f(-1,-.2), focusInCommand = self.clear_text2, width = 20)
            
    def set_height(self, height):
        try:
            height = int(height)
            self.height = height/10
            if(height>=1 and height <= 250):
                self.entry2.destroy()
        except:
            pass
        try:
            self.set_vars()
        except:
            pass
    def set_velocity(self, velocity):
        try:
            velocity = int(velocity)
            self.velocity = velocity/10
            if(velocity >=1 and velocity<=50):
                self.entry.destroy()
        except:
            pass
        try:
            self.set_vars()
        except:
            pass
    def clear_text(self):
        self.entry.enterText(' ')
    def clear_text2(self):
        self.entry2.enterText(' ')
    def set_vars(self):
        self.duration = sqrt((2*self.height)/.98)
        self.time = 0
        self.end = self.duration*self.velocity
        base.disableMouse()
        camera.setPosHpr(0, -64, 24, 0, -12, 0)
        self.loadModels()
        self.load_text()
        self.fall()
        self.taskMgr.add(self.rotate)


game = Game()
game.run() 
