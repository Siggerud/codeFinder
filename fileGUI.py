from tkinter import Label, Entry, StringVar, Checkbutton, IntVar, Listbox, Button, END, Frame, W
from tkinter.tix import *
from codeFinder import CodeFinder
import os

class fileGUI:
    # creates layout for a code file info tracker GUI that lets user easily open matches
    def __init__(self, master):
        # setting the layout
        self._master = master
        self._master.title("Code finder")
        self._master.geometry("500x550")

        self._allChecked = False
        self._font = ("Helvetica", 9)

        pathLabel = Label(master, text="Search path", font=self._font)
        pathLabel.place(x=5, y=5)

        self._path = StringVar()
        pathEntry = Entry(master, textvariable=self._path, width=30)
        pathEntry.place(x=5, y=30)
        self._path.set("C:")

        # checkboxes for user to choose code files to search for
        self._pyTracker = StringVar()
        self._pyCheck = Checkbutton(master, text="Python", variable=self._pyTracker, onvalue=".py", offvalue="", font=self._font)
        self._pyCheck.place(x=220, y=30)

        self._javaTracker = StringVar()
        self._javaCheck = Checkbutton(master, text="Java", variable=self._javaTracker, onvalue=".java", offvalue="", font=self._font)
        self._javaCheck.place(x=290, y=30)

        self._cSharpTracker = StringVar()
        self._cSharpCheck = Checkbutton(master, text="C#", variable=self._cSharpTracker, onvalue=".cs", offvalue="", font=self._font)
        self._cSharpCheck.place(x=360, y=30)

        self._javaScriptTracker = StringVar()
        self._javaScriptCheck = Checkbutton(master, text="Javascript", variable=self._javaScriptTracker, onvalue=".js", offvalue="", font=self._font)
        self._javaScriptCheck.place(x=220, y=60)

        # choose this to select or deselect all languages
        self._allCheckTracker = IntVar()
        allCheck = Checkbutton(master, text="All", command=self._checkAll, onvalue=1, offvalue=0, font=self._font)
        allCheck.place(x=360, y=60)

        keyWordLabel = Label(master, text="Code file contains word(s)", font=self._font)
        keyWordLabel.place(x=5, y=90)

        self._keyWordTrackerStr = StringVar()
        keyWordEntry = Entry(master, textvariable=self._keyWordTrackerStr, width=30)
        keyWordEntry.place(x=5, y=115)
        self._keyWordTrackerStr.set("Search query")

        tooltip = Balloon(master)
        tooltip.bind_widget(keyWordEntry, balloonmsg='Use "" around query for all words to match')

        self._keyWordTrackerChk = IntVar()
        self._keyWordCheck = Checkbutton(master, text="Include search word(s)", variable=self._keyWordTrackerChk, onvalue=1, offvalue=0, font=self._font)
        self._keyWordCheck.place(x=220, y=115)

        findButton = Button(master, text="Search", bg="springgreen", command=self._getCodePathsAndPrintInfo, font=self._font)
        findButton.place(x=5, y=150)

        self._listbox = Listbox(master, width=80, height=10)
        self._listbox.place(x=5, y=180)
        self._listbox.bind("<<ListboxSelect>>", self._openCodeFile)

        self._infoFrame = Frame(master)
        self._infoFrame.place(x=5, y=350)

    # Opens code file selected by user
    def _openCodeFile(self, event):
        selectedIndex = self._listbox.curselection()[0]
        path = self._listbox.get(selectedIndex)
        if len(path.split()) > 1 or len(path.split()) == 0:
            return

        os.system(f"start notepad {path}")

    # destroys widgets in the lower frame of the GUI
    def _destroyInfoWidgets(self):
        for widget in self._infoFrame.winfo_children():
            widget.destroy()

    # adds warning if specified path is not a dir
    def _addWarning(self):
        self._destroyInfoWidgets()
        warningLabel = Label(self._infoFrame, text=f"Search path is not a directory", font=self._font)
        warningLabel.pack(anchor=W)

    # retrieves and adds paths and info in the bottom frame of the GUI
    def _getCodePathsAndPrintInfo(self):
        # check if specified path is a directory
        if not os.path.isdir(self._path.get()):
            self._addWarning()
            return

        masterDrive = self._path.get()
        inputListRaw = [self._pyTracker.get(), self._cSharpTracker.get(), self._javaTracker.get(),
                        self._javaScriptTracker.get()]
        inputList = [i for i in inputListRaw if i] # remove empty values
        finder = CodeFinder(masterDrive, inputList)
        if self._keyWordTrackerChk.get() == 0:
            results = finder.getMatchesAndStats().values()
        else:
            searchWords = self._keyWordTrackerStr.get().split()
            searchWords = [word.lower() for word in searchWords]
            allwordsMustMatch = False
            # check if "" are around search query
            if searchWords[0][0] == '"' and searchWords[-1][-1] == '"':
                if len(searchWords) == 1:
                    searchWords[0] = searchWords[0][1:-1]
                else:
                    searchWords[0], searchWords[-1] = searchWords[0][1:], searchWords[-1][:-1]
                allwordsMustMatch = True

            if allwordsMustMatch:
                results = finder.getMatchesAndStatsWithMultipleMatch(searchWords).values()
            else:
                results = finder.getMatchesAndStatsWithSingleMatch(searchWords).values()

        self._setCodePaths(results)
        self._addSummaryInfo(results)

    # adds summary info for each language specified by user. Shows number of files, lines and size
    def _addSummaryInfo(self, finderDict):
        self._destroyInfoWidgets()

        infoTitleLabel = Label(self._infoFrame, text=f"Summary for {self._path.get()}:", font=self._font)
        infoTitleLabel.pack(anchor=W)
        for sublist in finderDict:
            numberOfFiles = len(sublist[0][1:])
            language = sublist[0][0].split()[0]
            if numberOfFiles == 0:
                text = f"No {language} files found"
            else:
                numberOfLines = sublist[1]
                size = sublist[2] / (1024 * 1024)
                metric = "Mb"
                if size < 1:
                    size = size * 1024
                    metric = "Kb"
                text = f"Number of {language} files: {numberOfFiles}\n Number of lines: {numberOfLines}. Size: {size:.2f} {metric}"
            infoLabel = Label(self._infoFrame, text=text, justify="left", font=self._font)
            infoLabel.pack(anchor=W)

    # select or deselect all languages
    def _checkAll(self):
        self._allChecked = not self._allChecked

        if self._allChecked:
            self._pyCheck.select()
            self._javaScriptCheck.select()
            self._cSharpCheck.select()
            self._javaCheck.select()
        else:
            self._pyCheck.deselect()
            self._javaScriptCheck.deselect()
            self._cSharpCheck.deselect()
            self._javaCheck.deselect()

    # sets code paths in the listbox
    def _setCodePaths(self, finderDict):
        self._listbox.delete(0, END)

        for sublist in finderDict:
            for filename in sublist[0]:
                self._listbox.insert(END, filename)
            self._listbox.insert(END, "\n")






master = Tk()
myGUI = fileGUI(master)
master.mainloop()