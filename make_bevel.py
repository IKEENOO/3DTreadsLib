import pythoncom
import math

class bevel_settings:
    def __init__(self, length, angle):
        self.length = length # Длина фаски
        self.angle = angle # Угол фаски

def make_bevel(kd, c_info, b_settings, iMacro=None):
    iCurve = c_info.sel_param_5.GetCurve3D()
    iPlacement = iCurve.GetCurveParam().GetPlacement()
    cx=cy=cz=0

    #Точка, в которой даже после фаски можно будет выбрать Face фигуры
    iPointFace = iPlacement.GetOrigin(cx, cy, cz)

    iPart = kd.iDocument3D.GetPart(kd.const_3d.pTop_Part)
    obj = iPart.NewEntity(kd.const_3d.o3d_chamfer)
    iDefinition = obj.GetDefinition()
    iDefinition.tangent = True
    iDefinition.SetChamferParam(True, b_settings.length, b_settings.length*math.tan(b_settings.angle/360*2*math.pi))

    iArray = iDefinition.array()
    iArray.Add(c_info.sel_param_5)
    obj.Create()

    # Объект изменился, для дальнейшего построения спирали нужно найти новую грань
    if c_info.is_inside:
        distance = 100000000
        MyCollection = c_info.iPlaneNear_5.EdgeCollection()
        for i in range(MyCollection.GetCount()):
             edge = MyCollection.GetByIndex(i)
             if edge.IsCircle():
                 iCurve = edge.GetCurve3D()
                 iPlacement = iCurve.GetCurveParam().GetPlacement()
                 iPointEdge = iPlacement.GetOrigin(cx, cy, cz)

                 distance_new = pow((iPointEdge[0] - iPointFace[0]),2) + pow((iPointEdge[1] - iPointFace[1]),2) + pow((iPointEdge[2] - iPointFace[2]),2)
                 if distance_new < distance:
                    c_info.sel_param_5 = edge
        c_info.sel_param_7 = kd.iKompasObject.TransferInterface(c_info.sel_param_5,2,0)
    else:
        iCollection = iPart.EntityCollection(kd.const_3d.o3d_face)
        iCollection.SelectByPoint(iPointFace[1], iPointFace[2], iPointFace[3])
        iFace = iCollection.Last()
        c_info.iPlane_5 = iFace
        c_info.sel_param_5 = iFace.GetDefinition().EdgeCollection().First()
        c_info.sel_param_7 = kd.iKompasObject.TransferInterface(c_info.sel_param_5,2,0)

    if not iMacro is None:
        pass
