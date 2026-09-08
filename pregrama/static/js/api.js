// ==========================================
// URL BASE DE LA API
// ==========================================

const API = "/api";


// ==========================================
// PETICIÓN GENÉRICA
// ==========================================

async function consumirAPI(url, datos) {

    try {

        const faltantes = Object.entries(datos)
            .filter(([clave, valor]) => clave !== "x0" && clave !== "y0" && valor === "")
            .map(([clave]) => clave);

        if (faltantes.length) {
            mostrarError("Completa los campos obligatorios.");
            return;
        }

        mostrarCargando();

        const respuesta = await fetch(

            API + url,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify(datos)

            }

        );

        const resultado = await respuesta.json();

        if (respuesta.ok && resultado.ok) {

            mostrarResultado(resultado.html);

            scrollResultado();

        } else {

            mostrarError(resultado.error || resultado.mensaje || "No fue posible resolver la ecuación.");

        }

    }

    catch (error) {

        mostrarError(error.message);

    }

}
async function resolverLineal() {

    await consumirAPI(

        "/lineal",

        {

            P: valor("P"),

            Q: valor("Q"),

            var: valor("variable"),

            x0: valor("x0"),

            y0: valor("y0")

        }

    );

}
async function resolverExacta() {

    await consumirAPI(

        "/exacta",

        {

            M: valor("MExacta"),

            N: valor("NExacta")

        }

    );

}
async function resolverNoExacta() {

    await consumirAPI(

        "/noexacta",

        {

            M: valor("MNoExacta"),

            N: valor("NNoExacta")

        }

    );

}
async function resolverCarbono() {

    await consumirAPI(

        "/carbono14",

        {

            vida_media: valor("vida_media"),

            cantidad_inicial: valor("cantidad_inicial"),

            cantidad_final: valor("cantidad_final")

        }

    );

}
async function resolverSeparable() {

    await consumirAPI(

        "/separable",

        {

            f: valor("fSeparable"),

            g: valor("gSeparable"),

            x0: valor("x0Separable"),

            y0: valor("y0Separable")

        }

    );

}
async function cargarEjercicio(numero) {

    try {

        const respuesta = await fetch(

            API + "/ejercicio/" + numero

        );

        const datos = await respuesta.json();

        if (!datos.ok) {

            mostrarError(datos.mensaje);

            return;

        }

        llenarFormulario(

            datos.ejercicio

        );

    }

    catch (error) {

        mostrarError(

            error.message

        );

    }

}
async function listarEjercicios() {

    const respuesta = await fetch(

        API + "/ejercicios"

    );

    return await respuesta.json();

}
