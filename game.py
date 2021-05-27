import json
from tkinter import *
from PIL import ImageTk, Image

"""
    Reading Files saved in sample.json
"""
with open('sample.json') as data:
    dataDict = dict(json.load(data))

# All the Constant Values Used in the program is kept here
BOARDSIZE = 600
NOOFDOTS = 10
DOTCOLOR = "#000000"
DOTWIDTH = 0.25 * (BOARDSIZE/NOOFDOTS)
DOTSEPERATION = BOARDSIZE / NOOFDOTS
SHAPES = dataDict


class Geoboard():
    def __init__(self):
        self.window = Tk()
        self.window.title('GoeBoard')
        self.window.iconbitmap(r"Geoboard.ico")
        self.window.minsize(1200, 600)
        self.window.maxsize(1200, 600)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        self.canvas = Canvas(
            self.window, width=BOARDSIZE, height=BOARDSIZE, bd=-2)
        self.image = ImageTk.PhotoImage(Image.open("background.jpg"))
        self.canvas.grid(row=0, column=0, rowspan=3, sticky="nsew")

        self.frameCreateShapes = Frame(self.window)
        self.frameEditShapes = Frame(self.window)
        self.frameDeleteShapes = Frame(self.window)
        self.frameOpenShapes = Frame(self.window)

        for frame in (self.frameCreateShapes, self.frameOpenShapes, self.frameEditShapes, self.frameDeleteShapes):
            frame.grid(row=0, column=1, sticky="nsew")

        self.rightFrame = Frame(self.window)
        self.rightFrame.grid(row=1, column=1, sticky="nsew")
        self.gapFrame = Frame(self.window)
        self.gapFrame.grid(row=2, column=1, sticky="nsew")

        self.coords = []
        self.COORDS = []
        self.editName = StringVar()
        self.toX = 0
        self.toY = 0
        self.fromX = 0
        self.fromY = 0

        self.refresh_board()
        self.showFrame(self.frameCreateShapes)

        self.rightFramePage()
        self.gapFramePage()

    def showFrame(self, frame):
        """
            All the frames are stacked over one another. This function takes the given frame and puts it 
            on the top of the stack i.e. the frame will be visible to the user. 
        """
        frame.tkraise()

    def gapFramePage(self):
        """
            This function is just to give a small margin bellow the 4 buttons of rightFrame
        """
        gap0 = Label(self.gapFrame,
                     text="             ")
        gap0.pack(fill="x")

    def createButtomCommand(self):
        """
            This function call the showFram function which means whenever this function is called the create 
            page will be visible to the user as this function will be called by the "Create Page" button.
            And secondly this function re-initalizes the create shapes frame so everything looks realtime.
        """
        self.showFrame(self.frameCreateShapes)
        self.frameCreateShape()

    def openButtomCommand(self):
        """
            This function call the showFram function which means whenever this function is called the open 
            page will be visible to the user as this function will be called by the "Open Page" button.
            And secondly this function re-initalizes the open shapes frame so everything looks realtime.
        """
        self.showFrame(self.frameOpenShapes)
        self.frameOpenShape()

    def deleteButtomCommand(self):
        """
            This function call the showFram function which means whenever this function is called the delete 
            page will be visible to the user as this function will be called by the "Delete Page" button.
            And secondly this function re-initalizes the delete shapes frame so everything looks realtime.
        """
        self.showFrame(self.frameDeleteShapes)
        self.frameDeleteShape()

    def editButtomCommand(self):
        """
            This function call the showFram function which means whenever this function is called the edit 
            page will be visible to the user as this function will be called by the "Edit Page" button.
            And secondly this function re-initalizes the edit shapes frame so everything looks realtime.
        """
        self.showFrame(self.frameEditShapes)
        self.frameEditShape()

    def rightFramePage(self):
        """
            This is frontend design code of the rightFrame ( or the frame containing the 4 button, you can refer to AU20B1011_A2_GeoboardDesignLayout.png )
        """
        gap1 = Label(self.rightFrame,
                     text="                 ")
        gap2 = Label(self.rightFrame,
                     text="      ")
        gap3 = Label(self.rightFrame,
                     text="      ")
        gap4 = Label(self.rightFrame,
                     text="      ")
        createShapesButton = Button(self.rightFrame, padx=15,
                                    pady=10, activebackground="#000", background="#fff", text="Create Shapes", command=lambda: self.createButtomCommand(), borderwidth=0)
        openShapesButton = Button(self.rightFrame, padx=15,
                                  pady=10, activebackground="#000", background="#fff", text="Open Shapes", command=lambda: self.openButtomCommand(), borderwidth=0)
        editShapesButton = Button(self.rightFrame, padx=15,
                                  pady=10, activebackground="#000", background="#fff", text="Edit Shapes", command=lambda: self.editButtomCommand(), borderwidth=0)
        deleteShapesButton = Button(self.rightFrame, padx=15,
                                    pady=10, activebackground="#000", background="#fff", text="Delete Shapes", command=lambda: self.deleteButtomCommand(), borderwidth=0)
        gap1.grid(row=0, column=0)
        createShapesButton.grid(row=1, column=1)
        gap2.grid(row=0, column=2)
        openShapesButton.grid(row=1, column=3)
        gap3.grid(row=0, column=4)
        editShapesButton.grid(row=1, column=5)
        gap4.grid(row=0, column=6)
        deleteShapesButton.grid(row=1, column=7)

    def frameCreateShape(self):
        """
            This is frontend design code of the Create Page or create shapes frame ( you can refer to AU20B1011_A2_GeoboardDesignLayout.png )
            The 2 main functions of this function is that:
            1. First off all it clears out the canvas so their are no prebuilt lines or shapes on it
            2. Secondly it clears out the whole frame and rebuilts it to make the data flow realtime.
        """
        self.refresh_board()
        for widgets in self.frameCreateShapes.winfo_children():
            widgets.destroy()
        self.canvas.bind('<Button-1>', self.click)
        frame1Canvas = Canvas(self.frameCreateShapes, width=200)
        frame1Canvas.pack(anchor=CENTER, expand=True)
        name = StringVar()
        frame1Input = Entry(frame1Canvas, textvariable=name,
                            borderwidth=0, background="white")
        frame1Input.pack(anchor=CENTER, expand=True)
        frame1Button = Button(frame1Canvas, padx=15,
                              pady=10, activebackground="#000", background="#fff", text="Save", command=lambda: self.saveShape(frame1Input, self.COORDS), borderwidth=0)
        frame1Button.pack(anchor=CENTER, expand=True)

    def frameOpenShape(self):
        """
            This is frontend design code of the Open Page or open shapes frame ( you can refer to AU20B1011_A2_GeoboardDesignLayout.png )
            The 2 main functions of this function is that:
            1. First off all it clears out the canvas so their are no prebuilt lines or shapes on it
            2. Secondly it clears out the whole frame and rebuilts it to make the data flow realtime.
        """
        self.refresh_board()
        for widgets in self.frameOpenShapes.winfo_children():
            widgets.destroy()
        self.canvas.unbind('<Button-1>')
        datalist = list(SHAPES.keys())
        frame2Canvas = Canvas(self.frameOpenShapes, width=200)
        frame2Canvas.pack(anchor=CENTER, expand=True)
        name = StringVar()
        frame2Input = Entry(frame2Canvas, textvariable=name,
                            borderwidth=0, background="white")
        frame2Input.pack(anchor=CENTER, expand=True)
        frame2Button = Button(frame2Canvas, padx=15,
                              pady=10, activebackground="#000", background="#fff", text="Open", command=lambda: self.openShape(frame2Input, self.COORDS), borderwidth=0)
        frame2Button.pack(anchor=CENTER, expand=True)
        if SHAPES:
            for i in datalist:
                names = Label(frame2Canvas, text=i)
                names.pack()
        else:
            none = Label(frame2Canvas, text="No Shapes Found")
            none.pack()

    def frameEditShape(self):
        """
            This is frontend design code of the Edit Page or edit shapes frame ( you can refer to AU20B1011_A2_GeoboardDesignLayout.png )
            The 2 main functions of this function is that:
            1. First off all it clears out the canvas so their are no prebuilt lines or shapes on it
            2. Secondly it clears out the whole frame and rebuilts it to make the data flow realtime.
        """
        self.refresh_board()
        for widgets in self.frameEditShapes.winfo_children():
            widgets.destroy()
        self.canvas.unbind("<Button-1>")
        self.canvas.bind('<Button-1>', self.editClick)
        datalist = list(SHAPES.keys())
        frame4Canvas = Canvas(self.frameEditShapes, width=200)
        frame4Canvas.pack(anchor=CENTER, expand=True)
        frame4Input = Entry(frame4Canvas, textvariable=self.editName,
                            borderwidth=0, background="white")
        frame4Input.pack(anchor=CENTER, expand=True)
        frame4Button = Button(frame4Canvas, padx=15,
                              pady=10, activebackground="#000", background="#fff", text="Edit", command=lambda: self._extracted_from_editShape_(frame4Input, SHAPES, self.COORDS), borderwidth=0)
        frame4Button.pack(anchor=CENTER, expand=True)
        if SHAPES:
            for i in datalist:
                names = Label(frame4Canvas, text=i)
                names.pack()
        else:
            none = Label(frame4Canvas, text="No Shapes Found")
            none.pack()

    def frameDeleteShape(self):
        """
            This is frontend design code of the Delete Page or delete shapes frame ( you can refer to AU20B1011_A2_GeoboardDesignLayout.png )
            The 2 main functions of this function is that:
            1. First off all it clears out the canvas so their are no prebuilt lines or shapes on it
            2. Secondly it clears out the whole frame and rebuilts it to make the data flow realtime.
        """
        self.refresh_board()
        for widgets in self.frameDeleteShapes.winfo_children():
            widgets.destroy()
        self.canvas.unbind('<Button-1>')
        datalist = list(SHAPES.keys())
        frame3Canvas = Canvas(self.frameDeleteShapes, width=200)
        frame3Canvas.pack(anchor=CENTER, expand=True)
        name = StringVar()
        frame3Input = Entry(frame3Canvas, textvariable=name,
                            borderwidth=0, background="white")
        frame3Input.pack(anchor=CENTER, expand=True)
        frame3Button = Button(frame3Canvas, padx=15,
                              pady=10, activebackground="#000", background="#fff", text="Delete", command=lambda: self.deleteShape(frame3Input, self.COORDS), borderwidth=0)
        frame3Button.pack(anchor=CENTER, expand=True)
        if SHAPES:
            for i in datalist:
                names = Label(frame3Canvas, text=i)
                names.pack()
        else:
            none = Label(frame3Canvas, text="No Shapes Found")
            none.pack()

    def is_Dot(self, x, y):
        """
            This function checks that the point on canvas where user is clicking is the black dot / nail or not. 
            If yes then it returns True elsr False.
        """
        isDot = False
        index = 0
        for i in self.coords:
            for j in range(i[0], i[2]):
                for k in range(i[1], i[3]):
                    if (j, k) == (x, y):
                        isDot = True
                        break
                if (j, k) == (x, y):
                    break
            index += 1
            if (j, k) == (x, y):
                break
        return (isDot, index)

    # New Board Logic

    def refresh_board(self):
        """
            The main function of this function is that first it clears out everything on canvas and then 
            rebuilt it so that their are lines remaining on the canvas. And also prints the canvas on the first run.
        """
        self.canvas.delete("all")
        self.COORDS = []
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        for i in range(NOOFDOTS):
            start_x = i*DOTSEPERATION+DOTSEPERATION/2
            for j in range(NOOFDOTS):
                end_x = j*DOTSEPERATION+DOTSEPERATION/2
                self.canvas.create_oval(start_x-DOTWIDTH/2, end_x-DOTWIDTH/2, start_x+DOTWIDTH/2,
                                        end_x+DOTWIDTH/2, fill=DOTCOLOR,
                                        outline=DOTCOLOR)
                self.coords.append([int(end_x-DOTWIDTH/2), int(start_x-DOTWIDTH/2), int(end_x+DOTWIDTH/2),
                                    int(start_x+DOTWIDTH/2)])

    # Mouse Click Logic

    def click(self, event):
        """
            This is the click event of the canvas. This evnet is triggered whenever user clicks the canvas 
            ( and only canvas won't work outside canvas ).
            Then it calls the is_Dot function to ckech wheather user have clicked on the dot / nail or not.
            If yes then it calls the drawLines function to draw the lines from one dot/nail to other which is 
            specifically clikced by the user.
            Else DOes nothing.
        """
        x, y = event.x, event.y
        (isDot, _) = self.is_Dot(x, y)
        if isDot:
            self.drawLines(x, y, self.COORDS)

    def drawLines(self, x, y, coords):  # sourcery no-metrics
        """
            This function takes x and y coordinates of the positions clicked by the user 
            ( by click function ). Draws Lines between them.
        """
        coords.append((x, y))

        v = len(coords)-1
        if v > 0:
            self.canvas.create_line(
                coords[v-1][0], coords[v-1][1], coords[v][0], coords[v][1], activefill="black", activewidth=6, width=4)

    # Save Shapes Logic

    def saveShape(self, name, coords):
        """
            This function saves the given coordinates and the respective name to the sample.json file.
            If the name or the coordinates ( i.e. if user tries to save the shape before making the shape of giving it a name ) 
            are not provided this function show a warning saying "You haven't entered name or coordinates of the shape properly."
            Else shows a message saying "Shape Saved Successfully!"
        """
        warningLabel = Label(self.frameCreateShapes,
                             text="You haven't entered name or coordinates of the shape properly.")
        successLabel = Label(self.frameCreateShapes,
                             text="Shape Saved Successfully!")
        shapeName = name.get()
        if shapeName and coords:
            SHAPES[shapeName] = coords
            with open("sample.json", "w") as outfile:
                json.dump(SHAPES, outfile)
            successLabel.pack()
        else:
            warningLabel.pack()

    # Edit Shape Logic
    # This function edits and saves the shape with given coordinates and the respective name to the sample.json file.
    # If the name or the coordinates ( i.e. if user tries to delete the shape before specifing which shape to open )
    # are not provided this function show a warning saying "You haven't entered name or coordinates of the shape properly."
    # Else shows a message saying "Shape Edited Successfully!"
    #
    #
    # NOTE: The explainaton given above is the expected result of the edit functionality but the edit fuctionality is stll under
    #       develepment and is partially complete so you might encounter some glitches while using this functionality.
    def editShapeCheck(self, coordinates):
        if self.fromX == 0 or self.fromY == 0:
            return

        (isDot, i) = self.is_Dot(self.fromX, self.fromY)
        index = -1
        for j in coordinates:
            for k in range(self.coords[i][0], self.coords[i][2]):
                for l in range(self.coords[i][1], self.coords[i][3]):
                    if [k, l] == coordinates:
                        break
                if [k, l] == coordinates:
                    break
            index += 1
            if [k, l] == coordinates:
                break
        return (isDot, index)

    def editClick(self, event):
        x, y = event.x, event.y
        print(f"x: {x} y: {y}")
        (isDot, _) = self.is_Dot(x, y)
        if self.toX == 0 and self.toY == 0:
            self.toX = x
            self.toY = y
            print(self.toX, self.toY)
        elif self.fromX == 0 and self.fromY == 0:
            self.fromX = x
            self.fromY = y
            print(self.fromX, self.fromY)
            self._extracted_from_editShape_(self.editName, SHAPES, self.COORDS)
        else:
            print("Not a Dot")

    def _extracted_from_editShape_(self, name, dataDict, coords):
        shapeName = name.get()
        coordinates = dataDict[shapeName]
        for i in range(len(coordinates)):
            self.drawLines(coordinates[i][0],
                           coordinates[i][1], coords)
        if self.toX != 0 and self.toY != 0:
            self._extracted_from__extracted_from_editShape_(
                coordinates, coords, dataDict
            )

    def _extracted_from__extracted_from_editShape_(self, coordinates, coords, dataDict):
        (_, index) = self.editShapeCheck(coordinates)
        coordinates[index][0] = self.toX
        coordinates[index][1] = self.toY
        # self.refresh_board()
        for i in range(len(coordinates)):
            self.drawLines(coordinates[i][0], coordinates[i][1], coords)

        with open("sample.json", 'w') as newData:
            json.dump(dataDict, newData)
        print("Shape Edited Successfully!")

    # Open Shape Logic

    def openShape(self, name, coords):
        """
            This function open the shape with given coordinates and the respective name from the sample.json file.
            If the name or the coordinates ( i.e. if user tries to delete the shape before specifing which shape to open ) 
            are not provided this function show a warning saying "You haven't entered name or coordinates of the shape properly."
            Else shows a message saying "Shape Opened Successfully!"
        """
        self.refresh_board()
        shapeName = name.get()
        if shapeName:
            coordinates = SHAPES[shapeName]
            print(coordinates)
            for i in range(len(coordinates)):
                self.drawLines(coordinates[i][0], coordinates[i][1], coords)
            label = Label(self.frameOpenShapes,
                          text="Shape Opened Successfully!")
        else:
            label = Label(self.frameOpenShapes,
                          text="You haven't entered name of the shape properly.")
        label.pack()

    # Delete Shape Logic

    def deleteShape(self, name, coords):
        """
            This function opens as well as deletes the shape with given coordinates and the respective name from the sample.json file at the same time.
            If the name or the coordinates ( i.e. if user tries to delete the shape before specifing which shape to delete ) 
            are not provided this function show a warning saying "You haven't entered name or coordinates of the shape properly."
            Else shows a message saying "Shape Deleted Successfully!"
        """
        self._extracted_from_deleteShape_(name, SHAPES, coords)

    def _extracted_from_deleteShape_(self, name, dataDict, coords):
        """
         This function is just an extraction from the delete function to make less complex. 
         All its functionality is defined in the delete shapes function.
        """
        shapeName = name.get()
        if shapeName:
            coordinates = dataDict[shapeName]
            for i in range(len(coordinates)):
                self.drawLines(coordinates[i][0],
                               coordinates[i][1], coords)
            dataDict.pop(shapeName)
            with open("sample.json", "w") as outfile:
                json.dump(dataDict, outfile)
            label = Label(self.frameOpenShapes,
                          text="Shape Opened Successfully!")
        else:
            label = Label(self.frameOpenShapes,
                          text="You haven't entered name of the shape properly.")
        label.pack()

    def mainloop(self):
        """
            mainloop() is used when the application is ready to run. mainloop() is an infinite 
            loop used to run the application, wait for an event to occur and process the event 
            as long as the window is not closed.
        """
        self.window.mainloop()


game_instance = Geoboard()
game_instance.mainloop()
