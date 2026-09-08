// ==========================================
// INICIALIZAR APLICACIÓN
// ==========================================

document.addEventListener("DOMContentLoaded", iniciarAplicacion);


// ==========================================
// FUNCIÓN PRINCIPAL
// ==========================================

function registrarEventos() {

    // =============================
    // ECUACIÓN LINEAL
    // =============================

    const btnLineal = document.getElementById("btnResolverLineal");

    if (btnLineal) {

        btnLineal.addEventListener(

            "click",

            resolverLineal

        );

    }

    // =============================
    // ECUACIÓN EXACTA
    // =============================

    const btnExacta = document.getElementById("btnResolverExacta");

    if (btnExacta) {

        btnExacta.addEventListener(

            "click",

            resolverExacta

        );

    }

    // =============================
    // ECUACIÓN NO EXACTA
    // =============================

    const btnNoExacta = document.getElementById("btnResolverNoExacta");

    if (btnNoExacta) {

        btnNoExacta.addEventListener(

            "click",

            resolverNoExacta

        );

    }

    // =============================
    // CARBONO 14
    // =============================

    const btnCarbono = document.getElementById("btnResolverCarbono");

    if (btnCarbono) {

        btnCarbono.addEventListener(

            "click",

            resolverCarbono

        );

    }

    const btnSeparable = document.getElementById("btnResolverSeparable");

    if (btnSeparable) {

        btnSeparable.addEventListener(

            "click",

            resolverSeparable

        );

    }

}
function registrarMenu() {

    const menuLineal = document.getElementById("menuLineal");

    if (menuLineal) {

        menuLineal.onclick = mostrarLineal;

    }

    const menuExacta = document.getElementById("menuExacta");

    if (menuExacta) {

        menuExacta.onclick = mostrarExacta;

    }

    const menuNoExacta = document.getElementById("menuNoExacta");

    if (menuNoExacta) {

        menuNoExacta.onclick = mostrarNoExacta;

    }

    const menuCarbono = document.getElementById("menuCarbono");

    if (menuCarbono) {

        menuCarbono.onclick = mostrarCarbono;

    }

    const menuSeparable = document.getElementById("menuSeparable");

    if (menuSeparable) {

        menuSeparable.onclick = mostrarSeparable;

    }

}
function registrarSidebar() {

    const boton = document.getElementById("btnSidebar");
    const botonMovil = document.getElementById("toggle-sidebar");

    if (!boton && !botonMovil) return;

    (boton || botonMovil).addEventListener(

        "click",

        toggleSidebar

    );

}
function registrarEjercicios() {

    const botones = document.querySelectorAll(".ejercicio");

    botones.forEach(boton => {

        boton.addEventListener(

            "click",

            function () {

                const numero = this.dataset.id;

                cargarVistaEjercicio(numero);

            }

        );

    });

}
function actualizarLatex() {

    if (!window.MathJax) return;

    MathJax.typesetPromise();

}
function inicializarFormularios() {

    const formularios = document.querySelectorAll("form");

    formularios.forEach(formulario => {

        formulario.addEventListener(

            "submit",

            function (e) {

                e.preventDefault();

            }

        );

    });

}
function iniciarAplicacion() {

    registrarEventos();

    registrarMenu();

    registrarSidebar();

    registrarEjercicios();

    inicializarFormularios();

    iniciarVistas();

    actualizarLatex();

}
