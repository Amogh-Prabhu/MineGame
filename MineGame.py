import tkinter
import random
from tkinter.font import BOLD
import tkinter.messagebox
import time
from PIL import Image
from typing import final

# Main window of the game
window = tkinter.Tk()

# Timer
currTime = 0
timer = 0

# Level of the game
level = 2
levels = [10,16,18]
n = levels[level - 1]
level = n/8

# Game status
gameOver = False
win = False
flag = False

# Colors used in this game
colors = {
    "Grey": "#708080",
    "Red": "#993000",
    "White": "#FFFFFF",
    "Green": "#009900",
    "Purple": "#570861",
    "DCyan": "#309999",
    "Cyan": "#50FFFF",
    "Background": "#110F39",
}

# Images used in this game
image = Image.open("Images\\image.png").resize((round(level * 207), round(level * 190)), Image.ANTIALIAS)
image.save("Images\\intro.png", "png")
image = {
    "ebomb": tkinter.PhotoImage(file= r"Images\\eBomb.png").subsample(14,14),
    "bomb": tkinter.PhotoImage(file= r"Images\\bomb.png").subsample(14,14),
    "flag": tkinter.PhotoImage(file= r"Images\\flag.png").subsample(20,20),
    "intro": tkinter.PhotoImage(file= r"Images\\intro.png"),
    "none": '',
}

class GameButton:
    def __init__(self, gameFrame, i, j, buttons,bombs, parent):
        self.i = i
        self.j = j
        self.flag = False
        self.index = n*i+j
        self.bombs = bombs
        self.parent = parent
        self.pressed = False
        self.color = colors["Grey"]
        self.button = tkinter.Button(
            gameFrame,
            width = 2,
            height = 1,
            bg=self.color, 
            command = lambda: self.onPressed(buttons)
        )
        self.checkNum()

    def checkNum(self):
        self.type = 0
        if self.index in self.bombs:
            self.type = -1
        else:
            surrBomb = 0
            if self.i!=0 and self.index - n in self.bombs:
                surrBomb+=1
            if self.i!=0 and self.j!=0 and self.index - (n+1) in self.bombs:
                surrBomb+=1
            if self.i!=0 and self.j!=(n-1) and self.index - (n-1) in self.bombs:
                surrBomb+=1
            if self.i!=(n-1) and self.index + n in self.bombs:
                surrBomb+=1
            if self.i!=(n-1) and self.j!=0 and self.index + (n-1) in self.bombs:
                surrBomb+=1
            if self.i!=(n-1) and self.j!=n-1 and self.index + (n+1) in self.bombs:
                surrBomb+=1
            if self.j!=0 and self.index - 1 in self.bombs:
                surrBomb+=1
            if self.j!=(n-1) and self.index + 1 in self.bombs:
                surrBomb+=1
            
            self.type = surrBomb

    def onPressed(self, buttons):
        global currTime
        global flag
        global gameOver
        global win
        if(currTime == 0):
            currTime = time.time()

        if flag == True and self.pressed != True:
            if self.flag == True:
                self.button.config(image = image["none"], width = 2,height = 1)
                self.flag = False
                return
            else:
                self.button.config(image = image["flag"], width = 18,height = 20)
                self.flag = True
                return

        if self.flag == False:
            self.pressed = True
            snapshot = []
            if self.type == -1:
                self.color = colors["Red"]
                for bomb in self.bombs:
                    buttons[bomb].button.config(bg = self.color, image = image["bomb"], width = 18,height = 20)
                    buttons[bomb].color = self.color
                self.button.config(image = image["ebomb"])
                tkinter.messagebox.showerror("Game Over","Game Over")
                gameOver = True

            elif self.type != 0:
                self.color = colors["White"]
                self.button.config(text = self.type, bg=self.color, relief=tkinter.SUNKEN)
            else:
                self.color = colors["White"]
                self.button.config(bg=self.color, relief=tkinter.SUNKEN)
                if self.j!=0:
                    buttons[self.index-1].checkWhite(buttons, snapshot)
                if self.j!=(n-1):
                    buttons[self.index+1].checkWhite(buttons, snapshot)
                if self.i!=0:
                    buttons[self.index- n].checkWhite(buttons, snapshot)
                if self.i!=(n-1):
                    buttons[self.index+ n].checkWhite(buttons, snapshot)

                if self.i!=0 and self.j!=0:
                    buttons[self.index - (n+1)].checkWhite(buttons, snapshot)

                if self.i!=0 and self.j!=(n-1):
                    buttons[self.index - (n-1)].checkWhite(buttons, snapshot)

                if self.i!=(n-1) and self.j!=0:
                    buttons[self.index + (n-1)].checkWhite(buttons, snapshot)

                if self.i!=(n-1) and self.j!=n-1:
                    buttons[self.index + (n+1)].checkWhite(buttons, snapshot)

            testFlag = 0
            for button in buttons:
                if button.type != -1 and button.color == colors["Grey"]:
                    testFlag = 1
            if testFlag == 0:
                for bomb in self.bombs:
                    buttons[bomb].button.config(bg = colors["Green"])
                    buttons[bomb].button.config(image = image["bomb"], width = 18,height = 20)
                tkinter.messagebox.showinfo("MineGame","You won!!")
                gameOver = True
                win = True

    def checkWhite(self, buttons, snapshot):
        if self.flag == False:
            if self.type == 0:
                self.color = colors["White"]
                self.button.config(bg=self.color, relief=tkinter.SUNKEN)
                self.pressed = True
                if self.j!=0 and buttons[self.index-1] not in snapshot:
                    snapshot.append(buttons[self.index-1])
                    buttons[self.index-1].checkWhite(buttons, snapshot)

                if self.j!=(n-1) and buttons[self.index+1] not in snapshot:
                    snapshot.append(buttons[self.index+1])
                    buttons[self.index+1].checkWhite(buttons, snapshot)

                if self.i!=0 and buttons[self.index- n] not in snapshot:
                    snapshot.append(buttons[self.index- n])
                    buttons[self.index- n].checkWhite(buttons, snapshot)

                if self.i!=(n-1) and buttons[self.index+ n] not in snapshot:
                    snapshot.append(buttons[self.index+ n])
                    buttons[self.index+ n].checkWhite(buttons, snapshot)

                if self.i!=0 and self.j!=0 and buttons[self.index - (n+1)] not in snapshot:
                    snapshot.append(buttons[self.index - (n+1)])
                    buttons[self.index - (n+1)].checkWhite(buttons, snapshot)

                if self.i!=0 and self.j!=(n-1) and buttons[self.index - (n-1)] not in snapshot:
                    snapshot.append(buttons[self.index - (n-1)])
                    buttons[self.index - (n-1)].checkWhite(buttons, snapshot)

                if self.i!=(n-1) and self.j!=0 and buttons[self.index + (n-1)] not in snapshot:
                    snapshot.append(buttons[self.index + (n-1)])
                    buttons[self.index + (n-1)].checkWhite(buttons, snapshot)

                if self.i!=(n-1) and self.j!=n-1 and buttons[self.index + (n+1)] not in snapshot:
                    snapshot.append(buttons[self.index + (n+1)])
                    buttons[self.index + (n+1)].checkWhite(buttons, snapshot)

            elif self.type!=-1:
                self.color = colors["White"]
                self.pressed = True
                self.button.config(text = self.type, bg=self.color, relief=tkinter.SUNKEN)
        
class BuildGame:
    def __init__(self, parent):
        self.parent = parent
        bombs = []
        for i in range(0,n*n,n):
            for j in range(n//16+1):
                bombs.append(random.randrange(i,i+n))
        
        Buttons = []

        for i in range(n):
            for j in range(n):
                Buttons.append(GameButton(self.parent, i, j, Buttons, bombs, window))

        for i in range(n):
            for j in range(n):
                Buttons[n*i+j].button.grid(row = i, column = j)

class BuildFlag:
    def __init__(self, parent):
        self.pressed = False
        self.flagButton = tkinter.Button(
            parent,
            text = "Flag",
            bg = colors["DCyan"],
            image = image["flag"],
            command = self.onPressed
        )
        self.flagButton.pack()

    def onPressed(self):
        global flag
        if self.pressed:
            self.pressed = False
            flag = False
            self.flagButton.config(relief = tkinter.RAISED, bg = colors["DCyan"])
        else:
            self.pressed = True
            flag = True
            self.flagButton.config(relief = tkinter.SUNKEN, bg = colors["Cyan"])

class BuildTimer:
    def __init__(self, parent):
        self.timeLabel = tkinter.Label(
            mainFrame, 
            font = ["Consolas", 15 if(level != 1) else 11, BOLD], 
            bg = "black", 
            fg = colors["Cyan"]
        )
        self.timeLabel.place(x = 1 , y = 7 if(level != 1) else 10) 
        self.digitalClock() 
    
    def digitalClock(self):
        global timer
        if currTime != 0:
            timer = round((time.time() - currTime))
        else:
            timer = 0
        string = "{0:02}:{1:02}:{2:02}".format(timer//3600,timer//60,timer-(timer//3600)*3600-(timer//60)*60)
        self.timeLabel.config(text = string)
        if not gameOver:
            self.timeLabel.after(100, self.digitalClock)
        else:
            window.destroy()

            endWindow = tkinter.Tk()
            endWindow.config(bg = colors["Background"])
            endWindow.title("Result")

            finalLabel = tkinter.Label(
                endWindow, 
                text = "Your Score:" if win else "\nBetter luck\nnext time!", 
                font = ["Consolas", 30, BOLD], 
                bg = colors["Background"], 
                fg = colors["Cyan"],
            )
            if win:
                scoreLabel = tkinter.Label(
                    endWindow,
                    text = timer,
                    font = ["Consolas", 40, BOLD], 
                    bg = colors["Background"], 
                    fg = colors["Cyan"]
                )

                scoreLabel.place(
                    relx = 0.5,
                    rely = 0.7,
                    anchor = 'center'
                )

            finalLabel.place(
                relx = 0.5,
                rely = 0.4,
                anchor = 'center'
            )
            endWindow.geometry("300x300")
            endWindow.mainloop()


# Main body

window.title("MineGame")
window.config(
    bg = colors["Background"], 
    padx=10,
    pady=10
)

introFrame = tkinter.Frame(
    window, 
    pady = round(20*level), 
    bg = colors["Background"]
)
label = tkinter.Label(
    introFrame,
    image = image["intro"],
    bg = colors["Background"],
)
label.pack()
introFrame.pack()

mainFrame = tkinter.Frame(
    window,
    bg = colors["Background"],
)
gameFrame = tkinter.Frame(      
        mainFrame, 
        borderwidth=10, 
        relief="solid",
        bg = colors["Background"]
)

optionFrame = tkinter.Frame(
        mainFrame,
        pady = 5,
        bg = colors["Background"],
)

BuildTimer(window)
BuildFlag(optionFrame)
BuildGame(gameFrame)

def game():
    introFrame.destroy()
    mainFrame.pack()
    optionFrame.pack()
    gameFrame.pack()

window.after(2000, game)
window.resizable(width=False, height=False)
window.mainloop()
