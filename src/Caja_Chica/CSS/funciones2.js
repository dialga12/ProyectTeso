var cnx;

function myFunction() {
   var lcNroRuc = document.getElementById('pcNroRuc').value;
   if (lcNroRuc != 0) {
      cnx = crearXMLHttpRequest();
      cnx.onreadystatechange = procesarEventos;
      cnx.open('GET', 'Clases/PProveedores.php?Id=' + lcNroRuc, true);
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
      var tmp = cnx.responseText;
      tmp = tmp.replace('?','');
	  var json = eval('('+tmp+')');
      var result = json.CNOMPRV;
      select2.value = result;
   } else {
      var d = document.getElementById('espera');
      d.innerHTML = '<img src="CSS/loading.gif" height="25" width="25">';
   }
}
