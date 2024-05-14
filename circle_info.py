class circle_info: #Информация о грани, на которой будет строиться спираль
    def __init__(self, sel_param_5, sel_param_7, iPlane_5, iPlaneNear_5):
        self.sel_param_5 = sel_param_5 #Представление выделенного объекта в API5
        self.sel_param_7 = sel_param_7 #Представление выделенного объекта в API7
        self.iPlane_5 = iPlane_5 #Грань, соответствующая выделенному ребру
        self.iPlaneNear_5 = iPlaneNear_5 #Грань, соответствующая боковому ребру цилиндра

def circle_check(kd, circle_candidate): #Подходит для для построения спирали выделенный 3Д-круг?
    # kd - это KompasData - типовые объекты, которые следует передать
    if circle_candidate.type == 7:
        param_5 = circle_candidate.GetDefinition()
        param_7 = kd.iKompasObject.TransferInterface(param_5,2,0)
        iPlane_5 = None
        iPlaneNear_5 = None

        if param_5.IsCircle(): #Если ребро имеет форму круга
            #print("Это круг!")
            if not(param_7.IsSketchEdge): #Если это НЕ ребро эскиза
                #print("Это реальный круг, а не эскиз!")
                """
                Волшебный код...
                В общем чтобы получить грань (а вместе с ней и нужное направление
                спирали) необходимо применять метод с параметром True или False
                В результате экспериментов было установлено, что правильно грань
                определяется, если при поиске соседних граней у нас возвращается
                коллекция из одного элемента (что логично для цилиндра)

                Вот по этой причине и возникает нехитрый перебор False, а потом True
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
                    print("Я уже не знаю, что пошло не так...")
            else:
                print("Тебе нужно выделить ребро ОБЪЕКТА, а не экскиза, формы 'Окружность'!")
        else:
            print("Тебе нужно выделить ребро формы 'ОКРУЖНОСТЬ'!")
    else:
        print("Тебе нужно выделить РЕБРО формы 'Окружность'!")
        return None

    return circle_info(param_5, param_7, iPlane_5, iPlaneNear_5)
