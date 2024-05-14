import pythoncom

class profile_settings:
    def __init__(self, shape, sizes):
        self.shape = shape #Форма профиля (0 - круг, 1 - треугольник)
        self.sizes = sizes #Линейные размеры элементов профиля

        #Реализован пока что только круг :(
        #Для круга всего один размер - радиус
        #Для равтостороннего треугольника было бы два: ширина основания и высота

def make_thread(kd, c_info, iSpiral_7, p_settings): #Создание профиля и резьбы
    # kd - это KompasData - типовые объекты, которые следует передать
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

    #print("Spiral begin", iPoint1)
    #print("Spiral end", iPoint2)
    #print("Сircle center", iPoint3)

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
    iPoint3D1.Name = "heeelp_point1" #На случай, если нам нужно будет удалять объект по названию
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
    iPoint3D2.Name = "heeelp_point2" #На случай, если нам нужно будет удалять объект по названию
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
    iPoint3D3.Name = "heeelp_point3" #На случай, если нам нужно будет удалять объект по названию
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
    plane_profile.name = "heeelp_plane"
    iColorParam = plane_profile.ColorParam()
    iColorParam.color = 16776960
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
        #print(rez)
        if p_settings.shape == 0:
            profile = iDocument2D.ksCircle(rez[1], -rez[2], p_settings.sizes[0], 1)
        else:
            raise ValueError("Неверный номер профиля резьбы!")
    except:
        print("Ошибки в построении профиля")
    finally: #Если в построении будет ошибка и не закрыть эскиз, то редактор зависнет
        #Поэтому эскиз надо закрыть в любом случае
        iDefinition.EndEdit()
        iDefinition.angle = 180
        iSketch_7.Update()


    #Вырезание на объекте резьбы
    extrusion_thread = iPart.NewEntity(kd.const_3d.o3d_cutEvolution)
    iDefinition = extrusion_thread.GetDefinition()
    iDefinition.cut = True
    iDefinition.cut = 1
    iDefinition.SetSketch(iSketch_profile)
    iArray = iDefinition.PathPartArray()
    iArray.Add(iCurve3D)
    iThinParam = iDefinition.ThinParam()
    iThinParam.thin = False
    extrusion_thread.name = "Резьба:1"
    iColorParam = extrusion_thread.ColorParam()
    iColorParam.ambient = 0.5
    iColorParam.color = 9474192
    iColorParam.diffuse = 0.6
    iColorParam.emission = 0.5
    iColorParam.shininess = 0.8
    iColorParam.specularity = 0.8
    iColorParam.transparency = 1
    extrusion_thread.Create()
