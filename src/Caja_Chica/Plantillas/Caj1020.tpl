<!DOCTYPE html>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<html>
<head>
   <link rel="stylesheet" href="CSS/jquery-ui-1.11.0/jquery-ui.css">
   <script type="text/javascript" src="CSS/jquery-1.10.2.min.js"></script> 
   <script type="text/javascript" src="CSS/jquery-ui-1.11.0/jquery-ui.js"></script>
   <script type="text/javascript" src="CSS/jquery.validate.js"></script>
   <script type="text/javascript" src="CSS/jquery.numeric.js"></script>
   <script type="text/javascript" src="CSS/Libgen.js"></script>
   <link href="CSS/Sixavi.css" media="screen" rel="stylesheet" type="text/css" />
   <title>Contabilidad</title>
</head>
<body onload="f_Init({$scBehavior})">
<form action="Caj1010.php#no-back" method="post">
   <div class="wrapper">
   <div id="MH">
      <ul>
      <li style="margin-left: 50px;"><h1>Contabilidad</h1></li>
      <li style="float:right;margin-right: 100px;"><a onclick="self.location='index.php'">Cerrar Sesión</a></li>
      </ul>
   </div>
   <div id="topnavbar"></div>
   <div id="navigation">
   <div id="navcontainer">
   {if $scBehavior eq "0"}
      <div style="overflow:scroll;height:500px;width:800px;overflow:auto;border: 1px">
      <table border=5 style="font-size:10px">
         <th bgcolor="#F29818" width="200">Contabilidad</th>
         <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
         {foreach from = null item = i}
            <tr>
            <td>{$i['1']}</td>
            <td><input type="radio" name="pcCodCon" value="{$i['0']}"/></td>
            </tr>
         {/foreach}
      </table>
      </div>
      <table>
         <tr>
         <td><input type="submit" name="Boton1" value="Editar" /></td>
         <td><input type="submit" name="Boton1" value="Salir" /></td>
         </tr>
      </table>
   {elseif $scBehavior eq "1"}
      <div style="overflow:scroll;height:500px;width:800px;overflow:auto;border: 1px">
      <table border=5 style="font-size:10px">
         <th bgcolor="#F29818" width="200">Proveedor</th>
         <th bgcolor="#F29818" width="50">Factura</th>
         <th bgcolor="#F29818" width="50">Glosa</th>
         <th bgcolor="#F29818" width="50">Monto</th>
         <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
         <th bgcolor="#F29818" width="50">C. Contable</th>
         {foreach from = null item = i}
            <tr>
            <td>{$i['1']}</td>
            <td>{$i['2']}</td>
            <td>{$i['3']}</td>
            <td>{$i['4']}</td>
            <td><input type="radio" name="pcCodCon" value="{$i['0']}"/></td>
            </tr>
         {/foreach}
      </table>
      </div>
      <table>
         <tr>
         <td><input type="submit" name="Boton1" value="Nuevo" /></td>
         <td><input type="submit" name="Boton1" value="Eliminar" /></td>
         <td><input type="submit" name="Boton1" value="Grabar" /></td>
         <td><input type="submit" name="Boton1" value="Salir" /></td>
         </tr>
      </table>
   {/if}
   </div>
   </div>
   <div id="content"></div>
   <div id="footer"></div>
   </div>
</form>
</body>
</html>
