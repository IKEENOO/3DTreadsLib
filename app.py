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


def spiral(spiral_height, spiral_step):
    # создадим эскиз
    iPart7 = iKompasDocument3D.TopPart
    # iModelContainer = KAPI7.IModelContainer(iPart7)
    # Создаём спираль
    iAuxiliaryGeomContainer = KAPI7.IAuxiliaryGeomContainer(iPart7)
    # print(iModelObjects)
    iSpirals = iAuxiliaryGeomContainer.Spirals3D
    iSpiral = iSpirals.Add(const_3d.o3d_cylindricSpiral)
    iSpiral.SetBasePoint(0.0, 0.0)  # Опорная точка для построения спирали
    iSpiral.BuildingType = 1  # 1 - Построение по шагу и высоте
    iSpiral.BuildingDirection = False  # Выбор направления
    iSpiral.Height = spiral_height  # Высота спирали
    iSpiral.Step = spiral_step  # Шаг навивки
    iSpiral.TurnDirection = True  # Направление навивки
    # iSpiral.BasePlane = const_3d.o3d_planeXOZ # Установка базовой плоскости спирали
    iSpiral.Update()


if __name__ == '__main__':
    root = Tk()

    root.title('ThreadsLib')
    root.iconbitmap(default="favicon.ico")
    root.geometry("500x400")
    
    create_frame_end_condition()

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

    frame_thread_type = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10, 10])

    # Создание Entry
    entry = ttk.Entry(frame_thread_type, width=23)
    entry.pack(anchor=NW, padx=5, pady=5)
    entry.insert(0, "10.0 мм")

    frame_thread_type.grid(sticky=NW, row=0, column=1, padx=5, pady=5)


    def click_button():
        return


    btn_create_thread = ttk.Button(text="Построить", command=click_button)
    btn_create_thread.grid(row=5, column=1, padx=6, pady=6)

    root.mainloop()
