// Avisos das perguntas
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);

    // Verifica se a variavel sucesso está presente
    if (urlParams.has("sucesso")) {
        const acao = urlParams.get("sucesso");  

        // Obtém diferentes msgs de acordo com a ação do usuário
        if (acao === "pergunta_enviada") {
            alert("Sua pergunta foi enviada com sucesso!!!");
        } else if (acao === "pergunta_editada") {
            alert("Sua pergunta foi editada com sucesso!!!");
        } else if (acao === "pergunta_excluida") {
            alert("Sua pergunta foi excluída com sucesso!!!");
        }

        // Limpa o parâmetro da URL após a exibição da mensagem
        history.replaceState(null, '', window.location.pathname);
    }
};