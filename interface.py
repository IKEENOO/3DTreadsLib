from tkinter import *
from tkinter import ttk


def create_frame_end_condition():
    def cbox_selected(event):
        selection = combobox_end_condition.get()
        if selection == "Задать длину":
            entry_end_condition["state"] = "normal"
        else:
            entry_end_condition["state"] = "disabled"

    frame_end_conditions = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10])

    label_end_condition = ttk.Label(frame_end_conditions, text="Граничные условия")
    label_end_condition.pack(anchor=NW, padx=5, pady=5)

    array_end_conditions = ["Задать длину", "На всю длину"]

    combobox_end_condition = ttk.Combobox(frame_end_conditions, values=array_end_conditions)
    combobox_end_condition.bind("<<ComboboxSelected>>", cbox_selected)
    combobox_end_condition.current(0)
    combobox_end_condition.pack(anchor=NW, padx=5, pady=5)

    entry_end_condition = ttk.Entry(frame_end_conditions, width=23)
    entry_end_condition.pack(anchor=NW, padx=5, pady=5)
    entry_end_condition.insert(0, "10.0 мм")

    label_thread_pitch = ttk.Label(frame_end_conditions, text="Шаг резьбы")
    label_thread_pitch.pack(anchor=NW, padx=5, pady=5)

    entry_thread_pitch = ttk.Entry(frame_end_conditions, width=23)
    entry_thread_pitch.pack(anchor=NW, padx=5, pady=5)
    entry_thread_pitch.insert(0, "2")

    frame_end_conditions.grid(sticky=NW, row=0, column=0, padx=5, pady=5)


def create_frame_thread_setting():
    frame_thread_setting = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10, 45, 10])

    right_thread = "Правая резьба"
    left_thread = "Левая резьба"

    thread_direction = StringVar(value=right_thread)

    label_thread_direction = ttk.Label(frame_thread_setting, text="Направление резьбы")
    label_thread_direction.pack(anchor=NW, padx=5, pady=5)

    radiobutton_thread_right = ttk.Radiobutton(frame_thread_setting, text=right_thread, value=right_thread,
                                               variable=thread_direction)
    radiobutton_thread_right.pack(anchor=NW, padx=5, pady=5)

    radiobutton_thread_left = ttk.Radiobutton(frame_thread_setting, text=left_thread, value=left_thread,
                                              variable=thread_direction)
    radiobutton_thread_left.pack(anchor=NW, padx=5, pady=5)

    frame_thread_setting.grid(sticky=NW, row=1, column=0, padx=5, pady=5)
