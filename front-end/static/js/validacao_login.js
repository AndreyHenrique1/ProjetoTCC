// Validação do formulário
function validarFormulario() {
    var email = document.getElementById("email").value;
    var nomeUsuario = document.getElementById("nomeUsuario").value;
    var senha = document.getElementById("senha").value;

    var regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var erros = false;

    // Validação do e-mail
    if (!regexEmail.test(email)) {
        document.getElementById("email").classList.add("is-invalid");
        document.getElementById("emailErro").innerText = "Por favor, insira um endereço de e-mail válido.";
        erros = true;
    } else {
        document.getElementById("email").classList.remove("is-invalid");
        document.getElementById("emailErro").innerText = "";
    }

    // Validação do nome de usuário
    if (nomeUsuario.length < 3) {
        document.getElementById("nomeUsuario").classList.add("is-invalid");
        document.getElementById("nomeUsuarioErro").innerText = "O nome de usuário deve ter pelo menos 3 caracteres.";
        erros = true;
    } else {
        document.getElementById("nomeUsuario").classList.remove("is-invalid");
        document.getElementById("nomeUsuarioErro").innerText = "";
    }

    // Validação da senha
    if (senha.length < 6) {
        document.getElementById("senha").classList.add("is-invalid");
        document.getElementById("senhaErro").innerText = "A senha deve ter pelo menos 6 caracteres.";
        erros = true;
    } else {
        document.getElementById("senha").classList.remove("is-invalid");
        document.getElementById("senhaErro").innerText = "";
    }

    return !erros;
}

// Verificação de nome de usuário duplicado
document.getElementById("nomeUsuario").addEventListener("input", function() {
    var nomeUsuario = this.value;

    fetch("{{ url_for('cadastrar_route.verificar_usuario') }}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ nomeUsuario: nomeUsuario })
    })
    .then(response => response.json())
    .then(data => {
        if (data.existe) {
            document.getElementById("nomeUsuario").classList.add("is-invalid");
            document.getElementById("nomeUsuarioErro").innerText = "Esse nome de usuário já está sendo usado.";
        } else {
            document.getElementById("nomeUsuario").classList.remove("is-invalid");
            document.getElementById("nomeUsuarioErro").innerText = "";
        }
    })
    .catch(error => console.error("Erro:", error));
});