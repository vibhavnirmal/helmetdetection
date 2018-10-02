import cv2
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import time

camera = cv2.VideoCapture(0)

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        global lmain, var

        self.master.title("Helmet Detection")

        menu = Menu(self.master)
        self.master.config(menu=menu)

        # menu
        file = Menu(menu)
        file.add_command(label="Save")
        file.add_command(label="Exit", command=self.close)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Redo")
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)




        # Graphics window
        imageFrame = Frame(root, width=600, height=500)
        imageFrame.grid(row=4, column=0, padx=10, pady=2)

        # Capture video frames
        lmain = Label(imageFrame)
        lmain.grid(row=0, column=0)

        # Slider window (slider controls stage position)
        sliderFrame = Frame(root, width=600, height=100)
        sliderFrame.grid(row=600, column=0, padx=10, pady=2)



        #live feed label
        livefeed = Label(root, text="Turn On the Live Feed~")
        livefeed.grid(row=1, column=0)

        #Live Feed
        var = IntVar()
        live_check_button = Checkbutton(root, text = "Live Feed", variable= var, command = self.detect)
        live_check_button.grid(row=1, column=1)
        print(var)

        #Select the video feed from your Device
        pic_button = Button(root, text="Get the Video File", fg="blue", width=20, command=self.add_vid)
        pic_button.grid(row=2, column=0)

        #Add the selected Video to the Screen
        add = Button(root, text="Add", fg="green", width=12, command=self.add_vid)
        add.grid(row=2, column=1)
        #
        # # About the Live Feed
        # canvas = Canvas(root, width=400, height=400, bg='#ffffff')
        # canvas.grid(row=4, column=0, rowspan=8, columnspan= 3)

        # showing the Picture that is taken
        canvas = Canvas(root, width=300, height=300, bg='#ffffff')
        canvas.grid(row=4, column=4, rowspan=2)

        withhelmet = Label(root, text="Waring a Helmet"+self.helmet())
        withhelmet.grid(row=6, column=4)

        withouthelmet = Label(root, text="Not Wearing a Helmet"+self.helmet())
        withouthelmet.grid(row=7, column=4)

        # close = Button(root, text="Close", fg="green", width=12, command=self.close)
        # close.grid(row=1, column=8)

    def add_vid(self):
        global vid_path
        vid_path = filedialog.askopenfilename(initialdir="/", title="Select an image file",
                                              filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))

    def show_frame(self):
        i = 100
        while i == 100:
            _, frame = camera.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, self.show_frame)
            i-=1

    def close(self):
        exit()

    def helmet(self):
        # if xxx:
        #     return str(" Yes")
        # else:
        #     return str(" No")
        return str(" Yes")

    def detect(self):
        face_cascade = cv2.CascadeClassifier('..\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('..\Lib\site-packages\cv2\data\haarcascade_eye_tree_eyeglasses.xml')

        camera = cv2.VideoCapture(0)

        while True:
            ret, frame = camera.read()
            print(ret)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]

                eyes = eye_cascade.detectMultiScale(roi_gray)

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            cv2.imshow("camera", imgtk)
            if cv2.waitKey(int(1000 / 12)) & 0xff == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()

root = Tk()

if __name__ == "__main__":
    app = Window(root)

root.mainloop()