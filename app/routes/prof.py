from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from app.models import db, User, Subject, ScopeLesson, LessonPlan, LessonPlanClass, LessonPlanLesson
from app.services.auth_service import login_required, active_prof_required, get_current_user
from app.services.pdf_exporter import generate_lesson_plan_pdf

prof_bp = Blueprint('prof', __name__)

@prof_bp.route('/prof')
@login_required
def dashboard():
    user = get_current_user()
    
    # Contar planos por bimestre do professor autenticado
    contagem_bimestres = {}
    for b in range(1, 5):
        contagem_bimestres[b] = LessonPlan.query.filter_by(user_id=user.id, bimester=b).count()

    bimestres_data = [
        {
            'id': 1,
            'titulo': '1º Bimestre',
            'periodo': 'Fevereiro a Abril',
            'planos': contagem_bimestres[1],
            'cor': 'verde',
            'status': 'Ativo' if contagem_bimestres[1] > 0 else 'Disponível',
            'status_classe': 'novo' if contagem_bimestres[1] > 0 else 'rascunho'
        },
        {
            'id': 2,
            'titulo': '2º Bimestre',
            'periodo': 'Abril a Julho',
            'planos': contagem_bimestres[2],
            'cor': 'amarelo',
            'status': 'Ativo' if contagem_bimestres[2] > 0 else 'Disponível',
            'status_classe': 'andamento' if contagem_bimestres[2] > 0 else 'rascunho'
        },
        {
            'id': 3,
            'titulo': '3º Bimestre',
            'periodo': 'Agosto a Outubro',
            'planos': contagem_bimestres[3],
            'cor': 'cinza',
            'status': 'Ativo' if contagem_bimestres[3] > 0 else 'Disponível',
            'status_classe': 'novo' if contagem_bimestres[3] > 0 else 'rascunho'
        },
        {
            'id': 4,
            'titulo': '4º Bimestre',
            'periodo': 'Outubro a Dezembro',
            'planos': contagem_bimestres[4],
            'cor': 'cinza',
            'status': 'Ativo' if contagem_bimestres[4] > 0 else 'Disponível',
            'status_classe': 'novo' if contagem_bimestres[4] > 0 else 'rascunho'
        }
    ]

    return render_template(
        'prof/dashboard.html',
        user=user,
        bimestres=bimestres_data,
        total_planos=sum(contagem_bimestres.values())
    )

@prof_bp.route('/prof/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    user = get_current_user()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            nome = request.form.get('nome', '').strip()
            telefone = request.form.get('telefone', '').strip()
            email = request.form.get('email', '').strip().lower()

            if not nome or not email:
                flash('Nome e e-mail são obrigatórios.', 'erro')
            else:
                # Verificar se o e-mail mudou e se já existe
                existente = User.query.filter(User.email == email, User.id != user.id).first()
                if existente:
                    flash('Este e-mail já está em uso por outro usuário.', 'erro')
                else:
                    user.name = nome
                    user.phone = telefone
                    user.email = email
                    db.session.commit()
                    session['name'] = user.name
                    session['email'] = user.email
                    flash('Perfil atualizado com sucesso!', 'sucesso')

        elif action == 'change_password':
            senha_atual = request.form.get('senha_atual', '')
            nova_senha = request.form.get('nova_senha', '')
            confirmacao = request.form.get('confirmacao', '')

            if not user.check_password(senha_atual):
                flash('A senha atual informada está incorreta.', 'erro')
            elif not nova_senha or len(nova_senha) < 6:
                flash('A nova senha deve ter no mínimo 6 caracteres.', 'erro')
            elif nova_senha != confirmacao:
                flash('A confirmação da nova senha não coincide.', 'erro')
            else:
                user.set_password(nova_senha)
                db.session.commit()
                flash('Senha alterada com sucesso!', 'sucesso')

        return redirect(url_for('prof.perfil'))

    return render_template('prof/perfil.html', user=user)

@prof_bp.route('/prof/bimestre/<int:bimestre>')
@login_required
def planos_bimestre(bimestre):
    user = get_current_user()
    if bimestre not in [1, 2, 3, 4]:
        flash('Bimestre inválido.', 'erro')
        return redirect(url_for('prof.dashboard'))

    busca = request.args.get('q', '').strip()
    query = LessonPlan.query.filter_by(user_id=user.id, bimester=bimestre)

    if busca:
        query = query.filter(
            db.or_(
                LessonPlan.grade.ilike(f'%{busca}%'),
                LessonPlan.selected_lesson_titles.ilike(f'%{busca}%'),
                LessonPlan.contents.ilike(f'%{busca}%'),
                LessonPlan.subject.has(Subject.name.ilike(f'%{busca}%'))
            )
        )

    planos = query.order_by(LessonPlan.created_at.desc()).all()
    return render_template('prof/planos_lista.html', user=user, bimestre=bimestre, planos=planos, busca=busca)

@prof_bp.route('/planos/novo')
@login_required
@active_prof_required
def novo_plano():
    user = get_current_user()
    subjects = Subject.query.filter_by(active=True).order_by(Subject.name).all()
    return render_template('prof/plano_form.html', user=user, subjects=subjects, plano=None)

@prof_bp.route('/planos/salvar', methods=['POST'])
@login_required
@active_prof_required
def salvar_plano():
    user = get_current_user()

    plano_id = request.form.get('plano_id')
    subject_id = request.form.get('subject_id')
    education_level = request.form.get('education_level')
    grade = request.form.get('grade')
    bimester = request.form.get('bimester')
    data_inicio_str = request.form.get('data_inicio')
    data_fim_str = request.form.get('data_fim')
    numero_aulas = request.form.get('numero_aulas', 1)
    turmas_selecionadas = request.form.getlist('turmas[]')
    aulas_selecionadas = request.form.getlist('aulas_escopo[]')
    
    # Textos dos blocos
    titulos_aulas = request.form.get('titulos_aulas', '')
    conteudos = request.form.get('conteudos', '')
    objetivos = request.form.get('objetivos', '')
    habilidades = request.form.get('habilidades', '')
    aes = request.form.get('aes', '')
    recursos = request.form.get('recursos', '')
    metodologia = request.form.get('metodologia', '')
    avaliacao = request.form.get('avaliacao', '')

    # Validações básicas
    if not subject_id or not education_level or not grade or not bimester or not data_inicio_str or not data_fim_str:
        flash('Por favor, preencha todos os campos obrigatórios do cabeçalho.', 'erro')
        return redirect(url_for('prof.novo_plano'))

    try:
        start_date = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Formato de data inválido.', 'erro')
        return redirect(url_for('prof.novo_plano'))

    if plano_id:
        # Edição
        plano = LessonPlan.query.filter_by(id=plano_id, user_id=user.id).first_or_404()
    else:
        # Novo Plano
        plano = LessonPlan(user_id=user.id)
        db.session.add(plano)

    plano.subject_id = int(subject_id)
    plano.education_level = education_level
    plano.grade = grade
    plano.bimester = int(bimester)
    plano.start_date = start_date
    plano.end_date = end_date
    plano.number_of_lessons = int(numero_aulas) if numero_aulas else 1
    
    plano.selected_lesson_titles = titulos_aulas
    plano.contents = conteudos
    plano.objectives = objetivos
    plano.skills = habilidades
    plano.essential_learnings = aes
    plano.resources = recursos
    plano.methodology = metodologia
    plano.evaluation = avaliacao

    # Atualizar turmas
    plano.classes.clear()
    for turma in turmas_selecionadas:
        if turma.strip():
            plano.classes.append(LessonPlanClass(class_name=turma.strip()))

    # Atualizar aulas vinculadas
    plano.lessons.clear()
    for aula_id in aulas_selecionadas:
        if aula_id.strip():
            plano.lessons.append(LessonPlanLesson(scope_lesson_id=int(aula_id)))

    db.session.commit()
    flash('Plano de aula salvo com sucesso!', 'sucesso')
    return redirect(url_for('prof.visualizar_plano', id=plano.id))

@prof_bp.route('/planos/<int:id>')
@login_required
def visualizar_plano(id):
    user = get_current_user()
    if user.role == 'admin':
        plano = db.get_or_404(LessonPlan, id)
    else:
        plano = LessonPlan.query.filter_by(id=id, user_id=user.id).first_or_404()

    return render_template('prof/plano_view.html', user=user, plano=plano)

@prof_bp.route('/planos/<int:id>/editar')
@login_required
@active_prof_required
def editar_plano(id):
    user = get_current_user()
    plano = LessonPlan.query.filter_by(id=id, user_id=user.id).first_or_404()
    subjects = Subject.query.filter_by(active=True).order_by(Subject.name).all()
    return render_template('prof/plano_form.html', user=user, subjects=subjects, plano=plano)

@prof_bp.route('/planos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_plano(id):
    user = get_current_user()
    if user.role == 'admin':
        plano = db.get_or_404(LessonPlan, id)
    else:
        plano = LessonPlan.query.filter_by(id=id, user_id=user.id).first_or_404()

    bimestre = plano.bimester
    db.session.delete(plano)
    db.session.commit()
    flash('Plano de aula excluído com sucesso.', 'sucesso')
    return redirect(url_for('prof.planos_bimestre', bimestre=bimestre))

@prof_bp.route('/planos/<int:id>/pdf')
@login_required
def exportar_pdf(id):
    user = get_current_user()
    if user.role == 'admin':
        plano = db.get_or_404(LessonPlan, id)
    else:
        plano = LessonPlan.query.filter_by(id=id, user_id=user.id).first_or_404()

    pdf_buffer = generate_lesson_plan_pdf(plano)
    filename = f"Plano_de_Aula_{plano.subject.name}_{plano.grade.replace(' ', '_')}_{plano.bimester}Bim.pdf"
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )
