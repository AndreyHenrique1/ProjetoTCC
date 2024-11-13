document.getElementById('btn-enviar').addEventListener('click', async () => {
    const pergunta = document.getElementById('input-pergunta').value;
    if (!pergunta) return;

    const respostaContainer = document.getElementById('resposta-container');
    respostaContainer.innerHTML += `<p><strong>Pergunta:</strong> ${pergunta}</p><p><em>Carregando...</em></p>`;
    document.getElementById('input-pergunta').value = '';

    try {
        const response = await fetch('/ia', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pergunta })
        });
        const data = await response.json();
        respostaContainer.innerHTML += `<p><strong>Resposta:</strong> ${data.resposta}</p>`;
    } catch (error) {
        respostaContainer.innerHTML += `<p><strong>Erro:</strong> Não foi possível obter a resposta.</p>`;
    }
});
