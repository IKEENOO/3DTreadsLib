# -*- coding: utf-8 -*-
#|44

class spiral_settings: #Информация о настройках построения спирали
    def __init__(self, is_object_height, direction, spiral_height, spiral_step):
        self.is_object_height = is_object_height #Строить спираль по длине объекта?
        self.direction = direction #направление навивки (True - прямое)
        self.spiral_height = spiral_height #Высота спирали (не имеет смысла при построении по длине объекта)
        self.spiral_step = spiral_step #длина шага спирали

def spiral_on_circle(kd, c_info, settings, iMacro=None): #Построение спирали на 3Д-круге
    # kd - переменная с константами Kompas3D

    #Построение спирали
    iPart7 = kd.iKompasDocument3D.TopPart
    iAuxiliaryGeomContainer = kd.KAPI7.IAuxiliaryGeomContainer(iPart7)
    iSpirals = iAuxiliaryGeomContainer.Spirals3D
    iSpiral_7 = iSpirals.Add(kd.const_3d.o3d_cylindricSpiral)

    iSpiral_5 = kd.iKompasObject.TransferInterface(iSpiral_7,1,0)
    iSpiral_5.SetPlane(c_info.iPlane_5)
    iSpiral_5.SetLocation(0,0)
    iSpiral_5.diamType = 0
    iSpiral_5.diam = c_info.radius*2
    iSpiral_5.buildMode = 1 #1 - Построение по шагу и высоте
    iSpiral_5.buildDir = False #Выбор направления
    iSpiral_5.heightType = 0

    #Высота спирали
    if settings.is_object_height: #Определять высоту по длине объекта?
        iSpiral_5.height = c_info.cylinder_height
    else:
        iSpiral_5.height = settings.spiral_height

    iSpiral_5.step = settings.spiral_step #Шаг навивки
    iSpiral_5.turnDir = settings.direction #Направление навивки

    if not iMacro is None:
        #iDefinition = iMacro.GetDefinition()
        #iDefinition.StaffVisible = True
        #iMacroCollection = iDefinition.FeatureCollection()
        iSpiral_7.Hidden = True
        #iMacroCollection.Add(iSpiral_7)
        #iMacro.Update()
    iSpiral_7.Update()
    return iSpiral_7