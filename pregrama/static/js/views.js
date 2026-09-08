// ==========================================
// VISTA ACTUAL
// ==========================================

let vistaActual = "inicio";


// ==========================================
// CAMBIAR VISTA
// ==========================================

function cambiarVista(idVista) {

    const vistas = document.querySelectorAll(".vista");
    const vista = document.getElementById(idVista);

    if (!vista) return;

    vistas.forEach(vista => {

        vista.style.display = "none";

    });

    vista.style.display = "block";

    vistaActual = idVista;

}   
function mostrarLineal() {

    cambiarVista("vistaLineal");
    activarMenu("menuLineal");

}
function mostrarExacta() {

    cambiarVista("vistaExacta");
    activarMenu("menuExacta");

}
function mostrarNoExacta() {

    cambiarVista("vistaNoExacta");
    activarMenu("menuNoExacta");

}
function mostrarCarbono() {

    cambiarVista("vistaCarbono");
    activarMenu("menuCarbono");

}
function mostrarSeparable() {

    cambiarVista("vistaSeparable");
    activarMenu("menuSeparable");

}
function mostrarInicio() {

    cambiarVista("inicio");

}
function abrirSidebar() {

    document

        .getElementById("sidebar")

        .classList

        .add("activo");

}


function cerrarSidebar() {

    document

        .getElementById("sidebar")

        .classList

        .remove("activo");

}
function toggleSidebar() {

    document

        .getElementById("sidebar")

        .classList

        .toggle("activo");


}
function activarMenu(id) {

    const menus = document.querySelectorAll(".menu-item");

    menus.forEach(menu => {

        menu.classList.remove("active");

    });

    const menu = document.getElementById(id);

    if (menu) menu.classList.add("active");

}
function cargarVistaEjercicio(numero) {

    cargarEjercicio(numero);

}
function llenarFormulario(ejercicio) {

    const camposPorTipo = {
        lineal: ["P", "Q", "variable", "x0", "y0"],
        exacta: ["MExacta", "NExacta"],
        no_exacta: ["MNoExacta", "NNoExacta"],
        carbono14: ["vida_media", "cantidad_inicial", "cantidad_final"],
        separable: ["fSeparable", "gSeparable", "x0Separable", "y0Separable"]
    };
    const campos = camposPorTipo[ejercicio.tipo] || [];

    campos.forEach(campo => {
        const elemento = document.getElementById(campo);
        if (elemento && ejercicio[campo] !== undefined) elemento.value = ejercicio[campo];
    });

    const mostrar = {
        lineal: mostrarLineal,
        exacta: mostrarExacta,
        no_exacta: mostrarNoExacta,
        carbono14: mostrarCarbono,
        separable: mostrarSeparable
    }[ejercicio.tipo];

    if (mostrar) mostrar();
}
function limpiarTodo() {

    document

        .querySelectorAll("form")

        .forEach(form => {

            form.reset();

        });

    limpiarResultado();

}
function iniciarVistas() {

    cambiarVista("inicio");

}
