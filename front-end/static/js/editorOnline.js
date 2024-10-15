// Editor de texto online (Quill)

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

// Função para lidar com o envio dos formulários
document.querySelectorAll('form').forEach(form => {
    form.onsubmit = function () {
        if (form.querySelector('#comentario')) {
            form.querySelector('#comentario').value = quillComentario.root.innerHTML;
        }
        if (form.querySelector('#descricao')) {
            form.querySelector('#descricao').value = quillEdicao.root.innerHTML;
        }
    };
});

function updatePreview() {
    var content = quill.root.innerHTML;
    document.querySelector('#Visualizacao-tempoReal').innerHTML = content;
}

// Atualizar visualização em tempo real
quill.on('text-change', updatePreview);

// Atualizar visualização ao carregar a página
updatePreview();

// Ao enviar o formulário, insira o conteúdo do editor no campo hidden
document.querySelector('form').onsubmit = function () {
    document.querySelector('#descricao').value = quill.root.innerHTML;
};