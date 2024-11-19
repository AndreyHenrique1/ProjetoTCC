document.addEventListener("DOMContentLoaded", function () {
    // Inicialização dos editores Quill
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

    // Apenas formularios com Quill devem ser manipulados
    document.querySelectorAll('.form-com-quill').forEach(form => {
        form.onsubmit = function (event) {
            event.preventDefault(); // Prevenir envio até que os valores sejam atualizados

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
        console.log("Texto alterado no editor", delta);
    }

    quillEdicao.on('text-change', updatePreview);
});
