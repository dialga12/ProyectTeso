var cnx;

function myFunction() {
   var lcNroRuc = document.getElementById('pcNroRuc').value;
   if (lcNroRuc != 0) {
      cnx = crearXMLHttpRequest();
      cnx.onreadystatechange = procesarEventos;
      cnx.open('GET', 'Clases/CAjaxProveedores.php?Id=' + lcNroRuc, true);
      cnx.send(null);
   } else {
      var select2 = document.getElementById('pcNomPrv');
      select2.options.length = 0;
   }
}

function procesarEventos() {
   if (cnx.readyState == 4) {
      var d = document.getElementById('espera');
      d.innerHTML  =  '';
      var select2 = document.getElementById('pcNomPrv');
      var json = eval('('+cnx.responseText+')');
      var result = json.CNOMPRV;
      select2.value = result;
   } else {
      var d = document.getElementById('espera');
      d.innerHTML = '<img src="CSS/loading.gif" height="25" width="25">';
   }
}

//***************************************
//Funciones comunes a todos los problemas
//***************************************
function addEvent(elemento, nomevento, funcion, captura) {
   if (elemento.attachEvent) {
      elemento.attachEvent('on'+nomevento, funcion);
      return true;
   } else if (elemento.addEventListener) {
      elemento.addEventListener(nomevento, funcion, captura);
      return true;
   } else
      return false;
}

function crearXMLHttpRequest() {
   var xmlHttp = null;
   if (window.ActiveXObject) 
      xmlHttp  =  new ActiveXObject("Microsoft.XMLHTTP");
   else if (window.XMLHttpRequest) 
      xmlHttp  =  new XMLHttpRequest();
   return xmlHttp;
}
