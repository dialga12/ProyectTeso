<?php
require_once "class/PHPExcel.php";
require_once 'class/RTFTable.php';

//------------------------------------------------------
// Clase Base
//------------------------------------------------------
class CBase {
   public $pcError;

   function __construct() {
   }
   
   public function mxValDate($p_dFecha) {
      $laFecha = explode("-", $p_dFecha);
      return checkdate((int)$laFecha[1], (int)$laFecha[2], (int)$laFecha[0]); 
   }

   protected function mxError($p_cXml) {
      if (empty($p_cXml)) {
         $this->pcError = '<DATA><ERROR>ERROR EN CADENA DE DATOS XML (DB)</ERROR></DATA>';
         return false;
      }
      $xml = new SimpleXMLElement($p_cXml);
      $xml->asXML();
      $lcError = $xml->ERROR;
      if (!empty($lcError)) {
         $this->pcError = $lcError;
         return false;
      }
      return true;
   }
}

//------------------------------------------------------
// Clase para fechas
//------------------------------------------------------
class CDate extends CBase {
   public $date;
   public $days;

   public function valDate($p_dFecha) {
      $laFecha = explode('-', $p_dFecha);
      $llOk = checkdate((int)$laFecha[1], (int)$laFecha[2], (int)$laFecha[0]); 
      if (!$llOk) {
         $this->pcError = 'FORMATO DE FECHA INVALIDA';
      }
      return $llOk;
   }

   public function add($p_dFecha, $p_nDias) {
      $llOk = $this->valDate($p_dFecha);
      if (!$llOk) {
         return false;
      }
      if (!is_int($p_nDias)) {
         $this->pcError = 'PARAMETRO DE DIAS ES INVALIDO';
         return false;
      } elseif ($p_nDias >= 0) {
         $lcDias = ' + '.$p_nDias.' days';
      } else {
         $p_nDias = $p_nDias * (-1);
         $lcDias = ' - '.$p_nDias.' days';
      }
      $this->date = date('Y-m-d', strtotime($p_dFecha.$lcDias));
      return true;
   }
   
   public function diff($p_dFecha1, $p_dFecha2) {
      $llOk = $this->valDate($p_dFecha1);
      if (!$llOk) {
         return false;
      }
      $llOk = $this->valDate($p_dFecha2);
      if (!$llOk) {
         return false;
      }
      $this->days = (strtotime($p_dFecha1) - strtotime($p_dFecha2)) / 86400;
      $this->days = floor($this->days);
	  return true;
   }
   
   public function dateText($p_dDate) {
      $llOk = $this->valDate($p_dDate);
      if (!$llOk) {
         return 'Error: '.$p_dDate;
      }
      $laDays = array('Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado');
      $laMonths = array('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre');
      $laDate = explode('-', $p_dDate);
      $ldDate = mktime(0, 0, 0, $laDate[1], $laDate[2], $laDate[0]);
      return $laDays[date('w', $ldDate)].', '.date('d', $ldDate).' '.$laMonths[date('m', $ldDate) - 1].' de '.date('Y', $ldDate);
   }
}

class CXls extends CBase {
   public $pcData = "";
   protected $loXls, $lo, $lcFilXls;

   public function __construct() {
      parent::__construct();
      $this->loXls = new PHPExcel();
      $this->lo = PHPExcel_IOFactory::createReader('Excel2007');      
   }
   
   public function openXls($p_cFilXls, $p_cCodUsu) {                  
      $this->loXls = $this->lo->load('./Xls/'.$p_cFilXls.'.xlsx');      
      $this->lcFilXls = './Ficheros/'.$p_cFilXls.'_'.$p_cCodUsu.'.xlsx';      
   }
   
   public function sendXls($p_nSheet, $p_cCol, $p_nRow, $p_xValue) {      
      $this->loXls->setActiveSheetIndex($p_nSheet)->setCellValue($p_cCol.$p_nRow, $p_xValue);            
      return;
   }
   
   public function closeXls() {    
      $lo = PHPExcel_IOFactory::createWriter($this->loXls, 'Excel2007');                        
      $lo->save($this->lcFilXls);           
   }
}


//------------------------------------------------------
// Trabaja cadenas XML
//------------------------------------------------------
class CXml extends CBase {
   public $pcData, $pcLabel, $pcValor;

   public function __construct() {
      parent::__construct();
   }

   public function omBuscar() {
      $llOk = false;
      $lcLabel = trim($this->pcLabel);
      if (empty($lcLabel)) {
         $this->lcError = "<DATA><ERROR>Etiqueta de busqueda no definida</ERROR></DATA>";
         return false;
      }
      $lcData = trim($this->pcData);
      $lcData = str_replace("<", "[", $lcData);
      $lcData = str_replace(">", "]", $lcData);
      $lcLabel1 = "[" . $lcLabel . "]";
      $lcLabel2 = "[/" . $lcLabel . "]";
      $i = strpos($lcData, $lcLabel1);
      if ($i === false) {
         $this->lcError = "<DATA><ERROR>Etiqueta de busqueda de inicio no encontrada</ERROR></DATA>";
         return false;
      }
      $j = strpos($lcData, $lcLabel2);
      if ($j === false) {
         $this->lcError = "<DATA><ERROR>Etiqueta de busqueda de cierre no encontrada</ERROR></DATA>";
         return false;
      }
      $i = $i + strlen($lcLabel1);
      $this->pcValor = substr($lcData, $i, $j - $i);
      $this->pcValor = str_replace($lcLabel1, "", $this->pcValor);
      return true;
   }
}

class CRtf extends CBase {
   public $pcFile, $paArray, $pcFilRet, $pcCodUsu, $paAArray;
   protected $lcFolXls, $lcFolSal, $lcFilRet, $lcFilInp, $lcTodo, $lp;
  
   function __construct () {
      parent::__construct();
      $this->paArray = null;
      $this->lcFolXls = './Xls/';
      $this->lcFolSal = './Ficheros/';
   }
   
   public function omInicializar() {
      $lcFile1 = $this->lcFolXls.$this->pcFile.'.rtf';
      if (empty($this->pcCodUsu)) {
         $this->pcError = 'CODIGO DE USUARIO NO DEFINIDO';
         return false;
      } elseif (!is_file($lcFile1)) {
         $this->pcError = 'ARCHIVO DE ORIGEN NO EXISTE';
         return false;
      }
      if (empty($this->pcFilRet)) {
         $this->pcFilRet = $this->lcFolSal.$this->pcFile.'_'.$this->pcCodUsu.'.doc';
      }
      $this->lp = fopen($this->pcFilRet, 'w');
      // Lee archivo formato
      $laTexto = file($lcFile1);
      $lnSize = sizeof($laTexto);
      $this->lcTodo = '';
      for ($i = 0;$i < $lnSize; $i++) {
          $this->lcTodo .= $lcTodo.$laTexto[$i];
      }
      return true;
   }
   
   protected function mxTerminar() {
      fputs($this->lp, $this->lcTodo);
      fclose($this->lp);
      return true;
   }
   
   public function omGenerar($p_lClose = false) {
      if (!(is_array($this->paArray) and count($this->paArray) > 0)) {
         fclose($this->lp);
         $this->pcError = '<DATA><ERROR>ARREGLO DE DATOS NO DEFINIDO</ERROR></DATA>';
         return false;
      }
      // Reemplazo de variables
      foreach ($this->paArray as $lcValor1 => $lcValor2) {
         $lcValor2 = utf8_decode($lcValor2);
         $this->lcTodo = str_replace($lcValor1, $lcValor2, $this->lcTodo);
      }
      if ($p_lClose) {
         $this->mxTerminar();
      }
      return true;
   }
   
   public function omGenerarArray($p_lClose = false) {
      if (!(is_array($this->paAArray) and count($this->paAArray) > 0)) {
         fclose($this->lp);
         $this->pcError = 'ARREGLO DE DATOS NO DEFINIDO';
         return false;
      }
      foreach ($this->paAArray as $lcValor1 => $lcValor2) {
         $loTabla = new RTFTable($lcValor2[0], $lcValor2[1]);
         if ($lcValor2[3]=='') {
            $loTabla->SetWideColsTable(round(10500/$lcValor2[0]));
         }else {
            for ($k = 0;$k < count($lcValor2[3]);$k++) {
                $loTabla->SetWideColTable($k,$lcValor2[3][$k]);
            }
         }
         //Llenar Tabla cn arreglo pos:2
         for ($i = 0;$i < count($lcValor2[2]);$i++) {
             for ($j = 0;$j < count($lcValor2[2][0]);$j++) {
                 $lcValor2[2][$i][$j] = utf8_decode($lcValor2[2][$i][$j]);
                 if ($j ==0 ) {
                    //Centrado
                    $loTabla->SetElementCell($i,$j,'\\qc '.$lcValor2[2][$i][$j]);
                 }else
                    $loTabla->SetElementCell($i,$j,' '.$lcValor2[2][$i][$j]);
             }
         }
         $this->lcTodo = str_replace($lcValor1,$loTabla->GetTable() ,$this->lcTodo);
      }
      if ($p_lClose) {
         $this->mxTerminar();
      }
      return true;
   }
   
   protected function mxLeerArchivo() {
      if (!is_file($this->pcFile)) {
         $this->pcError = '<DATA><ERROR>ARCHIVO DE ORIGEN NO EXISTE</ERROR></DATA>';
         return false;
      }
      $laTexto = file($this->pcFile);
      $lnSize = sizeof($laTexto);
      $lcTodo = '';
      for ($i = 0;$i < $lnSize;$i++) {
          $lcTodo = $lcTodo.$laTexto[$i];
      }
      return $lcTodo;
   }
   
   public function omProcesar() {
      $this->lcFilRet = $this->lcFolSal.$this->pcFile.'_'.$this->pcCodUsu.'.rtf';//-- DEFINIMOS EL NOMBRE DEL NUEVO FICHERO
      $this->pcFile = $this->lcFolXls.$this->pcFile.'.rtf';
      if ($lcTexto = $this->mxLeerArchivo()) {
         $lp = fopen($this->lcFilRet, 'w');
         if (is_array($this->paArray) and count($this->paArray) > 0) {
            foreach($this->paArray as $lcValor1 =>$lcValor2) {//-- REEMPLAZAMOS LAS VARIABLES
               $lcValor2 = utf8_decode($lcValor2);
               $lcTexto = str_replace($lcValor1, $lcValor2 ,$lcTexto);
            }
         }
         fputs($lp, $lcTexto);
         fclose($lp);
         header ('Content-Disposition: attachment;filename = '.$this->lcFilRet.'\n\n');
         header ('Content-Type: application/octet-stream');
         readfile($this->lcFilRet);
      }
   }
}

class CRtf_1 extends CBase {
   public $pcFile, $paArray, $pcError, $pcCodUsu;
   protected $lcFolXls, $lcFolSal, $lcFilRet;
 
   function __construct () {
      parent::__construct();
      $this->paArray = array();
      $this->lcFolXls = './Xls/';
      $this->lcFolSal = './Ficheros/';
   }
   
   protected function mxLeerArchivo() {
      if (!is_file($this->pcFile)) {
         $this->pcError = '<DATA><ERROR>Archivo de Origen no existe</ERROR></DATA>';
         return false;
      }
      $lcTexto = file($this->pcFile);
      $lnSize = sizeof($lcTexto);
      $lcTodo = '';
      for ($i = 0; $i < $lnSize; $i++) {
          $lcTodo = $lcTodo.$lcTexto[$i];
      }
      return $lcTodo;
   }
 
   public function omProcesar() {
      $this->lcFilRet = $this->lcFolSal.$this->pcFile.'_'.$this->pcCodUsu.'.rtf';//-- DEFINIMOS EL NOMBRE DEL NUEVO FICHERO
      $this->pcFile = $this->lcFolXls.$this->pcFile.'.rtf';
      if ($lcTexto = $this->mxLeerArchivo()) {
         $lp = fopen($this->lcFilRet, 'w');
         if (is_array($this->paArray) and count($this->paArray) > 0) {
            foreach($this->paArray as $lcValor1=>$lcValor2) {//-- REEMPLAZAMOS LAS VARIABLES
               $lcValor2 = utf8_decode($lcValor2);
               $lcTexto = str_replace($lcValor1, $lcValor2 ,$lcTexto);
            }
         }
         fputs($lp, $lcTexto);
         fclose($lp);
         header ("Content-Disposition: attachment; filename=".$this->lcFilRet."\n\n"); 
         header ("Content-Type: application/octet-stream");
         readfile($this->lcFilRet);
      }
   }
}

function right($lcCadena, $count) {
   return substr($lcCadena, ($count * -1));
}

function left($lcCadena, $count) {
   return substr($lcCadena, 0, $count);
}

function fxInitSession() {
   $llOk = false;
   if (isset($_SESSION["gcNombre"]) and isset($_SESSION["gcCodUsu"]) and isset($_SESSION["gcCodOfi"])) {
      $llOk = true;
   }
   //return $llOk;
   return true;
}

function fxNombreMes($p_cMes) {
   $laNomMes = array("EN", "FE", "MZ", "AB", "MY", "JN", "JL", "AG", "SE", "OC", "NO", "DI");
   return $laNomMes[intval($p_cMes) - 1];
}

function fxSanearCadena($p_cCadena) {
    $lcCadena = utf8_encode($p_cCadena);
    $lcCadena = str_replace(array('ñ', 'Ñ', 'Ã±','Ã‘'), 'N', $lcCadena);
    $lcCadena = trim($lcCadena);
    $lcCadena = str_replace(array('ç', 'Ç', 'Ã§', 'Ã'), 'C', $lcCadena);
    $lcCadena = str_replace(array('á', 'à', 'ä', 'â', 'ª', 'Á', 'À', 'Â', 'Ä', 'Ã¡', 'Ã ', 'Ã¤', 'Ã¢', 'Âª', 'Ã', 'Ã', 'Ã', 'Ã'), 'A', $lcCadena);
    $lcCadena = str_replace(array('é', 'è', 'ë', 'ê', 'É', 'È', 'Ê', 'Ë', 'Ã©', 'Ã¨', 'Ã«', 'Ãª', 'Ã', 'Ã', 'Ã', 'Ã'), 'E', $lcCadena);
    $lcCadena = str_replace(array('í', 'ì', 'ï', 'î', 'Í', 'Ì', 'Ï', 'Î', 'Ã­', 'Ã¬', 'Ã¯', 'Ã®', 'Ã', 'Ã', 'Ã', 'Ã'), 'I', $lcCadena);
    $lcCadena = str_replace(array('ó', 'ò', 'ö', 'ô', 'Ó', 'Ò', 'Ö', 'Ô', 'Ã³', 'Ã²', 'Ã¶', 'Ã´', 'Ã', 'Ã', 'Ã', 'Ã'), 'O', $lcCadena);
    $lcCadena = str_replace(array('ú', 'ù', 'ü', 'û', 'Ú', 'Ù', 'Û', 'Ü', 'Ãº', 'Ã¹', 'Ã¼', 'Ã»', 'Ã', 'Ã', 'Ã', 'Ã'), 'U', $lcCadena);
    //Esta parte se encarga de eliminar cualquier caracter extraño
    $lcCadena = str_replace(array("\\", "¨", "º", "~", "|" , "\"", "·", "$", "%", "'" , "¡" , "&", "¿", "^", "`", "¨", "´"), '', $lcCadena);
    $lcCadena = strtoupper($lcCadena);
    return $lcCadena;
}

function VMas($p_cCadena) {
   $lcCadena = str_replace(" ", '+', $p_cCadena);
   return $lcCadena;
}

function fxEliminarFila($laData, $laCheck) {
   // Numero de columnas
   $lnCol = 0;
   foreach($laData as $i) {
      foreach($i as $j) {
         $lnCol++;
      }
      break;
   }
   // Elimina filas
   $k = 0;
   $laData1 = null;
   foreach($laData as $i) {
      //print_r($i); echo '<br>';
      $llOk = true;
      foreach($laCheck as $j) {
         if ($i[0] == $j) {
            $llOk = false;
            break;
         }
      }
      if ($llOk) {
         $k++;
         $laData1[$k] = array();
         $laData1[$k][0] = $k;
         for ($j = 1; $j <= $lnCol; $j++) {
             $laData1[$k][$j] = $i[$j];
         }
      }
   }
   return $laData1;
}

function fxBuscarFila($laData, $laCheck, $lnCol) {
   $k = 0;
   $llOk = false;
   foreach($laData as $i) {
      $k++;
      foreach($laCheck as $j) {
         if ($i[0] == $j) {
         $llOk = true;
            break;
         }
      }
     if ($llOk)
        break;
   }
   $lcCodigo = $laData[$k][$lnCol];
   return $lcCodigo;
}

function fxValDelete($p_aCheck, $p_aDataB) {
   $llOk = true;
   if (isset($p_aCheck)) {
      foreach($p_aCheck as $i) {
         foreach($p_aDataB as $j) {
            if ($i == $j[0]) {
               $llOk = false;
               break;
            }
         }
        if (!$llOk)
           break;
      }
   }
   return $llOk;
} 

function fxValRepeated($p_aData, $p_nCol) {
   $i = 0;
   if (!isset($p_aData))
      return false;
   if (count($p_aData) == 1) 
      return false;
   foreach($p_aData as $laFila) {
      $i++;
      $j = 0;
      foreach($p_aData as $laFila1) {
         $j++;
         if ($i <= $j) {
            continue;
         }
         if ($laFila[$p_nCol] == $laFila1[$p_nCol]) {
            return true;
         }
      }
   }
   return false;
} 

function fxAlert($p_Message) {
   echo "<script type=\"text/javascript\">";
   echo "alert('$p_Message')";
   echo "alert('$p_Message')";
   echo "</script>";  
}

function fxXmlError($p_cXml) {
   $lcMessage = null;
   try {
      $xml = new SimpleXMLElement($p_cXml);
      $xml->asXML();
      $lcMessage = $xml->ERROR;
   } catch (Exception $e) {
      echo 'Excepción capturada: '.$e->getMessage();
   }
   return $lcMessage;
}

function fxValDate($p_dFecha) {
   $laFecha = explode("-", $p_dFecha);
   return checkdate((int)$laFecha[1], (int)$laFecha[2], (int)$laFecha[0]); 
}
   
function fxValTime($p_cTime) {
   $laTime = explode(":", $p_cTime);
   if (!($laTime[0] >= '00' and $laTime[0] <= '24')) 
      return false;
   if (!($laTime[1] >= '00' and $laTime[1] <= '59')) 
      return false;
   return true;
}

function fxCallIndex($p_cMensaje) {
   if (empty($p_cMensaje)) {
      echo "<script> window.location='index.php';</script>";
   } else {
      echo '<script>';
      echo "alert('$p_cMensaje');";
      echo "window.location='index.php';</script>";
   }
}

function fxHeader($p_cLocation, $p_cMensaje = '') {
   if (empty($p_cMensaje)) {
      $lcScript = "window.location='$p_cLocation';";
   } else {
      $lcScript = "alert('$p_cMensaje');window.location='$p_cLocation';";
   }
   echo '<script>'.$lcScript.'</script>';
}

function fxValEmail($p_cEmail) {
   $lcEmail = trim($p_cEmail);
   if (strpos($lcEmail,' ')) {
      return false;
   }
   if (!strpos($lcEmail,'@')){
      return false;
   }
   if (strpos('@',$lcEmail,1)){
      return false;
   }
   $lcCorreo = explode('@', $lcEmail);
   if (empty($lcCorreo[0])) {
      return false;
   }
   if (empty($lcCorreo[1])){
      return false;
   }
   $j = explode('.', $lcCorreo[1]);
   if (empty($j[0])) {
      return false;
   }
   if (empty($j[1])) {
      return false;
   }
   return true;
}

function fxAddDate($p_dFecha, $p_nDias) {
   $ldFecha = strtotime($p_nDias. ' day', strtotime($p_dFecha));
   $ldFecha = date('Y-m-d', $ldFecha);
   return $ldFecha;
}

function fxSumaFecha($p_dFecha, $p_nDia) {
   list($lnYear, $lnMonth, $lnDay) = explode('-', $p_dFecha);
   $ldFecha =  date('Y-m-d', mktime(0, 0, 0, $lnMonth, $lnDay + $p_nDia, $lnYear));
   return $ldFecha;
}

function dameFecha($fecha,$dia)
{   list($day,$mon,$year) = explode('/',$fecha);
    return date('d/m/Y',mktime(0,0,0,$mon,$day+$dia,$year));        
}

class CSendEmail extends CBase {
   public $pcForWho, $pcFrom, $pcSubject, $pcMessage;
 
   function __construct () {
      parent::__construct();
   }
   
   public function omSend() {
      if (empty($this->pcForWho)) {
         $this->pcError = '<DATA><ERROR>Email de destino no definido</ERROR></DATA>';
         return false;
      } elseif (empty($this->pcFrom)) {
         $this->pcError = '<DATA><ERROR>Email de origen no definido</ERROR></DATA>';
         return false;
      } elseif (empty($this->pcSubject)) {
         $this->pcError = '<DATA><ERROR>Tema del email no definido</ERROR></DATA>';
         return false;
      } elseif (empty($this->pcMessage)) {
         $this->pcError = '<DATA><ERROR>Texto del email no definido</ERROR></DATA>';
         return false;
      }
      $lcHeaders = 'From: '.$this->pcFrom.'\r\n' .
                   'Reply-To: '.$this->pcFrom.'\r\n' .
                   'X-Mailer: PHP/' . phpversion();
      mail($this->pcForWho, $this->pcSubject, $this->pcMessage, $lcHeaders);
      return true;
   }
}

function fxValMonto($p_cValor) {
   if (is_int($p_cValor)) {
      if ($p_cValor <= 0) 
         return false;
      return true;
   }
   if (is_float($p_cValor)) {
      if ($p_cValor <= 0) 
         return false;
      return true;
   }
   return false;
}

class CCifrar extends CBase {
   public $pcCadena;

   public function __construct() {
      parent::__construct();
   }
   
   public function omCifrar($p_cCadena, $p_nTipo) {
      if (!($p_nTipo == 1 or $p_nTipo == 2)) {
         $this->pcError = '<DATA><ERROR>TIPO NO DEFINIDO</ERROR></DATA>';
         return false;
      } elseif (empty($p_cCadena)) {
         $this->pcError = '<DATA><ERROR>CADENA NO DEFINIDA</ERROR></DATA>';
         return false;
      }
      if ($p_nTipo == 1)
         $llOk = $this->mxCifrar($p_cCadena);
      else
         $llOk = $this->mxDescifrar($p_cCadena);
      return $llOk;
   }
   
   protected function mxCifrar($p_cCadena) {
      $lcClave = trim($p_cCadena);
      // Invertirlo
      $lcTmp = '';
      $i = strlen($lcClave) - 1;
      for ($j = $i; $j >= 0; $j--) {
          $lcTmp.= substr($lcClave, $j, 1);
      }
      // Cifrarlo
      $lcClave = '';
      $llFlag = true;
      for ($j = 0; $j <= $i; $j++) {
          $lcChar = substr($lcTmp, $j, 1);
          $lnChar = ord($lcChar);
          $lnChar = ($llFlag)? ($lnChar + 1): ($lnChar - 1);
          $llFlag = (!$llFlag);
          $lcClave.= dechex($lnChar);
      }
     $this->pcCadena = $lcClave;
     return true;
   }

   protected function mxDescifrar($p_cCadena) {
      $lcClave = trim($p_cCadena);
      $i = strlen($lcClave) - 1;
      // Descifrarlo
      for ($j = 0; $j < $i; $j+=2) {
          $lnChar = substr($lcClave, $j, 2);
          $lcTmp.= chr(hexdec($lnChar));
      }
     $lcClave = '';
      $i = strlen($lcTmp);
      $llFlag = (($i % 2) == 0)? true: false;
      for ($j = ($i - 1); $j >= 0; $j--) {
          $lcChar = substr($lcTmp, $j, 1);
          $lnChar = ord($lcChar);
          $lnChar = ($llFlag)? ($lnChar + 1): ($lnChar - 1);
          $llFlag = (!$llFlag);
          $lcClave.= chr($lnChar);
      }
     $this->pcCadena = $lcClave;
     return true;
   }
}

class CValAcceso extends CBase {
   public $pcEmail, $pcCodUsu, $pcNombre;

   public function __construct() {
      parent::__construct();
   }
   
   public function omValidar() {
      if (empty($this->pcEmail)) {
         $this->pcError = '<DATA><ERROR>EMAIL VACIO. INTENTE INICIAR SU SESION</ERROR></DATA>';
         return false;
      } elseif (empty($this->pcCodUsu)) {
         $this->pcError = '<DATA><ERROR>CODIGO DE USUARIO VACIO. INTENTE INICIAR SU SESION</ERROR></DATA>';
         return false;
      }
      $loSql = new CSql();
      $llOk = $loSql->omConnect();
      if (!$llOk) {
         $this->pcError = $loSql->pcError;
         return false;
      }
	  $lcCodPer = '00'.$this->pcCodUsu;
      $RS = $loSql->omExec("SELECT cCodPer, cEmail FROM S03MPER WHERE cCodPer = '$lcCodPer'");
      $laFila = $loSql->fetch($RS);
      $loSql->omDisconnect();
      if (empty($laFila[0])) {
         $this->pcError = '<DATA><ERROR>CODIGO DE USUARIO NO EXISTE. INTENTE INICIAR SU SESION</ERROR></DATA>';
         return false;
      } elseif (trim($laFila[1]) != trim($this->pcEmail)) {
         $this->pcError = '<DATA><ERROR>EMAIL NO CORRESPONDE A USUARIO. INTENTE INICIAR SU SESION</ERROR></DATA>';
         return false;
      }
      $_SESSION['gcCodUsu'] = $this->pcCodUsu;
      $_SESSION['gcNombre'] = $laFila[0];
      return true;
   }
}

function fxMoneda($p_cMoneda) {
   if ($p_cMoneda == '1') {
      return 'S/.';
   } elseif ($p_cMoneda == '2') {
      return 'US$';
   }
   return 'N/E';
}

function fxValAcceso($p_cOpcion) {
   $loSql = new CSql();
   $llOk = $loSql->omConnect();
   if (!$llOk) {
      return false;
   }
   $lcCodUsu = $_SESSION['gcCodUsu'];
   $RS = $loSql->omExec("SELECT cCodPer FROM V_S03TUSU WHERE cCodUsu = '$lcCodUsu'");
   $laFila = $loSql->fetch($RS);
   if (empty($laFila[0])) {
      $loSql->omDisconnect();
      return false;
   }
   $lcCodPer = $laFila[0];
   if ($p_cOpcion == 'Aut1110' or $p_cOpcion == 'Aut1120') {
       $lcSql = "SELECT cEstado FROM S03PSES WHERE cCodPer = '$lcCodPer' AND cTipo = 'A' AND cEstado = 'A'";
   }
   $RS = $loSql->omExec($lcSql);
   $loSql->omDisconnect();
   $laFila = $loSql->fetch($RS);
   if (empty($laFila[0])) {
      return false;
   }
   return true;
}

function fxFmtNroCom($p_cNroCom) {
   return substr($p_cNroCom, 0, 4).'-'.substr($p_cNroCom, 4);
}

class COcultar extends CBase {
   public $pcCadena;

   public function __construct() {
      parent::__construct();
   }
   
   // Oculta cadena
   public function omOcultar($p_cCadena) {
      $j = strlen($p_cCadena);
      $lnSeed = rand(1, 9);
      $lcCadena = chr($lnSeed + 48);
      $llFlag = true;
      for ($i = 0; $i < $j; $i++) {
          if ($llFlag) {
             $lcCadena.=dechex(ord(substr($p_cCadena, $i, 1)) + $lnSeed + $i);
          } else {
             $lcCadena.=dechex(ord(substr($p_cCadena, $i, 1)) - $lnSeed - $i);
          }
          $llFlag = !$llFlag;
      }
      return $lcCadena;
   }

   // Revela cadena
   public function omRevelar($p_cCadena) {
      $lcClave = '';
      $llFlag = true;
      $lnSeed = substr($p_cCadena, 0, 1);
      $lcCadena = substr($p_cCadena, 1);
      $j = strlen($lcCadena);
      $k = 0;
      for ($i = 0; $i < $j; $i+=2) {
          $lcHex = substr($lcCadena, $i, 2);
          $lnVal = hexdec($lcHex);
          if ($llFlag) {
             $lnVal = $lnVal - $lnSeed - $k;
          } else {
             $lnVal = $lnVal + $lnSeed + $k;
          }
          $lcClave.=chr($lnVal);
          $llFlag = !$llFlag;
          $k++;
      }
      return $lcClave;
   }
}

function fxReplicate($p_cChar, $p_nVeces) {
   $lcCadena = $p_cChar;
   for ($i = 1; $i < $p_nVeces; $i++) {
       $lcCadena.=$p_cChar;
   }
   return $lcCadena;
}

function fxValidarRuc($p_cNroRuc) {
   $lcNroRuc = trim($p_cNroRuc);
   if (strlen($lcNroRuc) != 11) {
      return false;
   } elseif (!preg_match("/^[[:digit:]]+$/", $lcNroRuc)) {
      return false;
   }
   $laFactor = array(5, 4, 3, 2, 7, 6, 5, 4, 3, 2);
   $lnSuma = 0;
   for ($i = 0; $i < 10; $i++) {
       $lnSuma += $laFactor[$i] * substr($lcNroRuc, $i, 1);
   }
   $lnResto = ($lnSuma % 11);
   $lnResto = 11 - $lnResto;
   $lnResto = ($lnResto == 10) ? 0 : $lnResto;
   if ($lnResto != substr($lcNroRuc, 10, 1)) {
      return false;
   }
   return true;
}

function array_sort($array, $on, $order=SORT_ASC) {
    $new_array = array();
    $sortable_array = array();
    if (count($array) > 0) {
        foreach ($array as $k => $v) {
            if (is_array($v)) {
                foreach ($v as $k2 => $v2) {
                    if ($k2 == $on) {
                        $sortable_array[$k] = $v2;
                    }
                }
            } else {
                $sortable_array[$k] = $v;
            }
        }

        switch ($order) {
            case SORT_ASC:
                asort($sortable_array);
            break;
            case SORT_DESC:
                arsort($sortable_array);
            break;
        }

        foreach ($sortable_array as $k => $v) {
            $new_array[$k] = $array[$k];
        }
    }

    return $new_array;
}

function fxReadPdf($p_oPdf) {
   $lcFile = './Bak/'.rand().'.pdf';
   $pdfcode = $p_oPdf->ezOutput(1);
   $fp = fopen($lcFile, 'wb');
   fwrite($fp, $pdfcode);
   fclose($fp);
   return $lcFile;
}

class EnLetras 
{ 
  var $Void = ""; 
  var $SP = " "; 
  var $Dot = "."; 
  var $Zero = "0"; 
  var $Neg = "Menos"; 
   
function ValorEnLetras($x, $Moneda )  
{ 
    $s=""; 
    $Ent=""; 
    $Frc=""; 
    $Signo=""; 
         
    if(floatVal($x) < 0) 
     $Signo = $this->Neg . " "; 
    else 
     $Signo = ""; 
     
    if(intval(number_format($x,2,'.','') )!=$x) //<- averiguar si tiene decimales 
      $s = number_format($x,2,'.',''); 
    else 
      $s = number_format($x,2,'.',''); 
        
    $Pto = strpos($s, $this->Dot); 
         
    if ($Pto === false) 
    { 
      $Ent = $s; 
      $Frc = $this->Void; 
    } 
    else 
    { 
      $Ent = substr($s, 0, $Pto ); 
      $Frc =  substr($s, $Pto+1); 
    } 

    if($Ent == $this->Zero || $Ent == $this->Void) 
       $s = "Cero "; 
    elseif( strlen($Ent) > 7) 
    { 
       $s = $this->SubValLetra(intval( substr($Ent, 0,  strlen($Ent) - 6))) .  
             "Millones " . $this->SubValLetra(intval(substr($Ent,-6, 6))); 
    } 
    else 
    { 
      $s = $this->SubValLetra(intval($Ent)); 
    } 

    if (substr($s,-9, 9) == "Millones " || substr($s,-7, 7) == "Millón ") 
       $s = $s . "de "; 


    if($Frc != $this->Void) 
    { 
       $s = $s . " CON " . $Frc. "/100 "; 
       //$s = $s . " " . $Frc . "/100"; 
    } 
    $s = $s . $Moneda; 
    //$letrass=$Signo . $s . " M.N."; 
    //return ($Signo . $s . " M.N."); 
    $letrass=$Signo . $s; 
    return ($Signo . $letrass); 
    
} 


function SubValLetra($numero)  
{ 
    $Ptr=""; 
    $n=0; 
    $i=0; 
    $x =""; 
    $Rtn =""; 
    $Tem =""; 

    $x = trim("$numero"); 
    $n = strlen($x); 

    $Tem = $this->Void; 
    $i = $n; 
     
    while( $i > 0) 
    { 
       $Tem = $this->Parte(intval(substr($x, $n - $i, 1).  
                           str_repeat($this->Zero, $i - 1 ))); 
       If( $Tem != "Cero" ) 
          $Rtn .= $Tem . $this->SP; 
       $i = $i - 1; 
    } 

     
    //--------------------- GoSub FiltroMil ------------------------------ 
    $Rtn=str_replace(" Mil Mil", " Un Mil", $Rtn ); 
    while(1) 
    { 
       $Ptr = strpos($Rtn, "Mil ");        
       If(!($Ptr===false)) 
       { 
          If(! (strpos($Rtn, "Mil ",$Ptr + 1) === false )) 
            $this->ReplaceStringFrom($Rtn, "Mil ", "", $Ptr); 
          Else 
           break; 
       } 
       else break; 
    } 

    //--------------------- GoSub FiltroCiento ------------------------------ 
    $Ptr = -1; 
    do{ 
       $Ptr = strpos($Rtn, "Cien ", $Ptr+1); 
       if(!($Ptr===false)) 
       { 
          $Tem = substr($Rtn, $Ptr + 5 ,1); 
          if( $Tem == "M" || $Tem == $this->Void) 
             ; 
          else           
             $this->ReplaceStringFrom($Rtn, "Cien", "Ciento", $Ptr); 
       } 
    }while(!($Ptr === false)); 

    //--------------------- FiltroEspeciales ------------------------------ 
    $Rtn=str_replace("Diez Un", "Once", $Rtn ); 
    $Rtn=str_replace("Diez Dos", "Doce", $Rtn ); 
    $Rtn=str_replace("Diez Tres", "Trece", $Rtn ); 
    $Rtn=str_replace("Diez Cuatro", "Catorce", $Rtn ); 
    $Rtn=str_replace("Diez Cinco", "Quince", $Rtn ); 
    $Rtn=str_replace("Diez Seis", "Dieciseis", $Rtn ); 
    $Rtn=str_replace("Diez Siete", "Diecisiete", $Rtn ); 
    $Rtn=str_replace("Diez Ocho", "Dieciocho", $Rtn ); 
    $Rtn=str_replace("Diez Nueve", "Diecinueve", $Rtn ); 
    $Rtn=str_replace("Veinte Un", "Veintiun", $Rtn ); 
    $Rtn=str_replace("Veinte Dos", "Veintidos", $Rtn ); 
    $Rtn=str_replace("Veinte Tres", "Veintitres", $Rtn ); 
    $Rtn=str_replace("Veinte Cuatro", "Veinticuatro", $Rtn ); 
    $Rtn=str_replace("Veinte Cinco", "Veinticinco", $Rtn ); 
    $Rtn=str_replace("Veinte Seis", "Veintiseís", $Rtn ); 
    $Rtn=str_replace("Veinte Siete", "Veintisiete", $Rtn ); 
    $Rtn=str_replace("Veinte Ocho", "Veintiocho", $Rtn ); 
    $Rtn=str_replace("Veinte Nueve", "Veintinueve", $Rtn ); 

    //--------------------- FiltroUn ------------------------------ 
    If(substr($Rtn,0,1) == "M") $Rtn = "Un " . $Rtn; 
    //--------------------- Adicionar Y ------------------------------ 
    for($i=65; $i<=88; $i++) 
    { 
      If($i != 77) 
         $Rtn=str_replace("a " . Chr($i), "* y " . Chr($i), $Rtn); 
    } 
    $Rtn=str_replace("*", "a" , $Rtn); 
    return($Rtn); 
} 


function ReplaceStringFrom(&$x, $OldWrd, $NewWrd, $Ptr) 
{ 
  $x = substr($x, 0, $Ptr)  . $NewWrd . substr($x, strlen($OldWrd) + $Ptr); 
} 


function Parte($x) 
{ 
    $Rtn=''; 
    $t=''; 
    $i=''; 
    Do 
    { 
      switch($x) 
      { 
         Case 0:  $t = "Cero";break; 
         Case 1:  $t = "Un";break; 
         Case 2:  $t = "Dos";break; 
         Case 3:  $t = "Tres";break; 
         Case 4:  $t = "Cuatro";break; 
         Case 5:  $t = "Cinco";break; 
         Case 6:  $t = "Seis";break; 
         Case 7:  $t = "Siete";break; 
         Case 8:  $t = "Ocho";break; 
         Case 9:  $t = "Nueve";break; 
         Case 10: $t = "Diez";break; 
         Case 20: $t = "Veinte";break; 
         Case 30: $t = "Treinta";break; 
         Case 40: $t = "Cuarenta";break; 
         Case 50: $t = "Cincuenta";break; 
         Case 60: $t = "Sesenta";break; 
         Case 70: $t = "Setenta";break; 
         Case 80: $t = "Ochenta";break; 
         Case 90: $t = "Noventa";break; 
         Case 100: $t = "Cien";break; 
         Case 200: $t = "Doscientos";break; 
         Case 300: $t = "Trescientos";break; 
         Case 400: $t = "Cuatrocientos";break; 
         Case 500: $t = "Quinientos";break; 
         Case 600: $t = "Seiscientos";break; 
         Case 700: $t = "Setecientos";break; 
         Case 800: $t = "Ochocientos";break; 
         Case 900: $t = "Novecientos";break; 
         Case 1000: $t = "Mil";break; 
         Case 1000000: $t = "Millón";break; 
      } 

      If($t == $this->Void) 
      { 
        $i = $i + 1; 
        $x = $x / 1000; 
        If($x== 0) $i = 0; 
      } 
      else 
         break; 
            
    }while($i != 0); 
    
    $Rtn = $t; 
    Switch($i) 
    { 
       Case 0: $t = $this->Void;break; 
       Case 1: $t = " Mil";break; 
       Case 2: $t = " Millones";break; 
       Case 3: $t = " Billones";break; 
    } 
    return($Rtn . $t); 
} 
}
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////


class CNumeroLetras { 
   protected $lcVacio, $lcNegati; 

   public function __construct() {
      //parent::__construct();
      $this->lcVacio = '';
      $this->lcNegati = 'Menos'; 
   }
  
   public function omNumeroLetras($p_nNumero, $p_cDesMon) { 
      $lcSigno = ''; 
      if (floatVal($p_nNumero) < 0) {
         $lcSigno = $this->lcNegati.' '; 
      }
      $lcNumero = number_format($p_nNumero, 2, '.', ''); 
      // Posicion del punto decimal
      $Pto = strpos($lcNumero, '.'); 
      if ($Pto === false) { 
         $lcEntero = $lcNumero; 
         $lcDecima = $this->lcVacio; 
      } else { 
         $lcEntero = substr($lcNumero, 0, $Pto); 
         $lcDecima =  substr($lcNumero, $Pto+1); 
      } 
      if ($lcEntero == '0' || $lcEntero == $this->lcVacio) {
         $lcNumero = 'Cero '; 
      } elseif (strlen($lcEntero) > 7) {
         $lcNumero = $this->SubValLetra(intval(substr($lcEntero, 0,  strlen($lcEntero) - 6)))."Millones " . $this->SubValLetra(intval(substr($lcEntero, -6, 6))); 
      } else { 
         $lcNumero = $this->SubValLetra(intval($lcEntero)); 
      } 
      if (substr($lcNumero,-9, 9) == "Millones " || substr($lcNumero,-7, 7) == "Millón ") {
         $lcNumero = $lcNumero . "de "; 
      }
      if ($lcDecima != $this->lcVacio) { 
       $lcNumero = $lcNumero . " CON " . $lcDecima. "/100 "; 
      } 
      $lcNumero = $lcNumero . $p_cDesMon; 
      $letrass=$lcSigno . $lcNumero; 
      return ($lcSigno . $letrass); 
   } 

   protected function SubValLetra($numero) { 
      $Ptr=""; 
      $n=0; 
      $i=0; 
      $x =""; 
      $Rtn =""; 
      $Tem =""; 
      $x = trim("$numero"); 
      $n = strlen($x); 
      $Tem = $this->lcVacio; 
      $i = $n; 
      while($i > 0) { 
         $Tem = $this->Parte(intval(substr($x, $n - $i, 1).str_repeat('0', $i - 1))); 
         if ($Tem != "Cero") {
            $Rtn .= $Tem . ' '; 
         }
         $i = $i - 1; 
      } 
      //--------------------- GoSub FiltroMil ------------------------------ 
      $Rtn = str_replace(" Mil Mil", " Un Mil", $Rtn); 
      while (1) { 
         $Ptr = strpos($Rtn, "Mil ");        
         if (!($Ptr===false)) { 
            if (! (strpos($Rtn, "Mil ",$Ptr + 1) === false)) {
               $this->ReplaceStringFrom($Rtn, "Mil ", "", $Ptr); 
            } else {
               break; 
            }
         } else {
            break; 
         }
      } 
      //--------------------- GoSub FiltroCiento ------------------------------ 
      $Ptr = -1; 
      do { 
         $Ptr = strpos($Rtn, "Cien ", $Ptr+1); 
         if (!($Ptr===false)) { 
            $Tem = substr($Rtn, $Ptr + 5 ,1); 
            if ($Tem == "M" || $Tem == $this->lcVacio) 
             ; 
            else           
               $this->ReplaceStringFrom($Rtn, "Cien", "Ciento", $Ptr); 
         } 
      } while(!($Ptr === false)); 
      //--------------------- FiltroEspeciales ------------------------------ 
      $Rtn=str_replace("Diez Un", "Once", $Rtn); 
      $Rtn=str_replace("Diez Dos", "Doce", $Rtn); 
      $Rtn=str_replace("Diez Tres", "Trece", $Rtn); 
      $Rtn=str_replace("Diez Cuatro", "Catorce", $Rtn); 
      $Rtn=str_replace("Diez Cinco", "Quince", $Rtn); 
      $Rtn=str_replace("Diez Seis", "Dieciseis", $Rtn); 
      $Rtn=str_replace("Diez Siete", "Diecisiete", $Rtn); 
      $Rtn=str_replace("Diez Ocho", "Dieciocho", $Rtn); 
      $Rtn=str_replace("Diez Nueve", "Diecinueve", $Rtn); 
      $Rtn=str_replace("Veinte Un", "Veintiun", $Rtn); 
      $Rtn=str_replace("Veinte Dos", "Veintidos", $Rtn); 
      $Rtn=str_replace("Veinte Tres", "Veintitres", $Rtn); 
      $Rtn=str_replace("Veinte Cuatro", "Veinticuatro", $Rtn); 
      $Rtn=str_replace("Veinte Cinco", "Veinticinco", $Rtn); 
      $Rtn=str_replace("Veinte Seis", "Veintiseís", $Rtn); 
      $Rtn=str_replace("Veinte Siete", "Veintisiete", $Rtn); 
      $Rtn=str_replace("Veinte Ocho", "Veintiocho", $Rtn); 
      $Rtn=str_replace("Veinte Nueve", "Veintinueve", $Rtn); 
      //--------------------- FiltroUn ------------------------------ 
      if (substr($Rtn,0,1) == "M") {
         $Rtn = "Un " . $Rtn; 
      }
      //--------------------- Adicionar Y ------------------------------ 
      for ($i=65; $i<=88; $i++) { 
          if ($i != 77) {
             $Rtn=str_replace("a " . Chr($i), "* y " . Chr($i), $Rtn); 
          }
      } 
      $Rtn=str_replace("*", "a" , $Rtn); 
      return($Rtn); 
   } 


   protected function ReplaceStringFrom(&$x, $OldWrd, $NewWrd, $Ptr) { 
      $x = substr($x, 0, $Ptr)  . $NewWrd . substr($x, strlen($OldWrd) + $Ptr); 
   } 

   protected function Parte($x) { 
      $Rtn=''; 
      $t=''; 
      $i=''; 
      Do { 
         switch($x) { 
            Case 0:  $t = "Cero";break; 
            Case 1:  $t = "Un";break; 
            Case 2:  $t = "Dos";break; 
            Case 3:  $t = "Tres";break; 
            Case 4:  $t = "Cuatro";break; 
            Case 5:  $t = "Cinco";break; 
            Case 6:  $t = "Seis";break; 
            Case 7:  $t = "Siete";break; 
            Case 8:  $t = "Ocho";break; 
            Case 9:  $t = "Nueve";break; 
            Case 10: $t = "Diez";break; 
            Case 20: $t = "Veinte";break; 
            Case 30: $t = "Treinta";break; 
            Case 40: $t = "Cuarenta";break; 
            Case 50: $t = "Cincuenta";break; 
            Case 60: $t = "Sesenta";break; 
            Case 70: $t = "Setenta";break; 
            Case 80: $t = "Ochenta";break; 
            Case 90: $t = "Noventa";break; 
            Case 100: $t = "Cien";break; 
            Case 200: $t = "Doscientos";break; 
            Case 300: $t = "Trescientos";break; 
            Case 400: $t = "Cuatrocientos";break; 
            Case 500: $t = "Quinientos";break; 
            Case 600: $t = "Seiscientos";break; 
            Case 700: $t = "Setecientos";break; 
            Case 800: $t = "Ochocientos";break; 
            Case 900: $t = "Novecientos";break; 
            Case 1000: $t = "Mil";break; 
            Case 1000000: $t = "Millón";break; 
         } 
         if ($t == $this->lcVacio) { 
            $i = $i + 1; 
            $x = $x / 1000; 
            if ($x== 0) {
               $i = 0; 
            }
         } else {
            break; 
         }
            
      } while($i != 0); 
      $Rtn = $t; 
      Switch($i) { 
         Case 0: $t = $this->lcVacio;break; 
         Case 1: $t = " Mil";break; 
         Case 2: $t = " Millones";break; 
         Case 3: $t = " Billones";break; 
      } 
      return($Rtn.$t); 
   } 
} 

function objectToArray($p_oObject) {
   if (is_object($p_oObject)) {
      $p_oObject = get_object_vars($p_oObject);
   }
   if (is_array($p_oObject)) {
      return array_map(__FUNCTION__, $p_oObject);
   } else {
      return $p_oObject;
   }       
}

function f_DigControl($p_cCodigo) {
   $i = strlen($p_cCodigo);
   if ($i == 0) {
      return '';
   }
   $laTmp = array(5, 23, 19, 17, 13, 11, 7, 5, 3);
   $lnSuma = 0;
   for ($i = 0; $i < 9; $i++) {
       echo '*';
       $lnSuma += $laTmp[$i] * (int)substr($p_cCodigo, $i, 1);
   }
   $j = $lnSuma % 11;
   $j = ($j == 10) ? 0 : $j;
   return $p_cCodigo.(string)$j;
}
/*
function fxValCadena($p_cNombre) {
   for ($i = 0; $i < strlen($p_cNombre), $i++) {
       $c = substr($p_cNombre, $i, 1);
       $j = ord($c);
       if ($j >= 65 and $j <= 90) or ($j >= 97 and $j <= 122) or ($j >= 48 and $j <= 57) or $j = 32 {
       }
   }
}*/
?>
