import tkinter as tk
from tkinter import ttk
import pyautogui
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys    
import pygetwindow as gw
from hotkeyinfo import possible_keys 

class App(tk.Tk):

    num_rows=3
    entriesVal = []
    controlButtons=[]
    deleteRowButtons=[]
    windowSize=[550,250]


    def getWindowTabs(self):
        windowTab = []
        for x in gw.getAllWindows():
            windowTab.append(x)
            print(x)
        return windowTab

    def resetAll(self):
        for x in self.entriesVal:
            x.delete(0, tk.END)


    def verifyHotkey(self, inputValue):
        keys = inputValue.split(',')
        verdict = True

        for x in keys:
            if(x not in possible_keys):
                verdict = False
                break
        
        return verdict

    def openFloatingWindow(self, windowObj, fullScreenState, closeBtn):
        labelValue = []

        tempList = []
        tempI = 0
        for idx, x in enumerate(self.entriesVal):
            val = x.get()
            if(len(val) == 0):
                if(idx % 2 != 0):
                    tempList.append('')
                else:
                    tempList.append(str(int(idx/2)))
            else:
                tempList.append(val)
            if(idx % 2 != 0):
                tempList.append(self.verifyHotkey(val))

            tempI += 1

            if(tempI == 2):
                labelValue.append(tempList)
                tempList = []
                tempI = 0

        print(labelValue)
        
        if(hasattr(self,'floater')):
            self.floater.destroy()
        
        closeBtn['state']='normal'
        closeBtn.configure(bg='indianred1')
        
        #hwnd = win32gui.FindWindow(None, windowObj.title())
        #threadid, pid = win32process.GetWindowThreadProcessId(hwnd)

        print(labelValue)
        
        self.floater = FloatingWindow(labelValue=labelValue, windowObj=windowObj, fullscreenState=not fullScreenState)

    def closeFloatingWindow(self, closeBtn):
        closeBtn['state']='disabled'
        closeBtn.configure(bg="grey")
        self.floater.destroy()

    def refreshList(self):
        self.activeWindows = self.getWindowTabs()
        return self.activeWindows

    def changeComboState(self, state, comboBox):
        if(state):
            comboBox['state']='readonly'
        else:
            comboBox['state']='disabled'

    def addMoreEntries(self):
        nE = tk.Entry(self)
        nV = tk.Entry(self)
        nB = tk.Button(self, text=" - ", bg='salmon', command=lambda: self.delEntry(nB.grid_info()['row']))
        
        row = self.num_rows+1,
        nE.grid(row = row, column=0, sticky=tk.EW, padx=10, pady=5)
        nV.grid(row = row, column=1, sticky=tk.EW, padx=10, pady=5)
        nB.grid(row= row, column=2, padx=5)

        self.num_rows = self.num_rows+1
        self.controlButtons[0].grid(row=self.num_rows+1)
        self.controlButtons[1].grid(row=self.num_rows+1)
        self.genGeometry(0, 30)
        self.entriesVal.extend((nE, nV))
        self.deleteRowButtons.append(nB)

    def delEntry(self, rowInfo):
        normalRow = rowInfo - 3
        startIdx = 2 * normalRow + 0
        endIdx = 2 * normalRow + 1
        delBtnIdx = rowInfo - 4

        for entry in self.entriesVal:
            entryRowInfo = entry.grid_info()['row']
            if( entryRowInfo == rowInfo):
                entry.destroy()
            elif( entryRowInfo > rowInfo):
                entry.grid(row = entryRowInfo - 1)

        del self.entriesVal[startIdx:endIdx+1]

        for btnEntry in self.deleteRowButtons:
            entryRowInfo = btnEntry.grid_info()['row']
            if(entryRowInfo == rowInfo):
                btnEntry.destroy()
            if(entryRowInfo > rowInfo):
                btnEntry.grid(row = entryRowInfo - 1)

        del self.deleteRowButtons[delBtnIdx:delBtnIdx+1]

        self.num_rows -= 1

        self.controlButtons[0].grid(row=self.num_rows + 1)
        self.controlButtons[1].grid(row=self.num_rows + 1)

        self.genGeometry(0,-30)
        

    def genGeometry(self, xChange, yChange):
        self.windowSize[0] += xChange
        self.windowSize[1] += yChange
        geoStr = str(self.windowSize[0])+'x'+str(self.windowSize[1])
        self.geometry(geoStr)

    activeWindows = getWindowTabs(0)   

    def __init__(self):
        tk.Tk.__init__(self)
        self.genGeometry(0,0)
        self.title("Floating Hotkeys Bar")
        self.configure(bg='cornsilk2')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        tk.Label(self, text="Label", bg='white').grid(row=2, column=0)
        tk.Label(self, text="Keys/text", bg='white').grid(row=2, column=1)

        tk.Label(self, text="Select Window", bg='white').grid(row=1, pady=(10,30))
        e1 = tk.Entry(self)
        v1 = tk.Entry(self)
        e1.grid(row = 3, column=0, sticky=tk.EW, padx=10, pady=5)
        v1.grid(row = 3, column=1, sticky=tk.EW, padx=10, pady=5)

        selectedWindow = tk.StringVar(self)
        windowList = ttk.Combobox(self, textvariable=selectedWindow, postcommand=lambda: windowList.configure(values=tuple(window.title for window in self.refreshList())))
        windowList['state']='disabled'
        windowList.grid(row = 1, column=1, sticky=tk.EW, padx=10, pady=(10,30))
        self.entriesVal.extend((e1, v1))

        checkVar1 = tk.IntVar()
        checkBut = tk.Checkbutton(self, text='Only for window', bg='white',variable=checkVar1, onvalue=1, offvalue=0, command= lambda: self.changeComboState(checkVar1.get(), windowList))
        checkBut.grid(row=0, column=1)

        tk.Button(self, text="Help", bg='ivory2', command=lambda: HelpWindow(self)).grid(row=0,column=2, padx=5)
        tk.Button(self, text="Reset!", bg='darksalmon', command=lambda: self.resetAll()).grid(row=0, column=0, pady=10)
        tk.Button(self, text=" + ", bg='orange', command=lambda: self.addMoreEntries()).grid(row=2, column=2, padx=5)

        closeBtn = tk.Button(self, text="Close Floating Bar", bg="grey", command=lambda: self.closeFloatingWindow(closeBtn), pady=10)
        closeBtn.grid(row=self.num_rows+1, column=1, columnspan=1, pady=10)
        closeBtn['state']='disabled'

        openBtn = tk.Button(self, text="Floating Bar", bg='palegreen', command=lambda: self.openFloatingWindow(windowObj=windowList.get(), fullScreenState=checkVar1.get(), closeBtn=closeBtn), pady=10)
        openBtn.grid(row=self.num_rows+1, column=0, columnspan=1, pady=10)

        self.controlButtons.extend([closeBtn, openBtn])


class FloatingWindow(tk.Toplevel):

    labelValue = []
    windowObj = None
    fullScreen = False
    app = None

    def btnAction(self, keyCombo, isHotkey):
        print(keyCombo)
        #print(isHotkey)
        
        if(not self.fullScreen and self.windowObj != None):
            self.windowObj.activate()
        
        if(isHotkey):
            pyautogui.hotkey(*keyCombo.split(','))
        else:
            pyautogui.write(keyCombo)

    def __init__(self, labelValue, windowObj, fullscreenState, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.labelValue = labelValue

        if(fullscreenState):
            self.fullScreen = True
        elif (windowObj != None):
            windows = pyautogui.getWindowsWithTitle(windowObj.title())
            self.windowObj = windows[0]

        self.grip = tk.Label(self, bitmap="gray50", width=50, bg='darkorchid2')
        self.grip.pack(side="left", fill="y")
        
        frameButtons = tk.Frame(self, bg='red')
        frameButtons.pack(expand=True, fill="both")

        for entry in labelValue:
            nButton = tk.Button(frameButtons, text=entry[0], fg='black', font='sans 10 bold', padx=15, takefocus=False, command=lambda m=entry[1], n=entry[2]: self.btnAction(m,n))
            nButton.pack(side="left")

        self.grip.bind("<ButtonPress-1>", self.start_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_move)
        self.grip.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")



class HelpWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)

        root_x = self.master.winfo_rootx()
        root_y = self.master.winfo_rooty()
        self.geometry(f'700x550+{root_x-100}+{root_y-200}')
        self.title("Help")

        mainLabel=tk.Label(self, text="Hotkeys floating bar", font=('Sans 14'), pady=10, padx=5, width=100)
        mainLabel.pack()
        infoLabel=tk.Label(self, text="This is editable floating bar which provides you quick access for hotkeys or pieces of text.",  font=('Sans 10'), padx=5,pady=10,width=100)
        infoLabel.pack()
        firstLabel=tk.Label(self, text="1. Choose if you want to use in global screen or custom window. \nSome hotkeys works only on custom windows!",  font=('Sans 10'), padx=5,pady=5,width=100)
        firstLabel.pack()
        tk.Label(self, text="2. Add labels and hotkeys/pieces of text. Split keys by ','",  font=('Sans 10'), padx=5,pady=5,width=100).pack()
        tk.Label(self, text="3. Click green button to generate floating bar. It will pop up in upper left corner!\nYou can now use shortcuts by clicking them! You can move Bar by dragging purple field.",  font=('Sans 10'), padx=5,pady=5,width=100).pack()
        tk.Label(self, text="AVAILABLE HOTKEYS",  font=('Sans 10 bold',), padx=5,pady=15,width=100).pack()

        horizontalScroll = tk.Scrollbar(self, orient = 'horizontal')
        horizontalScroll.pack(side = tk.BOTTOM, fill = tk.X)

        verticalScroll = tk.Scrollbar(self)
        verticalScroll.pack(side = tk.RIGHT, fill = tk.Y)

        t = tk.Text(self, width = 15, height = 15, wrap = tk.NONE,
                 xscrollcommand = horizontalScroll.set,
                 yscrollcommand = verticalScroll.set)
  
        # insert some text into the text widget
        forLine = 5
        currLine = 0
        for key in possible_keys:
            t.insert(tk.END, key + ', ')
            currLine += 1
            if(currLine == forLine):
                currLine = 0
                t.insert(tk.END, '\n')
        t.pack(side=tk.TOP, fill=tk.X)
        horizontalScroll.config(command=t.xview)
        verticalScroll.config(command=t.yview)

        tk.Label(self, text="Bartlomiej Kopysc @ 2023",  font=('Sans 10 bold',), padx=5,pady=15,width=100).pack()



app=App()
app.eval('tk::PlaceWindow . center')
app.mainloop()
