document.addEventListener('DOMContentLoaded', () => {
    const campoBusca = document.getElementById('buscarPlano');
    const cards = Array.from(document.querySelectorAll('.prof-card-bimestre'));
    const semResultado = document.getElementById('semResultado');

    const normalizarTexto = (valor) => String(valor || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .trim();

    const filtrarPlanos = () => {
        const termo = normalizarTexto(campoBusca?.value);
        let encontrados = 0;

        cards.forEach((card) => {
            const conteudo = normalizarTexto(card.dataset.pesquisa);
            const mostrar = !termo || conteudo.includes(termo);

            card.classList.toggle('oculto', !mostrar);
            if (mostrar) encontrados += 1;
        });

        if (semResultado) {
            semResultado.hidden = encontrados > 0;
        }
    };

    campoBusca?.addEventListener('input', filtrarPlanos);

    document.querySelectorAll('.prof-abrir-pasta').forEach((botao) => {
        botao.addEventListener('click', () => {
            const bimestre = botao.dataset.bimestre;
            alert(`Pasta do ${bimestre}º bimestre. A listagem de planos será conectada aqui.`);
        });
    });
});
