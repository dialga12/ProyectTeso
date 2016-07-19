# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from CBase import *

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

    def mxNroComprobante(self, p_cNroCom):
        lcNroCom = p_cNroCom.strip() + '%'
        RS = self.loSql.omExecRS("SELECT MAX(cNroCom) FROM CNT.D01MDIA WHERE cNroCom LIKE '" + lcNroCom + "'")
        lcNumero = '000000';
        if RS[0][0] != None:
           lcNumero = RS[0][0]
           lcNumero = lcNumero[6:]
        lcNumero = '00000' + str(int(lcNumero) + 1)
        lcNumero = lcNumero[:6]
        lcNroCom = lcNroCom[:6] + lcNumero   # OJOFPM FALTA EL MES
        return lcNroCom

    # Validar usuario y estado de fases de planilla
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

    def mxNumeroDocumentoOficina(self):
        j = 0
        RS = self.loSql.omExecRS('SELECT cCodOfi FROM S01TOFI ORDER BY cCodOfi')
        for XOFI in RS:
            lcCodigo = XOFI[0] + self.pcTermId + '09'
            lcSql = "SELECT MAX(cNroDoc) FROM ADM.E10DCNT WHERE SUBSTRING(cNroDoc, 1, 7) = '" + lcCodigo + "'"
            RS1 = self.loSql.omExecRS(lcSql)
            if RS1 == None or RS1[0][0] == None:
               lcNumero = '00000'
            else:
               lcNumero = RS1[0][0]
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
           self.pcError = '<DATA><ERROR>NO HAY OFICINAS DEFINIDASŗ</ERROR></DATA>'
           return False
        return True
        
##############################################################
# Clase que procesa planillas
##############################################################
class CPlanillas(CPlanillaBase):
    paAnhos  = None
    paNumero = None
    pcNumero = None

    def omApertura(self):
        # Condiciones de excepcion
        if self.mxEmpty(self.pcCodPla):
           self.pcError = '<DATA><ERROR>CODIGO DE PLANILLA VACIO</ERROR></DATA>'
           return False
        elif len(self.pcCodPla) != 5:
           self.pcError = '<DATA><ERROR>LONGITUD DE CODIGO DE PLANILLA ERRADO</ERROR></DATA>'
           return False
        elif self.mxEmpty(self.pcDescri):
           self.pcError = '<DATA><ERROR>DESCRIPCION DE PLANILLA VACIA</ERROR></DATA>'
           return False
        elif self.mxEmpty(self.pcCodUsu):
           self.pcError = '<DATA><ERROR>CODIGO DE USUARIO VACIO</ERROR></DATA>'
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Verifica que todas las planillas esten cerradas
        lcSql = "SELECT cEstado FROM ADM.E01MPLA WHERE cEstado != 'B' LIMIT 1"
        RS = self.loSql.omExecRS(lcSql)
        if RS != None:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>ERROR: HAY PLANILLAS ABIERTAS. NO PUEDE CONTINUAR</ERROR></DATA>'
           return False
        # Valida usuario
        lcSql = "SELECT cCodUsu FROM S01TUSU WHERE cCodUsu = '" + self.pcCodUsu + "'"
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO EXISTE EN TABLA DE USUARIOS [S01TUSU]</ERROR></DATA>'
           return False
        # Verifica codigo de planilla
        lcSql = "SELECT cEstado FROM ADM.E01MPLA WHERE cCodPla = '" + self.pcCodPla + "'"
        RS = self.loSql.omExecRS(lcSql)
        if RS != None:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>CODIGO DE PLANILLA YA EXISTE</ERROR></DATA>'
           return False
        # Graba maestro de planillas
        lcSql = "INSERT INTO ADM.E01MPLA (cCodPla, cDescri, cTipo, cFases, cCodUsu) VALUES ('" + self.pcCodPla + "', '" + self.pcDescri + "', 'E', '0000000000', '" + self.pcCodUsu + "')"
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>ERROR AL GRABAR MAESTRO DE PLANILLA [E01MPLA]</ERROR></DATA>'
           return False
        lcSql = "SELECT MAX(cCodigo) FROM ADM.E01PPLA"
        RS = self.loSql.omExecRS(lcSql)
        # Ultimo codigo de empleado en planilla
        if RS == None or RS[0][0] == None:
           lcCodigo = '000000'
        else:
           lcCodigo = RS[0][0]
        j = 0
        lcSql = "SELECT cCodEmp FROM ADM.E01MEMP WHERE cEstado = 'A' ORDER BY cCodEmp"
        RS = self.loSql.omExecRS(lcSql)
        for XPLA in RS:
            j += 1
            i = int(lcCodigo) + 1
            lcCodigo = '00000' + str(i)
            lcCodigo = lcCodigo[-6:]
            lcSql = "INSERT INTO ADM.E01PPLA (cCodigo, cCodPla, cCodEmp, cCodUsu) VALUES ('" + lcCodigo + "', '" + self.pcCodPla + "', '" + XPLA[0] + "', '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
        if j == 0:
           self.pcError = '<DATA><ERROR>ERROR EN APERTUDA DE PLANILLA: NO HAY EMPLEADOS ACTIVOS</ERROR></DATA>';
           llOk = False
        else:
           self.loSql.omCommit()
           self.pcReturn = '<DATA><AVISO>GRABACION CONFORME</AVISO></DATA>'
        self.loSql.omDisconnect()
        return llOk

    def omInicio(self):
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Verifica que no haya planillas abiertas
        lcSql = "SELECT cCodPla FROM E01MPLA WHERE cEstado != 'E' LIMIT 1"
        RS = self.loSql.omExecRS(lcSql)
        if not RS == None:
           lcCodPla = RS[0][0]
           self.loSql.omDisconnect()
           self.pcError = 'HAY PLANILLA(S) QUE NO ESTA(N) CERRADA(S) [' + lcCodPla + ']'
           return False
        self.loSql.omDisconnect()
        # Carga valores para combos
        self.mxMeses()
        self.paAnhos = ['2012', '2013', '2014', '2015']
        self.paNumero = ['1', '2', '3', '4']
        return True

    def omAdelantoQuincena(self):
        # Condiciones de excepcion
        if self.mxEmpty(self.pcCodUsu):
           self.pcError = 'ERROR: CODIGO DE USUARIO VACIO'
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Realiza la apertura de planilla
        lcSql = "SELECT * FROM f_GenerarQuincena('" + self.pcCodUsu + "')"
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = 'ERROR AL REALIZAR EL ADELANTO DE QUINCENA. INFORME A TI'
           return False
        lcXml = RS[0][0]
        self.loSql.omCommit()
        # Evalua error
        lcError = None
        loRoot = ET.fromstring(lcXml)
        for lo in loRoot:
            if lo.tag == 'ERROR':
               lcError = lo.text
        if not lcError == None:
           self.loSql.omDisconnect()
           self.pcError = lcError
           return False
        # Trae datos para impresion
        lcSql = "SELECT cCodigo, cCodEmp, cNombre, cConcep, nMonto FROM V_Conceptos WHERE cCodPla IN (SELECT cCodPla FROM E01MPLA WHERE cEstado = 'B') AND cConcep = 'D01' ORDER BY cNombre"
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = 'ERROR: NO HAY DATOS PARA IMPRIMIR'
           return False
        # Impresion
        #loFile = open('REP001.prn', 'w')
        #loFile.write('[GCCODUSU]=None\n')
        #loFile.close()
        lcFecSis = '2013-01-17'
        import time
        lcTime = time.asctime()
        lcTime = lcTime[:19]
        lcTime = lcTime[11:]
        lnPag = 1
        lnTotal = 0
        print('CRAC INCASUR SA     ADELANTO DE QUINCENA                     PAG.:' + str(lnPag))
        print('ADM2120                                         ' + lcFecSis)
        print('PLANILLAS                                         ' + lcTime)
        print('-------------------------------------------------------------------')
        print('CODIGO NOMBRE                                                 MONTO')
        print('-------------------------------------------------------------------')
        for i in RS:
            print(i[1], self.mxSpace(i[2], 35), '{0:12,.2f}'.format(i[4]))
            lnTotal+=i[4]
        print('-------------------------------------------------------------------')
        print('TOTAL:', self.mxSpace('', 20), '{0:12,.2f}'.format(lnTotal))
        self.loSql.omDisconnect()
        return True

    def omInicioQuincena(self):
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Verifica si puede hacerse el adelanto de quincena
        lcSql = "SELECT cCodPla, cDescri FROM E01MPLA WHERE cEstado = 'A'"
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = 'NO HAY PLANILLAS EN ESTADO DE APERTURA'
           return False
        self.pcCodPla = RS[0][0]
        self.pcDescri = RS[0][1]
        self.loSql.omDisconnect()
        return True

    #-----------------------------------------------------------------
    # Valida si se puede procesar planilla
    #-----------------------------------------------------------------
    def omInitProcesarPlanilla(self):
        llOk = self.mxValInit()
        if self.lcFases != '1111000000':   # OJOFPM
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE PLANILLA NO PERMITE PROCESAR LA PLANILLA</ERROR></DATA>'
           return False
        self.pcData = '<DATA><CCODPLA>' + self.pcCodPla + '</CCODPLA><CDESCRI>' + self.pcDescri.strip() + '</CDESCRI></DATA>'
        return True

    #-----------------------------------------------------------------
    # Procesar planilla
    #-----------------------------------------------------------------
    def omProcesarPlanilla(self):
        # Valida usuario y estado de fase de planilla
        llOk = self.omInitProcesarPlanilla()
        if not llOk:
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        llOk = self.mxCargarParametros()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Elimina anteriores datos si fuera reproceso
        llOk = self.mxEliminar()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Generar transacciones de abonos
        llOk = self.mxAbonos()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Calcular descuentos
        llOk = self.mxDescuentos()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Calcula subtotales y total
        llOk = self.mxTotales()
        if llOk:
           self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111100000' WHERE cCodPla = '" + self.pcCodPla + "'")
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        self.pcData = '<DATA><MENSAJE>PLANILLA GENERADA CORRECTAMENTE</MENSAJE></DATA>'
        return llOk

    # Carga parametros para procesar planilla
    def mxCargarParametros(self):
        # Monto de asignacion familiar
        self.lnAsiFam = 150.00   # OJOFPM HAY QUE PARAMETRIZARLO
        # Rangos para impuesto a la renta
        self.laImpRen = [[3700*7, 0.15], [3700*14, .21], [3700*21, .30]]   # OJOFPM HAY QUE PARAMETRIZARLO
        return True

    # Elimina anteriores calculos
    def mxEliminar(self):
        lcSql = "DELETE FROM ADM.E01DTRX WHERE cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "') AND SUBSTRING(cConcep, 1, 1) IN ('A', 'C', 'E', 'N')"
        self.loSql.omExec(lcSql)
        self.loSql.omCommit()
        return True

    # Calcula subtotales y total
    def mxTotales(self):
        RS = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            # Abonos afectos a descuentos
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'A'")
            lnMonto = lnNeto = RS[0][0]
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N01', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
            # Abonos eventuales no afectos a descuentos
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'B'")
            lnMonto = RS[0][0]
            if lnMonto == None:
               lnMonto = 0
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N02', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            lnNeto += lnMonto
            # Descuentos obligatorios
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'C'")
            lnMonto = RS[0][0]
            if lnMonto == None:
               lnMonto = 0
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N03', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            lnNeto -= lnMonto
            # Descuentos no obligatorios
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'D'")
            lnMonto = RS[0][0]
            if lnMonto == None:
               lnMonto = 0
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N04', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            lnNeto -= lnMonto   # OJOFPM QUE PASA SI ES NEGATIVO
            # Neto a abonar
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N10', " + str(lnNeto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
        self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111111100' WHERE cCodPla = '" + self.pcCodPla + "'")
        self.loSql.omCommit()
        # Verifica si hay negativos
        RS = self.loSql.omExecRS("SELECT nMonto FROM ADM.V_E01DTRX WHERE cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "') AND nMonto < 0 LIMIT 1")
        if RS[0][0] != None:
            self.pcError = '<DATA><ERROR>HAY VALORES NEGATIVOS - REVISE</ERROR></DATA>'
            llOk = False
        return llOk
        
    # Calcula descuentos    
    def mxDescuentos(self):
        lcNroMes = self.pcCodPla[2: -1]
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodEmp FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            lcCodigo = XPLA[0]
            lcCodEmp = XPLA[1]
            # OJOFPM FALTA GENERAR LAS COMISIONES A03
            # Abonos afectos a impuesto a la renta: basico, asignacion familiar y comisiones
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03')")
            lnAbono = RS[0][0]
            # Calculo de gratificacion FFPP y navidad
            if lcNroMes == '07' or lcNroMes == '12':
               lnGratif = self.mxGratificacion(lcCodigo, lcCodEmp)
            else:
               # Gratificacion de FFPP y navidad
               lnGratif = float(lnAbono) * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
            self.mxImpuestoRenta(lcCodigo, lcCodEmp, lnAbono, lnGratif)
            # Calculo de aportes AFP
            lnTotal = lnAbono
            if lcNroMes == '07' or lcNroMes == '12':
               lnTotal += lnGratif
            self.mxAFP(lcCodigo, lnTotal)
        self.loSql.omCommit()
        return True

    # Calculo del impuesto a la renta
    def mxImpuestoRenta(self, p_cCodigo, p_cCodEmp, p_nAbono, p_nGratif):
        lcNroMes = self.pcCodPla[2: -1]
        lcYear = self.pcCodPla[:2]
        i = 13 - int(lcNroMes)
        lnTotal = float(p_nAbono) * i + p_nGratif
        # Pagos anteriores del anio de IR
        lnPagAnt = lnRetAnt = 0
        RS = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + p_cCodEmp + "' AND cCodPla < '" + self.pcCodPla + "' AND SUBSTRING(cCodPla, 1, 2) = '" + lcYear+ "'")
        for XPAG in RS:
            lcCodigo = RS1[0][0]
            if lcCodigo != None:
               # Abonos (pagos) de meses anteriores
               RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03', 'A04')")
               lnPagAnt += RS[0][0]
               # Suma retenciones IR del anio
               RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'C01'")
               lnRetAnt += RS1[0][0]
        # Total anual
        lnTotal += lnPagAnt
        lnImpRen = 0.00
        for i in range(0, len(self.laImpRen) - 1):
            if lnTotal >= self.laImpRen[i][0] and lnTotal < self.laImpRen[i + 1][0]:
               lnImpRen += (float(lnAbono) - self.laImpRen[i][0]) * self.laImpRen[i][1]
               break
            elif lnTotal >= self.laImpRen[i][0] and lnTotal > self.laImpRen[i + 1][0]:
               lnImpRen += (self.laImpRen[i + 1][0] - self.laImpRen[i][0]) * self.laImpRen[i][1]
        if lcNroMes <= '03':
           i = 12
        else:
           lnImpRen -= lnRetAnt   # OJOFPM SI ES NEGATIVO
           i = 13 - int(lcNroMes)
        lnImpRen = lnImpRen / i
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C01', " + str(lnImpRen) + ", '" + self.pcCodUsu + "')"
        self.loSql.omExec(lcSql)

    # Calcula la gratificacion de FFPP y navidad
    def mxGratificacion(self, p_cCodigo, p_cCodEmp):
        lcNroMes = self.pcCodPla[2: -1]
        lcYear = self.pcCodPla[:2]
        if lcNroMes == '07':
           lcPlaCod = lcYear + '011'
        else:
           lcPlaCod = lcYear + '061'
        lnComisi = 0
        RS = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + p_cCodEmp + "' AND cCodPla < '" + self.pcCodPla + "' AND cCodPla >= '" + lcPlaCod + "'")
        for XPAG in RS:
            lcCodigo = RS1[0][0]
            if lcCodigo != None:
               # Suma comisiones de meses anteriores
               RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'A03'")
               lnComisi += RS1[0][0]
        lnGratif = lnComisi / 6
        # Basico y asignacion familiar del mes
        RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + p_cCodigo + "' AND cConcep IN ('A01', 'A02')")
        lnGratif += RS[0][0]
        if lcNroMes == '12':
           # Aguinaldo
           lnGratif += 120.00   # OJOFPM PARAMETRIZAR
        if lnGratif > 0:
           lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'A04', " + str(lnGratif) + ", '" + self.pcCodUsu + "')"
           self.loSql.omExec(lcSql)
        if lcNroMes == '07':
           # Suma gratificacion de navidad
           lnGratif += RS[0][0] * 1.09   # OJOFPM PARAMETRIZAR EL 1.09
        elif lcNroMes == '12':
           # Gratificacion de FFPP y navidad
           lnGratif = RS[0][0] * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
        return lnGratif

    # Calcula AFP
    def mxAFP(self, p_cCodigo, p_nAbono):
        # Calcula AFP
        RS = self.loSql.omExecRS("SELECT A.nPorApo, A.nPorCom, A.nPorSeg, A.nMaxSeg FROM ADM.E01MAFP A INNER JOIN ADM.E01MEMP B ON A.cCodAfp = B.cCodAfp INNER JOIN ADM.E01PPLA C ON B.cCodEmp = C.cCodEmp WHERE C.cCodigo = '" + p_cCodigo + "'")
        # Aportacion AFP
        lnMonto = p_nAbono * RS[0][0]/100
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C02', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        self.loSql.omExec(lcSql)
        # Comision AFP
        lnMonto = p_nAbono * RS[0][1]/100
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C03', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        self.loSql.omExec(lcSql)
        # Seguro-prima AFP
        lnMonto = p_nAbono * RS[0][2]/100
        if lnMonto > RS[0][3]:
           lnMonto = RS[0][3]
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C04', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        self.loSql.omExec(lcSql)
            
    # Generar transacciones de abonos
    def mxAbonos(self):
        RS = self.loSql.omExecRS("SELECT cCodEmp, cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            RS = self.loSql.omExecRS("SELECT nBasico, lAsiFam FROM ADM.E01MEMP WHERE cCodEmp = '" + XPLA[0] + "'")
            # Basico
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[1] + "', 'A01', " + str(RS[0][0]) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
            # Asignacion familiar
            if RS[0][1] == 1:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[1] + "', 'A02', " + str(self.lnAsiFam) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            # Adelanto de comision
            RS = self.loSql.omExecRS("SELECT nMonto FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[1] + "' AND cConcep = 'D02'")
            if RS != None:   # OJOFPM
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[1] + "', 'A03', " + str(RS[0][0]) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
        self.loSql.omCommit()
        return True

##############################################################
# Clase que contabiliza transacciones de planillas
##############################################################
class CContabilizar(CPlanillaBase):
    pcCodUsu = None

    #-----------------------------------------------------------------
    # Valida si se puede contabilizar planilla
    #-----------------------------------------------------------------
    def omInitContabilizarPlanilla(self):
        llOk = self.mxValInit()
        if self.lcFases != '1111110000':   # OJOFPM
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE PLANILLA NO PERMITE CONTABILIZAR LA PLANILLA</ERROR></DATA>'
           return False
        self.pcData = '<DATA><CCODPLA>' + self.pcCodPla + '</CCODPLA><CDESCRI>' + self.pcDescri.strip() + '</CDESCRI></DATA>'
        return True

    #-----------------------------------------------------------------
    # Contabiliza planilla
    #-----------------------------------------------------------------
    def omContabilizarPlanilla(self):
        lcCodPla = self.pcCodPla
        llOk = self.omInitContabilizarPlanilla()
        if not llOk:
           return False
        if lcCodPla != self.pcCodPla:
           self.pcError = '<DATA><ERROR>ERROR EN CODIGO DE PLANILLA. REINTENTE Y VERIFIQUE PLANILLA A CONTABILIZAR</ERROR></DATA>'
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Nro de doc.
        llOk = self.mxNumeroDocumentoOficina()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Codigo contable
        lcCodCnt = self.pcCodPla + 'C';
        self.loSql.omExec("DELETE FROM ADM.E10DCNT WHERE cCodCnt = '" + lcCodCnt + "'")
        # Cuentas contables
        lcCtaPte = '1511010101'   # OJOFPM FALTA PARAMETRIZAR
        j = 0
        laCtaCnt = []
        RS = self.loSql.omExecRS("SELECT cConcep, cCodAfp, cCtaCnt FROM ADM.f_CuentasContables()")
        for XTMP in RS:
            laCtaCnt.append([])
            laCtaCnt[j].append(XTMP[0])
            laCtaCnt[j].append(XTMP[1])
            laCtaCnt[j].append(XTMP[2])
            j += 1
        if j == 0:
           self.pcError = '<DATA><ERROR>NO HAY CUENTAS CONTABLES DE CONCEPTOS DEFINIDOS</ERROR></DATA>'
           self.loSql.omDisconnect()
           return False
        # Contabiliza conceptos de cada empleado
        j = 0
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodOfi, cCodAfp, cCtaBco FROM ADM.V_E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XEMP in RS:
            lcCodigo = XEMP[0]
            lcCodOfi = XEMP[1]
            RS = self.loSql.omExecRS("SELECT nMonto, cConcep FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND (SUBSTRING(cConcep, 1, 1) IN ('A', 'B', 'C', 'D') OR cConcep IN ('E03', 'N10'))")
            for XTRX in RS:            
                j += 1
                # Numero de documento
                i = self.FindArray(self.laNroDoc, XEMP[1])
                lcNroDoc = self.laNroDoc[i][1]
                lnHaber = lnDebe = 0
                if XTRX[1][:1] == 'A':
                   lnHaber = XTRX[0]
                else:
                   lnDebe = XTRX[0]
                # Cuenta contable
                if XTRX[1] == 'C02' or XTRX[1] == 'C03' or XTRX[1] == 'C04':
                   # Cuentas de AFP
                   print '1)', XTRX[1], XEMP[2]
                   i = self.mxSeekAfp(laCtaCnt, XTRX[1], XEMP[2])
                else:
                   # Otras cuentas
                   i = self.FindArray(laCtaCnt, XTRX[1])
                   print '2)', XTRX[1]
                print '***', i
                lcCtaCnt = laCtaCnt[i][2]
                lcGlosa = 'PAGO SUELDO [' + XEMP[3] + ']'
                lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cGlosa, cCtaCnt, nDebeC, nHaberC, cCodUsu) VALUES ('" + lcCodCnt + "', '" + lcNroDoc + "',  '" + self.pdFecSis + "', '" + lcGlosa + "', '" + lcCtaCnt + "', " + str(lnDebe) + ", " + str(lnHaber) + ", '" + self.pcCodUsu + "')"
                self.loSql.omExec(lcSql)
        if j == 0:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>ERROR: NO HAY DATOS PARA CONTABILIZAR</ERROR></DATA>'
           return False
        # Descripcion de planilla
        lcSql = "SELECT cDescri FROM ADM.E01MPLA WHERE cCodPla = '" + lcCodCnt[:5] + "'"
        RS = self.loSql.omExecRS(lcSql)
        if RS[0][0] == None:
           self.loSql.omDisconnect()
           self.pcError = "CODIGO DE PLANILLA [" + lcCodPla[:5] + "] NO EXISTE"
           return False
        lcGlosa = 'PLANILLA - ' + RS[0][0].strip()
        lcNroDoc = '*'
        RS = self.loSql.omExecRS("SELECT cNroDoc, cCtaCnt, nDebeC, nHaberC, cGlosa FROM ADM.E10DCNT WHERE cCodCnt = '" + lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt")
        for XCNT in RS:
            if XCNT[0] != lcNroDoc:
               # Graba cabecera de comprobante contable
               lcNroDoc = XCNT[0]
               lcNroCom = lcNroDoc[:2] + 'PL01'
               lcNroCom = self.mxNroComprobante(lcNroCom)
               # cTipDoc = 'RI' [803]
               print '1)', lcNroCom
               print '2)', lcNroDoc
               print '3)', lcNroDoc[:2]
               print '4)', self.pdFecSis
               print '5)', self.pcCodUsu
               lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroDoc[:2] + "', 'S', 'ADELANTO DE COMISION', 'RI', '', '', '', '', '" + self.pdFecSis + "', '', '', '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            # Graba detalle de comprobante contable
            lcGlosa = XCNT[4]
            lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + XCNT[1] + "', '" + lcGlosa + "', 0, 0, " + str(XCNT[2]) + ", " + str(XCNT[3]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql) 
        self.loSql.omCommit()
        self.loSql.omDisconnect()
        self.pcMensaje = '<DATA><MENSAJE>CONTABILIZACION DE PLANILLA CONFORME</MENSAJE></DATA>'
        return True

    def mxSeekAfp(self, p_aCtaCnt, p_cConcep, p_cCodAfp):
        llFind = False
        i = 0
        for x in p_aCtaCnt:
            if x[0] == p_cConcep and x[1] == p_cCodAfp:
               llFind = True
               break
            i += 1
        if not llFind:
           return None
        return i
    
    

'''
    def omPlanilla(self):
        # Condiciones de excepcion
        if self.mxEmpty(self.pcCodUsu):
           self.pcError = 'ERROR: CODIGO DE USUARIO VACIO'
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        lcFecSis = '2013-01-29'  # OJOFPM FALTA PARAMETRIZAR
        # Realiza la apertura de planilla
        lcSql = "SELECT * FROM f_ContabilizarPlanilla('001', '" + self.pcCodUsu + "')"  # OJOFPM FALTA PARAMETRIZAR EL 001 GCTERMID
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = 'ERROR AL CONTABILIZAR LA PLANILLA'
           return False
        lcXml = RS[0][0]
        self.loSql.omCommit()
        # Evalua error
        lcError = lcCodCnt = None
        loRoot = ET.fromstring(lcXml)
        for lo in loRoot:
            if lo.tag == 'ERROR':
               lcError = lo.text
            if lo.tag == 'CCODCNT':
               lcCodCnt = lo.text
        if not lcError == None:
           self.loSql.omDisconnect()
           self.pcError = lcXml
           return False
        if lcCodCnt == None:
           self.loSql.omDisconnect()
           self.pcError = 'ERROR: NO EXISTE EL CODIGO CONTABLE'
           return False
        # Graba contabilizacion
        lcSql = "SELECT cDescri FROM E01MPLA WHERE cCodPla = '" + lcCodCnt[:5] + "'"
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = "NO HAY PLANILLA VIGENTE PARA CODIGO DE PLANILLA [" + lcCodPla[:5] + "]"
           return False
        lcGlosa = str('PLANILLA - ' + RS[0][0]).strip()
        lcSql = "SELECT cNroDoc, cCtaCnt, cCodOfi, nDebeC, nHaberC FROM S01DCNT WHERE cCodCnt = '" + lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt"
        RS = self.loSql.omExecRS(lcSql)
        if RS == None:
           self.loSql.omDisconnect()
           self.pcError = 'ERROR AL TRAER DATOS DE LA CONTABILIZACION DE PLANILLA'
           return False
        j = 0
        laData = []
        for i in RS:
            laData.append([])
            laData[j].append(i[0])   # Nro. documento
            laData[j].append(i[1])   # Cuenta contable
            laData[j].append(i[2])   # Oficina
            laData[j].append(i[3])   # Debe
            laData[j].append(i[4])   # Haber
            laData[j].append('')     # Descripcion cuenta contable
            j+=1
        self.loSql.omDisconnect()
        # Graba la contabilizacion en CNT
        llOk = self.loSql.omConnect('CNT')
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Valida cuenta contable
        self.pcError = ''
        llOk = True
        for i in range(len(laData)):
            lcCtaCnt = laData[i][1].strip()
            lcSql = "SELECT cDescri FROM D01MCTA WHERE cCtaCnt = '" + lcCtaCnt + "'"
            RS = self.loSql.omExecRS(lcSql)
            if RS == None:
               self.pcError = self.pcError + '[' + lcCtaCnt + ']'
               llOk = False
            else:
               laData[i][1] = lcCtaCnt
               laData[i][5] = RS[0][0].strip()[:40]
        if not llOk:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>' + self.pcError + '</ERROR></DATA>'
           return False
        self.pcError = None
        lcNroDoc = '*'
        for i in range(len(laData)):
            if lcNroDoc != laData[i][0]:
               lcMes = lcCodCnt[:4]
               lcMes = lcMes[2:]
               lcNroCom = str(laData[i][0][:2]) + 'PL' + lcMes + '%'
               lcSql = "SELECT MAX(cNroCom) FROM D01MDIA WHERE cNroCom LIKE '" + lcNroCom + "'"
               RS = self.loSql.omExecRS(lcSql)
               if RS[0][0] == None:
                  lcNroCom = str(laData[i][0][:2]) + 'PL' + lcMes + '000000'
               else:
                  lcNroCom = RS[0][0]
               lnNumero = int(lcNroCom[6:]) + 1
               lcNumero = '00000' + str(lnNumero)
               lcNumero = lcNumero[-6:]
               lcNroCom = str(laData[i][0][:2]) + 'PL' +lcMes + lcNumero
               lcSql = "INSERT INTO D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" 
               lcSql = lcSql + lcNroCom + "', '" + laData[i][0] + "', '', '" + laData[i][2]
               lcSql = lcSql + "', 'S', '" + lcGlosa + "', '', '', '', '0000000', '20455859728', '" + str(lcFecSis) + "', '', '', '" + str(self.pcCodUsu) + "')"
               self.loSql.omExec(lcSql)
               lcNroDoc = laData[i][0]
            lcSql = "INSERT INTO D01DMOV (cNroCom, cLibro, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '', '1', '" + laData[i][1] + "', '" + laData[i][5] + "', 0, 0, " + str(laData[i][3]) + ", " + str(laData[i][4]) + ", 0, '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
        self.loSql.omCommit()
        self.loSql.omDisconnect()
        self.pcMensaje = '<DATA><MENSAJE>CONTABILIZACION DE PLANILLA CONFORME</MENSAJE></DATA>'
        return True






        # Pagos anteriores del anio
        lnPagAnt = lnRetAnt = 0
            RS1 = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + XPLA[1] + "' AND cCodPla < '" + self.pcCodPla + "' AND SUBSTRING(cCodPla, 1, 2) = '" + lcYear+ "'")
            for XPAG in RS1:
                lcCodigo = RS1[0][0]
                if lcCodigo != None:
                   RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03', 'A04')")
                   lnPagAnt += RS1[0][0]
                   # Suma retenciones IR del anio
                   RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'C01'")
                   lnRetAnt += RS1[0][0]
            # Total anual
            lnTotal = lnAbono + lnGratif + lnPagAnt
            lnImpRen = 0.00
            for i in range(0, len(self.laImpRen) - 1):
                if lnTotal >= self.laImpRen[i][0] and lnTotal < self.laImpRen[i + 1][0]:
                   lnImpRen += (float(lnAbono) - self.laImpRen[i][0]) * self.laImpRen[i][1]
                   break
                elif lnTotal >= self.laImpRen[i][0] and lnTotal > self.laImpRen[i + 1][0]:
                   lnImpRen += (self.laImpRen[i + 1][0] - self.laImpRen[i][0]) * self.laImpRen[i][1]
            if lcNroMes <= '03':
               i = 12
            else:
               lnImpRen -= lnRetAnt   # OJOFPM SI ES NEGATIVO
               i = 13 - int(lcNroMes)
            lnImpRen = lnImpRen / i
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C01', " + str(lnImpRen) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)




            if lcNroMes == '01' or lcNroMes == '02' or lcNroMes == '03':   # Calcula impuesto a la renta: enero, febrero y marzo
               if lcNroMes == '01':
                  lnAbono = RS[0][0] * 12
               elif lcNroMes == '02':
                  lnAbono = RS[0][0] * 11
               else:
                  lnAbono = RS[0][0] * 10
               lnGratif = RS[0][0] * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
               # Pagos anteriores del anio
               lcYear = self.pcCodPla[:2]
               lnPagAnt = 0
               RS1 = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + XPLA[1] + "' AND cCodPla < '" + self.pcCodPla + "' AND SUBSTRING(cCodPla, 1, 2) = '" + lcYear+ "'")
               for XPAG in RS1:
                   lcCodigo = RS1[0][0]
                   if lcCodigo != None:
                      RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03')")
                      lnPagAnt += RS1[0][0]
               # Total anual
               lnTotal = lnAbono + lnGratif + lnPagAnt
               lnImpRen = 0.00
               for i in range(0, len(self.laImpRen) - 1):
                   if lnTotal >= self.laImpRen[i][0] and lnTotal < self.laImpRen[i + 1][0]:
                      lnImpRen += (float(lnAbono) - self.laImpRen[i][0]) * self.laImpRen[i][1]
                      break
                   elif lnTotal >= self.laImpRen[i][0] and lnTotal > self.laImpRen[i + 1][0]:
                      lnImpRen += (self.laImpRen[i + 1][0] - self.laImpRen[i][0]) * self.laImpRen[i][1]
               lnImpRen = lnImpRen / 12
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C01', " + str(lnImpRen) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
            elif lcNroMes == '04' or lcNroMes == '05':   # Calcula impuesto a la renta: abril y mayo
               if lcNroMes == '04':
                  lnAbono = RS[0][0] * 9
               elif lcNroMes == '05':
                  lnAbono = RS[0][0] * 8
               lnGratif = RS[0][0] * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
               # Pagos anteriores del anio
               lcYear = self.pcCodPla[:2]
               lnPagAnt = 0
               lnRetAnt = 0
               RS1 = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + XPLA[1] + "' AND cCodPla < '" + self.pcCodPla + "' AND SUBSTRING(cCodPla, 1, 2) = '" + lcYear+ "'")
               for XPAG in RS1:
                   lcCodigo = RS1[0][0]
                   if lcCodigo != None:
                      RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03')")
                      lnPagAnt += RS1[0][0]
                      # Suma retenciones IR del anio
                      RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'C01'")
                      lnRetAnt += RS1[0][0]
               # Total anual
               lnTotal = lnAbono + lnGratif + lnPagAnt
               lnImpRen = 0.00
               for i in range(0, len(self.laImpRen) - 1):
                   if lnTotal >= self.laImpRen[i][0] and lnTotal < self.laImpRen[i + 1][0]:
                      lnImpRen += (float(lnAbono) - self.laImpRen[i][0]) * self.laImpRen[i][1]
                      break
                   elif lnTotal >= self.laImpRen[i][0] and lnTotal > self.laImpRen[i + 1][0]:
                      lnImpRen += (self.laImpRen[i + 1][0] - self.laImpRen[i][0]) * self.laImpRen[i][1]
               lnImpRen -= lnRetAnt   # OJOFPM CON EL NEGATIVO
               if lcNroMes == '04':
                  lnImpRen = lnImpRen / 9
               else:
                  lnImpRen = lnImpRen / 8
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C01', " + str(lnImpRen) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)





            elif lcNroMes == '03':   # Calcula impuesto a la renta: marzo
               lnAbono = RS[0][0] * 10
               lnGrati = RS[0][0] * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
               # Pagos de enero y febrero
               lcYear = self.pcCodPla[:2]
               lnPagAnt = 0
               RS1 = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + XPLA[1] + "' AND cCodPla < '" + self.pcCodPla + "' AND SUBSTRING(cCodPla, 1, 2) = '" + lcYear+ "'")
               for XPAG in RS1:
                   lcCodigo = RS1[0][0]
                   if lcCodigo != None:
                      RS1 = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03')")
                      lnPagAnt += RS1[0][0]
               # Total anual
               lnTotal = lnAbono + lnGrati + lnPagAnt
               lnImpRen = 0.00
               for i in range(0, len(self.laImpRen) - 1):
                   if lnTotal >= self.laImpRen[i][0] and lnTotal < self.laImpRen[i + 1][0]:
                      lnImpRen += (float(lnAbono) - self.laImpRen[i][0]) * self.laImpRen[i][1]
                      break
                   elif lnTotal >= self.laImpRen[i][0] and lnTotal > self.laImpRen[i + 1][0]:
                      lnImpRen += (self.laImpRen[i + 1][0] - self.laImpRen[i][0]) * self.laImpRen[i][1]
               lnImpRen = lnImpRen / 12
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C01', " + str(lnImpRen) + ", '" + self.pcCodUsu + "')"
               self.loSql.omExec(lcSql)
               
            
            
            
            # Calcula AFP
            RS = self.loSql.omExecRS("SELECT A.nPorApo, A.nPorCom, A.nPorSeg, A.nMaxSeg FROM ADM.E01MAFP A INNER JOIN ADM.E01MEMP B ON A.cCodAfp = B.cCodAfp INNER JOIN ADM.E01PPLA C ON B.cCodEmp = C.cCodEmp WHERE C.cCodigo = '" + XPLA[0] + "'")
            # Aportacion AFP
            lnMonto = lnAbono * RS[0][0]/100
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C02', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
            # Comision AFP
            lnMonto = lnAbono * RS[0][1]/100
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C03', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
            # Seguro-prima AFP
            lnMonto = lnAbono * RS[0][2]/100
            if lnMonto > RS[0][3]:
               lnMonto = RS[0][3]
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'C04', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
            # Calcula EPS
            lnMonto = float(lnAbono) * 0.025   # OJOFPM PARAMETRIZAR
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'E03', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
            # Calcula ESSALUD
            lnMonto = float(lnAbono) * 0.09   # OJOFPM PARAMETRIZAR
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'E01', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            self.loSql.omExec(lcSql)
        self.loSql.omCommit()
        return True
'''            

