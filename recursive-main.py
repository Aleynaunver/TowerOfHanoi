from tkinter import *
from turtle import TurtleScreen, RawTurtle


class Disc(RawTurtle):
    def __init__(self, cv):
        RawTurtle.__init__(self, cv, shape="square", visible=False)
        self.pu()  
        self.goto(-140, 200)  

   
    def config(self, k, n):
        self.hideturtle()  
        f = float(k + 1) / n  
        self.shapesize(0.5, 1.5 + 5 * f) 
        self.fillcolor(f, 0, 1 - f) 
        self.showturtle()


# The Tower class represents each tower.
class Tower(list):
    # Initializer of the Tower object
    def __init__(self, x):
        self.x = x  

    # Adding the disk to the tower
    def push(self, d):
        d.setx(self.x)  
        d.sety(-70 + 10 * len(self))  
        self.append(d)  

    # Removing the disk from the tower
    def pop(self, y=90):
        d = list.pop(self)  
        d.sety(y) 
        return d


class HanoiEngine:

    def __init__(self, canvas, nrOfDiscs, speed, moveCntDisplay=None):
        self.ts = canvas  
        self.ts.tracer(False) 
        self.designer = RawTurtle(canvas, shape="square")
        self.designer.penup() 
        self.designer.shapesize(0.5, 21)  
        self.designer.goto(0, -80) 
        self.designer.stamp()  
        self.designer.shapesize(7, 0.5) 
        self.designer.fillcolor('darkgreen') 
     
        for x in -140, 0, 140:
            self.designer.goto(x, -5)  
            self.designer.stamp()  

        self.nrOfDiscs = nrOfDiscs  
        self.speed = speed  
        self.moveDisplay = moveCntDisplay 
        self.running = False
        self.moveCnt = 0  
        self.discs = [Disc(canvas) for i in range(10)]  
        self.towerA = Tower(-140)
        self.towerB = Tower(0)  
        self.towerC = Tower(140)
        self.ts.tracer(True)  

    # Adjusting disk speed
    def setspeed(self):
        for disc in self.discs:
            disc.speed(self.speed)  

  
    def hanoi(self, n, src, dest, temp):
        if n > 0:
            for x in self.hanoi(n - 1, src, temp, dest): yield None
            yield self.move(src, dest)
            for x in self.hanoi(n - 1, temp, dest, src): yield None

    
    def move(self, src_tower, dest_tower):
        dest_tower.push(src_tower.pop())  
        self.moveCnt += 1  
        if self.moveDisplay:
            self.moveDisplay(self.moveCnt) 

    # Reset the game
    def reset(self):
        self.ts.tracer(False)  
        self.moveCnt = 0 
        if self.moveDisplay:
            self.moveDisplay(0) 
       
        for t in self.towerA, self.towerB, self.towerC:
            while t != []: t.pop(200)
       
        for k in range(self.nrOfDiscs - 1, -1, -1):
            self.discs[k].config(k, self.nrOfDiscs)
            self.towerA.push(self.discs[k])
        self.ts.tracer(True)  
        self.HG = self.hanoi(self.nrOfDiscs, self.towerA, self.towerC, self.towerB)

    # Run the game
    def run(self):
        self.running = True
        try:
            while self.running:
                result = self.step()
            return result
        except StopIteration:
            return True

    # Performing the next move
    def step(self):
        try:
            next(self.HG)  
            return 2 ** self.nrOfDiscs - 1 == self.moveCnt  
        except TclError:
            return False

    # Stop the game
    def stop(self):
        self.running = False  


class Hanoi:
    def displayMove(self, move):
        self.moveCntLbl.configure(text="Hareket Sayısı:\n%d" % move)
   
    def adjust_nr_of_discs(self, e):
        self.hEngine.nrOfDiscs = self.discs.get() 
        self.reset() 

    def adjust_speed(self, e):
        self.hEngine.speed = self.tempo.get() % 10  
        self.hEngine.setspeed()  

    # Setting the game's start/stop status
    def setState(self, STATE):
        self.state = STATE  

        try:
            if STATE == "START":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")  
                self.discsLbl.configure(fg="black")  
                self.resetBtn.configure(state=DISABLED)
                self.startBtn.configure(text="start",
                                        state=NORMAL)  
                self.stepBtn.configure(state=NORMAL)  

            elif STATE == "RUNNING":
                self.discs.configure(state=DISABLED)  
                self.discs.configure(fg="gray70")  
                self.discsLbl.configure(fg="gray70")  
                self.resetBtn.configure(state=DISABLED) 
                self.startBtn.configure(text="pause",
                                        state=NORMAL)  
                self.stepBtn.configure(state=DISABLED) 

            elif STATE == "PAUSE":
                self.discs.configure(state=NORMAL) 
                self.discs.configure(fg="black")  
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)  
                self.startBtn.configure(text="resume",
                                        state=NORMAL)  
                self.stepBtn.configure(state=NORMAL)  

            elif STATE == "DONE":
                self.discs.configure(state=NORMAL) 
                self.discs.configure(fg="black")  
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)  
                self.startBtn.configure(text="start",
                                        state=DISABLED)
                self.stepBtn.configure(state=DISABLED) 

            elif STATE == "TIMEOUT":
                self.discs.configure(state=DISABLED)  
                self.discs.configure(fg="gray70")  
                self.discsLbl.configure(fg="gray70")  
                self.resetBtn.configure(state=DISABLED) 
                self.startBtn.configure(state=DISABLED) 
                self.stepBtn.configure(state=DISABLED)  

        except TclError:
            pass 


    def reset(self):
        self.hEngine.reset()  
        self.setState("START")

    def start(self):
        if self.state in ["START", "PAUSE"]:
            self.setState("RUNNING") 
            if self.hEngine.run():
                self.setState("DONE") 
            else:
                self.setState("PAUSE")  
        elif self.state == "RUNNING":
            self.setState("TIMEOUT") 
            self.hEngine.stop()  

    def step(self):
        self.setState("TIMEOUT")  
        if self.hEngine.step():
            self.setState("DONE") 
        else:
            self.setState("PAUSE") 



    def __init__(self, nrOfDiscs, speed):
        root = Tk() 
        root.title("Tower of Hanoi") 
        cv = Canvas(root, width=440, height=210, bg="gray90") 
        cv.pack() 
        cv = TurtleScreen(cv)  
        self.hEngine = HanoiEngine(cv, nrOfDiscs, speed, self.displayMove) 
        fnt = ("Arial", 12, "bold")
        attrFrame = Frame(root) 
        self.discsLbl = Label(attrFrame, width=7, height=2, font=fnt,
                              text="Disk Sayısı:\n") 
        self.discs = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=75, showvalue=1, repeatinterval=10,
                           command=self.adjust_nr_of_discs)  
        self.discs.set(nrOfDiscs) 
        self.tempoLbl = Label(attrFrame, width=8, height=2, font=fnt,
                              text="   Hız:\n")  
        self.tempo = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=100, showvalue=1, repeatinterval=10,
                           command=self.adjust_speed)  
        self.tempo.set(speed)  
        self.moveCntLbl = Label(attrFrame, width=5, height=2, font=fnt,
                                padx=20, text=" Hareket Sayısı:\n0",
                                anchor=CENTER) 
        for widget in (self.discsLbl, self.discs, self.tempoLbl, self.tempo,
                       self.moveCntLbl):
            widget.pack(side=LEFT)
        attrFrame.pack(side=TOP)  
        ctrlFrame = Frame(root)  
        self.resetBtn = Button(ctrlFrame, width=11, text="Reset", font=fnt,
                               state=DISABLED, padx=15, command=self.reset) 
        self.stepBtn = Button(ctrlFrame, width=11, text="Step", font=fnt,
                              state=NORMAL, padx=15, command=self.step)  
        self.startBtn = Button(ctrlFrame, width=11, text="Start", font=fnt,
                               state=NORMAL, padx=15, command=self.start)  
        for widget in self.resetBtn, self.stepBtn, self.startBtn:
            widget.pack(side=LEFT)
        ctrlFrame.pack(side=TOP)  

        self.state = "START" 
        root.mainloop()  


if __name__ == "__main__":
    Hanoi(7, 3) 
