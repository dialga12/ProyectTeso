# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from CBase import *
from CBasePlanillas import *
from decimal import *

##############################################################
# Clase que procesa planillas
##############################################################
class CPlanillas(CPlanillaBase):
    paAnhos  = None
    paNumero = None
    pcNumero = None

    #----------------------------------------------
    # Realiza la apertura de planilla
    #----------------------------------------------
    def omApertura(self):
        # Condiciones de excepcion
        lcYear = self.pcCodPla[:2]
        lcMonth = self.pcCodPla[2:][:2]
        lcNroPla =  self.pcCodPla[-1:]
        if self.mxEmpty(self.pcCodPla):
           self.pcError = '<DATA><ERROR>CODIGO DE PLANILLA VACIO</ERROR></DATA>'
           return False
        elif len(self.pcCodPla) != 5:
           self.pcError = '<DATA><ERROR>LONGITUD DE CODIGO DE PLANILLA ERRADO</ERROR></DATA>'
           return False
        elif not (lcYear > '00' and lcYear <= '99'):
           self.pcError = '<DATA><ERROR>AÑO DE PLANILLA NO ES VALIDO [01..99]</ERROR></DATA>'
           return False
        elif not (lcMonth > '00' and lcMonth <= '12'):
           self.pcError = '<DATA><ERROR>MES DE PLANILLA NO ES VALIDO [01..12]</ERROR></DATA>'
           return False
        elif not (lcNroPla > '0' and lcNroPla <= '9'):
           self.pcError = '<DATA><ERROR>NUMERO DE PLANILLA NO ES VALIDO [1..9]</ERROR></DATA>'
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
        #lcSql = "SELECT cEstado FROM ADM.E01MPLA WHERE cEstado != 'B' LIMIT 1"   ## OJOFPM VA A HABER SOLO DOS ESTADOS
        lcSql = "SELECT cEstado FROM ADM.E01MPLA WHERE cEstado = 'A' LIMIT 1"
        RS = self.loSql.omExecRS(lcSql)
        if len(RS) > 0:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>ERROR: HAY PLANILLAS ABIERTAS - NO PUEDE CONTINUAR</ERROR></DATA>'
           return False
        # Valida usuario
        lcSql = "SELECT cCodUsu FROM S01TUSU WHERE cCodUsu = '" + self.pcCodUsu + "'"
        RS = self.loSql.omExecRS(lcSql)
        if len(RS) == 0:
           self.loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>CODIGO DE USUARIO NO EXISTE EN TABLA DE USUARIOS [S01TUSU]</ERROR></DATA>'
           return False
        # Verifica codigo de planilla
        lcSql = "SELECT cEstado FROM ADM.E01MPLA WHERE cCodPla = '" + self.pcCodPla + "'"
        RS = self.loSql.omExecRS(lcSql)
        if len(RS) > 0:
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
        if RS[0][0] == None:
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
           self.pcData = '<DATA><AVISO>GRABACION CONFORME</AVISO></DATA>'
        self.loSql.omDisconnect()
        return llOk

    #---------------------------------------------- 
    # OJOFPM PARA QUE SIRVE? SE USA?
    #---------------------------------------------- 
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

    #---------------------------------------------- 
    # OJOFPM PARA QUE SIRVE? SE USA?
    #---------------------------------------------- 
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

    #---------------------------------------------- 
    # OJOFPM PARA QUE SIRVE? SE USA?
    #---------------------------------------------- 
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
        # Valida planilla, usuario y estado de fase de planilla
        llOk = self.omInitProcesarPlanilla()
        if not llOk:
           return False
        # Conectar base de datos           
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Carga parametros (rango para R5TA y valor de asignacion familiar)
        llOk = self.mxCargarParametros()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Elimina anteriores datos si fuera reproceso OJOFPM
        llOk = self.mxEliminar()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Generar transacciones de abonos
        llOk = self.mxAbonos()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Mes de proceso
        llOk = self.mxGratificacion()
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
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Calcular aportaciones
        llOk = self.mxAportaciones()
        if llOk:
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        self.pcData = '<DATA><MENSAJE>PLANILLA GENERADA CORRECTAMENTE</MENSAJE></DATA>'
        return llOk

    # Carga parametros para procesar planilla  OK
    def mxCargarParametros(self):
        # Porcentaje descuento ESSALUD
        self.laAport = None
        i = 0
        RS = self.loSql.omExecRS("SELECT cCodigo, nValor FROM ADM.E10TPAR WHERE cCodigo IN ('PL0006', 'PL0007', 'PL0008')")
        for XCTA in RS:
            RS = self.loSql.omExecRS("SELECT cCtaCnt FROM ADM.E10TCNT WHERE cCodigo = '" + XCTA[0] + "'")   ## OJOFPM PARECE QUE NO ES NECESARIA LA CUENTA CONTABLE
            lcCtaCnt = RS[0][0]
            if lcCtaCnt == None:
               self.pcError = '<DATA><ERROR>NO EXISTE CODIGO CONTABLE PARA DESCUENTO ESSALUD [' + XCTA[0] + ']. INFORME A TI</ERROR></DATA>'
               return False
            self.laAporta.append([])
            self.laAporta[i].append(XCTA[0])
            self.laAporta[i].append(XCTA[1])
            self.laAporta[i].append(lcCtaCnt)
            i+=1
        if i != 3:
           self.pcError = '<DATA><ERROR>NO EXISTEN CODIGOS PARA ESSALUD [PL0003, PL0004, PL0005]. INFORME A TI</ERROR></DATA>'
           return False
        # Monto de asignacion familiar
        self.lnAsiFam = 75.00   # OJOFPM HAY QUE PARAMETRIZARLO
        # Rangos para impuesto a la renta
        self.laImpRen = [[3700*7, 0.15], [3700*14, 0.21], [3700*21, 0.30]]   # OJOFPM HAY QUE PARAMETRIZARLO
        return True

    # Elimina anteriores calculos (OK)
    def mxEliminar(self): #OJOFPM REVISAR SI SON LOS CONCEPTOS A ELIMINAR
        lcSql = "DELETE FROM ADM.E01DTRX WHERE cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "') AND (cConcep IN ('A01', 'A02') OR SUBSTRING(cConcep, 1, 1) IN ('C', 'E', 'N'))"
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>NO SE PUDO ELIMINAR DATOS ANTERIORES. INFORME A TI</ERROR></DATA>'
        return llOk

    # Calcula subtotales y total (OK)
    def mxTotales(self):
        print 'Totales ...'
        RS = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            # Pagos afectos a descuentos
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'A'")
            lnMonto = lnNeto = RS[0][0]
            # Descuento por faltas y tardanzas
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND cConcep IN ('D10', 'D11')")
            lnFalTar = RS[0][0]
            if lnFalTar == None:
               lnFalTar = 0.00
            lnMonto = lnMonto - Decimal(lnFalTar)
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N01', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
            print lcSql
            llOk = self.loSql.omExec(lcSql)
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR AL GRABAR PAGOS AFECTOS A DESCUENTOS (N01). AVISE A TI</ERROR></DATA>'
               return False
            # Pagos eventuales no afectos a descuentos
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'B'")
            lnMonto = RS[0][0]
            if lnMonto == None:
               lnMonto = 0
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N02', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR PAGOS NO AFECTOS A DESCUENTOS (N02). AVISE A TI</ERROR></DATA>'
                  return False
            lnNeto += lnMonto
            # Descuentos obligatorios
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'C'")
            lnMonto = RS[0][0]
            if lnMonto == None:
               lnMonto = 0
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N03', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR DESCUENTOS OBLIGATORIOS (N03). AVISE A TI</ERROR></DATA>'
                  return False
            lnNeto -= lnMonto
            # Descuentos no obligatorios
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + XPLA[0] + "' AND SUBSTRING(cConcep, 1, 1) = 'D'")
            lnMonto = RS[0][0]
            if lnMonto == None:
               lnMonto = 0
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N04', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR DESCUENTOS NO OBLIGATORIOS (N04). AVISE A TI</ERROR></DATA>'
                  return False
            lnNeto -= lnMonto   # OJOFPM QUE PASA SI ES NEGATIVO
            # Neto a abonar
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[0] + "', 'N10', " + str(lnNeto) + ", '" + self.pcCodUsu + "')"
            llOk = self.loSql.omExec(lcSql)
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR AL GRABAR NETO A ABONAR (N10). AVISE A TI</ERROR></DATA>'
               return False
        # Verifica si hay negativos
        RS = self.loSql.omExecRS("SELECT cCodigo, cConcep, nMonto FROM ADM.V_E01DTRX WHERE cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "') AND nMonto < 0 order by CcODIGO")
        if len(RS) > 0:
           self.loSql.omCommit()   ## OJOFPM !!!!!!!!!!!!!!!!!!!!!!
           self.pcError = '<DATA><ERROR>HAY VALORES NEGATIVOS - REVISE</ERROR></DATA>'
           return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111100000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL ACTUALIZAR EL ESTADO (FASE) DE LA PLANILLA EN E01MPLA. AVISE A TI</ERROR></DATA>'
        return llOk
        
    # Calcula descuentos (OK)    
    def mxDescuentos(self):
        # Mes de proceso
        lcNroMes = self.pcCodPla[2: -1]
        # Lee todos los empleados de planilla
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodEmp FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            lcCodigo = XPLA[0]
            lcCodEmp = XPLA[1]
            # Abonos afectos a impuesto a la renta: basico, asignacion familiar y comisiones
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02', 'A03')")
            lnAbono = RS[0][0]
            # Gratificacion FFPP y navidad
            if lcNroMes == '07' or lcNroMes == '12':
               RS = self.loSql.omExecRS("SELECT nMonto FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'A04'")
               lnGratif = RS[0][0]
               if lnGratif == None:
                  lnGratif = 0
            else:
               # Gratificacion de FFPP y navidad
               lnGratif = float(lnAbono) * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
            llOk = self.mxImpuestoRenta(lcCodigo, lcCodEmp, lnAbono, lnGratif)
            if not llOk:
               return false
            # Calculo de aportes AFP
            lnTotal = lnAbono
            if lcNroMes == '07' or lcNroMes == '12':
               lnTotal += lnGratif
            self.mxAFP(lcCodigo, lnTotal)
        return True

    # Calculo del impuesto a la renta (OK)
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
               lnImpRen += (float(lnTotal) - self.laImpRen[i][0]) * self.laImpRen[i][1]
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
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL GRABAR DESCUENTO DE IMPUESTO A LA RENTA EN E01DTRX. AVISE A TI</ERROR></DATA>'
        return llOk

    # Calcula la gratificacion de FFPP y navidad (OK)
    def mxGratificacion(self):
        lcNroMes = self.pcCodPla[2: -1]
        if not (lcNroMes == '07' or lcNroMes == '12'):
           return True
        if lcNroMes == '07':
           lcPlaCod = lcYear + '011'
        else:
           lcPlaCod = lcYear + '061'
        # Lee todos los empleados de planilla
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodEmp FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            lcCodigo = XPLA[0]
            lcCodEmp = XPLA[1]
            lnComisi = 0
            # Planillas de meses anteriores de empleado
            RS = self.loSql.omExecRS("SELECT cCodigo FROM ADM.E01PPLA WHERE cCodEmp = '" + lcCodEmp + "' AND cCodPla < '" + self.pcCodPla + "' AND cCodPla >= '" + lcPlaCod + "'")
            for XPAG in RS:
                lcCodTmp = RS[0][0]
                if lcCodTmp != None:
                   # Suma comisiones de meses anteriores
                   RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodTmp + "' AND cConcep = 'A03'")
                   lnComisi += RS[0][0]
            # Promedio de comisiones
            lnGratif = lnComisi / 6
            # Basico y asignacion familiar del mes
            RS = self.loSql.omExecRS("SELECT SUM(nMonto) FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep IN ('A01', 'A02')")
            lnGratif += RS[0][0]
            if lcNroMes == '12':
               # Aguinaldo
               lnGratif += 120.00   # OJOFPM PARAMETRIZAR
            if lnGratif > 0:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + lcCodigo + "', 'A04', " + str(lnGratif) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR GRATIFICACION EN E01DTRX. AVISE A TI</ERROR></DATA>'
                  return False
            ''' OJOFPM
            if lcNroMes == '07':
               # Suma gratificacion de navidad
               lnGratif += RS[0][0] * 1.09   # OJOFPM PARAMETRIZAR EL 1.09
            elif lcNroMes == '12':
               # Gratificacion de FFPP y navidad
              lnGratif = RS[0][0] * 1.09 * 2   # OJOFPM PARAMETRIZAR EL 1.09
           return lnGratif
           '''
        return True

    # Calcula AFP
    def mxAFP(self, p_cCodigo, p_nAbono):
        # Calcula AFP
        RS = self.loSql.omExecRS("SELECT A.nPorApo, A.nPorCom, A.nPorSeg, A.nMaxSeg FROM ADM.E01MAFP A INNER JOIN ADM.E01MEMP B ON A.cCodAfp = B.cCodAfp INNER JOIN ADM.E01PPLA C ON B.cCodEmp = C.cCodEmp WHERE C.cCodigo = '" + p_cCodigo + "'")
        # Aportacion AFP
        lnMonto = p_nAbono * RS[0][0]/100
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C02', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL GRABAR DESCUENTO(1) DE AFP. AVISE A TI</ERROR></DATA>'
           return False
        # Comision AFP
        lnMonto = p_nAbono * RS[0][1]/100
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C03', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL GRABAR DESCUENTO(2) DE AFP. AVISE A TI</ERROR></DATA>'
           return False
        # Seguro-prima AFP
        lnMonto = p_nAbono * RS[0][2]/100
        if lnMonto > RS[0][3]:
           lnMonto = RS[0][3]
        lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + p_cCodigo + "', 'C04', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
        llOk = self.loSql.omExec(lcSql)
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL GRABAR DESCUENTO(3) DE AFP. AVISE A TI</ERROR></DATA>'
        return llOk
            
    # Generar transacciones de abonos (OK)
    def mxAbonos(self):
        # Lee todos los empleados de planilla del mes
        RS = self.loSql.omExecRS("SELECT cCodEmp, cCodigo, nDiaTra FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            # Dias trabajados
            lnDiaTra = XPLA[2]
            if lnDiaTra > 30:
               lnDiaTra = 30
            elif lnDiaTra < 0:
               lnDiaTra = 0
            # Trae basico y asignacion familiar
            RS = self.loSql.omExecRS("SELECT nBasico, lAsiFam FROM ADM.E01MEMP WHERE cCodEmp = '" + XPLA[0] + "'")
            # Basico
            lnBasico = RS[0][0] * lnDiaTra / 30
            lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[1] + "', 'A01', " + str(lnBasico) + ", '" + self.pcCodUsu + "')"
            llOk = self.loSql.omExec(lcSql)
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR AL GRABAR BASICO EN E01DTRX. AVISE A TI</ERROR></DATA>'
               return False
            # Asignacion familiar
            if RS[0][1] == 1:
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XPLA[1] + "', 'A02', " + str(self.lnAsiFam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR ASIGNACION FAMILIAR EN E01DTRX. AVISE A TI</ERROR></DATA>'
                  return False
        return True

    # Calcula aportaciones
    def mxAportaciones(self):
        self.loSql.omCommit()
        RS = self.loSql.omExecRS("SELECT cCodigo, cEmpEps FROM ADM.V_E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        for XPLA in RS:
            lcCodigo = XPLA[0]
            lcEmpEps = XPLA[1]
            # Pagos afectos menos faltas y tardanzas
            print "SELECT nMonto FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'N01'"
            RS = self.loSql.omExecRS("SELECT nMonto FROM ADM.E01DTRX WHERE cCodigo = '" + lcCodigo + "' AND cConcep = 'N01'")
            print RS
            if len(RS) == 0:
               self.pcError = '<DATA><ERROR>NO EXISTE EL CONCEPTO DE PAGOS AFECTOS [N01]. INFORME A TI</ERROR></DATA>'
               return False
            lnMonAfe = RS[0][0]
            if lcEmpEps == '00':
               # Solo ESSALUD
               i = self.FindArray(self.laAporta, 'PL0006')
               lnMonto = self.laAporta[i][1] * lnMonAfe / 100
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + lcCodigo + "', 'E01', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR APORTACION DE ESSALUD (1). INFORME A TI</ERROR></DATA>'
                  return False
            else:
               # ESSALUD + EPS
               i = self.FindArray(self.laAporta, 'PL0007')
               lnMonto = self.laAporta[i][1] * lnMonAfe / 100
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + lcCodigo + "', 'E01', " + str(self.lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR APORTACION DE ESSALUD (2). INFORME A TI</ERROR></DATA>'
                  return False
               i = self.FindArray(self.laAporta, 'PL0008')
               lnMonto = self.laAporta[i][1] * lnMonAfe / 100
               lcSql = "INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + lcCodigo + "', 'E03', " + str(self.lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR AL GRABAR APORTACION DE EPS. INFORME A TI</ERROR></DATA>'
                  return False
        return True


