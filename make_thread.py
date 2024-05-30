# -*- coding: utf-8 -*-
#|44

import pythoncom
import math

class profile_settings:
    def __init__(self, shape, sizes):
        self.shape = shape
        """
        Форма профиля:
            0 - круг. Размеры: [радиус]
            1 - треугольник. Размеры: [основание, высота]
            2 - ГОСТ 9150-202: Размеры вычисляются сами на основании шага спирали
            3 - ГОСТ 9150-202 скругл: Размеры вычисляются сами на основании шага спирали
        """
        self.sizes = sizes #Линейные размеры элементов профиля

def make_thread(kd, c_info, iSpiral_7, p_settings, iMacro=None): #Создание профиля и резьбы
    # kd - переменная с константами Kompas3D
    iSpiral_5 = kd.iKompasObject.TransferInterface(iSpiral_7,1,0)

    iCurve = c_info.sel_param_5.GetCurve3D()
    iPlacement = iCurve.GetCurveParam().GetPlacement()
    iCurve3D = iSpiral_5.GetCurve3D()

    cx=cy=cz=0
    #Точка начала спирали, в которой можно построить профиль
    iPoint1 = iCurve3D.GetPoint(iCurve3D.GetParamMin(), cx, cy, cz)
    #Точка окончания спирали
    iPoint2 = iCurve3D.GetPoint(iCurve3D.GetParamMax(), cx, cy, cz)
    #Точка центра круга, на котором строится спираль
    iPoint3 = iPlacement.GetOrigin(cx, cy, cz)
    #Точка, находящаяся на противоположном конце диаметра спирали
    iPoint4 = iCurve3D.GetPoint((iCurve3D.GetParamMax()-iCurve3D.GetParamMin())/(iSpiral_5.step+1)/2, cx, cy, cz)

    iKompasDocument = kd.iApplication.ActiveDocument
    iKompasDocument3D = kd.KAPI7.IKompasDocument3D(iKompasDocument)
    iDocument3D = kd.iKompasObject.ActiveDocument3D()

    iPart7 = iKompasDocument3D.TopPart
    iPart = iDocument3D.GetPart(kd.const_3d.pTop_Part)

    iModelContainer = iPart7._oleobj_.QueryInterface(kd.KAPI7.IModelContainer.CLSID, pythoncom.IID_IDispatch)
    iModelContainer = kd.KAPI7.IModelContainer(iModelContainer)

    #Создание первой точки
    iPoints3D = iModelContainer.Points3D
    iPoint3D1 = iPoints3D.Add()
    iPoint3D1.ParameterType = kd.const_3d.ksPParamCoord
    iPoint3D1.Symbol = kd.const.ksDotPoint
    iPoint3D1.X = iPoint1[1]
    iPoint3D1.Y = iPoint1[2]
    iPoint3D1.Z = iPoint1[3]
    iPoint3D1_7 = kd.iKompasObject.TransferInterface(iPoint3D1, 2, 0)
    iPoint3D1.SetAssociationObject(iPoint3D1_7)
    #iPoint3D1.Name = "heeelp_point1" #На случай, если нам нужно будет удалять объект по названию
    if not iMacro is None:
        #iDefinition = iMacro.GetDefinition()
        #iDefinition.StaffVisible = True
        #iMacroCollection = iDefinition.FeatureCollection()
        iPoint3D1.Hidden = True
        #iMacroCollection.Add(iPoint3D1)
        #iMacro.Update()
    iPoint3D1.Update()

    #Создание второй точки
    iPoint3D2 = iPoints3D.Add()
    iPoint3D2.ParameterType = kd.const_3d.ksPParamCoord
    iPoint3D2.Symbol = kd.const.ksDotPoint
    iPoint3D2.X = iPoint2[1]
    iPoint3D2.Y = iPoint2[2]
    iPoint3D2.Z = iPoint2[3]
    iPoint3D2_7 = kd.iKompasObject.TransferInterface(iPoint3D2, 2, 0)
    iPoint3D2.SetAssociationObject(iPoint3D2_7)
    #iPoint3D2.Name = "heeelp_point2"
    if not iMacro is None:
        iPoint3D2.Hidden = True
        #iMacroCollection.Add(iPoint3D2)
        #iMacro.Update()
    iPoint3D2.Update()

    #Создание третьей точки
    iPoint3D3 = iPoints3D.Add()
    iPoint3D3.ParameterType = kd.const_3d.ksPParamCoord
    iPoint3D3.Symbol = kd.const.ksDotPoint
    iPoint3D3.X = iPoint3[1]
    iPoint3D3.Y = iPoint3[2]
    iPoint3D3.Z = iPoint3[3]
    iPoint3D3_7 = kd.iKompasObject.TransferInterface(iPoint3D3, 2, 0)
    iPoint3D3.SetAssociationObject(iPoint3D3_7)
    #iPoint3D3.Name = "heeelp_point3"
    if not iMacro is None:
        iPoint3D3.Hidden = True
        #iMacroCollection.Add(iPoint3D3)
        #iMacro.Update()

    iPoint3D3.Update()
    #Используя эти 3 точки можем построить плоскост, в которой будем рисовать профиль
    plane_profile = iPart.NewEntity(kd.const_3d.o3d_plane3Points)
    iDefinition = plane_profile.GetDefinition()
    iCollection = iPart.EntityCollection(kd.const_3d.o3d_point3D)
    iCollection.SelectByPoint(iPoint1[1], iPoint1[2], iPoint1[3])
    iPoint = iCollection.First()
    iDefinition.SetPoint(1, iPoint)
    iCollection = iPart.EntityCollection(kd.const_3d.o3d_point3D)
    iCollection.SelectByPoint(iPoint2[1], iPoint2[2], iPoint2[3])
    iPoint = iCollection.First()
    iDefinition.SetPoint(2, iPoint)
    iCollection = iPart.EntityCollection(kd.const_3d.o3d_point3D)
    iCollection.SelectByPoint(iPoint3[1], iPoint3[2], iPoint3[3])
    iPoint = iCollection.First()
    iDefinition.SetPoint(3, iPoint)
    #plane_profile.name = "heeelp_plane"
    iColorParam = plane_profile.ColorParam()
    iColorParam.color = 16776960
    if not iMacro is None:
        plane_profile.hidden = True
        #iMacroCollection.Add(iDefinition)
        #iMacro.Update()
    plane_profile.Create()

    #Создаём на плоскости эских и пытаемся на нём
    iSketch_profile = iPart.NewEntity(kd.const_3d.o3d_sketch)
    iDefinition = iSketch_profile.GetDefinition()
    iDefinition.SetPlane(plane_profile)
    iSketch_profile.Create()

    iDocument2D = iDefinition.BeginEdit()
    iKompasDocument2D = kd.KAPI7.IKompasDocument2D(iKompasDocument)
    iDocument2D = kd.iKompasObject.ActiveDocument2D()

    iSketch_7 = kd.iKompasObject.TransferInterface(iDefinition, 2, 0)
    iSketch_7.LeftHandedCS = True

    profile = None

    try:
        #Получение координат точки iPoint1 в координатах эскиза, чтобы нарисовать в ней профиль
        bx=by=0
        rez = iSketch_7.GetPointProjectionToXY(iPoint1[1], iPoint1[2], iPoint1[3], bx, by)
        rez2 = iSketch_7.GetPointProjectionToXY(iPoint4[1], iPoint4[2], iPoint4[3], bx, by)
        vector_inside = [rez2[1] - rez[1], rez2[2] - rez[2]]
        vector_OX = [-1, 0]
        vector_OY = [0, -1]

        scalar_prod_ox = vector_inside[0]*vector_OX[0] + vector_inside[1]*vector_OX[1]
        scalar_prod_oy = vector_inside[0]*vector_OY[0] + vector_inside[1]*vector_OY[1]

        #Компенсация различных вариантов систем координат из-за
        #повооротов Canvas в пространстве
        dir1 = 1 #Нужно для корректного направления вершины профиля
        if scalar_prod_ox*scalar_prod_oy <= 0:
            ox = 0
            oy = 1
            if scalar_prod_ox < 0 and scalar_prod_oy > 0:
                dir1 = -1
        else: #Компенсация эффекта "Елочки"
            ox = 1
            oy = 0
            if scalar_prod_ox > 0 and scalar_prod_oy > 0:
                dir1 = -1
        dir2 = -1 #Нужно для корректного смещения профиля чуть выше спирали
        if scalar_prod_ox >= 0: dir2 = 1

        if c_info.is_inside:
            dir1 *= -1
        #Создание профиля
        if p_settings.shape == 0: #Круглый профиль
            profile = iDocument2D.ksCircle(rez[1], -rez[2], p_settings.sizes[0], 1)
        elif p_settings.shape == 1: #Треугольный профиль: основание, высота
            width_offset = [0, p_settings.sizes[0]/2*dir2] #Ширина основания треугольника
            depth_offset = [p_settings.sizes[1]*dir1, 0]  #Высота основания треугольника

            profile = iDocument2D.ksLineSeg(rez[1], -rez[2], rez[1] + width_offset[ox]*2, -rez[2] + width_offset[oy]*2, 1)
            profile = iDocument2D.ksLineSeg(rez[1], -rez[2], rez[1], -rez[2], 1)
            profile = iDocument2D.ksLineSeg(rez[1] + width_offset[ox]*2, -rez[2] + width_offset[oy]*2, rez[1] - depth_offset[ox]  + width_offset[ox], -rez[2] - depth_offset[oy]  + width_offset[oy], 1)
            profile = iDocument2D.ksLineSeg(rez[1], -rez[2], rez[1] - depth_offset[ox]  + width_offset[ox], -rez[2] - depth_offset[oy]  + width_offset[oy], 1)
        elif p_settings.shape == 2: #Треугольный профиль: ГОСТ 9150-202
            P = iSpiral_5.step
            H = P * 0.866025404 #Эта константа была в ГОСТ
            angle = 60 * math.pi/180 #Угол профиля - 60

            A = [0, 0]
            B = [0, (7/8*P)*dir2]
            C = [-5/8*H*dir1, (7/8*P - 5/8*H*math.tan(math.pi/2 - angle))*dir2]
            D = [-5/8*H*dir1, (5/8*H*math.tan(math.pi/2 - angle))*dir2]

            profile = iDocument2D.ksLineSeg(rez[1] + A[ox], -rez[2] + A[oy], rez[1] + B[ox], -rez[2] + B[oy], 1)
            profile = iDocument2D.ksLineSeg(rez[1] + B[ox], -rez[2] + B[oy], rez[1] + C[ox], -rez[2] + C[oy], 1)
            profile = iDocument2D.ksLineSeg(rez[1] + C[ox], -rez[2] + C[oy], rez[1] + D[ox], -rez[2] + D[oy], 1)
            profile = iDocument2D.ksLineSeg(rez[1] + A[ox], -rez[2] + A[oy], rez[1] + D[ox], -rez[2] + D[oy], 1)

        elif p_settings.shape == 3: #Круглый профиль: ГОСТ 9150-202
            P = iSpiral_5.step

            dir_rad = 1
            if c_info.is_inside:
                P *= 0.95
                dir_rad *= -1

            H = P * 0.960491 #Эта константа была в ГОСТ
            R = 0.137329 * P # Эта константа была в ГОСТ
            alpha = 55 * math.pi/180 #Угол профиля - 55

            beta = math.pi - alpha
            m = R * math.tan(beta/2)
            nx = H/6
            mx = -nx + H
            my = P/2

            A = [0, 0]
            R1 = [-R*dir1, 0]
            C = [-(-nx + m*math.cos(alpha/2))*dir1, (m*math.sin(alpha/2))*dir2]
            D = [-(mx - m*math.cos(alpha/2))*dir1, (my - m*math.sin(alpha/2))*dir2]
            R2 = [-(mx-nx-R)*dir1, (my)*dir2]
            E = [-(mx - m*math.cos(alpha/2))*dir1, (my + m*math.sin(alpha/2))*dir2]
            F = [C[0], (P-m*math.sin(alpha/2))*dir2]
            G = [0, (P)*dir2]
            R3 = [-R*dir1, G[1]]

            profile = iDocument2D.ksArcByPoint(rez[1] + R1[ox], -rez[2] + R1[oy], R, rez[1] + A[ox], -rez[2] + A[oy], rez[1] + C[ox], -rez[2] + C[oy], dir_rad, 1)
            profile = iDocument2D.ksLineSeg(rez[1] + C[ox], -rez[2] + C[oy], rez[1] + D[ox], -rez[2] + D[oy], 1)
            profile = iDocument2D.ksArcByPoint(rez[1] + R2[ox], -rez[2] + R2[oy], R, rez[1] + D[ox], -rez[2] + D[oy], rez[1] + E[ox], -rez[2] + E[oy], -dir_rad, 1)
            profile = iDocument2D.ksLineSeg(rez[1] + E[ox], -rez[2] + E[oy], rez[1] + F[ox], -rez[2] + F[oy], 1)
            profile = iDocument2D.ksArcByPoint(rez[1] + R3[ox], -rez[2] + R3[oy], R, rez[1] + F[ox], -rez[2] + F[oy], rez[1] + G[ox], -rez[2] + G[oy], dir_rad, 1)
            profile = iDocument2D.ksLineSeg(rez[1] + G[ox], -rez[2] + G[oy], rez[1] + A[ox], -rez[2] + A[oy], 1)
        else:
            raise ValueError("Ошибка в типе профиля!")
    except:
        print("Ошибка при построении профиля!")
    finally: #Если в построении будет ошибка и не закрыть эскиз, то редактор зависнет
        #Поэтому эскиз надо закрыть в любом случае
        iDefinition.EndEdit()
        iDefinition.angle = 180
        if not iMacro is None:
            iSketch_7.Hidden = True
            #iMacroCollection.Add(iSketch_7)
            #iMacro.Update()
        iSketch_7.Update()


    #Вырезание на объекте резьбы
    extrusion_thread = iPart.NewEntity(kd.const_3d.o3d_cutEvolution)
    iDefinition = extrusion_thread.GetDefinition()
    iDefinition.cut = True
    iDefinition.cut = 1
    iDefinition.SetSketch(iSketch_profile)

    if p_settings.shape == 3 and not c_info.is_inside:
        iDefinition.sketchShiftType = 2 #Перемещать резец ортогонально спираль

    iArray = iDefinition.PathPartArray()
    iArray.Add(iCurve3D)
    iThinParam = iDefinition.ThinParam()
    iThinParam.thin = False
    #extrusion_thread.name = "heeelp_extrusion"
    iColorParam = extrusion_thread.ColorParam()
    iColorParam.ambient = 0.5
    iColorParam.color = 9474192
    iColorParam.diffuse = 0.6
    iColorParam.emission = 0.5
    iColorParam.shininess = 0.8
    iColorParam.specularity = 0.8
    iColorParam.transparency = 1
    #extrusion_thread.Create()

    if not iMacro is None:
        #iMacroCollection.Add(extrusion_thread)
        #iMacro.Update()
        pass
    extrusion_thread.Create()