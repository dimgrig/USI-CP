#pip install pyserial

import binascii
import io
import serial
from serial.tools import list_ports
import time
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText


ser = serial.Serial()






root = Tk()

root.configure(bg='#F5F6F7')
frame_1_1 = Frame(root, width=60, height=20)
frame_1_2 = Frame(root, width=60, height=20)
frame_1_3 = Frame(root, width=60, height=20)
frame_1_4 = Frame(root, width=70, height=20)

frame_2_1 = Frame(root, width=300, height=300)

frame_1_1.grid(row=0, column=0)
frame_1_2.grid(row=0, column=1, padx=2)
frame_1_3.grid(row=0, column=2)
frame_1_4.grid(row=0, column=3)
frame_2_1.grid(row=1, column=0, columnspan=4)
frame_2_1.columnconfigure(0, weight=10)
frame_2_1.pack_propagate(False)




console = ScrolledText(frame_2_1)
console.pack()

def refresh_ports():
    cp_list = list_ports.comports(include_links=False)
    console.insert(END, "Available Ports\n")
    for cp in cp_list:
        console.insert(END, cp)
        console.insert(END, "\n")
    console.insert(END, "\n")
    console.see(END)

    global ports
    ports.destroy()
    optionList = []
    for port in list_ports.comports(include_links=False):
        optionList.append(port.device)
    optionList.insert(0, optionList[0])

    ports_var = StringVar(root)
    ports_var.set(optionList[0])
    ports = OptionMenu(frame_1_1, ports_var, *optionList)
    ports.pack()

    return(cp_list)


def open_port():
    global ser
    port = ports_var.get()
    ser.close()
    console.insert(END, "Port " + port + " opened\n")
    ser.baudrate = 9600
    ser.port = port.split(" ")[0]
    ser.open()
    #sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser), newline=binascii.unhexlify('0a').decode("utf-8"))
    console.insert(END, ser)
    console.insert(END, "\n")
    console.see(END)

def close_port():
    port = ports_var.get()
    console.insert(END, "Port " + port + " closed\n")
    console.insert(END, "\n")
    console.see(END)
    ser.close()

def clear():
    console.delete('1.0', END)

class TimeError(Exception):
    def __init__(self, msg):
        self.msg=msg

def readLine(ser):
    str = ""

    threadCount = 0

    while 1:
        # try:
        #time.sleep(0.001)
        #threadCount = threadCount + 1



        ch = ser.read().decode("utf-8")
        #print(threadCount, ch)
        if(ch == '\r' or ch == '' or ch == '\n'):
            #print("BREAK")
            break
        str += ch

            # if threadCount > 10 and str == "":
            #     raise TimeError("5 seconds elapsed!")

        # except TimeError as e:
        #      break

    #"print "str = " + str
    console.insert(END, "Received: " + str +" \n")
    console.see(END)

    return str




optionList = []
for port in list_ports.comports(include_links=False):
    optionList.append(port.device)

optionList.insert(0, optionList[0])
#print(tuple(optionList))
ports_var = StringVar(root)
ports_var.set(optionList[0])
ports = OptionMenu(frame_1_1, ports_var, *optionList)
ports.pack()

# # on change dropdown value
# def change_dropdown(*args):
#     print(ports_var.get())
#
# # link function to change dropdown
# ports_var.trace('w', change_dropdown)

b_open_port = Button(frame_1_2, text="Open", command=open_port)
b_open_port.pack(expand=True, fill='both')
b_close_port = Button(frame_1_3, text="Close", command=close_port)
b_close_port.pack(expand=True, fill='both')
b_clear = Button(frame_1_4, text="Clear", command=clear)
b_clear.pack(expand=True, fill='both')

main_menu = Menu(root)
root.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=first_item)
first_item.add_command(label='Refresh', command=refresh_ports)
first_item.add_command(label='Exit', command=exit)

#print("sio", sio)
#print("ser", ser)

def my_mainloop():
    global ser
    #print("sio", sio)
    #print("ser", ser)
    if ser.is_open:
        #print("IN LOOP")

        if (ser.inWaiting() > 0):
            readLine(ser)
            #print(readLine(ser))
        else:
            pass
            #print("NO DATA")
        #line = ser.readline()
        #print(line)
        #print("IN LOOP cont")
        #console.insert(END, "\n")
    else:
        pass
        #print("NO LOOP")
    root.after(10, my_mainloop)

root.after(10, my_mainloop)
root.mainloop()

# while True:
#     line = ser.readline()
#     print(line)
#
#     #root.update_idletasks()
#     root.update()
#     #time.sleep(0.01)

