document.addEventListener('DOMContentLoaded', function () {
    const inputEtiquetas = document.getElementById('etiquetas_input');
    const listaSugestoes = document.getElementById('etiquetas_sugestoes');

    if (!inputEtiquetas || !listaSugestoes) {
        return;
    }

    // Função para carregar as cinco primeiras etiquetas
    function carregarEtiquetasIniciais() {
        fetch('/etiquetas_iniciais')
            .then(response => response.json())
            .then(data => {
                listaSugestoes.innerHTML = ''; // Limpa a lista antes de adicionar novas sugestões
                if (data.length > 0) {
                    data.forEach(etiqueta => {
                        const item = document.createElement('li');
                        item.textContent = etiqueta.nome;
                        item.style.cursor = 'pointer';
                        listaSugestoes.appendChild(item);

                        item.addEventListener('click', function () {
                            adicionarEtiquetaAoInput(etiqueta.nome);
                            listaSugestoes.style.display = 'none';
                        });
                    });
                    listaSugestoes.style.display = 'block'; // Mostra a lista de sugestões
                } else {
                    listaSugestoes.innerHTML = '<li>Etiqueta não encontrada</li>';
                    listaSugestoes.style.display = 'block';
                }
            });
    }

    // Função para mostrar as etiquetas relacionadas
    function mostrarSugestoes() {
        const valorAtual = inputEtiquetas.value.trim();
        const etiquetasAtuais = valorAtual.split('#').map(e => e.trim()).filter(e => e);
        const ultimaEtiqueta = etiquetasAtuais.length > 0 ? etiquetasAtuais.pop() : ''; 

        if (ultimaEtiqueta) {
            fetch(`/etiquetas_relacionadas?termo=${encodeURIComponent(ultimaEtiqueta)}`)
                .then(response => response.json())
                .then(data => {
                    listaSugestoes.innerHTML = ''; // Limpa a lista de sugestões
                    if (data.length > 0) {
                        data.forEach(etiqueta => {
                            const item = document.createElement('li');
                            item.textContent = etiqueta.nome;
                            item.style.cursor = 'pointer';
                            listaSugestoes.appendChild(item);

                            item.addEventListener('click', function () {
                                adicionarEtiquetaAoInput(etiqueta.nome);
                                listaSugestoes.style.display = 'none';
                            });
                        });
                    } else {
                        listaSugestoes.innerHTML = '<li>Etiqueta não encontrada</li>';
                    }
                    listaSugestoes.style.display = 'block'; // Mostra a lista de sugestões
                });
        } else {
            // Se não houver valor, mostrar as etiquetas iniciais
            carregarEtiquetasIniciais();
        }
    }

    function adicionarEtiquetaAoInput(etiqueta) {
        const etiquetasAtuais = inputEtiquetas.value.split('#').map(e => e.trim()).filter(e => e);

        if (!etiquetasAtuais.includes(etiqueta)) {
            inputEtiquetas.value += `#${etiqueta} `;
        } else {
            alert('Essa etiqueta já foi adicionada.');
        }
    }

    inputEtiquetas.addEventListener('focus', carregarEtiquetasIniciais); // Carrega etiquetas iniciais ao focar no input
    inputEtiquetas.addEventListener('input', mostrarSugestoes); // Mostra sugestões enquanto digita
    inputEtiquetas.addEventListener('blur', function () {
        setTimeout(function () {
            listaSugestoes.style.display = 'none'; // Esconde a lista ao sair do input
        }, 200);
    });
});
