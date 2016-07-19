# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from CBase import *
from decimal import *

class CPlanillaBase(CBase):
    pdFecSis = None
    lcFases  = None
    pcCodPla = None
    pcDescri = None
    pcFecSis = None
    lnTipCam = 0
    lnAsiFam = 0
    laImpRen = None
    laNroDoc = []
    laAporta = []
    
    # Valida si hay planilla abierta y carga la fecha del sistema
    def mxValPlanilla(self):
        # Carga fecha del sistema
        RS = self.loSql.omExecRS("SELECT cConVar FROM S01TVAR WHERE cNomVar = 'GDFECSIS'")
        if len(RS) == 0:
           self.pcError = '<DATA><ERROR>ERROR: FECHA DEL SISTEMA NO DEFINIDO [GDFECSIS]. AVISE A TI</ERROR></DATA>'
           return False
        self.ldFecSis = self.mxValDate(RS[0][0])
        if self.ldFecSis == None:
           self.pcError = '<DATA><ERROR>ERROR: FECHA DEL SISTEMA INVALIDA [GDFECSIS]. AVISE A TI</ERROR></DATA>'
           return False
        # Verifica si hay una planilla abierta
        lcSql = "SELECT COUNT(*) FROM ADM.E01MPLA WHERE cEstado = 'A'"
        RS = self.loSql.omExecRS(lcSql)
        if RS[0][0] > 1:
           self.pcError = '<DATA><ERROR>ERROR: HAY VARIAS PLANILLAS ABIERTAS. NO PUEDE CONTINUAR</ERROR></DATA>'
           return False
        elif RS[0][0] == 0:
           self.pcError = '<DATA><ERROR>ERROR: NO HAY PLANILLA ABIERTA. NO PUEDE CONTINUAR</ERROR></DATA>'
           return False
        # Trae datos de planilla abierta
        lcSql = "SELECT cCodPla, cDescri, cFases FROM ADM.E01MPLA WHERE cEstado = 'A'"
        RS = self.loSql.omExecRS(lcSql)
        self.pcCodPla = RS[0][0]
        self.pcDescri = RS[0][1]
        self.lcFases  = RS[0][2]
        return True

    # Validar usuario y estado de fases de planilla  (OK)
    def mxValInit(self):
        # Condiciones de excepcion
        if self.mxEmpty(self.pcCodUsu):
           self.pcError = 'Codigo de usuario vacio'
           return False
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Valida el usuario
        RS = self.loSql.omExecRS("SELECT cCodUsu FROM S01TUSU WHERE cCodUsu = '" + self.pcCodUsu + "'")   # OJOFPM FALTA VALIDAR SI EL USUARIO TIENE PERMISO PARA LA OPCION
        if RS[0][0] == None:
           self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO EXISTE EN [S01TUSU]</ERROR></DATA>'
           self.loSql.omDisconnect()
           return False
        # Valida si hay planilla abierta
        RS = self.loSql.omExecRS("SELECT COUNT(cCodPla) FROM ADM.E01MPLA WHERE cEstado = 'A'")
        if RS[0][0] == 0:
           self.pcError = '<DATA><ERROR>NO HAY PLANILLAS ABIERTAS</ERROR></DATA>'
           self.loSql.omDisconnect()
           return False
        elif RS[0][0] > 1:
           self.pcError = '<DATA><ERROR>HAY MAS DE UNA PLANILLA ABIERTA. AVISE A TI</ERROR></DATA>'
           self.loSql.omDisconnect()
           return False
        RS = self.loSql.omExecRS("SELECT cCodPla, cDescri, cFases FROM ADM.E01MPLA WHERE cEstado = 'A'")
        self.pcCodPla = RS[0][0]
        self.pcDescri = RS[0][1]
        self.lcFases  = RS[0][2]
        self.loSql.omDisconnect()
        return True

    # Numero de documentos por oficina (documento de referencia en contabilidad)
    def mxNumeroDocumentoOficina(self):
        self.laNroDoc = []
        j = 0
        RS = self.loSql.omExecRS('SELECT cCodOfi FROM S01TOFI ORDER BY cCodOfi')
        for XOFI in RS:
            lcCodigo = XOFI[0] + self.pcTermId + '09'   # 09: Planillas
            lcSql = "SELECT MAX(cNroDoc) FROM ADM.E10DCNT WHERE SUBSTRING(cNroDoc, 1, 7) = '" + lcCodigo + "'"
            RS = self.loSql.omExecRS(lcSql)
            if RS == None or RS[0][0] == None:
               lcNumero = '00000'
            else:
               lcNumero = RS[0][0]
               lcNumero = lcNumero[-5:]   # 6 digitos de la derecha
            i = int(lcNumero) + 1
            lcNumero = '0000' + str(i)
            lcNumero = lcNumero[-5:]
            self.laNroDoc.append([])
            self.laNroDoc[j].append(XOFI[0])
            self.laNroDoc[j].append(XOFI[0] + self.pcTermId + '09' + lcNumero)
            self.laNroDoc[j].append(0)
            j += 1
        # Verifica si hay oficinas            
        if j == 0:
           self.pcError = '<DATA><ERROR>NO HAY OFICINAS DEFINIDAS</ERROR></DATA>'
           return False
        return True

    # Genera siguiente numero de comprobante
    def mxNroComprobante(self, p_cNroCom):
        lcNroCom = p_cNroCom.strip() + '%'
        lcSql = "SELECT MAX(cNroCom) FROM CNT.D01MDIA WHERE cNroCom LIKE '" + lcNroCom + "'"
        RS = self.loSql.omExecRS(lcSql)
        lcNumero = '0000';
        if RS[0][0] != None:
           lcNumero = RS[0][0]
           lcNumero = lcNumero[8:]
        lcNumero = '000' + str(int(lcNumero) + 1)
        lcNumero = lcNumero[-4:]
        lcNroCom = lcNroCom[:8] + lcNumero
        return lcNroCom
        

