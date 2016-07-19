<?php
require_once "Clases/CBase.php";
//-------------------------------------
// Inicio de sesion 
//-------------------------------------
class CLogin extends CBase {
   public $paData, $pcCodigo, $pcClave, $pcClave1, $pcClave2, $pcNombre, $pcCodPer, $pcTipo, $pcCadena, $pnCambio;

   public function __construct() {
      parent::__construct();
      $this->paData = null;
   }

   public function omCambiarClave() {
      // Condiciones de excepcion
      if (empty($this->pcCodUsu)) {
         $this->pcError = '<DATA><ERROR>CODIGO DE USUARIO NO ESTA DEFINIDO</ERROR></DATA>';
         return false;
      } else if (empty($this->pcClave)) {
         $this->pcError = '<DATA><ERROR>CLAVE NO DEFINIDA</ERROR></DATA>';
         return false;
      } else if (empty($this->pcClave1)) {
         $this->pcError = '<DATA><ERROR>NUEVA CLAVE NO DEFINIDA</ERROR></DATA>';
         return false;
      } else if (empty($this->pcClave2)) {
         $this->pcError = '<DATA><ERROR>REINGRESO DE NUEVA CLAVE NO DEFINIDA</ERROR></DATA>';
         return false;
      } else if ($this->pcClave1 != $this->pcClave2) {
         $this->pcError = '<DATA><ERROR>REINGRESO DE NUEVA CLAVE NO DEFINIDA</ERROR></DATA>';
         return false;
      }
      // Conectar DB
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
      // Verificar la clave antigua
      $lcSql = "SELECT cCodUsu, cClave FROM S02TUSU WHERE cCodUsu = '$this->pcCodUsu'";
      $RS = $loSql->omExec($lcSql);
      $laFila = $loSql->fetch($RS);
      if (empty($laFila[0])) {
         $loSql->omDisconnect();
         $this->pcError = '<DATA><ERROR>USUARIO NO EXISTE</ERROR></DATA>';
         return false;
      }
      if (md5($this->pcClave) != $laFila[1]) {
         $loSql->omDisconnect();
         $this->pcError = '<DATA><ERROR>CLAVE INCORRECTA</ERROR></DATA>';
         return false;
      }
      // Guardamos nueva clave
      $lcClave = md5($this->pcClave1);
      $lcSql = "UPDATE S02TUSU SET cClave = '$lcClave', dFecFin = SYSDATE + 45 WHERE cCodUsu = '$this->pcCodUsu'";
      $llOk = $loSql->omExec($lcSql);
      $loSql->omDisconnect();
      if (!$llOk) {
         $this->pcError = '<DATA><ERROR>ERROR AL ACTUALIZAR LA CLAVE</ERROR></DATA>';
      }
      return $llOk;
   }

   public function omLogin() {
      if (empty($this->paData['CCODIGO'])) {         
         $this->pcError = 'CODIGO DE USUARIO NO ESTA DEFINIDO';
         return false;
      } elseif (empty($this->paData['CCLAVE'])) {
         $this->pcError = 'CLAVE NO DEFINIDA';
         return false;
      }
      $lcWsdl = 'http://localhost:8080/WS_FTIA/Alfa?WSDL';
      $loClient = new SOAPClient($lcWsdl);
      //$functions = $loClient->__getFunctions();
      //var_dump ($functions);   
      // Verifica el usuario y clave
      $llOk = true;
      try {
         $laParams = array('CCODIGO' => $this->paData['CCODIGO'], "CCLAVE" => $this->paData['CCLAVE']);
         $loObject = $loClient->WSLogin($laParams);
         $laArray = objectToArray($loObject);
         $lcResult = $laArray['return'];
         //echo '<br>*'.$lcResult.'*<br>';
         $loXml = new SimpleXMLElement($lcResult);
         $loXml->asXML();
         $lcError = $loXml->ERROR;
         if (!empty($lcError)) {
            $this->pcError = $lcError;
            return false;
         }
         $this->paData = array('CNOMBRE' => $loXml->CNOMBRE, 'CCODOFI' => $loXml->CCODOFI, 'CCODUSU' => $loXml->CCODUSU);
      } catch (Exception $E) {
         $this->pcError = 'EXCEPCION: '.$E->setMessage;
         $llOk = false;
      }
      return $llOk;
   }
}
?>
