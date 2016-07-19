<?php
require_once "Clases/CBase.php";
require_once "Clases/CSql.php";

//-------------------------------------
// Mantenimiento alumnos
//-------------------------------------
class CIFinanciera extends CBase {
   public $paNomIfi, $paEstado, $plNuevo;

   public function __construct() {
      parent::__construct();
      $this->paNomIfi = $this->plNuevo =$this->paEstado = null;
   }
   
   //
   public function omInitFinanciera() {
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
     //trae institucion
      $lcSql ="SELECT cCodIfi, cNomIfi, cEstado FROM S01MIFI ORDER BY cNomIfi";
      $RS = $loSql->omExec($lcSql);
      while ($laFila =$loSql->fetch($RS)){
         $this->paNomIfi[] = array($laFila[0], $laFila[1], $laFila[2]);
      }
      
      //trae Estado
      $i = 0;
      $lcSql = "SELECT SUBSTR(cCodigo, 1, 1), cDescri FROM V_S01TTAB WHERE cCodTab = '041'";
      $RS = $loSql->omExec($lcSql);
      while ($laFila = $loSql->fetch($RS)) {
         $i++;
         $this->paEstado[] = array($laFila[0], $laFila[1]);
      }
     // print_r($this->paEstado);
     // die();
      $loSql->omDisconnect();
      
      if ($i == 0) {
         $this->pcError = 'NO HAY ESTADO DEFINIDO. SUBTABLA [041]';
         return false;
      }
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