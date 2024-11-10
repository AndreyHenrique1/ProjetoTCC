// Avisos de ações do usuário
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);

    // Verifica se a variável 'sucesso' está presente na URL
    if (urlParams.has("sucesso")) {
        const acao = urlParams.get("sucesso");  

        // Exibe mensagens com base na ação realizada
        switch (acao) {
            case "pergunta_enviada":
                alert("Sua pergunta foi enviada com sucesso!!!");
                break;
            case "pergunta_editada":
                alert("Sua pergunta foi editada com sucesso!!!");
                break;
            case "pergunta_excluida":
                alert("Sua pergunta foi excluída com sucesso!!!");
                break;
            case "like_realizado":
                alert("Like realizado com sucesso!!!");
                break;
            case "deslike_realizado":
                alert("Deslike realizado com sucesso!!!");
                break;
            case "comentario_excluido":
                alert("Comentário excluído com sucesso!!!")
            default:
                break;
        }

        // Limpa o parâmetro 'sucesso' da URL após exibir a mensagem
        history.replaceState(null, '', window.location.pathname);
    }
};
