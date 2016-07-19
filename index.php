<?php
 /** CakePHP(tm) : Rapid Development Framework (http://cakephp.org)
 * Copyright (c) Cake Software Foundation, Inc. (http://cakefoundation.org)
 *
 * Licensed under The MIT License
 * For full copyright and license information, please see the LICENSE.txt
 * Redistributions of files must retain the above copyright notice.
 *
 * @copyright     Copyright (c) Cake Software Foundation, Inc. (http://cakefoundation.org)
 * @link          http://cakephp.org CakePHP(tm) Project
 * @since         0.10.0
 * @license       http://www.opensource.org/licenses/mit-license.php MIT License
 *

require 'webroot' . DIRECTORY_SEPARATOR . 'index.php'; */

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
