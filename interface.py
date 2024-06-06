from tkinter import *
from tkinter import ttk
from utils import *
from lang import *


def create_frame_end_condition():
    def cbox_selected(event):
        selection = combobox_end_condition.get()
        if selection == "Задать длину":
            entry_end_condition["state"] = "normal"
        else:
            entry_end_condition["state"] = "disabled"

    frame_end_conditions = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10])

    label_end_condition = ttk.Label(frame_end_conditions, text="Граничные условия")
    label_end_condition.pack(**utils_position_setting_pack)

    combobox_end_condition = ttk.Combobox(frame_end_conditions, values=array_end_conditions)
    combobox_end_condition.bind("<<ComboboxSelected>>", cbox_selected)
    combobox_end_condition.current(0)
    combobox_end_condition.pack(**utils_position_setting_pack)

    entry_end_condition = ttk.Entry(frame_end_conditions, width=23)
    entry_end_condition.pack(**utils_position_setting_pack)
    entry_end_condition.insert(0, "10.0 мм")

    label_thread_pitch = ttk.Label(frame_end_conditions, text="Шаг резьбы")
    label_thread_pitch.pack(**utils_position_setting_pack)

    entry_thread_pitch = ttk.Entry(frame_end_conditions, width=23)
    entry_thread_pitch.pack(**utils_position_setting_pack)
    entry_thread_pitch.insert(0, "2")

    frame_end_conditions.grid(row=0, column=0, **utils_position_setting_grid)


def create_frame_thread_setting():
    frame_thread_setting = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10, 33, 10])

    var_thread_direction = BooleanVar().set(1)

    label_thread_direction = ttk.Label(frame_thread_setting, text=name_label_thread_direction)
    label_thread_direction.pack(**utils_position_setting_pack)

    radiobutton_thread_right = ttk.Radiobutton(frame_thread_setting, text=name_right_thread, value=1,
                                               variable=var_thread_direction)
    radiobutton_thread_right.pack(**utils_position_setting_pack)

    radiobutton_thread_left = ttk.Radiobutton(frame_thread_setting, text=name_left_thread, value=0,
                                              variable=var_thread_direction)
    radiobutton_thread_left.pack(**utils_position_setting_pack)

    frame_thread_setting.grid(row=2, column=0, **utils_position_setting_grid)


def create_frame_thread_type():    
    frame_thread_type = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10])

    label_thread_type = ttk.Label(frame_thread_type, text="Тип резьбы")
    label_thread_type.pack(**utils_position_setting_pack)

    selected_text = StringVar(value=array_thread_type_names[0])

    combobox_thread_type = ttk.Combobox(frame_thread_type, values=array_thread_type_names)
    combobox_thread_type.current(0)
    combobox_thread_type.pack(**utils_position_setting_pack)

    frame_thread_type.grid(row=0, column=1, **utils_position_setting_grid)


def create_frame_bevel_setting():
    frame_bevel_setting = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10])

    label_thread_type = ttk.Label(frame_bevel_setting, text="Параметры фаски")
    label_thread_type.pack(**utils_position_setting_pack)
    
    checkbutton_make_bevel = ttk.Checkbutton(frame_bevel_setting, text="Включить")
    checkbutton_make_bevel.pack(**utils_position_setting_pack)

    frame_bevel_setting.grid(row=0, column=1, **utils_position_setting_grid)