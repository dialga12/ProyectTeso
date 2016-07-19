jQuery(function($){
      $.datepicker.regional['es'] = {
            closeText: 'Cerrar',
            prevText: '&#x3c;Ant',
            nextText: 'Sig&#x3e;',
            currentText: 'Hoy',
            monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
            'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
            monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun',
            'Jul','Ago','Sep','Oct','Nov','Dic'],
            dayNames: ['Domingo','Lunes','Martes','Mi&eacute;rcoles','Jueves','Viernes','S&aacute;bado'],
            dayNamesShort: ['Dom','Lun','Mar','Mi&eacute;','Juv','Vie','S&aacute;b'],
            dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
            weekHeader: 'Sm',
            dateFormat: 'yy-mm-dd',
			//dateFormat: 'dd/mm/yy',
            firstDay: 1,
            isRTL: false,
            showMonthAfterYear: false,
            yearSuffix: ''};
      $.datepicker.setDefaults($.datepicker.regional['es']);
}); 

	  jQuery(document).ready(function() {
        jQuery('.input_num').keypress(function(tecla) {
           if(tecla.charCode < 48 || tecla.charCode > 57) return false;
              });
        });

      //Funciones comunes a todos los problemas
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
