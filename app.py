from tkinter import *
from tkinter import ttk

from tkinter.messagebox import showerror, showwarning, showinfo
import pythoncom
from win32com.client import Dispatch, gencache


#  Подключим константы API Компас
const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
const_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants
#  Подключим описание интерфейсов API5
KAPI = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
iKompasObject = KAPI.KompasObject(Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(KAPI.KompasObject.CLSID, pythoncom.IID_IDispatch))
#  Подключим описание интерфейсов API7
KAPI7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
iApplication = KAPI7.IApplication(Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(KAPI7.IApplication.CLSID, pythoncom.IID_IDispatch))
#  Получим активный документ
if iApplication.ActiveDocument:
  iKompasDocument3D = KAPI7.IKompasDocument3D(iApplication.ActiveDocument)
  iDocument3D = iKompasObject.ActiveDocument3D()
else:
  showerror(title="Ошибка", message="Документ не активен")


def spiral():
  #создадим эскиз
  iPart7 = iKompasDocument3D.TopPart
  #iModelContainer = KAPI7.IModelContainer(iPart7)
  #Создаём спираль
  iAuxiliaryGeomContainer = KAPI7.IAuxiliaryGeomContainer(iPart7)
  #print(iModelObjects)
  iSpirals = iAuxiliaryGeomContainer.Spirals3D
  iSpiral = iSpirals.Add(const_3d.o3d_cylindricSpiral)
  iSpiral.SetBasePoint(0.0, 0.0) #Опорная точка для построения спирали
  iSpiral.BuildingType = 1 #1 - Построение по шагу и высоте
  iSpiral.BuildingDirection = False #Выбор направления
  iSpiral.Height = 30.0 #Высота спирали
  iSpiral.Step = 5.0 #Шаг навивки
  iSpiral.TurnDirection = True #Направление навивки
  #iSpiral.BasePlane = const_3d.o3d_planeXOZ #Установка базовой плоскости спирали
  iSpiral.Update()


if __name__ == '__main__':
  root = Tk()
  root.title('Библиотека 3D резьб')
  root.iconbitmap(default="favicon.ico")
  end_conditions = ["Задать длину", "На всю длину"]
  combobox = ttk.Combobox(values=end_conditions)
  combobox.current(0)
  combobox.pack(anchor=NW, padx=6, pady=6)
  entry = ttk.Entry(root, width=23)
  entry.pack(anchor=NW, padx=6, pady=6)
  entry.insert(0, "10.0 мм")
  
  clicks = 0
  
  def click_button():
    label["text"] = entry.get()   

  
  btn = ttk.Button(text="Click Me", command=click_button)
  btn.pack(anchor=NW, padx=6, pady=6)
  label = ttk.Label()
  label.pack(anchor=NW, padx=6, pady=6)

  entry_override_pitch = ttk.Entry(root, width=23)
  entry.pack(anchor=NW, padx=6, pady=6)
  entry.insert(0, "1,5")

  position = {"padx": 6, "pady": 6, "anchor": NW}

  right_thread = "Правая резьба)"
  left_thread = "Левая резьба"

  thread_direction = StringVar(value=right_thread)

  header = ttk.Label(textvariable=thread_direction)
  header.pack(**position)

  right_thread_btn = ttk.Radiobutton(text=right_thread, value=right_thread, variable=thread_direction)
  right_thread_btn.pack(**position)

  left_thread_btn = ttk.Radiobutton(text=left_thread, value=left_thread, variable=thread_direction)
  left_thread_btn.pack(**position)
  root.mainloop()