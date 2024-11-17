document.addEventListener("DOMContentLoaded", function () {
    // Inicialização do editor Quill para os comentários
    var quillComentario = new Quill('#editor-comentario', {
        theme: 'snow',
        placeholder: 'Explique e escreva aqui sua resposta de forma clara e objetiva...',
        modules: {
            toolbar: [
                [{ 'header': [1, 2, false] }],
                ['bold', 'italic', 'underline'],
                [{ 'color': [] }, { 'background': [] }],
                [{ 'align': [] }],
                ['link', 'image', 'code-block'],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                ['clean']
            ]
        },
    });

    // Inicialização do editor Quill para as perguntas e blogs
    var quillEdicao = new Quill('#editor-geral', {
        theme: 'snow',
        placeholder: 'Escreva aqui de forma clara e objetiva...',
        modules: {
            toolbar: [
                [{ 'header': [1, 2, false] }],
                ['bold', 'italic', 'underline'],
                [{ 'color': [] }, { 'background': [] }],
                [{ 'align': [] }],
                ['link', 'image', 'code-block'],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                ['clean']
            ]
        },
    });

    // Função para lidar com o envio dos formulários de comentários e edições
    document.querySelectorAll('form').forEach(form => {
        form.onsubmit = function (event) {
            event.preventDefault(); // Prevenir envio até que os valores sejam atualizados

            // Verificar se os elementos de texto existem antes de atribuir os valores
            const comentarioElement = form.querySelector('#comentario');
            const descricaoElement = form.querySelector('#descricao');
            
            if (comentarioElement) {
                comentarioElement.value = quillComentario.root.innerHTML;
            }
            if (descricaoElement) {
                descricaoElement.value = quillEdicao.root.innerHTML;
            }

            // Enviar o formulário após atualizar os valores necessários
            form.submit(); 
        };
    });

    // Adicionar listener para mudança de texto no Quill (definindo a função updatePreview)
    function updatePreview(delta, oldDelta, source) {
        // Lógica para atualizar a visualização do preview
        console.log("Texto alterado no editor", delta);
    }

    quillEdicao.on('text-change', updatePreview);
});
