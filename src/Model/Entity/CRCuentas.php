<?php

require_once "src/Model/Entity/CBase.php";
die('123');
require_once "src/Model/Entity/CSql.php";

//-------------------------------------
// Rendicion de Cuentas
//-------------------------------------
class CRCuentas extends CBase {
   public $paNomPer, $paEstado, $plNuevo, $paData;

   public function __construct() {
      parent::__construct();
      $this->paData = $this->plNuevo =$this->paEstado = null;
   }
   
   //
   public function omInitCuenta() {

      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      echo('qwerty');

      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      /*$conexion = pg_connect("host=localhost dbname=Caja port=5432 user=postgres password=postgres") or die("Casa");
      if (!$conexion) {
         $this->pcError = $loSql->pcError;
         return false;
      }*/
      //if (!$llOk) {
      //trae Personal
      $lcSql ="SELECT cNombre, cNroDni, cEntida FROM E02MPER where cNroDni='70155132'";
      /*$RS = pg_query($lcSql);
      print_r($RS);
      $this->paNomPer = pg_fetch_array($RS);*/
      $RS = $loSql->omExec($lcSql);
      $this->paNomPer = $loSql->fetch($RS);
      return true;
   }

   public function omBuscarPersonal(){
      if (empty($this->paData['CNRODNI'])) {
         $this->pcError = 'NO HA DEFINIDO CRITERIO DE BUSQUEDA';
         return false;
      }
      //die($this->paData['CNRODNI'].'asdasd');
      $lcNroDni = $this->paData['CNRODNI'];
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if(!$llOk){
         $this->pcError = $loSql->pcError;
         return false;
      }
      $lcSql = "SELECT cNomPer, cNomEnt, cEntida FROM V_E02MPER WHERE cNroDni = '$lcNroDni'"; 
      $RS= $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);

      if (empty($laFila[0])) {
         $loSql->omDisconnect();
         $this->pcError = 'DNI ['.$lcNroDni.'] NO EXISTE';
         return false;
      }
      $this->paData = array('CNOMBRE' => $laFila[0], 'CENTIDA' => $laFila[1],
                            'CNRODNI' => $lcNroDni, 'CCODENT' => $laFila[2]);
      $loSql->omDisconnect();
      return $llOk;     
   }
   
   public function omAbrirCuenta(){
      $llOk = $this -> mxValAbrirCuenta();
      if(!$llOk){
         return false;
      }
      // Conexion DB
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      $llOk = $this->mxAbrirCuenta($loSql);
      $loSql->omDisconnect();
      return $llOk;
   }

   public function mxValAbrirCuenta(){
      if(empty($this->paData['CNRODNI'])){
         $this->pcError= 'Nro de Dni no Definido';
         return false;
      } elseif (empty($this->paData['CCODENT'])){
         $this->pcError= 'Entidad no Definida';
         return false;
      } elseif (empty($this->paData['NMONTO'])){
         $this->pcError= 'Monto no Especificado';
         return false;
      }  elseif (empty($this->paData['DFECHA'])){
         $this->pcError= 'Fecha no Definida';
         return false;
      }  
      return true;
   }

   public function mxAbrirCuenta($p_oSql){
      $lcNroDni = $this->paData['CNRODNI'];
      $lcCodEnt = $this->paData['CCODENT'];
      $lnMonto = $this->paData['NMONTO'];
      $ldFecha = $this->paData['DFECHA'];
      $lcGlosa = $this->paData['CGLOSA'];
      $lcCodUsu = $this->paData['CCODUSU'];
      //Selecciona El numero de Rendicion de Cuenta
      $RS = $p_oSql->omExec("SELECT MAX(cIdenti) FROM E02MRCH");
      $laFila = $p_oSql->fetch($RS);
      $lcIdenti = $laFila[0];
      if (empty($lcIdenti)) {
         $lcIdenti = '000000';
      }
      $i = (int)$lcIdenti + 1;
      $lcIdenti = (string)$i;
      $lcIdenti = right('00000'.trim($lcIdenti), 6);
      //Abrir Nueva Rendicion de Cuentas
      $lcSql = "INSERT INTO E02MRCH (cIdenti, cTipo, cNroDni, dFecReg, cEstado, cGlosa , cEntida, nMonto, cMoneda, cCodUsu, tModifi)
               VALUES ('$lcIdenti','R','$lcNroDni','$ldFecha','A','$lcGlosa','$lcCodEnt',$lnMonto,'S','$lcCodUsu',NOW())";
      //die($lcSql);
      $llOk = $p_oSql->omExec($lcSql);

      if (!$llOk) {
         $this->pcError = 'ERROR EN GRABACION DE FINANCIERA';
      }
      return $llOk;
   }

   public function omBuscarRendicion(){
      $loSql = new CSQL();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      //Trae Rendicion
      $i = 0;
      $lcSql = "SELECT cIdenti, cGlosa, dFecReg, cTipo, cNroDni FROM E02MRCH 
               WHERE cEstado = 'A'";
      $RS = $loSql->omExec($lcSql);
      while ($laFila =$loSql->fetch($RS)){
         $i++;
         $this->paIdenti[] = array($laFila[0], $laFila[1], $laFila[2], $laFila[3], $laFila[4]);
      }
      $loSql->omDisconnect();
      if ($i == 0) {
         $this->pcError = 'NO EXISTEN RENDICIONES PENDIENTES';
         return false;
      }
      return true;
   }

   public function omIniciarRegistro(){
      if(empty($this->paData['CIDENTI'])){
         $this->pcError = 'CODIGO NO DEFINIDO';
         return false;
      }
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      //Trae datos
      $lcIdenti = $this->paData['CIDENTI'];
      $lcSql = "SELECT cIdenti, cTipo, dFecReg, cEstado, cGlosa, nMonto, cMoneda, cNomPer, cNomEnt, cNroDni FROM V_E02MRCH
               WHERE cIdenti = '$lcIdenti'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      if (empty($laFila[0])) {
         $loSql->omDisconnect();
         return false;
      }
      $this->paData = array('CIDENTI'=> $laFila[0],'CTIPO'=> $laFila[1], 'DFECREG'=> $laFila[2],
                           'CESTADO'=> $laFila[3],'CGLOSA'=> $laFila[4],'NMONTO'=> $laFila[5],
                           'CMONEDA'=> $laFila[6],'CNOMPER'=> $laFila[7],'CNOMENT'=> $laFila[8],'CNRODNI'=> $laFila[9] );
      return true;
   }

   public function omGrabarFinanciera() {
      $llOk = $this->mxValGrabarFinanciera();
      if (!$llOk) {
         return false;
      }
      // Conexion DB
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      $llOk = $this->mxGrabarFinanciera($loSql);
      $loSql->omDisconnect();
      return $llOk;
   }

   protected function mxValGrabarFinanciera() {
      if (empty($this->paData['CCODIFI']) &&$this->plNuevo) {
         $this->pcError = 'CODIGO NO DEFINIDO';
         return false;
      } elseif (empty($this->paData['CNOMIFI'])) {
         $this->pcError = 'NOMBRE DE INSTITUCION NO DEFINIDO';
         return false;
      } elseif (empty($this->paData['CCODUSU'])) {
         $this->pcError = 'CODIGO DE USUARIO NO DEFINIDO';
         return false;
      } elseif (empty($this->paData['CESTADO'])) {
         $this->pcError = 'ESTADO NO DEFINIDO';
         return false;
      }
      return true;
   }
   
   protected function mxGrabarFinanciera($p_oSql) {
      $lcCodIfi = $this->paData['CCODIFI'];
      $lcNomIfi = $this->paData['CNOMIFI'];
      $lcEstado = $this->paData['CESTADO'];
      $lcCodUsu = $this->paData['CCODUSU'];
      // INGRESAR NUEVO FINANCIERA
      if(!$this->plNuevo){
        $lcSql = "SELECT cCodIfi FROM S01MIFI WHERE cCodIfi = '$lcCodIfi'";
        $RS = $p_oSql->omExec($lcSql);
        $laFila = $p_oSql->fetch($RS);
        if (empty($laFila[0])) {
           $this->pcError = 'CODIGO ['.$lcCodIfi.'] NO EXISTE';
           return false;
        }
      }
      if ($this->plNuevo) {
         $lcSql = "INSERT INTO S01MIFI (cCodIfi, cNomIfi, cEstado, cCodUsu, tModifi)
                  VALUES ('$lcCodIfi', '$lcNomIfi','$lcEstado','$lcCodUsu', NOW())";
         $llOk = $p_oSql->omExec($lcSql);
      } else {
         $lcSql = "UPDATE S01MIFI SET cNomIfi = '$lcNomIfi', cEstado = '$lcEstado', tModifi=NOW()
                   WHERE cCodIfi = '$lcCodIfi'";
         
         $llOk = $p_oSql->omExec($lcSql);
      }
      if (!$llOk) {
         $this->pcError = 'ERROR EN GRABACION DE FINANCIERA';
      }
      return $llOk;
   }
   
   public function omEditarFinanciera() {
      if (empty($this->paData['CCODIFI'])) {
         $this->pcError = 'CODIGO NO DEFINIDO';
         return false;
      }
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      // Trae personal
      $lcCodIfi = $this->paData['CCODIFI'];
      $lcSql = "SELECT cCodIfi, cNomIfi, cEstado, cCodUsu FROM S01MIFI WHERE cCodIfi = '$lcCodIfi'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      if (empty($laFila[0])) {
         $loSql->omDisconnect();
         $this->pcError = 'FINANCIERA ['.$lcCodIfi.'] NO EXISTE';
         return false;
      }
      $this->paData = array('CCODIFI' => $laFila[0], 'CNOMIFI' => $laFila[1], 'CESTADO' => $laFila[2], 'CCODUSU'=> $laFila[3]);

      return true;
   }
}
?>