(() => {
    'use strict';

    const el = (id) => document.getElementById(id);

    const ensino = el('ensino');
    const componente = el('componente');
    const serie = el('serie');
    const bimestre = el('bimestre');
    const listaAulas = el('listaAulas');
    const contadorSelecionadas = el('contadorSelecionadas');
    const fonteDados = el('fonteDados');
    const mensagem = el('mensagem');
    const multiTurmaMenu = el('menuTurmas');

    const selecionadas = new Set();
    let aulasDoEscopo = [];

    // Preencher Select genérico
    function preencherSelect(select, itens, selecionadoDefault, mapFn) {
        if (!select) return;
        select.innerHTML = '';
        
        itens.forEach(item => {
            const opt = document.createElement('option');
            const val = mapFn ? mapFn(item).value : (item.id || item);
            const label = mapFn ? mapFn(item).label : (item.name || item);
            opt.value = val;
            opt.textContent = label;
            if (String(val) === String(selecionadoDefault)) {
                opt.selected = true;
            }
            select.appendChild(opt);
        });
    }

    // 1. Carregar Disciplinas por Segmento (Fundamental / Médio)
    async function carregarDisciplinas() {
        const nivel = ensino ? ensino.value : 'medio';
        if (!nivel) return;

        try {
            const resp = await fetch(`/api/materias?ensino=${encodeURIComponent(nivel)}`);
            const materias = await resp.json();
            
            const selectedSubjectId = el('subject_id')?.value;
            preencherSelect(componente, materias, selectedSubjectId, (m) => ({ value: m.id, label: m.name }));
            
            // Sincronizar subject_id e planoComponente
            atualizarSubjectId();
            carregarSeries();
        } catch (e) {
            console.error("Erro ao carregar disciplinas:", e);
        }
    }

    // 2. Carregar Séries
    async function carregarSeries() {
        const nivel = ensino ? ensino.value : 'medio';
        try {
            const resp = await fetch(`/api/series?ensino=${encodeURIComponent(nivel)}`);
            const series = await resp.json();
            
            const selectedGrade = el('grade')?.value;
            preencherSelect(serie, series, selectedGrade, (s) => ({ value: s, label: s }));
            
            atualizarTurmas();
            carregarEscopo();
        } catch (e) {
            console.error("Erro ao carregar séries:", e);
        }
    }

    // 3. Atualizar Turmas no Multiselect
    async function atualizarTurmas() {
        const gradeVal = serie ? serie.value : '';
        const nivel = ensino ? ensino.value : 'medio';
        if (!multiTurmaMenu) return;

        try {
            const resp = await fetch(`/api/turmas?grade=${encodeURIComponent(gradeVal)}&ensino=${encodeURIComponent(nivel)}`);
            const turmas = await resp.json();
            
            // Renderizar opções de checkboxes
            multiTurmaMenu.innerHTML = '';
            
            // Turmas pré-selecionadas se for edição
            const turmasAtuais = (el('turmas_atuais')?.value || '').split(',').map(t => t.trim());

            turmas.forEach(t => {
                const labelEl = document.createElement('label');
                labelEl.className = 'multi-turma-opcao';
                
                const isChecked = turmasAtuais.includes(t.value);
                if (isChecked) labelEl.classList.add('selecionada');

                labelEl.innerHTML = `
                    <input type="checkbox" name="turmas[]" value="${t.value}" data-label="${t.label}" ${isChecked ? 'checked' : ''}>
                    <span>${t.label}</span>
                `;
                
                const chk = labelEl.querySelector('input');
                chk.addEventListener('change', () => {
                    labelEl.classList.toggle('selecionada', chk.checked);
                    atualizarTextoTurmas();
                });

                multiTurmaMenu.appendChild(labelEl);
            });

            atualizarTextoTurmas();
        } catch (e) {
            console.error("Erro ao carregar turmas:", e);
        }
    }

    function atualizarTextoTurmas() {
        if (!multiTurmaMenu) return;
        const checkboxes = Array.from(multiTurmaMenu.querySelectorAll('input[type="checkbox"]:checked'));
        const labels = checkboxes.map(c => c.dataset.label || c.value);
        const txtEl = el('textoTurmas');
        if (txtEl) {
            txtEl.textContent = labels.length ? labels.join(', ') : 'Selecione as turmas';
        }
    }

    // 4. Carregar Escopo-Sequência do Banco
    async function carregarEscopo() {
        const subjectId = componente ? componente.value : '';
        const gradeVal = serie ? serie.value : '';
        const bimVal = bimestre ? bimestre.value : 1;
        const nivel = ensino ? ensino.value : 'medio';

        if (!subjectId || !bimVal) return;

        if (fonteDados) fonteDados.textContent = 'Buscando aulas no banco de dados...';

        try {
            const resp = await fetch(`/api/escopo?subject_id=${subjectId}&grade=${encodeURIComponent(gradeVal)}&bimester=${bimVal}&education_level=${encodeURIComponent(nivel)}`);
            aulasDoEscopo = await resp.json();
            
            if (fonteDados) {
                fonteDados.textContent = `Banco de Dados · ${aulasDoEscopo.length} aula(s) encontrada(s)`;
            }

            renderAulas();
        } catch (e) {
            console.error("Erro ao carregar escopo:", e);
            if (fonteDados) fonteDados.textContent = 'Erro ao consultar o banco de dados';
        }
    }

    // 5. Renderizar Lista de Aulas com Checkboxes
    function renderAulas() {
        if (!listaAulas) return;
        listaAulas.innerHTML = '';

        if (!aulasDoEscopo.length) {
            listaAulas.innerHTML = '<p class="lista-vazia">Nenhuma aula cadastrada no Escopo para esta seleção. Importe o PDF do componente correspondente pelo painel de administração.</p>';
            atualizarFormulario([]);
            return;
        }

        // Recuperar IDs pré-selecionados (em caso de edição de plano)
        const preSelectedInput = el('pre_selected_lesson_ids');
        const preSelectedIds = preSelectedInput && preSelectedInput.value ? preSelectedInput.value.split(',').map(Number) : [];

        aulasDoEscopo.forEach((aula) => {
            const isSelected = selecionadas.has(aula.id) || preSelectedIds.includes(aula.id);
            if (isSelected) selecionadas.add(aula.id);

            const label = document.createElement('label');
            label.className = 'aula-opcao' + (isSelected ? ' ativa' : '');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.name = 'aulas_escopo[]';
            checkbox.value = aula.id;
            checkbox.checked = isSelected;

            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    selecionadas.add(aula.id);
                    label.classList.add('ativa');
                } else {
                    selecionadas.delete(aula.id);
                    label.classList.remove('ativa');
                }
                atualizarFormulario(Array.from(selecionadas));
            });

            const info = document.createElement('span');
            const habTxt = aula.skills ? ` · ${aula.skills}` : '';
            const aeTxt = aula.essential_learning_code ? ` · ${aula.essential_learning_code}` : '';

            info.innerHTML = `
                <span class="aula-numero">Aula ${aula.lesson_number}${habTxt}${aeTxt}</span>
                <span class="aula-titulo">${aula.title}</span>
            `;

            label.appendChild(checkbox);
            label.appendChild(info);
            listaAulas.appendChild(label);
        });

        // Limpar pre_selected após primeira renderização
        if (preSelectedInput) preSelectedInput.value = '';

        atualizarFormulario(Array.from(selecionadas));
    }

    // 6. Atualizar os campos do Plano com preenchimento automático
    async function atualizarFormulario(lessonIds) {
        if (contadorSelecionadas) {
            contadorSelecionadas.textContent = `${lessonIds.length} selecionada${lessonIds.length === 1 ? '' : 's'}`;
        }

        const planoComponente = el('planoComponente');
        const planoBimestre = el('planoBimestre');
        const titulosAulas = el('titulosAulas');
        const objetivos = el('objetivos');
        const conteudos = el('conteudos');
        const habilidades = el('habilidades');
        const aes = el('aes');

        // Campos cabeçalho
        if (planoComponente && componente) {
            planoComponente.value = componente.options[componente.selectedIndex]?.text || '';
        }
        if (planoBimestre && bimestre) {
            planoBimestre.value = `${bimestre.value}º Bimestre`;
        }

        if (!lessonIds.length) {
            if (titulosAulas) titulosAulas.value = '';
            if (objetivos) objetivos.value = '';
            if (conteudos) conteudos.value = '';
            if (habilidades) habilidades.value = '';
            if (aes) aes.value = '';
            return;
        }

        try {
            const resp = await fetch('/api/detalhes-aulas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lesson_ids: lessonIds })
            });
            const dados = await resp.json();

            if (titulosAulas) titulosAulas.value = dados.titulos;
            if (conteudos) conteudos.value = dados.conteudos;
            if (objetivos) objetivos.value = dados.objetivos;
            if (habilidades) habilidades.value = dados.habilidades;
            if (aes) aes.value = dados.aes;
        } catch (e) {
            console.error("Erro ao obter detalhes agregados das aulas:", e);
        }
    }

    function atualizarSubjectId() {
        const subIdHidden = el('subject_id_hidden');
        if (subIdHidden && componente) {
            subIdHidden.value = componente.value;
        }
        const planoComp = el('planoComponente');
        if (planoComp && componente) {
            planoComp.value = componente.options[componente.selectedIndex]?.text || '';
        }
    }

    // Eventos de troca
    ensino?.addEventListener('change', () => {
        carregarDisciplinas();
    });

    componente?.addEventListener('change', () => {
        atualizarSubjectId();
        selecionadas.clear();
        carregarEscopo();
    });

    serie?.addEventListener('change', () => {
        const gradeHidden = el('grade_hidden');
        if (gradeHidden && serie) gradeHidden.value = serie.value;
        atualizarTurmas();
        selecionadas.clear();
        carregarEscopo();
    });

    bimestre?.addEventListener('change', () => {
        const bimHidden = el('bimestre_hidden');
        if (bimHidden && bimestre) bimHidden.value = bimestre.value;
        const planoBim = el('planoBimestre');
        if (planoBim && bimestre) planoBim.value = `${bimestre.value}º Bimestre`;
        selecionadas.clear();
        carregarEscopo();
    });

    // Toggle Multiturma Menu
    const btnTurmas = el('btnTurmas');
    const multiTurma = el('multiTurma');
    if (btnTurmas && multiTurmaMenu) {
        btnTurmas.addEventListener('click', (e) => {
            e.stopPropagation();
            multiTurmaMenu.classList.toggle('aberto');
            btnTurmas.classList.toggle('aberto');
        });

        document.addEventListener('click', (e) => {
            if (multiTurma && !multiTurma.contains(e.target)) {
                multiTurmaMenu.classList.remove('aberto');
                btnTurmas.classList.remove('aberto');
            }
        });
    }

    // Flatpickr para seleção de período
    if (el('periodo') && typeof window.flatpickr !== 'undefined') {
        window.flatpickr('#periodo', {
            mode: 'range',
            locale: 'pt',
            dateFormat: 'd/m/Y',
            conjunction: ' até ',
            allowInput: false,
            onChange(selectedDates) {
                const inicio = el('data_inicio');
                const fim = el('data_fim');
                if (inicio && selectedDates[0]) {
                    const d = selectedDates[0];
                    inicio.value = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
                }
                if (fim && selectedDates[1]) {
                    const d = selectedDates[1];
                    fim.value = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
                }
            }
        });
    }

    // Inicialização
    carregarDisciplinas();
})();
