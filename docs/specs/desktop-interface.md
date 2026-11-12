# Design — Desktop Interface

> Epic: #22 · Stories: #24
> Owner: NguyenVGH · Sprint: 3 · Status: draft
> Specification: [`/docs/design/desktop-interfface.md`](/docs/design/desktop-interfface.md)


## 1. Interface Prototype

An attempt at creating an interface that contains a file explorer, process manager, system log viewer, and network activity viewer. 

```
import tkinter
import tkinter.messagebox

class Interface:
    def __init__(self):
        self._main_interface = tkinter.Tk()

        self._main_interface.title('Cyber Sandbox')

        self._label = tkinter.Label(self._main_interface, text='Welcome to the Cyber Sandbox!')
        self._label.pack()

        self._button1 = tkinter.Button(self._main_interface, text="File Explorer", command=self.call1)
        self._button.pack()

        self._button2 = tkinter.Button(self._main_interface, text="Process Manager", command=self.call2)
        self._button.pack()

        self._button3 = tkinter.Button(self._main_interface, text="System Log Viewer", command=self.call3)
        self._button.pack()

        self._button4 = tkinter.Button(self._main_interface, text="Network Activity Viewer", command=self.call4)
        self._button.pack()

        self._button5 = tkinter.Button(self._main_interface, text="Quit", command=self._main_interface.destroy)
        self._button5_.pack()

        tkinter._main_interface.mainloop()

    def call1(self):
        tkinter.messagebox.showinfo('File Explorer', 'Example Files')

    def call2(self):
        tkinter.messagebox.showinfo('Process Manager', 'Example Management Process')

    def call3(self):
        tkinter.messagebox.showinfo('System Log Viewer', 'Example Log')

    def call4(self):
        tkinter.messagebox.showinfo('Network Activity Viewer', 'Example Network Activity')

```

## 2. Prototype Design

The interface design is a protoype and may change in future implementations. 