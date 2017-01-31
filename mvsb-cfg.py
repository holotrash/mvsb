from Tkinter import *
import tkFileDialog, os

#change the background video
def changeBgVid():
    print("changing bg video...") 
    bgVidPath.set(tkFileDialog.askopenfilename())

#add a video to the set list
def addVid():
    print("adding a video to the set list")
    vidListBox.insert(END, tkFileDialog.askopenfilename())

#delete a video from the set list
def deleteVid():
    print("deleting the selected video from the set list")
    vidListBox.delete(ANCHOR)

#test function
def saveFunction():
    print("saving configuration...")
    if bgVidPath.get() == "":
        print("error: no background selected!")
        return
    if vidListBox.size() == 0:
        print("error: set list is empty!")
        return
    print(bgVidPath.get())
    print(setList.get())
    print("opening playlist.cfg")
    playlistFile = open("playlist.cfg", 'w')
    playlistFile.write(bgVidPath.get())
    playlistFile.write("?")
    for item in enumerate(vidListBox.get(0, END)):
        playlistFile.write(item[1])
        print(item[1])
        playlistFile.write("?")
    playlistFile.close()

window = Tk()
bgVidPath = StringVar() 
setList = StringVar()

window.geometry('600x400+5+5')
window.title('MIDI Video Sequencer of Benni - Configuration Utility')

backgroundVidLabel = Label(window, text="background video:")
backgroundVidEntry = Entry(window, width=50, textvariable=bgVidPath)
changeBgVidButton = Button(window, text="change", width=6, command=changeBgVid)

vidListLabel = Label(window, text="video set list:")
vidListBox = Listbox(window, width=50, listvariable=setList)

addVidButton = Button(window, text="add", width=6, command=addVid)
deleteVidButton = Button(window, text="delete", width=6, command=deleteVid)

saveButton = Button(window, text="save", width=6, command=saveFunction).place(x=300,y=300)

backgroundVidLabel.place(x=5,y=5)
backgroundVidEntry.place(x=5,y=25)
changeBgVidButton.place(x=425,y=15)

vidListLabel.place(x=5,y=50)
vidListBox.place(x=5,y=70)
addVidButton.place(x=425,y=70)
deleteVidButton.place(x=425,y=100)

#open cfg file, if it exists
if os.path.isfile("playlist.cfg"):
    loadFile = open("playlist.cfg")
    loadList = loadFile.read().split("?")
    bgVidPath.set(loadList[0])
    for x in range(1,len(loadList)):
        vidListBox.insert(END, loadList[x])

window.mainloop()
