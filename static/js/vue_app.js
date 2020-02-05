window.addEventListener("load", function(event) {

  // create main vue app
  var vue_app = new Vue({
    el: '#vue_app', //elemento en el que se monta la app de vue
    delimiters: ['[[', ']]'], //para que en el template se use [[ ]] en vez de {{ }} que es de django
  })

  function update_backend_availability() {
    // cuando hay cambio de conectividad, avisar a la app del mismo
    vue_app.backend_available = is_online()
  }

  // agregar soporte offline para que la app sepa si hay conexion
  window.addEventListener('online', update_backend_availability);
  window.addEventListener('offline', update_backend_availability);

});
