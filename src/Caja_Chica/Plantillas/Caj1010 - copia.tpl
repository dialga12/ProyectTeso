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
   <script>
      function f_NuevoCampo() {
         /*var str = document.getElementById("pcNroDni").value;
         if (str.length != 8 ){
             alert("Numero de DNI invalido");
             return;
         }*/
         //comprobar q no se repita
         //var str = document.getElementById("pcNroDni").value;
         var xmlhttp = new XMLHttpRequest();
         xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               document.getElementById("divData").innerHTML = xmlhttp.responseText;
               var d = document.getElementById("wait1");
               d.innerHTML = '';
               //document.getElementById("pcNroDni").value='';
            } else {
               var d = document.getElementById("wait1");
               d.innerHTML = '<img src="CSS/Cargando.gif" height="12" width="25">';
            }
         }  
         xmlhttp.open("GET", "PAjax.php?Id=100", true);
         xmlhttp.send();
      }

      function f_EliminarCampo(form) {
         var i = getSelectedButton(form.pcCheck);
         var str=form.pcCheck[i].value;
         var xmlhttp = new XMLHttpRequest();
         xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               document.getElementById("divData").innerHTML = xmlhttp.responseText;
               var d = document.getElementById("wait1");
               d.innerHTML = '';
            } else {
               var d = document.getElementById("wait1");
               d.innerHTML = '<img src="CSS/Cargando.gif" height="12" width="25">';
            }
         }  
         xmlhttp.open("GET", "PAjax.php?Id=012&str="+str, true);
         xmlhttp.send();
      }
   </script>
   <title>Rendicion de Cuentas</title>
</head>
<body onload="f_Init({$scBehavior})">
<form action="Caj1010.php#no-back" method="post">
   <div class="wrapper">
   <div id="MH">
      <ul>
      <li style="margin-left: 50px;"><h1>Rendicion de Cuentas</h1></li>
      <li style="float:right;margin-right: 100px;"><a onclick="self.location='index.php'">Cerrar Sesión</a></li>
      </ul>
   </div>
   <div id="topnavbar"></div>
   <div id="navigation">
   <div id="navcontainer">
   {if $scBehavior eq "0"}
      <div style="overflow:scroll;height:500px;width:800px;overflow:auto;border: 1px">
      <table border=5 style="font-size:10px">
         <th bgcolor="#F29818" width="200">Razon Social</th>
         <th bgcolor="#F29818" width="150">Factura</th>
         <th bgcolor="#F29818" width="200">Fecha</th>
         <th bgcolor="#F29818" width="200">Glosa</th>
         <th bgcolor="#F29818" width="100">Tipo de Documento</th>
         <th bgcolor="#F29818" width="50">Monto Imponible</th>
         <th bgcolor="#F29818" width="50">Monto IGV</th>
         <th bgcolor="#F29818" width="50">Monto Renta</th>
         <th bgcolor="#F29818" width="50">Monto Inferido</th>
         <th bgcolor="#F29818" width="100">Moneda</th>
         <th bgcolor="#F29818" align="center"><img src="CSS/Check.jpg" width="25" height="25"></th>
         </table>
            <p><span id="divData"></span></p>
         <table>
      </table>
      </div>
      <table>
         <tr>
         <td><input type="button" class="boton" name="Boton1" value="Nuevo" onclick="f_NuevoCampo();"/></td>
         <td><input type="button" class="boton" name="Boton1" value="Eliminar" onclick="f_EliminarCampo(this.form);"/></td>
         <td><input type="submit" name="Boton1" value="Grabar" /></td>
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
         {foreach from = null item = i}
            <tr>
            <td>{$i['1']}</td>
            <td>{$i['2']}</td>
            <td>{$i['3']}</td>
            <td>{$i['4']}</td>
            <td><input type="radio" name="pcCodIfi" value="{$i['0']}"/></td>
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
