<?php /* Smarty version Smarty-3.1.8, created on 2016-07-19 21:21:29
         compiled from "src\Template\Pages\Mnu0000.tpl" */ ?>
<?php /*%%SmartyHeaderCode:30243578e99d98b5e71-86974212%%*/if(!defined('SMARTY_DIR')) exit('no direct access allowed');
$_valid = $_smarty_tpl->decodeProperties(array (
  'file_dependency' => 
  array (
    'fb6b9b494c773aa20402107a5039d96d7ba81d2c' => 
    array (
      0 => 'src\\Template\\Pages\\Mnu0000.tpl',
      1 => 1468963225,
      2 => 'file',
    ),
  ),
  'nocache_hash' => '30243578e99d98b5e71-86974212',
  'function' => 
  array (
  ),
  'variables' => 
  array (
    'scNivel' => 0,
    'scCodigo' => 0,
    'scNombre' => 0,
  ),
  'has_nocache_code' => false,
  'version' => 'Smarty-3.1.8',
  'unifunc' => 'content_578e99d9cb6941_07037305',
),false); /*/%%SmartyHeaderCode%%*/?>
<?php if ($_valid && !is_callable('content_578e99d9cb6941_07037305')) {function content_578e99d9cb6941_07037305($_smarty_tpl) {?><meta HTTP-EQUIV="Content-Type" content="text/html; charset=utf-8" />
<html>
<head>
<title>Rendicion de Cuentas y Caja Chica</title>
   <link href="CSS/Sixavi.css" media="screen" rel="stylesheet" type="text/css" />
   <script language="javascript" type="text/javascript" src="CSS/funMarcado.js"></script>
</head>
<body>
   <span id="che" style="display: none;visibility: hidden;"><?php echo $_smarty_tpl->tpl_vars['scNivel']->value;?>
</span>
   <div class="wrapper">
   <div id="MH">
      <ul>
      <li style="margin-left: 50px;"><h1>Módulo de Gestión de Rendicion de Cuentas y Caja Chica</h1></li>
      <li style="float:right;margin-right: 100px;"><a onclick="self.location = 'index.php'"> Cerrar Sesión</a></li>
      </ul>
   </div>
   <font color = blue size=1><?php echo $_smarty_tpl->tpl_vars['scCodigo']->value;?>
 - <?php echo $_smarty_tpl->tpl_vars['scNombre']->value;?>
</font>
   <div id="MT">
      <ol class="tree">
         <li>
            <label for="folder1">Caja Chica</label><input type="checkbox" id="folder1" onClick="desmarcar('folder1')"/>
            <ol>
            <li class="file"><a href="src/Controller/Caja1000.php"> Apertura de Caja Chica</a></li>
            <li class="file"><a href="Caja1010.php"> Ingreso de Caja Chica</a></li>
            </ol>
            </li>
            <li>
            <label for="folder2">Rendicion de Cuentas</label><input type="checkbox" id="folder2" onClick="desmarcar('folder2')"/>
            <ol>
            <li class="file"><a href="Caj1000.php"> Apertura de Cuenta</a></li>
            <li class="file"><a href="Caj1010.php"> Ingreso de Rendicion de Cuenta</a></li>
            </ol>
            </li>
            <li>
            <label for="folder3">Asignar Cuentas Contables</label><input type="checkbox" id="folder3" onClick="desmarcar('folder3')"/>
            <ol>
            <li class="file"><a href="Caj1000.php"> Asignar Cuentas Contables</a></li>
            </ol>
            </li>
            <li>
            <label for="folder4">Mantenimiento</label><input type="checkbox" id="folder4" onClick="desmarcar('folder4')"/>
            <ol>
            <li class="file"><a href="Caj1000.php"> Registro de Caja Chica</a></li>
            </ol>
            </li>
        </ol>
   </div>
   <div id="topnavbar"></div>
   <div id="navigation">
   <div id="navcontainer">  
   </div>
   </div>
   <div id="content">
   </div>
   <div id="footer">
   </div>
   </div>   
</body>
</html>
<?php }} ?>