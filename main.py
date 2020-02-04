from tkinter import *
master = Tk()

canvas_width = master.winfo_screenwidth()
canvas_height = master.winfo_screenheight()
canvas = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
canvas.pack()
master.title("UAV Tracking Simulation")#title
master.resizable(0, 0)#stay size always
master.wm_attributes("-topmost", 1)#topmost window

y = int(canvas_height / 2)
class UAV:
    def __init__(self, canvas, color, starting):
        self.canvas = canvas
        self.color = color
        self.pos = starting
        self.starting = starting
        self.id = canvas.create_rectangle(self.starting[0], self.starting[1], self.starting[2], self.starting[3], fill = self.color)
        self.pos = self.canvas.coords(self.id)
    def move(self, x, y):
        self.canvas.move(self.id, x, y)#move
        self.pos = self.canvas.coords(self.id)#reset pos

def animation():
    drone = UAV(canvas, "blue", [100,100,110,110])
animation()
mainloop()