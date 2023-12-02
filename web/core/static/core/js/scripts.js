// CODIGO CARRUSEL
$(document).ready(function() {
    // Inicia el carrusel
    $('#miCarrusel').carousel();

    // Configura la velocidad de cambio (en milisegundos)
    $('#miCarrusel').carousel({
        interval: 1000 // Cambiar cada 2 segundos
    });
});
// FIN

//TESTIMONIOS.HTML CARRUSEL

$(document).ready(function() {
    // Inicia el carrusel de testimonios
    $('#testimoniosCarousel').carousel();

    // Configura la velocidad de cambio para el carrusel de testimonios (en milisegundos)
    $('#testimoniosCarousel').carousel({
        interval: 8000 // Cambiar cada 3 segundos
    });
});