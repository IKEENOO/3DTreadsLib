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

  position = {"padx": 6, "pady": 6, "anchor": NW}

  label_end_conditions = ttk.Label(text = "Граничные условия")
  label_end_conditions.pack()

  end_conditions = ["Задать длину", "На всю длину"]
  cbox_end_conditions = ttk.Combobox(values = end_conditions)
  cbox_end_conditions.current(0)
  cbox_end_conditions.pack(**position)

  
  def cbox_selected(event):
    # получаем выделенный элемент
    selection = cbox_end_conditions.get()
    if selection == "Задать длину":
      entry_end_conditions["state"] = "normal"
    else:
      entry_end_conditions["state"] = "disabled"  


  cbox_end_conditions.bind("<<ComboboxSelected>>", cbox_selected)

  entry_end_conditions = ttk.Entry(root, width = 23)
  entry_end_conditions.pack(**position)
  entry_end_conditions.insert(0, "30.0")  

  label_thread_pitch = ttk.Label(text = "Шаг резьбы")
  label_thread_pitch.pack()

  entry_thread_pitch = ttk.Entry(root, width = 23)
  entry_thread_pitch.pack(**position)
  entry_thread_pitch.insert(0, "5.0")

  label_thread_pitch = ttk.Label(text = "Направление резьбы")
  label_thread_pitch.pack()

  thread_directions = ["Правая резьба", "Левая резьба"]
  #thread_direction_right = True
  #thread_direction_left = False
  #default_thread_directions = StringVar(value = thread_directions[0])

  rb_var = BooleanVar()
  rb_var.set(1)

  radiobtn_thread_right = ttk.Radiobutton(text = thread_directions[0], value = 1, variable = rb_var)
  radiobtn_thread_right.pack(**position)

  radiobtn_thread_left = ttk.Radiobutton(text = thread_directions[1], value = 0, variable = rb_var)
  radiobtn_thread_left.pack(**position)


  def get_circle_selected(kd): #Получить 3Д-круг из выделения в редакторе
      iSelectionMng = iDocument3D.GetSelectionMng()
      
      try:
        if(iSelectionMng.GetCount() == 1): #Если выделен только один объект
          return circle_check(kd,iSelectionMng.GetObjectByIndex(0))
      except:
        #print("Выдели одно из рёбер цилиндра!")
        showerror(title="Ошибка", message="Выдели ребро")
      
      return None


  def click_btn_create_spiral():
    spiral_height = entry_end_conditions.get()
    spiral_step = entry_thread_pitch.get()
    #spiral(spiral_height, spiral_step)

    kd = kompas_data()

    circle_selected = get_circle_selected(kd)

    if circle_selected != None:
        my_bevel_settings=bevel_settings(2, math.pi/4) # Bevel это значит фаска
        make_bevel(kd, circle_selected, my_bevel_settings)

        my_spiral_settings = spiral_settings(cbox_end_conditions.get() == "На всю длину", rb_var.get(), spiral_height, spiral_step)
        my_spiral = spiral_on_circle(kd, circle_selected, my_spiral_settings)

        #my_profile_settings=profile_settings(0, [2]) #Круглый профиль радиуса 2
        my_profile_settings=profile_settings(1, [2, 4]) #Треугольный профиль с основанием 2 и высотой 4
        make_thread(kd, circle_selected, my_spiral, my_profile_settings)



  btn_create_spiral = ttk.Button(text = "Построить", command = click_btn_create_spiral)
  btn_create_spiral.pack()

  root.mainloop()
