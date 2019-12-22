from direct.showbase.ShowBase import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from math import *

class Game(ShowBase):
    def __init__(self, velocity=20, height=200):
        ShowBase.__init__(self)
        self.height = height/10
        self.velocity = velocity/10
        self.duration = sqrt((2*self.height)/.98)
        self.time = 0
        self.end = self.duration*self.velocity
        base.disableMouse()
        camera.setPosHpr(0, -64, 24, 0, -12, 0)
        self.loadModels()
        self.load_text()
        self.fall()
        self.taskMgr.add(self.rotate)
        
    def loadModels(self):
        self.scene = self.loader.loadModel("env.egg")
        
        self.scene.reparentTo(self.render)
        self.scene.setScale(40)
        self.ball = self.loader.loadModel("bowlingBall.egg")
        self.ball.reparentTo(self.render)
        self.ball.setPosHprScale(-20,.1,self.height, 0, 0 ,0,  2.5, 2.5, 2.5)
        self.box = self.loader.loadModel("models/box")
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
#20m/s max
#200m max
vel = -1
while (vel < 1 or vel > 50):
    
    try:
        vel = float(input("Enter velocity that is greater than or equal to 1 and less than or equal to 50: "))
    except: 
        continue
h = -1
while (h < 1 or h > 250):
    
    try:
        h = float(input("Enter height that is greater than or equal to 1 and less than or equal to 250: "))
    except: 
        continue


game = Game(vel, h)
game.run()