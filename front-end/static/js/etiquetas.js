document.addEventListener('DOMContentLoaded', function () {
    const inputEtiquetas = document.getElementById('etiquetas_input');
    const listaSugestoes = document.getElementById('etiquetas_sugestoes');

    // Função para buscar etiquetas populares
    function carregarEtiquetasPopulares() {
        fetch('/etiquetas_populares') // Rota que retorna as etiquetas populares
            .then(response => response.json())
            .then(data => {
                listaSugestoes.innerHTML = ''; // Limpa a lista antes de adicionar novas sugestões
                data.forEach(etiqueta => {
                    const item = document.createElement('li');
                    item.textContent = etiqueta;
                    item.style.cursor = 'pointer';
                    listaSugestoes.appendChild(item);

                    // Adiciona a funcionalidade de clique
                    item.addEventListener('click', function () {
                        adicionarEtiquetaAoInput(etiqueta);
                        listaSugestoes.style.display = 'none'; // Esconde a lista de sugestões
                    });
                });
                listaSugestoes.style.display = 'block'; // Mostra a lista de sugestões
            });
    }

    // Função para adicionar etiqueta ao input
    function adicionarEtiquetaAoInput(etiqueta) {
        const etiquetasAtuais = inputEtiquetas.value.split('#').map(e => e.trim()).filter(e => e);

        // Verifica se a etiqueta já foi adicionada
        if (!etiquetasAtuais.includes(etiqueta)) {
            inputEtiquetas.value += `#${etiqueta} `; // Adiciona a etiqueta com '#'
        } 
        // Caso a etiqueta tenha já sido adicionada aparece uma msg de alerta
        else {
            alert('Essa etiqueta já foi adicionada.'); 
        }
    }

    // Função para mostrar as etiquetas de acordo com a pesquisa do usuário
    function mostrarSugestoes() {
        const valorAtual = inputEtiquetas.value.trim();
        const etiquetasAtuais = valorAtual.split('#').map(e => e.trim()).filter(e => e);
        // Pega a última etiqueta para pesquisar no banco de dados
        const ultimaEtiqueta = etiquetasAtuais.length > 0 ? etiquetasAtuais.pop() : ''; 

        // Rota que retorna as etiquetas populares
        fetch('/etiquetas_populares') 
            .then(response => response.json())
            .then(data => {
                // Limpa a lista de sugestões
                listaSugestoes.innerHTML = ''; 
                if (ultimaEtiqueta) {
                    // Filtra as etiquetas
                    const sugestoes = data.filter(etiqueta => etiqueta.toLowerCase().startsWith(ultimaEtiqueta.toLowerCase()));

                    if (sugestoes.length > 0) {
                        sugestoes.forEach(etiqueta => {
                            const item = document.createElement('li');
                            item.textContent = etiqueta;
                            item.style.cursor = 'pointer';
                            listaSugestoes.appendChild(item);

                            // Adiciona a funcionalidade de clique
                            item.addEventListener('click', function () {
                                adicionarEtiquetaAoInput(etiqueta);
                                // Esconde a lista de sugestões
                                listaSugestoes.style.display = 'none'; 
                            });
                        });
                    } 
                }
                // Mostrar a lista de sugestões
                listaSugestoes.style.display = 'block'; 
            });
    }

    // Mostrar as etiquetas populares quando o input é clicado
    inputEtiquetas.addEventListener('focus', carregarEtiquetasPopulares);

    // Adiciona a funcionalidade de digitar no input
    inputEtiquetas.addEventListener('input', mostrarSugestoes);

    // Esconde a lista de sugestões caso o usuário saia do input de etiquetas
    inputEtiquetas.addEventListener('blur', function () {
        setTimeout(function () {
            listaSugestoes.style.display = 'none';
        }, 200); // Um pequeno atraso para permitir clicar nas sugestões antes de esconder
    });
});