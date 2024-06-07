from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
import pythoncom
from win32com.client import Dispatch, gencache
import math
from circle_info import circle_check, circle_info
from kompas_data import kompas_data
from make_thread import profile_settings, make_thread
from spiral_on_circle import spiral_on_circle, spiral_settings
from make_bevel import bevel_settings, make_bevel
from utils import *
from lang import *
from PIL import ImageTk, Image
"""
# Подключим константы API Компас
const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
const_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants
# Подключим описание интерфейсов API5
KAPI = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
iKompasObject = KAPI.KompasObject(
    Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(KAPI.KompasObject.CLSID, pythoncom.IID_IDispatch))
# Подключим описание интерфейсов API7
KAPI7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
iApplication = KAPI7.IApplication(
    Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(KAPI7.IApplication.CLSID, pythoncom.IID_IDispatch))
# Получим активный документ
if iApplication.ActiveDocument:
    iKompasDocument3D = KAPI7.IKompasDocument3D(iApplication.ActiveDocument)
    iDocument3D = iKompasObject.ActiveDocument3D()
else:
    showerror(title=name_error_kompas_api_title, message=name_error_kompas_api_connect)
"""

if __name__ == '__main__':
    root = Tk()

    root.title('ThreadsLib')
    # root.iconbitmap(default="favicon.ico")
    # root.geometry("500x400")

    def cbox_selected(event):
        selection = combobox_end_condition.get()
        if selection == "Задать длину":
            entry_end_condition["state"] = "normal"
        else:
            entry_end_condition["state"] = "disabled"

    frame_thread_setting = ttk.LabelFrame(**utils_labelframe_params, text=name_frame_thread_setting)

    label_end_condition = ttk.Label(frame_thread_setting, text=name_label_end_condition)
    label_end_condition.pack(**utils_position_setting_pack)

    combobox_end_condition = ttk.Combobox(frame_thread_setting, values=array_end_conditions, state="readonly")
    combobox_end_condition.bind("<<ComboboxSelected>>", cbox_selected)
    combobox_end_condition.current(0)
    combobox_end_condition.pack(**utils_position_setting_pack)

    entry_end_condition = ttk.Entry(frame_thread_setting, width=23)
    entry_end_condition.pack(**utils_position_setting_pack)
    entry_end_condition.insert(0, "10.0 мм")

    label_thread_pitch = ttk.Label(frame_thread_setting, text=name_label_thread_pitch)
    label_thread_pitch.pack(**utils_position_setting_pack)

    combobox_thread_pitch = ttk.Combobox(frame_thread_setting, values=array_thread_pitches, state="readonly")
    combobox_thread_pitch.current(0)
    combobox_thread_pitch.pack(**utils_position_setting_pack)

    var_thread_direction = BooleanVar()
    var_thread_direction.set(1)

    label_thread_direction = ttk.Label(frame_thread_setting, text=name_label_thread_direction)
    label_thread_direction.pack(**utils_position_setting_pack)

    radiobutton_thread_right = ttk.Radiobutton(frame_thread_setting, text=name_right_thread, value=1,
                                               variable=var_thread_direction)
    radiobutton_thread_right.pack(**utils_position_setting_pack)

    radiobutton_thread_left = ttk.Radiobutton(frame_thread_setting, text=name_left_thread, value=0,
                                              variable=var_thread_direction)
    radiobutton_thread_left.pack(**utils_position_setting_pack)

    frame_thread_setting.grid(row=0, column=0, **utils_position_setting_grid)

    frame_thread_type = ttk.LabelFrame(**utils_labelframe_params, text=name_frame_thread_type)

    label_thread_type = ttk.Label(frame_thread_type, text=name_label_thread_type)
    label_thread_type.pack(**utils_position_setting_pack)

    selected_text = StringVar(value=array_thread_type_names[0])


    def update_image(event):
        selected_item = combobox_thread_type.get()
        
        if selected_item == array_thread_type_names[0]:
            image_label.configure(image=image_thread_profile_1)
        elif selected_item == array_thread_type_names[1]:
            image_label.configure(image=image_thread_profile_2)
        elif selected_item == array_thread_type_names[2]:
            image_label.configure(image=image_thread_profile_3)


    image_thread_profile_1 = ImageTk.PhotoImage(Image.open(array_thread_type_images[0]).resize((375, 200)))
    image_thread_profile_2 = ImageTk.PhotoImage(Image.open(array_thread_type_images[1]).resize((375, 200)))
    image_thread_profile_3 = ImageTk.PhotoImage(Image.open(array_thread_type_images[2]).resize((375, 200)))

    combobox_thread_type = ttk.Combobox(frame_thread_type, values=array_thread_type_names)
    combobox_thread_type.bind("<<ComboboxSelected>>", update_image)
    combobox_thread_type.current(0)
    combobox_thread_type.pack(**utils_position_setting_pack)

    image_label = ttk.Label(frame_thread_type, image=image_thread_profile_1)
    image_label.pack(**utils_position_setting_pack)

    frame_thread_type.grid(row=0, column=1, **utils_position_setting_grid)

    def get_circle_selected(kd): # Получить 3Д-круг из выделения в редакторе
        iSelectionMng = iDocument3D.GetSelectionMng()

        try:
            if(iSelectionMng.GetCount() == 1):
                return circle_check(kd,iSelectionMng.GetObjectByIndex(0))
        except:
            showerror(title=name_warning_common_title, message=name_warning_edge_type_error)

        return None


    def click_button():
        spiral_height = entry_end_condition.get()
        spiral_step = entry_thread_pitch.get()
        kd = kompas_data()
        iMacro = True
        circle_selected = get_circle_selected(kd)
        my_bevel_settings = bevel_settings(2, 45)
        make_bevel(kd, circle_selected, my_bevel_settings)

        my_spiral_settings = spiral_settings(combobox_end_condition.get() == array_end_conditions[1], var_thread_direction.get(), spiral_height, spiral_step)
        my_spiral = spiral_on_circle(kd, circle_selected, my_spiral_settings, iMacro=iMacro)

        my_profile_settings = profile_settings(2, [])
        make_thread(kd, circle_selected, my_spiral, my_profile_settings, iMacro=iMacro)


    btn_create_thread = ttk.Button(frame_thread_setting, text="Построить", command=click_button)
    btn_create_thread.pack(**utils_position_setting_pack)

    root.mainloop()
