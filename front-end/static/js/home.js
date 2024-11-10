document.addEventListener('DOMContentLoaded', function() {
    // Seleciona o botão de expandir, o menu lateral e o conteúdo principal
    const btnExpandir = document.getElementById('btn-exp');
    const menuLateral = document.querySelector('.menu-lateral');
    const conteudoPrincipal = document.querySelector('.main-conteudo');
    const textoMenu = document.querySelectorAll('.menu-lateral .txt-link');

    // Verifica se o estado do menu está salvo no localStorage
    if (localStorage.getItem('menuExpandido') === 'true') {
        // Remove a transição para que o menu não execute a animação
        menuLateral.style.transition = 'none';

        // Remove a transição de texto das letras do menu
        textoMenu.forEach(item => item.style.transition = 'none');

        menuLateral.classList.add('expandir');
        conteudoPrincipal.classList.add('expandido');
        
        // Depois de aplicar o estado, reativa a transição para as próximas interações
        setTimeout(() => {
            menuLateral.style.transition = '0.5s';  // Ou o valor da sua transição anterior
            textoMenu.forEach(item => item.style.transition = 'margin-left 0.5s'); // Ajusta a transição do texto
        }, 50);
    }

    // Quando o botão de expandir for clicado, alterna as classes 'expandir' no menu e 'expandido' no conteúdo
    btnExpandir.addEventListener('click', function() {
        menuLateral.classList.toggle('expandir');
        conteudoPrincipal.classList.toggle('expandido');

        // Salva o estado do menu no localStorage
        if (menuLateral.classList.contains('expandir')) {
            localStorage.setItem('menuExpandido', 'true');
        } else {
            localStorage.setItem('menuExpandido', 'false');
        }
    });
});
