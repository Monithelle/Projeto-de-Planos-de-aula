import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from app.models import db, User, Subject, CurriculumDocument, ScopeLesson, LessonPlan
from app.services.auth_service import admin_required, get_current_user
from app.services.pdf_parser import CurriculumPdfParser, SUBJECT_NAMES

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def dashboard():
    user = get_current_user()

    total_professores = User.query.filter_by(role='professor').count()
    total_arquivos = CurriculumDocument.query.count()
    total_pendentes = User.query.filter_by(role='professor', status='pendente').count()

    # Professores e seus planos agrupados
    professores_raw = User.query.filter_by(role='professor').all()
    professores_cards = []

    for prof in professores_raw:
        planos = LessonPlan.query.filter_by(user_id=prof.id).all()
        # Matérias distintas com planos
        materias = list(set([p.subject.name for p in planos if p.subject]))
        
        professores_cards.append({
            'id': prof.id,
            'nome': prof.name,
            'email': prof.email,
            'status': prof.status,
            'total_planos': len(planos),
            'materias': materias,
            'criado_em': prof.created_at.strftime('%d/%m/%Y') if prof.created_at else ''
        })

    resumo = {
        'professores': total_professores,
        'arquivos': total_arquivos,
        'pendentes': total_pendentes
    }

    return render_template(
        'admin/dashboard.html',
        user=user,
        resumo=resumo,
        professores=professores_cards
    )

@admin_bp.route('/perfil', methods=['GET', 'POST'])
@admin_required
def perfil():
    user = get_current_user()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            nome = request.form.get('nome', '').strip()
            email = request.form.get('email', '').strip().lower()

            if not nome or not email:
                flash('Nome e e-mail são obrigatórios.', 'erro')
            else:
                existente = User.query.filter(User.email == email, User.id != user.id).first()
                if existente:
                    flash('Este e-mail já está em uso.', 'erro')
                else:
                    user.name = nome
                    user.email = email
                    db.session.commit()
                    session['name'] = user.name
                    session['email'] = user.email
                    flash('Perfil administrativo atualizado com sucesso!', 'sucesso')

        elif action == 'change_password':
            senha_atual = request.form.get('senha_atual', '')
            nova_senha = request.form.get('nova_senha', '')
            confirmacao = request.form.get('confirmacao', '')

            if not user.check_password(senha_atual):
                flash('A senha atual está incorreta.', 'erro')
            elif not nova_senha or len(nova_senha) < 6:
                flash('A nova senha deve ter no mínimo 6 caracteres.', 'erro')
            elif nova_senha != confirmacao:
                flash('A confirmação da nova senha não coincide.', 'erro')
            else:
                user.set_password(nova_senha)
                db.session.commit()
                flash('Senha do administrador alterada com sucesso!', 'sucesso')

        return redirect(url_for('admin.perfil'))

    return render_template('admin/perfil.html', user=user)

@admin_bp.route('/professores')
@admin_required
def professores():
    user = get_current_user()
    busca = request.args.get('busca', '').strip()

    query = User.query.filter_by(role='professor')
    if busca:
        query = query.filter(
            db.or_(
                User.name.ilike(f'%{busca}%'),
                User.email.ilike(f'%{busca}%'),
                User.phone.ilike(f'%{busca}%')
            )
        )

    lista = query.order_by(User.created_at.desc()).all()
    professores_info = []

    for p in lista:
        total_p = LessonPlan.query.filter_by(user_id=p.id).count()
        professores_info.append({
            'id': p.id,
            'nome': p.name,
            'email': p.email,
            'telefone': p.phone or '-',
            'status': p.status,
            'total_planos': total_p,
            'criado_em': p.created_at.strftime('%d/%m/%Y') if p.created_at else ''
        })

    return render_template('admin/professores.html', user=user, professores=professores_info, busca=busca)

@admin_bp.route('/cadastros')
@admin_required
def cadastros():
    user = get_current_user()
    pendentes = User.query.filter_by(role='professor', status='pendente').order_by(User.created_at.desc()).all()
    return render_template('admin/cadastros.html', user=user, pendentes=pendentes)

@admin_bp.route('/cadastros/<int:id>/aprovar', methods=['POST'])
@admin_required
def aprovar_cadastro(id):
    admin_user = get_current_user()
    professor = User.query.filter_by(id=id, role='professor').first_or_404()

    professor.status = 'ativo'
    professor.approved_at = datetime.utcnow()
    professor.approved_by = admin_user.id
    db.session.commit()

    flash(f'O cadastro do professor(a) {professor.name} foi aprovado com sucesso!', 'sucesso')
    return redirect(url_for('admin.cadastros'))

@admin_bp.route('/cadastros/<int:id>/recusar', methods=['POST'])
@admin_required
def recusar_cadastro(id):
    professor = User.query.filter_by(id=id, role='professor').first_or_404()
    nome = professor.name
    db.session.delete(professor)
    db.session.commit()

    flash(f'A solicitação de cadastro de {nome} foi recusada e removida.', 'aviso')
    return redirect(url_for('admin.cadastros'))

@admin_bp.route('/arquivos')
@admin_required
def arquivos():
    user = get_current_user()
    docs = CurriculumDocument.query.order_by(CurriculumDocument.imported_at.desc()).all()
    subjects = Subject.query.filter_by(active=True).order_by(Subject.name).all()
    return render_template('admin/arquivos.html', user=user, documentos=docs, subjects=subjects)

@admin_bp.route('/arquivos/preview-pdf', methods=['POST'])
@admin_required
def preview_pdf():
    file = request.files.get('pdf_file')
    if not file or not file.filename.endswith('.pdf'):
        flash('Por favor, selecione um arquivo no formato PDF.', 'erro')
        return redirect(url_for('admin.arquivos'))

    # Salvar temporariamente para análise
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    timestamped_filename = f"upload_{int(datetime.utcnow().timestamp())}_{filename}"
    filepath = os.path.join(upload_dir, timestamped_filename)
    file.save(filepath)

    try:
        parser = CurriculumPdfParser(filepath)
        detected_meta = parser.detect_metadata()
        
        # Permitir sobrescrita dos metadados se o formulário enviar
        subject_override = request.form.get('subject_name')
        level_override = request.form.get('education_level')
        grade_override = request.form.get('grade')
        year_override = request.form.get('document_year')

        meta = {
            'subject_name': subject_override or detected_meta['subject_name'],
            'education_level': level_override or detected_meta['education_level'],
            'grade': grade_override or detected_meta['grade'],
            'document_year': int(year_override) if year_override else detected_meta['document_year']
        }

        # Extrair aulas
        aulas = parser.extract_scope_lessons(metadata=meta)
        
        # Encontrar ou associar Subject no banco
        subject = Subject.query.filter_by(name=meta['subject_name'], education_level=meta['education_level']).first()
        if not subject:
            subject = Subject(name=meta['subject_name'], education_level=meta['education_level'], active=True)
            db.session.add(subject)
            db.session.commit()

        # Calcular estatísticas de validação
        total_identificadas = len(aulas)
        duplicidades = 0
        validas = 0

        for a in aulas:
            existente = ScopeLesson.query.filter_by(
                subject_id=subject.id,
                education_level=meta['education_level'],
                grade=meta['grade'],
                bimester=a['bimester'],
                lesson_number=a['lesson_number'],
                year=meta['document_year']
            ).first()
            if existente:
                duplicidades += 1
            else:
                validas += 1

        resumo_importacao = {
            'total_identificadas': total_identificadas,
            'validas': validas,
            'duplicidades': duplicidades,
            'erros': 0
        }

        return render_template(
            'admin/preview_pdf.html',
            meta=meta,
            subject=subject,
            aulas=aulas,
            resumo=resumo_importacao,
            temp_filename=timestamped_filename,
            original_filename=filename,
            all_subjects=SUBJECT_NAMES
        )

    except Exception as e:
        flash(f'Erro ao processar o PDF: {str(e)}', 'erro')
        return redirect(url_for('admin.arquivos'))

@admin_bp.route('/arquivos/confirmar-importacao', methods=['POST'])
@admin_required
def confirmar_importacao():
    temp_filename = request.form.get('temp_filename')
    original_filename = request.form.get('original_filename', 'curriculo.pdf')
    subject_id = request.form.get('subject_id')
    education_level = request.form.get('education_level')
    grade = request.form.get('grade')
    document_year = int(request.form.get('document_year', 2026))
    
    aulas_json = request.form.get('aulas_json')

    if not temp_filename or not aulas_json:
        flash('Dados de importação incompletos.', 'erro')
        return redirect(url_for('admin.arquivos'))

    try:
        aulas = json.loads(aulas_json)
        subject = db.get_or_404(Subject, int(subject_id))

        novas_aulas = 0
        atualizadas = 0

        for a in aulas:
            existente = ScopeLesson.query.filter_by(
                subject_id=subject.id,
                education_level=education_level,
                grade=grade,
                bimester=int(a['bimester']),
                lesson_number=int(a['lesson_number']),
                year=document_year
            ).first()

            if existente:
                existente.title = a['title']
                existente.content = a['content']
                existente.learning_objectives = a['learning_objectives']
                existente.skills = a.get('skills', '')
                existente.essential_learning_code = a.get('essential_learning_code', '')
                existente.essential_learning = a.get('essential_learning', '')
                atualizadas += 1
            else:
                nova = ScopeLesson(
                    subject_id=subject.id,
                    education_level=education_level,
                    grade=grade,
                    bimester=int(a['bimester']),
                    lesson_number=int(a['lesson_number']),
                    title=a['title'],
                    content=a['content'],
                    learning_objectives=a['learning_objectives'],
                    skills=a.get('skills', ''),
                    essential_learning_code=a.get('essential_learning_code', ''),
                    essential_learning=a.get('essential_learning', ''),
                    year=document_year
                )
                db.session.add(nova)
                novas_aulas += 1

        # Registrar documento importado
        doc = CurriculumDocument(
            subject_id=subject.id,
            education_level=education_level,
            grade=grade,
            document_year=document_year,
            file_name=original_filename,
            file_path=os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename),
            total_lessons=len(aulas),
            status='processado'
        )
        db.session.add(doc)
        db.session.commit()

        flash(f'Importação concluída com sucesso! {novas_aulas} novas aulas inseridas e {atualizadas} atualizadas.', 'sucesso')
    except Exception as e:
        db.session.rollback()
        flash(f'Falha ao gravar registros no banco de dados: {str(e)}', 'erro')

    return redirect(url_for('admin.arquivos'))

@admin_bp.route('/professores/<int:id>/planos')
@admin_required
def professor_planos(id):
    user = get_current_user()
    professor = User.query.filter_by(id=id, role='professor').first_or_404()
    
    # Filtros
    tipo_ensino = request.args.get('ensino', '')
    ano_serie = request.args.get('grade', '')
    turma = request.args.get('turma', '')
    data_inicio_str = request.args.get('data_inicio', '')
    data_fim_str = request.args.get('data_fim', '')

    query = LessonPlan.query.filter_by(user_id=professor.id)

    if tipo_ensino:
        query = query.filter_by(education_level=tipo_ensino)
    if ano_serie:
        query = query.filter_by(grade=ano_serie)
    if turma:
        query = query.join(LessonPlan.classes).filter(LessonPlanClass.class_name == turma)
    if data_inicio_str:
        try:
            d_ini = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            query = query.filter(LessonPlan.start_date >= d_ini)
        except ValueError:
            pass
    if data_fim_str:
        try:
            d_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
            query = query.filter(LessonPlan.end_date <= d_fim)
        except ValueError:
            pass

    planos = query.order_by(LessonPlan.bimester, LessonPlan.created_at.desc()).all()

    # Organização hierárquica por Bimestre -> Segmento -> Componente
    estrutura_planos = {1: {'fundamental': {}, 'medio': {}},
                        2: {'fundamental': {}, 'medio': {}},
                        3: {'fundamental': {}, 'medio': {}},
                        4: {'fundamental': {}, 'medio': {}}}

    for p in planos:
        bim = p.bimester
        segmento = p.education_level
        mat = p.subject.name if p.subject else 'Outros'

        if mat not in estrutura_planos[bim][segmento]:
            estrutura_planos[bim][segmento][mat] = []
        estrutura_planos[bim][segmento][mat].append(p)

    return render_template(
        'admin/professor_planos.html',
        user=user,
        professor=professor,
        estrutura=estrutura_planos,
        total_encontrados=len(planos),
        filtros={
            'ensino': tipo_ensino,
            'grade': ano_serie,
            'turma': turma,
            'data_inicio': data_inicio_str,
            'data_fim': data_fim_str
        }
    )
