from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import time
import serial.tools.list_ports
from tkinter.filedialog import *
from functools import partial
import csv

# print(list(serial.tools.list_ports.comports()))

comlist = serial.tools.list_ports.comports()
running = True
fileroot = 'untitled.csv'


class Toppart(Frame):
    def __init__(self):
        super().__init__()
        self.connPort = 'COM10'
        self.baudRate = 9600
        self.arduino = serial.Serial()
        self.exi = False
        self.labelserial = "connected to"
        self.recordingStatus = False
        self.saveMode = False
        self.open = False
        self.new = False
        self.initUI()

    def initUI(self):

        self.master.title("Emedding")

        menubar = Menu(self.master)
        toolbar = Frame(self.master, bd=1, relief=RAISED)
        self.master.config(menu=menubar)
        igniteButton = Button(toolbar, text="ignite", relief=FLAT, command=partial(self.write_read, "IGNITE"))
        igniteButton.pack(side=LEFT, padx=2, pady=2)
        runButton = Button(toolbar, text="Start", relief=FLAT, command=partial(self.recordSatus, True))
        runButton.pack(side=LEFT, padx=2, pady=2)
        stopButton = Button(toolbar, text="Stop", relief=FLAT, command=partial(self.recordSatus, False))
        stopButton.pack(side=LEFT, padx=2, pady=2)
        fileMenu = Menu(menubar, )

        submenu = Menu(fileMenu)
        porlist = Menu(submenu)
        baudspeeds = Menu(submenu)
        bps = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200]
        for x in range(0, len(comlist)):
            porlist.add_command(label=comlist[x].description, underline=0, command=partial(self.onPort, comlist[x].device))
        for x in range(0, len(bps)):
            baudspeeds.add_command(label=bps[x], underline=0, command=partial(self.onBaud, bps[x]))
        submenu.add_cascade(label="Ports", underline=0, menu=porlist)
        submenu.add_cascade(label="Baudrate", underline=0, menu=baudspeeds)
        fileMenu.add_command(label="New", command=partial(self.new_file))
        fileMenu.add_command(label="Open", command=partial(self.open_file))
        fileMenu.add_command(label="Save", command=partial(self.save_file))
        fileMenu.add_command(label="Save As", command=partial(self.save_file))
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
        menubar.add_cascade(label="Tools", underline=0, menu=submenu)
        toolbar.pack(side=TOP, fill=X)
        try:
            if serial.Serial(port=self.connPort, baudrate=self.baudRate, timeout=0.1).is_open is True:
                self.arduino = serial.Serial(port=self.connPort, baudrate=self.baudRate, timeout=0.1)
                self.labelserial = "connected to port:{} and baudrate:{}".format(self.connPort, self.baudRate)
                # print(self.labelserial)
        except serial.serialutil.SerialException:
            self.labelserial = "choose port and speed"

    def onExit(self):
        self.exi = True
        self.quit()

    def onPort(self, dport):
        global comlist
        comlist = serial.tools.list_ports.comports()
        self.connPort = dport
        self.initUI()

    def onBaud(self, bau):
        self.baudRate = bau
        self.initUI()

    def write_read(self, x):
        while True:
            self.arduino.write(bytes(x, 'utf-8'))
            if self.arduino.in_waiting:
                # wait to get confirmation of command send
                data = str(self.arduino.readline())
                if data.__contains__("acknowledge"):
                    break
        if x == "IGNITE":
            self.recordingStatus = True

    def recordSatus(self, stat):
        self.recordingStatus=stat

    def save_file(self):
        self.recordingStatus = False
        self.saveMode = True
        
    def open_file(self):
        global fileroot
        if fileroot != "untitled.csv":
            self.save_file()
        self.open = True

    def new_file(self):
        global fileroot
        if fileroot != "untitled.csv":
            self.save_file()
        fileroot = "untitled.csv"
        self.new = True


def onOpen():
    global fileroot
    filetypes = (('excel files', '*.csv'), ('All files', '*.*'))
    fileroot = askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    rows = []
    with open(fileroot) as file_obj:
        # Create reader object by passing the file
        # object to reader method
        reader_obj = csv.reader(file_obj)

        # Iterate over each row in the csv
        # file using reader object
        k = 0
        xval = []
        yval = []
        for row in reader_obj:
            if k != 0:
                xval.append(row[0])
                yval.append(row[1])
            k += 1
        rows.append(xval)
        rows.append(yval)
    return rows


def close_window():
  global running
  running = False  # turn off while loop


def save(result):
    global fileroot
    header = ['time', 'load measured']
    with open(fileroot, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for res in result:
            # write the header
            # write multiple rows
            writer.writerow(res)
    if fileroot == 'untitled.csv':
        f = asksaveasfile(initialfile=fileroot, defaultextension=".csv",
                      filetypes=[("All Files", "*.*"), ("Excel ", "*.csv")])
        fileroot = f.name


def main():
    global comlist
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", close_window)
    root.resizable(width=0, height=0)
    root.geometry("900x500")
    root.update_idletasks()  # Update the idle to update display
    ui = Toppart()
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    graphframe = Frame(root, bg="skyblue3", width=root.winfo_width() / 2 + 55,
                       height=root.winfo_height() - 30)
    graphframe.pack(side=RIGHT, anchor=NE, expand=1)
    serialframe = Frame(root, bg="white", width=root.winfo_width() / 2 - 55,
                        height=root.winfo_height()-20)
    serialframe.pack(side=LEFT, anchor=NW, expand=1)
    var = StringVar()
    serialdet = Label(root, textvariable=var, bg="pink", bd=5, justify=LEFT)
    serialdet.place(anchor=SW, relx=0.05, rely=0.98)
    var.set(ui.labelserial)
    canvas = FigureCanvasTkAgg(fig, master=graphframe)  # A tk.DrawingArea.
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)
    toolbar = NavigationToolbar2Tk(canvas, graphframe)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    canvas.draw()
    txt_label = Label(serialframe, text="Serial Data", font=('Helvetica 15 bold'), bg="white")
    txt_label.pack(side=TOP, padx=10)
    scroll_bar = Scrollbar(serialframe)
    scroll_bar.pack(side=RIGHT, fill='y')
    output = Text(serialframe, width=290, bg="white", yscrollcommand=scroll_bar.set)
    output.pack(side=LEFT)
    scroll_bar.config(command=output.yview)
    prevTime = 0.0
    xd = [0.0]
    yd = [0.0]
    accpt = [[]]
    while running:
        # print(app.ui.connPort)
        nlst = serial.tools.list_ports.comports()
        if len(nlst) != len(comlist):
            comlist = nlst
            ui.initUI()
            var.set(ui.labelserial)
        try:
            # print(ui.arduino.isOpen())
            if ui.arduino.isOpen():
                if ui.arduino.in_waiting:
                    tt = time.time()
                    packet = ui.arduino.readline()
                    st = str(packet.decode('utf'))
                    output.insert(END, st)
                    v = st.find("Load_cell output val: ")
                    if 0 <= v and ui.recordingStatus:
                        prevTime += int((time.time()-tt)*1000)/1000
                        xd.append(prevTime)
                        yval = float(st[v+len("Load_cell output val: "):])
                        yd.append(yval)
                        accpt.append([prevTime, yval])
                        ax.plot(xd, yd, color='g')
                        ax.set_xlim(left=max(0, prevTime-0.02), right=prevTime+0.02)
                        canvas.draw()
                    elif ui.recordingStatus is False:
                        if ui.saveMode is True:
                            save(accpt)
                            ui.saveMode = False
                        xd = [0.0]
                        yd = [0.0]
                        accpt.clear()
                        canvas.draw()
                if ui.exi or not running is True:
                    break
            if ui.open:
                rv = onOpen()
                ax.plot(rv[0], rv[1], color='g')
                canvas.draw()
                ui.open = False
            elif ui.new:
                ui.initUI()
                var.set(ui.labelserial)
                canvas.draw()
                ui.new = False
        except IOError:
            ui.arduino.close()
        root.update()


if __name__ == '__main__':
    main()


# canvas2 = FigureCanvasTkAgg(fig2, master=root)  # A tk.DrawingArea.

# canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)


# toolbar1 = NavigationToolbar2Tk(canvas2, root)
# toolbar1.update()
# canvas2.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)
# canvas2.draw()
