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


def spiral(spiral_height, spiral_step):
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
  iSpiral.Height = spiral_height #Высота спирали
  iSpiral.Step = spiral_step #Шаг навивки
  iSpiral.TurnDirection = True #Направление навивки
  #iSpiral.BasePlane = const_3d.o3d_planeXOZ #Установка базовой плоскости спирали
  iSpiral.Update()


if __name__ == '__main__':
  root = Tk()

  root.title('Библиотека 3D резьб')
  root.iconbitmap(default = "favicon.ico")

  label_end_conditions = ttk.Label(text = "Граничные условия")
  label_end_conditions.pack()

  end_conditions = ["Задать длину", "На всю длину"]
  cbox_end_conditions = ttk.Combobox(values = end_conditions)
  cbox_end_conditions.current(0)
  cbox_end_conditions.pack(anchor = NW, padx = 6, pady = 6)

  entry_end_conditions = ttk.Entry(root, width = 23)
  entry_end_conditions.pack(anchor = NW, padx = 6, pady = 6)
  entry_end_conditions.insert(0, "30.0")

  label_thread_pitch = ttk.Label(text = "Шаг резьбы")
  label_thread_pitch.pack()

  entry_thread_pitch = ttk.Entry(root, width = 23)
  entry_thread_pitch.pack(anchor = NW, padx = 6, pady = 6)
  entry_thread_pitch.insert(0, "5.0")

  label_thread_pitch = ttk.Label(text = "Направление резьбы")
  label_thread_pitch.pack()

  position = {"padx": 6, "pady": 6, "anchor": NW}
  thread_directions = ["Правая резьба", "Левая резьба"]
  default_thread_directions = StringVar(value = thread_directions[0])

  radiobtn_thread_right = ttk.Radiobutton(text = thread_directions[0], value = thread_directions[0], variable = default_thread_directions)
  radiobtn_thread_right.pack(**position)

  radiobtn_thread_left = ttk.Radiobutton(text = thread_directions[1], value = thread_directions[1], variable = default_thread_directions)
  radiobtn_thread_left.pack(**position)


  def click_btn_create_spiral():
    spiral_height = entry_end_conditions.get()
    spiral_step = entry_thread_pitch.get()
    spiral(spiral_height, spiral_step)


  btn_create_spiral = ttk.Button(text = "Построить", command = click_btn_create_spiral)
  btn_create_spiral.pack()

  root.mainloop()
