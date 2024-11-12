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
            case 'comentario_realizado':
                alert("Comentário realizado com sucesso!!!")
                break;
            case "comentario_excluido":
                alert("Comentário excluído com sucesso!!!")
                break;
            case "blog_enviado":
                alert("Seu blog foi enviado com sucesso!!!")
                break;
            case "blog_editado":
                alert("Seu blog foi editado com sucesso!!!")
                break;
            case "blog_excluido":
                alert("Seu blog foi excluído com sucesso!!!")
                break;
            case "comentario_denunciado":
                alert("O comentário foi denunciado com sucesso! Obrigado por ajudar a manter nossa comunidade segura e confiável!!!")
                break;
            case "comentario_ja_denunciado":
                alert("Você já denunciou este comentário!! Você não pode denunciar novamente!!")
                break;
            case "blog_denunciado":
                alert("Blog denunciado com sucesso! Obrigado por ajudar a manter nossa comunidade segura e confiável!!!")
                break;
            case "blog_ja_denunciado":
                alert("Você já denunciou este blog!! Você não pode denunciar novamente!!!")
                break;
            case "usuario_cadastrado":
                alert("Cadastro realizado com sucesso!!!")
                break;
            case "usuario_editado":
                alert("Usuário editado com sucesso!!!")
                break;
            default:
                break;
        }

        // Limpa o parâmetro 'sucesso' da URL após exibir a mensagem
        history.replaceState(null, '', window.location.pathname);
    }
};
