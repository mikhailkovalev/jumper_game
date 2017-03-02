#!/usr/bin/python3

from managers import *



manager = JumperManager()
manager.run()



# root = tk.Tk()

# root.title('Jumper')

# canvas = tk.Canvas()

# canvas.pack()

#

# bg = Image.open('./images/background.png')

# jumper_img = Image.open('./images/doodle.png')

# platform_img = Image.open('./images/platform.png')

# # print(bg.size)

# canvas.config(width = bg.size[0], height = bg.size[1])

#

# tkbg = ImageTk.PhotoImage(bg)

# tk_jumper_img = ImageTk.PhotoImage(jumper_img)

# tk_platform_img = ImageTk.PhotoImage(platform_img)

#

# context = TkContext(canvas)

# context.drawImage(0, 0, tkbg)

# context.drawImage(125, 213, tk_jumper_img)

# context.drawImage(100, 450, tk_platform_img)

#

# root.mainloop()
