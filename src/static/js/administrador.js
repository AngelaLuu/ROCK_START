document.addEventListener('DOMContentLoaded', function () {
    // Obtiene la referencia a la imagen por su id
var iconoAdmin = document.getElementById("iconoAdmin");

// Agrega un evento de clic a la imagen
iconoAdmin.addEventListener("click", function() {
  // Redirecciona a la página deseada cuando se hace clic en la imagen
  window.location.href = "/login";
});

});
