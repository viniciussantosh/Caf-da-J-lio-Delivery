function telaCadastro() {
    var tela_c = document.getElementsByClassName('sign')[0]; 
    var tela_l = document.getElementsByClassName('login')[0];

    tela_l.style.display = 'none';

    if (window.getComputedStyle(tela_c).display === 'none') {
        tela_c.style.display = 'flex';
    }
}

function telaLogin() {
    var tela_c = document.getElementsByClassName('sign')[0];
    var tela_l = document.getElementsByClassName('login')[0];

    tela_c.style.display = 'none';

    if (window.getComputedStyle(tela_l).display === 'none') {
        tela_l.style.display = 'flex';
    }
}

document.addEventListener('click', function(event) {
    var tela_c = document.getElementsByClassName('sign')[0];
    var tela_l = document.getElementsByClassName('login')[0];

    var criarContaBtn = document.getElementById('criarConta');
    var entrarContaBtn = document.getElementById('entrarConta');

    if (
        tela_c.style.display === 'flex' && 
        !tela_c.contains(event.target) &&
        event.target !== criarContaBtn
    ) {
        tela_c.style.display = 'none';
    }

    if (
        tela_l.style.display === 'flex' && 
        !tela_l.contains(event.target) &&
        event.target !== entrarContaBtn
    ) {
        tela_l.style.display = 'none';
    }
});