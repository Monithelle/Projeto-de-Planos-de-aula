function mostrarLogin() {

    document
        .getElementById("formLogin")
        .classList.remove("escondido");

    document
        .getElementById("formCadastro")
        .classList.add("escondido");


    document
        .getElementById("btnEntrar")
        .classList.add("ativa");

    document
        .getElementById("btnCadastrar")
        .classList.remove("ativa");
}


function mostrarCadastro() {

    document
        .getElementById("formLogin")
        .classList.add("escondido");

    document
        .getElementById("formCadastro")
        .classList.remove("escondido");


    document
        .getElementById("btnEntrar")
        .classList.remove("ativa");

    document
        .getElementById("btnCadastrar")
        .classList.add("ativa");
}