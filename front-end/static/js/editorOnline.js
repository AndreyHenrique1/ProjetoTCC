document.addEventListener("DOMContentLoaded", function () {
    // Inicialização do editor Quill para os comentários
    var quillComentario = new Quill('#editor-comentario', {
        theme: 'snow',
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

            if (form.querySelector('#comentario')) {
                form.querySelector('#comentario').value = quillComentario.root.innerHTML;
            }
            if (form.querySelector('#descricao')) {
                form.querySelector('#descricao').value = quillEdicao.root.innerHTML;
            }

            // Enviar o formulário após atualizar os valores necessários
            this.submit(); 
        };
    });

    // Atualização de visualização em tempo real (se necessário)
    function updatePreview() {
        var content = quillEdicao.root.innerHTML; // Utilize o quillEdicao aqui
        document.querySelector('#Visualizacao-tempoReal').innerHTML = content;
    }

    // Atualizar visualização ao carregar a página
    updatePreview();

    // Adicionar listener para mudança de texto no Quill
    quillEdicao.on('text-change', updatePreview);
});
