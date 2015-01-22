from subprocess import call
from Tkinter import *
import os, sys

root = Tk()

path = '/usr/share/applications/'
dirs = os.listdir(path)

objs = []
filteredObjs = []
labels = []
i = 0

for file in dirs:
    if file.endswith('.desktop'):
        f = open(path + file)
        obj = {'name': '', 'command': '', 'namelower': ''}
        for line in f:
            if line.startswith('Name=') and obj['name'] == '':
                obj['name'] = line.replace('Name=', '')
                obj['namelower'] = obj['name'].lower()
            elif line.startswith('Exec=') and obj['command'] == '':
                obj['command'] = line.replace('Exec=', '').strip()
        objs.append(obj)

def callback(sv):
    text = sv.get().lower()
    if len(text) > 1:
        for l in labels:
            l.destroy()
        del labels[:] 
        del filteredObjs[:]
        for o in objs:
            if text in o['namelower']:
                l = Label(root, text=o['name'])
                l.pack()
                labels.append(l)
                filteredObjs.append(o)
        i = 0
        select()
   

def onEnter(o):
    if len(filteredObjs) > 0: 
        print '(' + filteredObjs[i]['command'] + ' &)'
        os.system('(' + filteredObjs[i]['command'] + ' &)')
        quit()

def select():
    labels[i].configure(text = '> ' + filteredObjs[i]['name'])

def unselect():
    labels[i].configure(text = filteredObjs[i]['name'])

def onUp(o):
    global i
    if i > 0:
        unselect()
        i -= 1
        select()

def onDown(o):
    global i
    if i < len(objs) - 1:
        unselect()
        i += 1
        select()

def onEscape(o):
    quit()

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
e = Entry(root, textvariable=sv, width=80)
e.pack()

e.focus_set()

e.bind('<Return>', onEnter)
e.bind('<Up>', onUp)
e.bind('<Down>', onDown)
e.bind('<Escape>', onEscape)

root.mainloop()
