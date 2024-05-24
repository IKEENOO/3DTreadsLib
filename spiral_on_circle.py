# -*- coding: utf-8 -*-
#|44

import math

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

    iCurve = c_info.sel_param_5.GetCurve3D()
    iPlacement = iCurve.GetCurveParam().GetPlacement()
    cx=cy=cz=0
    iPoint3 = iPlacement.GetOrigin(cx, cy, cz)

    iSpiral_5 = kd.iKompasObject.TransferInterface(iSpiral_7,1,0)
    iSpiral_5.SetPlane(c_info.iPlane_5)

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


    #Нам понадобилось создавать скетч, чтобы понять насколько сильно нужно
    #сместить спираль в плоскости, чтобы она попала, куда надо
    iKompasDocument = kd.iApplication.ActiveDocument
    iKompasDocument3D = kd.KAPI7.IKompasDocument3D(iKompasDocument)
    iDocument3D = kd.iKompasObject.ActiveDocument3D()

    iPart7 = iKompasDocument3D.TopPart
    iPart = iDocument3D.GetPart(kd.const_3d.pTop_Part)
    iSketch_profile = iPart.NewEntity(kd.const_3d.o3d_sketch)
    iDefinition = iSketch_profile.GetDefinition()
    iDefinition.SetPlane(c_info.iPlane_5)
    iSketch_profile.Create()

    iDocument2D = iDefinition.BeginEdit()
    iKompasDocument2D = kd.KAPI7.IKompasDocument2D(iKompasDocument)
    iDocument2D = kd.iKompasObject.ActiveDocument2D()

    iSketch_7 = kd.iKompasObject.TransferInterface(iDefinition, 2, 0)
    iSketch_7.LeftHandedCS = True

    iCurve3D = iSpiral_5.GetCurve3D()

    #Точка начала спирали
    iPoint1 = iCurve3D.GetPoint(iCurve3D.GetParamMin(), cx, cy, cz)
    #Точка, находящаяся на противоположном конце диаметра спирали
    iPoint4 = iCurve3D.GetPoint((iCurve3D.GetParamMax()-iCurve3D.GetParamMin())/(iSpiral_5.step+1)/2, cx, cy, cz)

    try:
        #Получение координат точки iPoint1 в координатах эскиза, чтобы нарисовать в ней профиль
        bx=by=0
        rez1 = iSketch_7.GetPointProjectionToXY(iPoint3[1], iPoint3[2], iPoint3[3], bx, by)
        rez2 = iSketch_7.GetPointProjectionToXY((iPoint1[1] + iPoint4[1])/2, (iPoint1[2] + iPoint4[2])/2, (iPoint1[3] + iPoint4[3])/2, bx, by)
        spiralOffset = [rez1[1] - rez2[1], rez1[2] - rez2[2]]
    except:
        print("Ошибка при построении спирали!")
    finally: #Если в построении будет ошибка и не закрыть эскиз, то редактор зависнет
        #Поэтому эскиз надо закрыть в любом случае
        iDefinition.angle = 180
        iDefinition.EndEdit()

        if not iMacro is None:
            iSketch_7.Hidden = True
            #iMacroCollection.Add(iSketch_7)
            #iMacro.Update()
        iSketch_7.Update()

    iSpiral_5.SetLocation(spiralOffset[0],spiralOffset[1])
    iSpiral_7.Update()

    return iSpiral_7