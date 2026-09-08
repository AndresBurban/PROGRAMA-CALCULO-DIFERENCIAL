// ==========================================
// VARIABLES GLOBALES
// ==========================================

const $ = (id) => document.getElementById(id);


// ==========================================
// LIMPIAR RESULTADOS
// ==========================================

function limpiarResultado() {

    const resultado = $("resultado");
    const caja = $("resultado-box");

    if (resultado) resultado.innerHTML = "";
    if (caja) caja.classList.remove("show", "error");

}


// ==========================================
// MOSTRAR RESULTADOS
// ==========================================

function mostrarResultado(html) {

    const resultado = $("resultado");
    const caja = $("resultado-box");

    if (!resultado) return;

    resultado.innerHTML = html;
    if (caja) caja.classList.add("show");

    if (window.MathJax) {

        MathJax.typesetPromise();

    }

}


// ==========================================
// MOSTRAR ERROR
// ==========================================

function mostrarError(mensaje) {

    const resultado = $("resultado");
    const caja = $("resultado-box");

    if (!resultado) return;

    resultado.textContent = "";
    const alerta = document.createElement("div");
    alerta.className = "alert alert-danger";
    alerta.innerHTML = "<strong>Error</strong><br>";
    alerta.append(document.createTextNode(String(mensaje || "Error desconocido.")));
    resultado.append(alerta);
    if (caja) caja.classList.add("show", "error");

}


// ==========================================
// MENSAJE DE CARGA
// ==========================================

function mostrarCargando() {

    const resultado = $("resultado");
    const caja = $("resultado-box");

    if (!resultado) return;

    resultado.innerHTML = `

        <div class="text-center p-5">

            <div class="spinner-border"></div>

            <p class="mt-3">

                Procesando...

            </p>

        </div>

    `;
    if (caja) caja.classList.add("show");

}


// ==========================================
// LIMPIAR INPUTS
// ==========================================

function limpiarFormulario(idFormulario) {

    const formulario = $(idFormulario);

    if (!formulario) return;

    formulario.reset();

}


// ==========================================
// OBTENER VALOR
// ==========================================

function valor(id) {

    const elemento = $(id);
    return elemento ? elemento.value.trim() : "";

}


// ==========================================
// ASIGNAR VALOR
// ==========================================

function asignar(id, valor) {

    $(id).value = valor;

}


// ==========================================
// VALIDAR CAMPO
// ==========================================

function validar(id) {

    return valor(id) !== "";

}


// ==========================================
// SCROLL
// ==========================================

function scrollResultado() {

    const resultado = $("resultado");

    if (!resultado) return;

    resultado.scrollIntoView({

        behavior: "smooth"

    });

}