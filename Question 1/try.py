import tkinter as tk
import threading


def my_thread(event):
    print("Starting thread...")
    event.wait()
    print("Thread finished.")


def set_event(thread,event):
    if thread.is_alive():
        event.set()
    else:
        print("Thread already exited")


if "__main__" == __name__:
    root = tk.Tk()
    root.geometry('200x200')
    stopbtn=tk.Button(root, text="Stop me", command=lambda: set_event(thread, event))
    stopbtn.pack()
    event = threading.Event()
    thread = threading.Thread(target=lambda: my_thread(event))
    thread.daemon = True
    thread.start()
    root.mainloop()