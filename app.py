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
from interface import *
'''
#  Подключим константы API Компас
const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
const_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants
#  Подключим описание интерфейсов API5
KAPI = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
iKompasObject = KAPI.KompasObject(
    Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(KAPI.KompasObject.CLSID, pythoncom.IID_IDispatch))
#  Подключим описание интерфейсов API7
KAPI7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
iApplication = KAPI7.IApplication(
    Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(KAPI7.IApplication.CLSID, pythoncom.IID_IDispatch))
#  Получим активный документ
if iApplication.ActiveDocument:
    iKompasDocument3D = KAPI7.IKompasDocument3D(iApplication.ActiveDocument)
    iDocument3D = iKompasObject.ActiveDocument3D()
else:
    showerror(title="Ошибка", message='Ошибка!\n\nНет активного документа.\nНеобходимо открыть документ типа "Деталь"')
'''

if __name__ == '__main__':
    root = Tk()

    root.title('ThreadsLib')
    root.iconbitmap(default="favicon.ico")
    # root.geometry("500x400")
    
    # create_frame_end_condition()
    # create_frame_thread_setting()
    # create_frame_thread_type()
    # create_frame_bevel_setting()

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

    def get_circle_selected(kd): # Получить 3Д-круг из выделения в редакторе
        iSelectionMng = iDocument3D.GetSelectionMng()

        try:
            if(iSelectionMng.GetCount() == 1): # Если выделен только один объект
                return circle_check(kd,iSelectionMng.GetObjectByIndex(0))
        except:
            showerror(title="Ошибка", message="Выдели ребро")

        return None


    def click_button():
        spiral_height = entry_end_condition.get()
        spiral_step = entry_thread_pitch.get()
        kd = kompas_data()
        circle_selected = get_circle_selected(kd)
        my_bevel_settings=bevel_settings(2, math.pi/4) # Bevel это значит фаска
        make_bevel(kd, circle_selected, my_bevel_settings)

        my_spiral_settings = spiral_settings(combobox_end_condition.get() == "На всю длину", var_thread_direction.get(), spiral_height, spiral_step)
        my_spiral = spiral_on_circle(kd, circle_selected, my_spiral_settings)

        #my_profile_settings=profile_settings(0, [2]) #Круглый профиль радиуса 2
        my_profile_settings=profile_settings(1, [2, 4]) #Треугольный профиль с основанием 2 и высотой 4
        make_thread(kd, circle_selected, my_spiral, my_profile_settings)


    btn_create_thread = ttk.Button(text="Построить", command=click_button)
    btn_create_thread.grid(row=3, column=0, padx=6, pady=6)

    root.mainloop()
