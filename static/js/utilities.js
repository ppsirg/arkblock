function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function ToastMessage(type, message) {
  // muestra un mensaje emergente al que se le puede seleccionar un tipo de mensaje
  const msg_types = {
    online: {
      backgroundColor: "linear-gradient(to right, #33ee77, #22ff88)"
    },
    offline: {
      backgroundColor: "linear-gradient(to right, #555555, #777777)"
    },
    new_message: {
      backgroundColor: "linear-gradient(to right, #a25983, #a25983)"
    },
    deleted_message: {
      backgroundColor: "linear-gradient(to right, #dd5533, #ff4444)"
    },
  };
  Toastify({
    text: message,
    duration: 3000,
    // destination: "https://github.com/apvarun/toastify-js",
    // newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    // position: 'left', // `left`, `center` or `right`
    backgroundColor: msg_types[type].backgroundColor,
    stopOnFocus: true, // Prevents dismissing of toast on hover
    onClick: function() {} // Callback after click
  }).showToast();
}

function is_online() {
  if (navigator.onLine) {
    // detectar si tenemos conexion
    console.log('going online');
    ToastMessage('online', 'Conexión a internet establecida');
    return true;
  } else {
    // hacer un ping por conexion
    return fetch('/ping')
      .then(resp => {
        // tenemos conexion, pero el navegador no soporta
        // navigator.onLine
        console.log('is online but doesnt have navigator support');
        ToastMessage('online', 'Conexión a internet establecida');
        return true;
      })
      .catch(err => {
        // no tenemos conexion
        console.log('going offline');
        ToastMessage('offline', 'Conexión a internet interrumpida');
        return false;
      })
  }
}