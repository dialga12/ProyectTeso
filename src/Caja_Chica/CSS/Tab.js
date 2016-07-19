// Declaro un array en el cual los indices son los ID's de los DIVS que funcionan como pestaña y los valores son los identificadores de las secciones a cargar
//var tabsId = new Array();
//tabsId['tab1'] = 'seccion1';
//tabsId['tab2'] = 'seccion2';
// Declaro el ID del DIV que actuará como contenedor de los datos recibidos
//var contenedor='tabContenido';

/*
function nuevoAjax()
{ 
   // Crea el objeto AJAX. Esta funcion es generica para cualquier utilidad de este tipo, por
   //lo que se puede copiar tal como esta aqui
   var xmlhttp=false; 
   try 
   { 
      // Creacion del objeto AJAX para navegadores no IE
      xmlhttp=new ActiveXObject("Msxml2.XMLHTTP"); 
   }
   catch(e)
   { 
      try
      { 
         // Creacion del objeto AJAX para IE 
         xmlhttp=new ActiveXObject("Microsoft.XMLHTTP"); 
      } 
      catch(E) { xmlhttp=false; }
   }
   if (!xmlhttp && typeof XMLHttpRequest!='undefined') { xmlhttp=new XMLHttpRequest(); } 

   return xmlhttp; 
}*/

/*
function mouseSobre()
{
   // Si el evento no se produjo en la pestaña seleccionada...
   if(this.className!='tabOn')
   {
      // Cambio el color de fondo de la pestaña
      this.className='tabHover';
   }
}*/

/*
function mouseFuera()
{
   // Si el evento no se produjo en la pestaña seleccionada...
   if(this.className!='tabOn')
   {
      // Cambio el color de fondo de la pestaña
      this.className='tabOff';
   }
}*/

/*
onload=function()
{
   for(key in tabsId)
   {
      // Voy obteniendo los ID's de los elementos declarados en el array que representan a las pestañas
      elemento=document.getElementById(key);
      // Asigno que al hacer click en una pestaña se llame a la funcion cargaContenido
      elemento.onclick=cargaContenido;
      // El cambio de estilo es en 2 funciones diferentes debido a la incompatibilidad del string de backgroundColor devuelto por Mozilla e IE.
      // Se podría pasar de rgb(xxx, xxx, xxx) a formato #xxxxxx pero complicaría innecesariamente el ejemplo 
      elemento.onmouseover=mouseSobre;
      elemento.onmouseout=mouseFuera;
   }
   // Obtengo la capa contenedora de datos
   tabContenedor=document.getElementById(contenedor);
    var a = document.getElementById('A1');
    tabContenedor.innerHTML = a.innerHTML;
    
} */
