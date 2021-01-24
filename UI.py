from ImageCollectorClass import ImageGrabber
from tkinter import *
from tkinter import ttk
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from PIL.ImageTk import PhotoImage
from PIL import Image
import os
from natsort import natsorted as ns
import time
import pandas as pd


root = Tk()
root.title('Pinterest Bot')
bot = None


def grab_images(search, total_no, dir_name, progress):
    global bot
    search = search.get(1.0, 'end').replace('\n', '')
    if total_no.get(1.0, 'end').replace('\n', ''):
        total_no = int(total_no.get(1.0, 'end').replace('\n', ''))
    else:
        total_no = None
    dir_name = dir_name.get(1.0, 'end').replace('\n', '')

    if search and total_no and dir_name:
        bot = ImageGrabber(search, total_no, dir_name, progress)
        images_list(dir_name)


def images_list(dir_name):
    images = ns(os.listdir(dir_name))[:-1 ]
    for i in range(len(images)):
        collected_images.insert(i, images[i])


def selected_image(event):
    global bot
    caption_image.config(state=NORMAL)
    caption_image.delete(1.0, 'end')
    folder_name = dir_text.get(1.0, 'end').replace("\n", "")
    print(collected_images.get(collected_images.curselection()))
    image_name = collected_images.get(collected_images.curselection())
    img_path = folder_name+"/"+image_name
    img = Image.open(img_path)
    img.thumbnail((400, 300), Image.ANTIALIAS)
    img = PhotoImage(img)
    image_box.configure(image=img)
    image_box.image = img

    df = pd.read_csv(folder_name+"/"+folder_name+".csv")
    data = df.loc[df['Image Name'] == image_name]
    data = data['Caption'].values[0]
    caption_image.insert(INSERT, data)
    caption_image.config(state=DISABLED)


def reset():
    caption_image.config(state=NORMAL)
    dir_text.delete(1.0, END)
    total_text.delete(1.0, END)
    search_text.delete(1.0, END)
    collected_images.delete(0, 'end')
    caption_image.delete(1.0, END)
    image_box.config(image='')
    progress['value'] = 0
    progress.update()


frame = Frame(root, width=800, height=900)
frame.pack()
canvas = Canvas(root, bg='#ececec')
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

img1 = Image.open('Images/logo.png')
img1.thumbnail((200, 200), Image.ANTIALIAS)
img1 = PhotoImage(img1)
logo1 = Label(canvas, image=img1, bg="#ececec")
logo1.place(relx=0.23, rely=0.03, relwidth=0.32, relheight=0.12)

img2 = Image.open('Images/Bot.png')
img2.thumbnail((150, 100), Image.ANTIALIAS)
img2 = PhotoImage(img2)
logo2 = Label(canvas, image=img2, bg="#ececec")
logo2.place(relx=0.52, rely=0.01, relwidth=0.15, relheight=0.12)

# img3 = Image.open('Images/logo1.png')
# img3.thumbnail((30, 30), Image.ANTIALIAS)
# img3 = PhotoImage(img3)
# logo3 = Label(canvas, image=img3, bg="black")
# logo3.place(relx=0.63, rely=0.085, relwidth=0.035, relheight=0.027)

search_box = LabelFrame(canvas, text="Search Box", bg="#ececec", bd=3, font="Helvetica 16 bold")
search_box.place(relx=0.08, rely=0.15, relwidth=0.35, relheight=0.38)


search_label = Label(canvas, text='Search Image:', font="Helvetica 16 bold", bg='#ececec')
search_label.place(relx=0.1, rely=0.2, relwidth=0.15, relheight=0.05)

search_text = Text(canvas, bd=3, font="Helvetica 16 bold")
search_text.place(relx=0.25, rely=0.2, relwidth=0.15, relheight=0.05)

total_label = Label(canvas, text='Total Images:', font="Helvetica 16 bold", bg='#ececec')
total_label.place(relx=0.096, rely=0.29, relwidth=0.15, relheight=0.05)

total_text = Text(canvas, bd=3, font="Helvetica 16 bold")
total_text.place(relx=0.25, rely=0.29, relwidth=0.15, relheight=0.05)

dir_label = Label(canvas, text='Name Folder:', font="Helvetica 16 bold", bg='#ececec')
dir_label.place(relx=0.096, rely=0.38, relwidth=0.15, relheight=0.05)

dir_text = Text(canvas, bd=3, font="Helvetica 16 bold")
dir_text.place(relx=0.25, rely=0.38, relwidth=0.15, relheight=0.05)

progress = ttk.Progressbar(canvas, length=100, orient=VERTICAL, mode='determinate')
progress.place(relx=0.45, rely=0.2, relwidth=0.1, relheight=0.3)

search_button = Button(canvas, text='Search', font="Helvetica 16 bold", command=lambda: grab_images(search_text, total_text, dir_text, progress))
search_button.place(relx=0.25, rely=0.46, relwidth=0.15, relheight=0.05)

grabbed_box = LabelFrame(canvas, text="Grabbed Images", bg="#ececec", bd=3, font="Helvetica 16 bold")
grabbed_box.place(relx=0.575, rely=0.15, relwidth=0.35, relheight=0.38)

collected_images = Listbox(canvas, bd=3, font="Helvetica 18 bold", yscrollcommand=True, selectmode=SINGLE)
collected_images.bind('<<ListboxSelect>>', selected_image)
collected_images.place(relx=0.6, rely=0.185, relwidth=0.3, relheight=0.32)

selected_box = LabelFrame(canvas, text="Selected Image", bg="#ececec", bd=3, font="Helvetica 16 bold")
selected_box.place(relx=0.08, rely=0.6, relwidth=0.35, relheight=0.38)

# img = Image.open('cats/cats4.jpg')
# img.thumbnail((250, 290), Image.ANTIALIAS)
# img = PhotoImage(img)
image_box = Label(canvas, bg="#ececec", bd=3)
image_box.place(relx=0.095, rely=0.63, relwidth=0.32, relheight=0.33)

caption_box = LabelFrame(canvas, text="Image Caption", bg="#ececec", bd=3, font="Helvetica 16 bold")
caption_box.place(relx=0.575, rely=0.6, relwidth=0.35, relheight=0.16)

caption_image = Text(canvas, borderwidth=2, font="Helvetica 16 bold")
caption_image.place(relx=0.6, rely=0.64, relwidth=0.3, relheight=0.1)
caption_image.tag_configure("center", justify='center')
caption_image.tag_add("center", 1.0, "end")

reset_button = Button(canvas, text='Reset', font="Helvetica 16 bold", command=lambda: reset())
reset_button.place(relx=0.65, rely=0.85, relwidth=0.2, relheight=0.05)

root.mainloop()