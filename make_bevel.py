# -*- coding: utf-8 -*-
#|44

import pythoncom
import math

class bevel_settings:
    def __init__(self, length, angle):
        self.length = length #Длина грани фаски
        self.angle = angle #Угол, под которым выполняется операция фаски

def make_bevel(kd, c_info, b_settings, iMacro=None): #Создание профиля и резьбы
    # kd - переменная с константами Kompas3D
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

    #Наша фигура изменилась, поэтому для дальнейшего построения спирали нужно найти новую грань
    iCollection = iPart.EntityCollection(kd.const_3d.o3d_face)
    iCollection.SelectByPoint(iPointFace[1], iPointFace[2], iPointFace[3])
    iFace = iCollection.Last()
    c_info.iPlane_5 = iFace
    c_info.sel_param_5 = iFace.GetDefinition().EdgeCollection().First()
    c_info.sel_param_7 = kd.iKompasObject.TransferInterface(c_info.sel_param_5,2,0)

    iPart7 = kd.iKompasDocument3D.TopPart
    iPart = kd.iDocument3D.GetPart(kd.const_3d.pTop_Part)

    if not iMacro is None:
        #iDefinition = iMacro.GetDefinition()
        #iDefinition.StaffVisible = True
        #iMacroCollection = iDefinition.FeatureCollection()
        #iMacroCollection.Add(obj.GetFeature())
        #iMacro.Update()
        pass


