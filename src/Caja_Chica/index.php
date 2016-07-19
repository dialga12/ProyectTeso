<?php
   require_once 'src/Libs/Smarty.class.php';
   session_start();
   //unset($_SESSION["gcNombre"]);
   //unset($_SESSION["gcCodUsu"]);
   //unset($_SESSION["gcTipo"]);
   $_SESSION["gcNombre"] = 'PACHECO/TORRES,MOISES';
   $_SESSION["gcCodUsu"] = 'EPIS';
   $_SESSION["gdFecSis"] = '2016-01-01';
   $loSmarty = new Smarty;
   $loSmarty->assign('scNombre', $_SESSION["gcNombre"]);
   $loSmarty->assign('scCodigo', $_SESSION["gcCodUsu"]);
   $loSmarty->display('src/Template/Pages/Mnu0000.tpl');
?> 
