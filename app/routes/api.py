from flask import Blueprint, request, jsonify
from app.models import Subject, ScopeLesson

api_bp = Blueprint('api', __name__, url_prefix='/api')

FUNDAMENTAL_SUBJECTS = [
    'Ciências', 'Língua Portuguesa', 'Arte', 'Educação Física',
    'Língua Inglesa', 'Matemática', 'Geografia', 'História'
]

MEDIO_SUBJECTS = [
    'Língua Portuguesa', 'Arte', 'Educação Física', 'Língua Inglesa',
    'Matemática', 'Geografia', 'História', 'Sociologia',
    'Filosofia', 'Biologia', 'Física', 'Química'
]

@api_bp.route('/materias')
def get_materias():
    ensino = request.args.get('ensino', 'medio').lower()
    
    query = Subject.query.filter_by(education_level=ensino, active=True).order_by(Subject.name)
    subjects = query.all()
    
    return jsonify([s.to_dict() for s in subjects])

@api_bp.route('/series')
def get_series():
    ensino = request.args.get('ensino', 'medio').lower()
    if ensino == 'fundamental':
        series = ['6º Ano', '7º Ano', '8º Ano', '9º Ano']
    else:
        series = ['1ª Série', '2ª Série', '3ª Série']
    return jsonify(series)

@api_bp.route('/turmas')
def get_turmas():
    grade = request.args.get('grade', '')
    ensino = request.args.get('ensino', 'medio')
    
    # Gerar turmas A..F baseadas no ano/série
    letras = ['A', 'B', 'C', 'D', 'E', 'F']
    turmas = []
    
    prefix = grade if grade else ('1ª' if ensino == 'medio' else '6º')
    # Se já tiver 'Série' ou 'Ano', extrair o número/ordem
    prefix_clean = prefix.replace(' Série', 'ª').replace(' Ano', 'º')
    
    for l in letras:
        turmas.append({
            'value': f"{prefix_clean} {l}",
            'label': f"{prefix_clean} {l}"
        })
        
    return jsonify(turmas)

@api_bp.route('/escopo')
def get_escopo():
    subject_id = request.args.get('subject_id')
    education_level = request.args.get('education_level')
    grade = request.args.get('grade')
    bimester = request.args.get('bimester')

    if not subject_id or not bimester:
        return jsonify([])

    query = ScopeLesson.query.filter_by(
        subject_id=int(subject_id),
        bimester=int(bimester)
    )

    if education_level:
        query = query.filter_by(education_level=education_level)
    if grade:
        query = query.filter_by(grade=grade)

    lessons = query.order_by(ScopeLesson.lesson_number).all()
    return jsonify([l.to_dict() for l in lessons])

@api_bp.route('/detalhes-aulas', methods=['POST'])
def get_detalhes_aulas():
    data = request.get_json() or {}
    lesson_ids = data.get('lesson_ids', [])

    if not lesson_ids:
        return jsonify({
            'titulos': '',
            'conteudos': '',
            'objetivos': '',
            'habilidades': '',
            'aes': ''
        })

    lessons = ScopeLesson.query.filter(ScopeLesson.id.in_(lesson_ids)).order_by(ScopeLesson.lesson_number).all()

    titulos_list = []
    conteudos_list = []
    objetivos_list = []
    habilidades_set = []
    aes_set = []

    for l in lessons:
        # Título
        titulos_list.append(f"Aula {l.lesson_number} - {l.title}")

        # Conteúdo
        if l.content:
            conteudos_list.append(f"• Aula {l.lesson_number}: {l.content}")

        # Objetivos
        if l.learning_objectives:
            objetivos_list.append(f"• Aula {l.lesson_number}:\n{l.learning_objectives}")

        # Habilidades (Deduplicação mantendo ordem)
        if l.skills:
            for s in [x.strip() for x in l.skills.split(',') if x.strip()]:
                if s not in habilidades_set:
                    habilidades_set.append(s)

        # Aprendizagens Essenciais (Deduplicação mantendo ordem)
        if l.essential_learning:
            ae_text = l.essential_learning.strip()
            if ae_text not in aes_set:
                aes_set.append(ae_text)

    return jsonify({
        'titulos': "\n".join(titulos_list),
        'conteudos': "\n\n".join(conteudos_list),
        'objetivos': "\n\n".join(objetivos_list),
        'habilidades': ", ".join(habilidades_set),
        'aes': "\n\n".join(aes_set)
    })

