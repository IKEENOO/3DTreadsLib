# -*- coding: utf-8 -*-
#|44

import pythoncom
from win32com.client import Dispatch, gencache

class kompas_data:
    def __init__(self):
        #  Подключим константы API Компас
        self.const = gencache.EnsureModule("{75C9F5D0-B5B8-4526-8681-9903C567D2ED}", 0, 1, 0).constants
        self.const_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants

        #  Подключим описание интерфейсов API5
        self.KAPI = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
        self.iKompasObject = self.KAPI.KompasObject(
            Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(self.KAPI.KompasObject.CLSID, pythoncom.IID_IDispatch))

        #  Подключим описание интерфейсов API7
        self.KAPI7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
        self.iApplication = self.KAPI7.IApplication(
            Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(self.KAPI7.IApplication.CLSID, pythoncom.IID_IDispatch))

        #  Получим активный документ
        self.iKompasDocument = self.iApplication.ActiveDocument
        self.iKompasDocument3D = self.KAPI7.IKompasDocument3D(self.iKompasDocument)
        self.iDocument3D = self.iKompasObject.ActiveDocument3D()