document.addEventListener('DOMContentLoaded', () => {
    const arquivoExcel = document.getElementById('adminExcel');
    const selecionarExcel = document.getElementById('selecionarExcel');
    const nomeArquivo = document.getElementById('nomeArquivo');

    if (arquivoExcel && selecionarExcel && nomeArquivo) {
        selecionarExcel.addEventListener('click', () => arquivoExcel.click());

        arquivoExcel.addEventListener('change', () => {
            const arquivo = arquivoExcel.files?.[0];
            nomeArquivo.textContent = arquivo ? arquivo.name : 'Nenhum arquivo selecionado.';
        });
    }

    const atualizarPendentes = () => {
        const quantidade = document.querySelectorAll('.cadastro-linha').length;
        const contadorPendentes = document.getElementById('contadorPendentes');
        const resumoPendentes = document.getElementById('resumoPendentes');

        if (contadorPendentes) contadorPendentes.textContent = String(quantidade);
        if (resumoPendentes) resumoPendentes.textContent = String(quantidade);
    };

    document.querySelectorAll('.cadastro-linha').forEach((linha) => {
        const aceitar = linha.querySelector('.botao.aceitar');
        const recusar = linha.querySelector('.botao.recusar');

        aceitar?.addEventListener('click', () => {
            linha.remove();
            atualizarPendentes();
        });

        recusar?.addEventListener('click', () => {
            linha.remove();
            atualizarPendentes();
        });
    });
});
