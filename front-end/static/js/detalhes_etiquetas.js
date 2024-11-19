// Script para alternar entre perguntas e blogs
document.getElementById("btn-perguntas").addEventListener("click", function () {
    document.getElementById("perguntas").style.display = "block"; // Mostrar perguntas
    document.getElementById("blogs").style.display = "none"; // Esconder blogs
    document.getElementById("btn-perguntas").classList.add("active"); // Ativar botão de perguntas
    document.getElementById("btn-blogs").classList.remove("active"); // Desativar botão de blogs
});

document.getElementById("btn-blogs").addEventListener("click", function () {
    document.getElementById("perguntas").style.display = "none"; // Esconder perguntas
    document.getElementById("blogs").style.display = "block"; // Mostrar blogs
    document.getElementById("btn-blogs").classList.add("active"); // Ativar botão de blogs
    document.getElementById("btn-perguntas").classList.remove("active"); // Desativar botão de perguntas
});