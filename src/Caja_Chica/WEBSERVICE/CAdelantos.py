# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from decimal import *
from CBase import *
from CBasePlanillas import *

#########################################################
## Clase que proceso adelantos de quincena y comisiones
#########################################################
class CAdelantos(CPlanillaBase):
    pcTermId = None
    lcCodCnt = None
    lcCtaAde = None
    lcCtaInt = None
    lcDescri = None
    lnPorQui = None
    laCtaCnt = []
        
    # Genera adelanto de quincena
    def omGenerarQuincena(self):
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Condiciones de excepcion
        llOk = self.mxExcepciones()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Parametros de adelanto de quincena
        llOk = self.mxParamAdelantoQuincena()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Carga cuentas contables
        llOk = self.mxCuentasContables()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Numero de documento por oficina
        llOk = self.mxNumeroDocumentoOficina()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba adelanto de quincena
        llOk = self.mxGrabarAdelantoQuincena()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba contabilizacion de adelanto de quincena
        llOk = self.mxCntAdelantoQuincena()
        if llOk:
           # Confirma la grabacion
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        return llOk

    # Realiza el pago del adelanto de quincena
    def omPagoQuincena(self):
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Condiciones de excepcion
        self.pcTermId = '*'   # OJOFPM
        llOk = self.mxExcepciones()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Parametros de pago de quincena
        llOk = self.mxParamPagoQuincena()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Carga cuentas contables
        llOk = self.mxCuentasContables()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Pago de quincena
        llOk = self.mxPagoQuincena()
        if llOk:
           # Confirma la grabacion
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        return llOk

    ##############################################################
    # Genera comisiones
    ##############################################################
    def omGenerarComision(self):
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Condiciones de excepcion
        llOk = self.mxExcepciones()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        llOk = self.mxParamAdelantoComision()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Carga cuentas contables
        llOk = self.mxCuentasContables()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Numero de documento por oficina
        llOk = self.mxNumeroDocumentoOficina()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba adelanto de quincena
        llOk = self.mxGrabarAdelantoComision()   #
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Graba contabilizacion de adelanto de quincena
        llOk = self.mxCntAdelantoComision()   #
        if llOk:
           # Confirma la grabacion
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        return llOk

    ##########################################################
    # Realiza el pago del adelanto de comision
    ##########################################################
    def omPagoComision(self):
        # Conectar base de datos
        self.loSql = CSql()
        llOk = self.loSql.omConnect()
        if not llOk:
           self.pcError = self.loSql.pcError
           return False
        # Condiciones de excepcion
        self.pcTermId = '*'   # OJOFPM
        llOk = self.mxExcepciones()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Parametros de pago de quincena
        llOk = self.mxParamPagoComision()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Carga cuentas contables
        llOk = self.mxCuentasContables()
        if not llOk:
           self.loSql.omDisconnect()
           return False
        # Pago de quincena
        llOk = self.mxPagoComision()
        if llOk:
           # Confirma la grabacion
           self.loSql.omCommit()
        self.loSql.omDisconnect()
        return llOk

    # Graba la contabilizacion del adelanto de comision
    def mxGrabarAdelantoComision(self):
        # Borra anteriores registros
        llOk = self.loSql.omExec("DELETE FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL ELIMINAR CONTABILIZACION ANTERIOR [E10DCNT]</ERROR></DATA>'
           return False
        # Extrae adelantos de comision
        RS = self.loSql.omExecRS("SELECT cCodOfi, cCtaBco, nMonto FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D02'")
        if len(RS) == 0:
           self.pcError = '<DATA><ERROR>NO HAY ADELANTO DE QUINCENA DEFINIDOS PARA PLANILLA [' + self.pcCodPla + ']</ERROR></DATA>';
           return False
        # Cuenta contable de adelanto de comision
        i = self.FindArray(self.laCtaCnt, 'PL0005', 2)
        if i == None:
           self.pcError = '<DATA><ERROR>NO HAY CUENTA CONTABLE PARA ADELANTO DE COMISION [PL0005]</ERROR></DATA>';
           return False
        lcCtaCnt = self.laCtaCnt[i][0];
        for XCOM in RS:
            # Glosa y monto
            lcGlosa = 'ADEL.COMISION CTA: [' + XCOM[1] + ']'
            lnMonto = XCOM[2]
            # Asiento de adelanto de quincena por oficina
            i = self.FindArray(self.laNroDoc, XCOM[0])
            lcNroDoc = self.laNroDoc[i][1]
            llOk = self.loSql.omExec("INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcGlosa + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')")
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE MOVIMIENTOS CONTABLES [E10DCNT]</ERROR></DATA>'
               return False
            #print self.laNroDoc[i][2]
            #print lnMonto
            self.laNroDoc[i][2] += lnMonto
        # Cuenta contable puente
        i = self.FindArray(self.laCtaCnt, 'PL0002', 2)
        if i == None:
           self.pcError = '<DATA><ERROR>NO HAY CUENTA CONTABLE PUENTE PARA ADELANTO DE COMISION [PL0002]</ERROR></DATA>';
           return False
        lcCtaCnt = self.laCtaCnt[i][0];
        lcDescri = self.laCtaCnt[i][1];
        # Graba totales
        for i in range(0, len(self.laNroDoc)):
            lcNroDoc = self.laNroDoc[i][1];
            lnMonto = self.laNroDoc[i][2]
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + lcCtaCnt + "', '" + lcDescri + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE MOVIMIENTOS CONTABLES [E10DCNT]</ERROR></DATA>'
                  return False
        self.loSql.omCommit()
        return True

    # Envia a contabilidad la contabilizacion del adelanto de comisiones
    def mxCntAdelantoComision(self):
        # Graba en contabilidad
        lcPeriod = self.pcCodPla[:4]
        lcNroDoc = '*'
        RS = self.loSql.omExecRS("SELECT cNroDoc, cCtaCnt, nDebeC, nHaberC, cGlosa FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt")
        for XCNT in RS:
            if XCNT[0] != lcNroDoc:
               lcNroDoc = XCNT[0]
               # Graba cabecera de comprobante contable
               lcNroCom = XCNT[0][:2] + 'PL' + lcPeriod
               lcNroCom = self.mxNroComprobante(lcNroCom)
               # cTipDoc = 'RI' [803]
               lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroDoc[:2] + "', 'S', 'ADELANTO DE COMISION', 'RI', '', '', '', '', '" + str(self.ldFecSis) + "', '', '', '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE CABECERA DE COMPROBANTES CONTABLES [D01MDIA]</ERROR></DATA>'
                  return False
            # Graba detalle de comprobante contable
            lcGlosa = XCNT[4]
            lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + XCNT[1] + "', '" + lcGlosa + "', 0, 0, " + str(XCNT[2]) + ", " + str(XCNT[3]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
            llOk = self.loSql.omExec(lcSql) 
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [D01DMOV]</ERROR></DATA>'
               return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1110000000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN ACTUALIZACION DE FASES DE PLANILLA [E01MPLA]</ERROR></DATA>'
           return False
        self.pcData = '<DATA><MENSAJE>GENERACION DE COMISION CONFORME</MENSAJE></DATA>';
        return True

    def mxGrabarAdelantoQuincena(self):
        # Elimina anteriores adelantos de quincena
        llOk = self.loSql.omExec("DELETE FROM ADM.E01DTRX WHERE cConcep = 'D01' AND cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '" + self.pcCodPla + "')")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL ELIMINAR TRANSACCIONES DE ADELANTO DE QUINCENA - D01 [E01DTRX]</ERROR></DATA>'
           return False
        # Elimina anteriores comprobantes contables de adelantos de quincena
        llOk = self.loSql.omExec("DELETE FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR AL ELIMINAR TRANSACCIONES CONTABLES [E10DCNT]</ERROR></DATA>'
           return False
        # Graba adelantos de quincena
        RS = self.loSql.omExecRS("SELECT cCodigo, cCodOfi, nBasico, cCtaBco FROM ADM.V_E01PPLA WHERE cCodPla = '" + self.pcCodPla + "'")
        if RS == None:
           self.pcError = '<DATA><ERROR>NO HAY EMPLEADOS DEFINIDOS PARA PLANILLA [' + self.pcCodPla + ']</ERROR></DATA>';
           return False
        # Cuenta contable de adelanto de quincena
        i = self.FindArray(self.laCtaCnt, 'PL0001', 2)
        lcCtaCnt = self.laCtaCnt[i][0]
        for XEMP in RS:
            lnMonto = float(XEMP[2]) * float(self.lnPorQui) / 100
            llOk = self.loSql.omExec("INSERT INTO ADM.E01DTRX (cCodigo, cConcep, nMonto, cCodUsu) VALUES ('" + XEMP[0] + "', 'D01', " + str(lnMonto) + ", '" + self.pcCodUsu + "')")
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA DE TRANSACCIONES [ADM.E01DTRX]</ERROR></DATA>'
               return False
            # Glosa
            lcData = 'ADEL.QUINCENA ' + XEMP[3]
            # Asiento de adelanto de quincena por oficina
            i = self.FindArray(self.laNroDoc, XEMP[1])
            lcNroDoc = self.laNroDoc[i][1];
            llOk = self.loSql.omExec("INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, dFecha, cCtaCnt, cGlosa, nDebeC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + str(self.ldFecSis) + "', '" + lcCtaCnt + "', '" + lcData + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')")
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE TABLA CONTABLE [ADM.E10DCNT]</ERROR></DATA>'
               return False
            self.laNroDoc[i][2] += lnMonto
        # Cuenta contable puente
        lcCtaCnt = self.laCtaCnt[1][0];
        lcDescri = self.laCtaCnt[1][1];
        # Graba totales
        for i in range(0, len(self.laNroDoc)):
            lcNroDoc = self.laNroDoc[i][1];
            lnMonto = self.laNroDoc[i][2]
            if lnMonto > 0:
               lcSql = "INSERT INTO ADM.E10DCNT (cCodCnt, cNroDoc, cCtaCnt, cGlosa, nHaberC, cCodUsu) VALUES ('" + self.lcCodCnt + "', '" + lcNroDoc + "', '" + lcCtaCnt + "', '" + lcDescri + "', " + str(lnMonto) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE MOVIMIENTOS CONTABLES [E10DCNT]</ERROR></DATA>'
                  return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1000000000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE FASES DE PLANILLAS [E01MPLA]</ERROR></DATA>'
           return False
        return True

    # Graba adelanto de quincena en contabilidad
    def mxCntAdelantoQuincena(self):
        # Periodo
        lcPeriod = self.pcCodPla[:4]
        lcNroDoc = '*'
        # Trae movimientos contables
        RS = self.loSql.omExecRS("SELECT cNroDoc, cCtaCnt, nDebeC, nHaberC, cGlosa FROM ADM.E10DCNT WHERE cCodCnt = '" + self.lcCodCnt + "' ORDER BY cNroDoc, cCtaCnt")
        for XCNT in RS:
            if XCNT[0] != lcNroDoc:
               # Documento de referencia
               lcNroDoc = XCNT[0]
               # Numero de comprobante
               lcNroCom = XCNT[0][:2] + 'PL' + lcPeriod
               lcNroCom = self.mxNroComprobante(lcNroCom)
               # Graba cabecera de comprobante contable
               lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroDoc[:2] + "', 'S', 'ADELANTO DE QUINCENA', 'RI', '', '', '', '', '" + str(self.ldFecSis) + "', '', '', '" + self.pcCodUsu + "')"

               print lcSql

               llOk = self.loSql.omExec(lcSql) 
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE CABECERA DE COMPROBANTES CONTABLES [CNT.D01MDIA]</ERROR></DATA>'
                  return False
            # Graba detalle de comprobante contable
            lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + XCNT[1] + "', '" + XCNT[4] + "', 0, 0, " + str(XCNT[2]) + ", " + str(XCNT[3]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"

            print lcSql

            llOk = self.loSql.omExec(lcSql)
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
               return False
        self.pcData = '<DATA><MENSAJE>GENERACION QUINCENA CONFORME</MENSAJE></DATA>';
        return True

    # Carga cuentas contables para adelanto de quincena
    def mxCuentasContables(self):
        self.laCtaCnt = []
        RS = self.loSql.omExecRS("SELECT cCtaCnt, cDescri, cCodigo FROM ADM.E10TCNT WHERE cCodigo LIKE 'PL%' ORDER BY cCodigo")
        i = 0
        for XCNT in RS:
            lcCtaCnt = XCNT[0].strip() + '%'
            RS = self.loSql.omExecRS("SELECT COUNT(cCtaCnt) FROM CNT.D01MCTA WHERE cCtaCnt LIKE '" + lcCtaCnt + "'")
            if RS[0][0] > 1:
               self.pcError = '<DATA><ERROR>CUENTA CONTABLE [' + XCNT[0].strip() + '] NO ES DE ULTIMO NIVEL</ERROR></DATA>'
               return False
            self.laCtaCnt.append([])
            self.laCtaCnt[i].append(XCNT[0].strip())
            self.laCtaCnt[i].append(XCNT[1].strip())
            self.laCtaCnt[i].append(XCNT[2])
            i+=1
        if i == 0:
           self.pcError = '<DATA><ERROR>CUENTAS CONTABLES PARA PLANILLAS NO DEFINIDAS</ERROR></DATA>'
           return False
        return True
            
    # Excepciones para generar y pagar quincena
    def mxExcepciones(self):
        if self.mxEmpty(self.pcTermId):
           self.pcError = '<DATA><ERROR>IDENTIFICADOR DE TERMINAL VACIO</ERROR></DATA>'
           return False
        elif self.mxEmpty(self.pcCodUsu):
           self.pcError = '<DATA><ERROR>CODIGO DE USUARIO VACIO</ERROR></DATA>'
           return False
        # Verifica planillas 
        llOk = self.mxValPlanilla()
        if not llOk:
           return False
        # Tipo de cambio
        RS = self.loSql.omExecRS("SELECT nTipFij FROM CNT.D01DCAM WHERE dCambio = '" + str(self.ldFecSis) + "' ORDER BY nCorrel DESC LIMIT 1")
        if RS == None:
           self.pcError = '<DATA><ERROR>NO HAY TIPO DE CAMBIO PARA FECHA [' + self.ldFecSis + ']</ERROR></DATA>'
           return False
        self.lnTipCam = RS[0][0]
        return True

    # Valida estado de fase   OJOFPM DEBE DESAPARECER
    def mxValFases(self, p_nFlag):
        if p_nFlag == 0 and self.lcFases != '0000000000':
           self.pcError = '<DATA><ERROR>GENERACION DE ADELANTO DE QUINCENA YA REALIZADO</ERROR></DATA>'
           return False
        elif p_nFlag == 1 and self.lcFases != '1000000000':
           self.pcError = '<DATA><ERROR>PAGO DE QUINCENA YA REALIZADO</ERROR></DATA>'
           return False
        elif p_nFlag == 2 and self.lcFases != '1110000000':
           self.pcError = '<DATA><ERROR>PAGO DE COMISION YA REALIZADO</ERROR></DATA>'
           return False
        return True

    # Pago de quincena   OJOFPM ES IGUAL A PAGO DE COMISION mxPagoComision
    def mxPagoQuincena(self):
        # Lee todos los pagos de adelanto de quincena
        RS = self.loSql.omExecRS("SELECT cCodOfi, nMonto, cCtaBco FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D01' ORDER BY cCodOfi")
        for XPAG in RS:
            # Abona en cuenta de ahorros   OJOFPM FALTA
            print XPAG[2], XPAG[1]
        # Nro documento referencia
        lcCodCnt = self.pcCodPla + 'AQU'
        # Numeros de comprobantes contables por oficinas
        lcPeriod = self.pcCodPla[:4]
        i = 0
        laNroCom = []
        lcSql = "SELECT DISTINCT cCodOfi FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D01' UNION SELECT DISTINCT SUBSTRING(cCtaBco, 1, 2) AS cCodOfi FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D01'"
        RS = self.loSql.omExecRS(lcSql)
        for XOFI in RS:
            # Busca documento de referencia
            RS = self.loSql.omExecRS("SELECT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '" + lcCodCnt + "' AND SUBSTRING(cNroDoc, 1, 2) = '" + XOFI[0] + "' LIMIT 1")
            if RS == None:
               # Si no hay documento de referencia de oficina toma el primero
               RS = self.loSql.omExecRS("SELECT MIN(cNroDoc) FROM ADM.E10DCNT WHERE cCodCnt = '" + lcCodCnt + "' LIMIT 1")
            lcNroDoc = RS[0][0]
            # Nro Comprobante
            lcNroCom = XOFI[0] + 'AV' + lcPeriod
            lcNroCom = self.mxNroComprobante(lcNroCom)
            laNroCom.append([])
            laNroCom[i].append(XOFI[0])
            laNroCom[i].append(lcNroCom)
            i += 1
            # cTipDoc = 'RI' [803]
            lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroCom[:2] + "', 'S', 'ABONO DE QUINCENA', 'RI', '', '', '', '', '" + str(self.ldFecSis) + "', '', '', '" + self.pcCodUsu + "')"
            print lcSql
            llOk = self.loSql.omExec(lcSql) 
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE CABECERA DE COMPROBANTES CONTABLES [CNT.D01MDIA]</ERROR></DATA>'
               return False
        if i == 0:
           self.pcError = '<DATA><ERROR>NO HAY OFICINAS DEFINIDAS</ERROR></DATA>';
           return False
        # Contabiliza pagos de adelanto de quincena
        lcSql = "SELECT cCodOfi, cOfiCod, SUM(nMonto) FROM (SELECT cCodOfi, nMonto, SUBSTRING(cCtaBco, 1, 2) AS cOfiCod FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D01') A GROUP BY cCodOfi, cOfiCod ORDER BY cCodOfi"
        RS = self.loSql.omExecRS(lcSql)
        for XCNT in RS:
            if XCNT[0] == XCNT[1]:
               i = self.FindArray(laNroCom, XCNT[0])
               lcNroCom = laNroCom[i][1]
               # Cuenta puente
               lcCtaCnt = self.laCtaCnt[1][0]
               lcDescri = self.laCtaCnt[1][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0," + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')" 
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Cuenta ahorros
               lcCtaCnt = self.laCtaCnt[3][0]
               lcDescri = self.laCtaCnt[3][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
            else:
               # Agencia origen
               i = self.FindArray(laNroCom, XCNT[0])
               lcNroCom = laNroCom[i][1]
               # Cuenta puente
               lcCtaCnt = self.laCtaCnt[1][0]
               lcDescri = self.laCtaCnt[1][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0, " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Cuenta interagencias
               lcCtaCnt = self.laCtaCnt[2][0]
               lcDescri = self.laCtaCnt[2][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Agencia destino
               i = self.FindArray(laNroCom, XCNT[1])
               lcNroCom = laNroCom[i][1]
               #i = int(XCNT[1]) - 1
               #lcNroCom = laNroCom[i][1]
               # Cuenta interagencias
               lcCtaCnt = self.laCtaCnt[2][0]
               lcDescri = self.laCtaCnt[2][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0, "  + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Cuenta ahorros
               lcCtaCnt = self.laCtaCnt[3][0]
               lcDescri = self.laCtaCnt[3][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1100000000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN ACTUALIZACION DE FASES DE PLANILLA [E01MPLA]</ERROR></DATA>'
           return False
        self.pcData = '<DATA><MENSAJE>PAGO QUINCENA CONFORME</MENSAJE></DATA>';
        return True

    # Pago de comision   OJOFPM ES IGUAL A PAGO DE QUINCENA mxPagoQuincena
    def mxPagoComision(self):
        # Lee todos los pagos de adelanto de comision
        RS = self.loSql.omExecRS("SELECT cCodOfi, nMonto, cCtaBco FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D02' ORDER BY cCodOfi")
        for XPAG in RS:
            # Abona en cuenta de ahorros
            print XPAG[2], XPAG[1]
        # Numeros de comprobantes contables por oficinas
        lcPeriod = self.pcCodPla[:4]
        i = 0
        laNroCom = []
        lcSql = "SELECT DISTINCT cCodOfi FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D02' UNION SELECT DISTINCT SUBSTRING(cCtaBco, 1, 2) AS cCodOfi FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D02'"
        RS = self.loSql.omExecRS(lcSql)
        for XOFI in RS:
            # Nro documento referencia
            lcCodCnt = self.pcCodPla + 'ACO'
            RS = self.loSql.omExecRS("SELECT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '" + lcCodCnt + "' AND SUBSTRING(cNroDoc, 1, 2) = '" + XOFI[0] + "' LIMIT 1")
            if RS == None:
               # Si no hay documento de referencia de oficina toma el primero
               RS = self.loSql.omExecRS("SELECT MIN(cNroDoc) FROM ADM.E10DCNT WHERE cCodCnt = '" + lcCodCnt + "' LIMIT 1")
            lcNroDoc = RS[0][0]
            # Nro Comprobante
            lcNroCom = XOFI[0] + 'AV' + lcPeriod
            lcNroCom = self.mxNroComprobante(lcNroCom)
            laNroCom.append([])
            laNroCom[i].append(XOFI[0])
            laNroCom[i].append(lcNroCom)
            i += 1
            # cTipDoc = 'RI' [803]
            lcSql = "INSERT INTO CNT.D01MDIA (cNroCom, cDocRef, cDocRel, cCodOfi, cHisSal, cGlosa, cTipDoc, cSerie, cNroDoc, cCodEmp, cNroRuc, dFecCnt, cEstado, cGravam, cCodUsu) VALUES ('" + lcNroCom + "', '" + lcNroDoc + "', '', '" + lcNroCom[:2] + "', 'S', 'ABONO DE ADELANTO COMISION', 'RI', '', '', '', '', '" + str(self.ldFecSis) + "', '', '', '" + self.pcCodUsu + "')"
            llOk = self.loSql.omExec(lcSql) 
            if not llOk:
               self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE CABECERA DE COMPROBANTES CONTABLES [CNT.D01MDIA]</ERROR></DATA>'
               return False
        if i == 0:
           self.pcError = '<DATA><ERROR>NO HAY OFICINAS DEFINIDAS</ERROR></DATA>';
           return False
        # Contabiliza abono de adelanto de comision
        lcSql = "SELECT cCodOfi, cOfiCod, SUM(nMonto) FROM (SELECT cCodOfi, nMonto, SUBSTRING(cCtaBco, 1, 2) AS cOfiCod FROM ADM.V_E01DTRX WHERE cCodPla = '" + self.pcCodPla + "' AND cConcep = 'D02') A GROUP BY cCodOfi, cOfiCod ORDER BY cCodOfi"
        RS = self.loSql.omExecRS(lcSql)
        for XCNT in RS:
            if XCNT[0] == XCNT[1]:
               i = self.FindArray(laNroCom, XCNT[0])
               lcNroCom = laNroCom[i][1]
               # Cuenta puente
               lcCtaCnt = self.laCtaCnt[1][0]
               lcDescri = self.laCtaCnt[1][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0," + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')" 
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Cuenta ahorros
               lcCtaCnt = self.laCtaCnt[3][0]
               lcDescri = self.laCtaCnt[3][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
            else:
               # Agencia origen
               i = self.FindArray(laNroCom, XCNT[0])
               lcNroCom = laNroCom[i][1]
               # Cuenta puente
               lcCtaCnt = self.laCtaCnt[1][0]
               lcDescri = self.laCtaCnt[1][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0, " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Cuenta interagencias
               lcCtaCnt = self.laCtaCnt[2][0]
               lcDescri = self.laCtaCnt[2][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Agencia destino
               i = self.FindArray(laNroCom, XCNT[1])
               lcNroCom = laNroCom[i][1]
               # Cuenta interagencias
               lcCtaCnt = self.laCtaCnt[2][0]
               lcDescri = self.laCtaCnt[2][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, " + str(XCNT[2]) + ", 0, "  + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
               # Cuenta ahorros
               lcCtaCnt = self.laCtaCnt[3][0]
               lcDescri = self.laCtaCnt[3][1]
               lcSql = "INSERT INTO CNT.D01DMOV (cNroCom, cMoneda, cCtaCnt, cGlosa, nDebe, nHaber, nDebeC, nHaberC, nTipCam, cCodUsu) VALUES ('" + lcNroCom + "', '1', '" + lcCtaCnt + "', '" + lcDescri + "', 0, 0, 0, " + str(XCNT[2]) + ", " + str(self.lnTipCam) + ", '" + self.pcCodUsu + "')"
               llOk = self.loSql.omExec(lcSql)
               if not llOk:
                  self.pcError = '<DATA><ERROR>ERROR EN GRABACION DE DETALLE DE COMPROBANTES CONTABLES [CNT.D01DMOV]</ERROR></DATA>'
                  return False
        llOk = self.loSql.omExec("UPDATE ADM.E01MPLA SET cFases = '1111000000' WHERE cCodPla = '" + self.pcCodPla + "'")
        if not llOk:
           self.pcError = '<DATA><ERROR>ERROR EN ACTUALIZACION DE FASES DE PLANILLA [E01MPLA]</ERROR></DATA>'
           return False
        self.pcData = '<DATA><MENSAJE>PAGO DE ADELANTO DE COMISION CONFORME</MENSAJE></DATA>';
        return True

    # Parametros de adelanto de quincena
    def mxParamAdelantoQuincena(self):
        if self.lcFases != '0000000000':
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE LA PLANILLA NO PERMITE GENERAR EL ADELANTO DE QUINCENA</ERROR></DATA>'
           return False
        self.lcCodCnt = self.pcCodPla + 'AQU';
        # Porcentaje de pago del basico para el adelanto de quincena
        RS = self.loSql.omExecRS("SELECT nValor FROM ADM.E10TPAR WHERE cCodigo = 'PL0001'")
        if RS == None:
           self.pcError = '<DATA><ERROR>PORCENTAJE DE ADELANTO DE QUINCENA [PL0001] NO DEFINIDO</ERROR></DATA>'
           return False
        self.lnPorQui = float(RS[0][0])
        return True

    # Parametros de pago de quincena
    def mxParamPagoQuincena(self):
        if self.lcFases != '1000000000':
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE LA PLANILLA NO PERMITE GENERAR EL PAGO DE QUINCENA</ERROR></DATA>'
           return False
        self.lcCodCnt = self.pcCodPla + 'PQU';
        return True

    # Parametros de adelanto de quincena
    def mxParamAdelantoComision(self):
        if self.lcFases != '1100000000':
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE LA PLANILLA NO PERMITE GENERAR EL ADELANTO DE COMISION</ERROR></DATA>'
           return False
        self.lcCodCnt = self.pcCodPla + 'ACO';
        return True

    # Parametros de pago de adelanto de comision
    def mxParamPagoComision(self):
        print self.lcFases
        if self.lcFases != '1110000000':
           self.pcError = '<DATA><ERROR>ESTADO DE FASES DE LA PLANILLA NO PERMITE REALIZAR EL PAGO DE ADELANTO DE COMISION</ERROR></DATA>'
           return False
        self.lcCodCnt = self.pcCodPla + 'PCO';
        return True


'''        
        if self.mxEmpty(self.pcTermId):
           self.pcError = '<DATA><ERROR>IDENTIFICADOR DE TERMINAL VACIO</ERROR></DATA>'
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
        # Verifica planillas 
        llOk = self.mxValPlanilla()
        if not llOk:
           return False
        # Valida estado de fase
        if self.lcFases != '0000000000':
           loSql.omDisconnect()
           self.pcError = '<DATA><ERROR>GENERACION DE ADELANTO DE QUINCENA YA REALIZADO</ERROR></DATA>'
           return False
'''

# EXTORNAR GENERACION DE QUINCENA
'''
-- Borrar detalle de la contabilidad
DELETE FROM CNT.D01DMOV WHERE cNroCom IN 
   (SELECT cNroCom FROM CNT.D01MDIA WHERE CDOCREF IN (SELECT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '13011A'));
-- Borra maestro de comprobantes contables   
DELETE FROM CNT.D01MDIA WHERE CDOCREF IN (SELECT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '13011A');
-- Borra detalle contable de planillas
DELETE FROM ADM.E10DCNT WHERE cCodCnt = '13011A';
-- Borra transacciones de adelanto de quincena
DELETE FROM ADM.E01DTRX WHERE cCodigo IN (SELECT cCodigo FROM ADM.E01PPLA WHERE cCodPla = '13011') AND cConcep = 'D01';
-- Actualiza estado de fases
UPDATE ADM.E01MPLA SET cFases = '0000000000' WHERE cCodPla = '13011'

# EXTORNAR GENERACION DE COMISIONES
-- Borrar detalle de la contabilidad
DELETE FROM CNT.D01DMOV WHERE cNroCom IN 
   (SELECT cNroCom FROM CNT.D01MDIA WHERE CDOCREF IN (SELECT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '13011B'));
-- Borra maestro de comprobantes contables   
DELETE FROM CNT.D01MDIA WHERE CDOCREF IN (SELECT cNroDoc FROM ADM.E10DCNT WHERE cCodCnt = '13011B');
-- Borra detalle contable de planillas
DELETE FROM ADM.E10DCNT WHERE cCodCnt = '13011B';
-- Actualiza estado de fases
UPDATE ADM.E01MPLA SET cFases = '1100000000' WHERE cCodPla = '13011'






CREATE TABLE s01tvar (
   cnomvar character(15),
   cdesvar character varying(50),
   ctipvar character(1),
   lcarini integer,
   cconvar character varying(60) NOT NULL,
   mdatos text,
   ccodusu character(4) NOT NULL,
   tmodifi abstime NOT NULL DEFAULT now()
);

INSERT INTO S01TVAR VALUES 
('GCNOMINS ','NOMBRE DE LA INSTITUCION','C',1,'CAJA INCASUR','','9999'),
('GCNOMOFI ','NOMBRE DE LA OFICINA','C',1,'OFICINA PRINCIPAL','','9999'),
('PNEDADMIN ','EDAD MINIMA DE UN CLIENTE','N',0,'18','','9999'),
('PNMONUNI ','MONTO LIMITE PARA OPERACIONES DE MAYOR CUANTIA','N',0,'10000.00','','9999'),
('PNMONMAXAUT ','Monto maximo para Autorizar Precancelacion','N',0,'30000','','9999'),
('PCPORCOMPREMN ','COMISION POR PREPAGO COMERCIAL O TOTAL','C',0,'3','','9999'),
('PNDISCTS ','DIPONIBLE DE CTS','N',0,'40','','9999'),
('GCPTHPTS ','RUTA DE LAS PLANTILLAS EXCEL','C',1,'/FTIA/ANX/PTS/','','9999'),
('GCPTHTAS ','PATH DE TABLAS DEL SERVIDOR','C',1,'/FTIA/TAS/','','9999'),
('GCPTHTCN ','TRANSFERENCIAS A CONTABILIDAD','C',0,'/FTIA.CNT/ADT/TCN/','','9999'),
('PCPTHPRN ','RUTA DE ALMACENAMIENTO DE IMPRESIONES','C',0,'/FTIA/PRINT/','','9999'),
('GCPTHTAB ','PATH DE TABLAS LOCALES','C',1,'/FTIA/TAB/','','9999'),
('GCPTHTMP ','RUTA PARA ARCHIVOS TEMPORALES','C',1,'C:\FTIA\TMP\','','9999'),
('GNREDMON ','UNIDAD MONETARIA A REDONDEAR','N',1,'0.01','','9999'),
('GCPTHXLS ','UBICACION DE PLANTILLAS EXCEL','C',1,'/FTIA/ANX/XLS/','','9999'),
('PCLEVGAR ','LEVANTAMIENTO DE GARANTIA ','C',0,'100.00 ','','9999'),
('PNPLAREN ','PLAZO DE RENOVACION','N',0,'30','','9999'),
('GNBLQAHO ','DIAS PARA BLOQUEAR CUENTAS DE AHORROS','C',0,'210','','9999'),
('GNINAAHO ','DIAS PARA INACTIVAR CUENTAS DE AHORROS','C',0,'390','','9999'),
('PCPAREND ','PARAMETROS ENDEUDAMIENTO','C',0,' ','','9999'),
('PCSECECO ','SECTORES ECONOMICOS','C',0,' ','','9999'),
('PNLIMGLO ','LIMITE GLOBAL','N',0,'200000','','9999'),
('PNLIMIND ','LIMITE INDIVIDUAL','N',0,'13000','','9999'),
('GCPTHEXE ','RUTA DE EJECUTABLES','C',1,'/BAT/','','9999'),
('PNAPESOL ','MONTO MINIMO APERTURA SOLES','N',1,'20','','9999'),
('PNAPEDOL ','MONTO MINIMO APERTURA DOLARES','N',1,'10','','9999'),
('PNMONMINMN ','MONTO MINIMO DE CREDITO EN MN','N',0,'300.00','','9999'),
('PNMONMINME ','MONTO MINIMO DE CREDITO EN ME','N',0,'100.00','','9999'),
('PNAHOAUT1 ','LIMITE RETIRO AUTORIZACION EN AHORROS MN','C',0,'5000','','9999'),
('PNAHOAUT2 ','LIMITE RETIRO AUTORIZACION EN AHORROS ME','C',0,'1800','','9999'),
('PCPTHRCI ','RUTA REPORTES DE CIERRE','C',0,'I:\FTIA\RCI\','','9999'),
('PNMONFSD ','MONTO DE FSD','N',0,'85793.00','','9999'),
('PNMONFSD ','LIMITE MONTO SEGURO DE DEPOSITO','N',0,'18000','','9999'),
('PNTASITF ','TASA ITF','N',0,'0.005','','9999'),
('GCSERVER ','NOMBRE DEL SERVIDOR LOCAL','C',1,'I:','','9999'),
('PNENCJMN ','MONTO BASE ENCAJE MN','N',0,'0.00','','9999'),
('PNENCJME ','MONTO BASE ENCAJE ME','N',0,'0.00','','9999'),
('PCCOMADE ','COMISION DE ADEUDOS','C',0,'COMISION DE ADEUDOS','COMISION BANCARIA,4101010101','9999'),
('PNPORIGV ','PORCENTAJE DE IGV','N',0,'0.18','','9999'),
('GNCANCTA ','CANCELAR CUENTAS APERTURADAS','N',0,'2','','9999'),
('PNPORREN ','PORCENTAJE DE RENTA','N',0,'0.30','','9999'),
('GCPTHFIR ','UBICACION DE FIRMAS','C',1,'I:/FTIA/FIRMAS/','','9999'),
('PNCHQGER ','CHEQUE DE GERENCIA','N',0,'13','','9999'),
('PNLIMBOV ','LIMITE DE BOVEDA','N',0,'150000.00','','9999'),
('PNLIMCAJ ','LIMITE DE CAJA','N',0,'20','','9999'),
('PCSEGDES ','OPCIONES PARA SEGURO DE DESGRAVAMEN','T',0,'','','9999'),
('PCTASSEG ','TASAS DE SEGURO DE DESGRAVAMEN','T',0,'','','9999'),
('PNSEGM70 ','SEGURO PARA MAYORES DE 70 AÑOS','N',0,'0.000','','9999'),
('GLOBVDOM ','OBVIAR DOMINGOS','L',0,'V','','9999'),
('PNPORAMO ','% AMORTIZACION PARA RENOVAR PAGARES','N',0,'0.10','','9999'),
('PCGASMORME ','Gastos de Mora en Moneda Extranjera','C',0,'US $ 0.00','','9999'),
('PNPORTED ','MONTO RENOVACION DE PORTES (DOLARES)','N',0,'0.00','','9999'),
('PNPORTES ','MONTO RENOVACION DE PORTES (SOLES)','N',0,'0.00','','9999'),
('GCCODINS ','CODIGO DE LA INSTITUCION','C',1,'00171','','9999'),
('PCGASMORMN ','Gastos de Mora en Moneda Nacional','C',0,'0','','9999'),
('PNVALCLA ','INTERVALO DE RENOVACION DE CLAVE (DIAS)','N',0,'30','','9999'),
('PCNRODUC ','NUMERO DE RUC DE LA EMPRESA','C',0,'00000000000','','9999'),
('PCNRODUC ','NUMERO DE RUC DE LA EMPRESA','C',0,'00000000000','','9999'),
('PNPORDMN ','PORCENTAJE DEDUCCION ENCAJE MN','N',0,' 5.6000','','9999'),
('PNTASAMN ','TASA DE CALCULO ENCAJE MN','N',0,' 9.9900','','9999'),
('PNTMARMN ','TASA MARGINAL ENCAJE MN','N',0,' 25.0000','','9999'),
('PNBASEME ','MONTO BASE DE ENCAJE ME','N',0,' 0.0000','','9999'),
('PNPORDME ','PORCENTAJE DEDUCCION ENCAJE ME','N',0,' 5.6000','','9999'),
('PNTASAME ','TASA DE CALCULO ENCAJE ME','N',0,' 9.0000','','9999'),
('PNTMARME ','TASA MARGINAL ENCAJE ME','N',0,' 55.5500','','9999'),
('PNMAXDMN ','MAXIMA DEDUCCION ENCAJE MN','N',0,' 50000000','','9999'),
('PCNRORUC ','NUMERO DE RUC DE LA EMPRESA','C',0,'00000000000','','9999'),
('PCDIREMP ','DIRECCION DE LA EMPRESA','C',0,'VIDAURRAZAGA 666','','9999'),
('GDFECPRO ','FECHA DEL SISTEMA','D',1,'2011.11.04','','9999'),
('GCESTATP ','ESTADO DE ATENCION AL PUBLICO (1>SI / 0>NO)','C',0,'1','','9999'),
('PNBASEMN ','MONTO BASE DE ENCAJE MN','N',0,'0.00','','9999'),
('PNMAXDME ','MAXIMA DEDUCCION ENCAJE ME','N',0,' 50000000.0000','','9999'),
('PNVALUIT ','VALOR DE UIT','N',0,'3750.00','','9999'),
('PNPORASF ','PORCENTAJE ASIGNACION FAMILIAR','N',0,'10.00','','9999'),
('PNDESESL ','PORCENTAJE DE APORTACION ESSALUD','N',0,'9.00','','9999'),
('PNREMMIN ','REMUNERACION MINIMA VITAL','N',0,'450','','9999'),
('PNRIECAJ ','RIESGO DE CAJA','N',0,'542','','9999'),
('GDFECSIS ','FECHA DE PROCESO','D',1,'2013.01.31','','9999'),
('GCESTAPL ','ESTADO DEL APLICATIVO DE CREDITOS','C',0,'00000000000000000000000000','','9999');

INSERT INTO CNT.D01DCAM (dCambio, cMoneda, nInsCom, nInsVen, nSbsCom, nSbsVen, nTipFij, cCodUsu) VALUES 
   ('2013-01-31', '2', 2.6, 2.8, 2.65, 2.8, 2.781, '9999')

'''

