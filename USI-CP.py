import binascii
import collections
from datetime import datetime
#import io
#from numpy import asarray
import serial # pip install pyserial
from serial.tools import list_ports
from sys import exit
#import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
import unicodecsv as csv

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

d_compress = {}
d_uncompress = {}
d_result = {}
d_saved = False
visible_plot = True
visible_console = True

ser = serial.Serial()
root = Tk()
root.iconbitmap('USI-CP.ico')
root.title("USI-CP")
root.resizable(0,0)
ports_var = StringVar(root)

root.configure(bg='#F5F6F7')
frame_1_1 = Frame(root, width=60, height=20)
frame_1_2 = Frame(root, width=60, height=20)
frame_1_3 = Frame(root, width=60, height=20)
frame_1_4 = Frame(root, width=70, height=20)
frame_2_1 = Frame(root, width=60, height=40)
frame_2_2 = Frame(root, width=60, height=40)
frame_2_3 = Frame(root, width=60, height=40)
frame_2_4 = Frame(root, width=60, height=40)
frame_3_1 = Frame(root, width=300, height=300)
frame_plot = Frame(root, width=300, height=300)

frame_1_1.grid(row=0, column=0)
frame_1_2.grid(row=0, column=1, padx=2)
frame_1_3.grid(row=0, column=2)
frame_1_4.grid(row=0, column=3)
frame_2_1.grid(row=1, column=0)
frame_2_2.grid(row=1, column=1, padx=2)
frame_2_3.grid(row=1, column=2)
frame_2_4.grid(row=1, column=3)
# frame_2_1.columnconfigure(0, weight=10)
# frame_2_2.columnconfigure(0, weight=10)
# frame_2_3.columnconfigure(0, weight=10)
frame_2_1.pack_propagate(False)
frame_2_2.pack_propagate(False)
frame_2_3.pack_propagate(False)

frame_3_1.grid(row=2, column=0, columnspan=4)
# frame_3_1.columnconfigure(0, weight=100)
frame_3_1.pack_propagate(False)
frame_3_1.grid_forget()
frame_1_4.grid_forget()
visible_console = False

frame_plot.grid(row=0, column=4, rowspan=4)
# frame_plot.pack_propagate(False)
frame_plot.grid_forget()
visible_plot = False

console = ScrolledText(frame_3_1)
console.pack()

optionList = []
for port in list_ports.comports(include_links=False):
    optionList.append(port.device)
optionList.insert(0, optionList[0])

ports_var = StringVar(root)
ports_var.set(optionList[0])
ports = OptionMenu(frame_1_1, ports_var, *optionList)
ports.pack()

def refresh_ports_list():
    global ports
    global ports_var
    try:
        ports.destroy()
    except:
        pass
    optionList = []
    for port in list_ports.comports(include_links=False):
        optionList.append(port.device)
    optionList.insert(0, optionList[0])

    ports_var = StringVar(root)
    ports_var.set(optionList[0])
    ports = OptionMenu(frame_1_1, ports_var, *optionList)
    ports.pack()

def refresh_ports():
    close_port()
    cp_list = list_ports.comports(include_links=False)
    console.insert(END, "Available Ports\n")
    for cp in cp_list:
        console.insert(END, cp)
        console.insert(END, "\n")
    console.insert(END, "\n")
    console.see(END)

    refresh_ports_list()
    return(cp_list)

def exit_function():
    ser.close()
    exit(0)
    
def read_csv():
    csv_file_path = askopenfilename()
    f_csv = open(csv_file_path, 'rb')
    reader = csv.reader(f_csv, encoding='utf-8')
    headers = next(reader)

    dict = {rows[1]: rows[2] for rows in reader}
    #print(dict)

    f_csv.close()
    write_plot(dict, {})
    global visible_plot
    visible_plot = False
    hide_plot()

def open_port():
    global ser
    global ports_var
    port = ports_var.get()
    #print(ports_var.get())
    ser.close()
    console.insert(END, "Port " + port + " opened\n")
    ser.baudrate = 9600
    ser.port = port.split(" ")[0]
    #print(ser.port)
    ser.open()
    console.insert(END, ser)
    console.insert(END, "\n")
    console.see(END)
    b_open_port.configure(state=DISABLED)
    b_close_port.configure(state=NORMAL)

def close_port():
    global ports_var
    port = ports_var.get()
    console.insert(END, "Port " + port + " closed\n")
    console.insert(END, "\n")
    console.see(END)
    ser.close()
    b_open_port.configure(state=NORMAL)
    b_close_port.configure(state=DISABLED)

def clear():
    console.delete('1.0', END)

def hide_plot():
    global visible_plot
    if visible_plot:
        frame_plot.grid_forget()
        visible_plot = False
    else:
        frame_plot.grid(row=0, column=4, rowspan=4)
        visible_plot = True

def hide_console():
    global visible_console
    if visible_console:
        frame_3_1.grid_forget()
        frame_1_4.grid_forget()
        visible_console = False
    else:
        frame_3_1.grid(row=2, column=0, columnspan=4)
        frame_1_4.grid(row=0, column=3)
        visible_console = True

l_state = Label(frame_2_1, text="State")
l_state.pack()
t_state = Text(frame_2_1)
t_state.pack()
l_f = Label(frame_2_2, text="F")
l_f.pack()
t_f = Text(frame_2_2)
t_f.pack()
l_a = Label(frame_2_3, text="A")
l_a.pack()
t_a = Text(frame_2_3)
t_a.pack()

b_open_port = Button(frame_1_2, text="Open", command=open_port)
b_open_port.pack(expand=True, fill='both')
b_close_port = Button(frame_1_3, text="Close", command=close_port)
b_close_port.pack(expand=True, fill='both')
b_close_port.configure(state=DISABLED)
b_clear = Button(frame_1_4, text="Clear", command=clear)
b_clear.pack(expand=True, fill='both')
b_hide_plot = Button(frame_2_4, text=">", command=hide_plot)
b_hide_plot.pack(expand=True, fill='both')
b_hide_console = Button(frame_2_4, text="v", command=hide_console)
b_hide_console.pack(expand=True, fill='both')

figure_plot = Figure(figsize=(5, 3), dpi=100)
figure_sub_plot = figure_plot.add_subplot(111)
#figure_plot.suptitle("Title")
figure_sub_plot.set_ylabel('F')
figure_sub_plot.set_xlabel('A')
figure_plot.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95)
figure_sub_plot.xaxis.major.formatter._useMathText = False
figure_sub_plot.set_yscale('linear')


canvas = FigureCanvasTkAgg(figure_plot, master=frame_plot)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, frame_plot)
toolbar.update()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)


main_menu = Menu(root)
root.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=first_item)
first_item.add_command(label='Refresh', command=refresh_ports)
first_item.add_command(label='Exit', command=exit_function)

second_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='CSV', menu=second_item)
second_item.add_command(label='Open CSV', command=read_csv)

def readLine(ser):
    str = ""
    cnt = 0
    while 1:
        ch = ser.read().decode("utf-8")
        if(ch == '\r' or ch == '' or ch == '\n'):
            cnt = 0
            break
        else:
            cnt += 1

        if cnt > 100:
            break
        str += ch

    if cnt == 0:
        #print("str = " + str)
        timestamp = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        console.insert(END, "Received at " + timestamp + " : " + str +" \n")
        console.see(END)
    else:
        console.insert(END, "No data received ... \n")
        console.see(END)

    return str


def CRC(line):
    try:
        CRC_computed = 0
        line_bytes = str.encode(line)
        for el in line_bytes[:-2]:
            CRC_computed += el

        CRC_computed = (CRC_computed & 255)
        CRC_received = str(line_bytes[-2:], 'utf-8')

        # print(CRC_computed)
        # print(type(CRC_computed))
        # print(line_bytes[-2:])
        # print(type(line_bytes[-2:]))
        # print(CRC_received.lower())
        # print(type(CRC_received))
        # print(int(CRC_received, 16))

        if int(CRC_received, 16) == CRC_computed:
            return True

    except:
        pass

    return False


def write_csv(d_c, d_u):
    timestamp = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    timestamp = timestamp.replace(".", "_").replace(" ", "_").replace(":", "_")
    f_csv = open(timestamp + '.csv', 'w', encoding='utf-8')
    line = ("№,F,A")
    f_csv.write(line)
    f_csv.write('\n')

    i = 1
    od_c = collections.OrderedDict(sorted(d_c.items()))
    for k, v in od_c.items():
        line = ("{},{},{}").format(i, k, v)
        i = i + 1
        f_csv.write(line)
        f_csv.write('\n')

    od_u = collections.OrderedDict(sorted(d_u.items(), reverse=True))
    for k, v in od_u.items():
        line = ("{},{},{}").format(i, k, v)
        i = i + 1
        f_csv.write(line)
        f_csv.write('\n')

    f_csv.close()


def write_plot(d_c, d_u):
    global figure_sub_plot
    global canvas, figure_plot, toolbar

    y, x = [], []
    od_c = collections.OrderedDict(sorted(d_c.items()))
    for k, v in od_c.items():
        y.append(float(k))
        x.append(float(v))

    od_u = collections.OrderedDict(sorted(d_u.items(), reverse=True))
    for k, v in od_u.items():
        y.append(float(k))
        x.append(float(v))

    try:
        canvas.get_tk_widget().destroy()
        toolbar.destroy()
    except:
        pass

    figure_plot = Figure(figsize=(5, 3), dpi=100)
    figure_sub_plot = figure_plot.add_subplot(111)
    # figure_plot.suptitle("Title")
    figure_sub_plot.set_ylabel('F')
    figure_sub_plot.set_xlabel('A')
    figure_plot.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95)
    figure_sub_plot.xaxis.major.formatter._useMathText = False
    figure_sub_plot.set_yscale('linear')

    figure_sub_plot.plot(x, y, 'ro')

    canvas = FigureCanvasTkAgg(figure_plot, master=frame_plot)
    canvas.show()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, frame_plot)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

def console_clearing():
    console_length = len(console.get(1.0, END))
    print(console_length)
    if console_length > 10000:
        console.delete(1.0, 100.0)

def my_mainloop():
    global ser
    global d_saved
    global d_compress
    global d_uncompress
    global d_result

    console_clearing()

    if ser.is_open:
        #print("ISOPEN")        
        if (ser.inWaiting() > 0):
            line = readLine(ser)
            if line[0] == binascii.unhexlify('02').decode("utf-8") and line[-1] == binascii.unhexlify('03').decode("utf-8"):
                if CRC(line[1:-1]):
                    State = line[1]
                    F, A = line[2:-3].split(';')
                    #print(State, F, A)
                    t_state.delete("1.0", END)
                    t_state.insert(INSERT, State)
                    t_f.delete("1.0", END)
                    t_f.insert(INSERT, F)
                    t_a.delete("1.0", END)
                    t_a.insert(INSERT, A)

                    if State == "1" or State == "2":
                        if d_saved == True or len(d_compress) != 0 or len(d_uncompress) !=0 :
                            d_saved = False
                            d_compress = {}
                            d_uncompress = {}
                            #print("CLEARED")
                            #print("d_compress: ", d_compress)
                            #print("d_uncompress: ", d_uncompress)

                    if State == "3":
                        #print("d_compres: ", d_compress)
                        if F in d_compress:
                            pass
                        else:
                            d_compress[F] = A

                    if State == "4":
                        #print("d_uncompress: ", d_uncompress)
                        if F in d_uncompress:
                            pass
                        else:
                            d_uncompress[F] = A

                    if State == "5":
                        if d_saved == False:
                            d_saved = True
                            #print("d_compress: ", d_compress)
                            #print("d_uncompress: ", d_uncompress)
                            if d_compress == {} or d_uncompress == {}:
                                pass
                            else:
                                write_csv(d_compress, d_uncompress)
                                write_plot(d_compress, d_uncompress)
                                global visible_plot
                                visible_plot = False
                                hide_plot()


                else:
                    console.insert(END, "Received wrong CRC \n")

                    console.see(END)
            else:
                console.insert(END, "Received wrong data \n")
                console.see(END)
            #print(readLine(ser))
        else:
            pass
        #line = ser.readline()
        #print(line)
        #console.insert(END, "\n")
    else:
        pass
    root.after(10, my_mainloop)

root.after(10, my_mainloop)
root.mainloop()


