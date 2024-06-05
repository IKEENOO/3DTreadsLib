from tkinter.messagebox import showwarning
from lang import *

class circle_info: # Описание грани, на которой производится построение спирали
    def __init__(self, sel_param_5, sel_param_7, iPlane_5, iPlaneNear_5, is_inside):
        self.sel_param_5 = sel_param_5 # Представление выделенного объекта в API5
        self.sel_param_7 = sel_param_7 # Представление выделенного объекта в API7
        self.iPlane_5 = iPlane_5 # Грань, соответствующая выделенному ребру
        self.iPlaneNear_5 = iPlaneNear_5 # Грань, соответствующая боковому ребру цилиндра

        # Получение радиуса выделенной окружности
        self.radius = None
        if self.sel_param_5.GetCurve3D() != None:
            iCurve = self.sel_param_5.GetCurve3D()
            iCircle = iCurve.GetCurveParam()
            self.radius = iCircle.radius

        self.is_inside = is_inside

        # Получение высоты цилиндрической грани
        self.cylinder_height = None
        if iPlaneNear_5 != None:
            self.cylinder_height = 0
            if self.iPlaneNear_5.IsCylinder():
                rez = self.iPlaneNear_5.GetCylinderParam()
                self.cylinder_height = rez[1]

def circle_check(kd, circle_candidate): # Проверка выделенного объекта на соответствование требованиям для построения
    if circle_candidate.type == 7:
        param_5 = circle_candidate.GetDefinition()
        param_7 = kd.iKompasObject.TransferInterface(param_5,2,0)
        iPlane_5 = None
        iPlaneNear_5 = None

        if param_5.IsCircle(): # Если ребро имеет форму круга
            if not(param_7.IsSketchEdge): # Если выбрано ребро объекта
                """
                Чтобы получить грань,а вместе с ней и нужное направление
                спирали, необходимо применять метод с параметром True или False
                Грань определяется правильно, если при поиске соседних граней 
                возвращается коллекция из одного элемента
                """

                is_correct_object = False
                directions = [True, False]
                for i in directions:
                    iPlane_5 = param_5.GetAdjacentFace(directions[i])
                    if iPlane_5.ConnectedFaceCollection().GetCount() == 1:
                        iPlaneNear_5 = iPlane_5.ConnectedFaceCollection().First()
                        if(iPlaneNear_5.IsCylinder()):
                            is_correct_object = True
                            break
                if not(is_correct_object):
                    for i in directions:
                        iPlane_5 = param_5.GetAdjacentFace(directions[i])
                        for k in range(iPlane_5.ConnectedFaceCollection().GetCount()):
                            iPlaneNear_5 = iPlane_5.ConnectedFaceCollection().GetByIndex(k)
                            if(iPlaneNear_5.IsCylinder()):
                                return circle_info(param_5, param_7, iPlane_5, iPlaneNear_5, True)
                    showwarning(title=name_warning_common_title, message=name_warning_default_circle_info)
                    return None
            else:
                showwarning(title=name_warning_common_title, message=name_warning_object_edge_error)
                return None
        else:
            showwarning(title=name_warning_common_title, message=name_warning_edge_type_error)
            return None
    else:
        showwarning(title=name_warning_common_title, message=name_warning_edge_select_error)
        return None

    return circle_info(param_5, param_7, iPlane_5, iPlaneNear_5, False)
