from functools import wraps
from flask import session, redirect, url_for, flash, abort, request, jsonify
from app.models import db, User

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.session.get(User, user_id)

def login_user(user: User):
    session.clear()
    session['user_id'] = user.id
    session['name'] = user.name
    session['email'] = user.email
    session['role'] = user.role
    session['status'] = user.status

def logout_user():
    session.clear()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Não autenticado'}), 401
            flash('Por favor, faça login para acessar esta página.', 'aviso')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Acesso restrito. Faça login como administrador.', 'aviso')
            return redirect(url_for('auth.login'))
        
        user = get_current_user()
        if not user or user.role != 'admin':
            if request.is_json:
                return jsonify({'error': 'Acesso não autorizado'}), 403
            flash('Você não tem permissão para acessar o painel administrativo.', 'erro')
            return redirect(url_for('prof.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def active_prof_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login.', 'aviso')
            return redirect(url_for('auth.login'))
        
        user = get_current_user()
        if not user:
            session.clear()
            return redirect(url_for('auth.login'))

        # Admins can bypass, but professors must be 'ativo'
        if user.role != 'admin' and user.status != 'ativo':
            if request.is_json:
                return jsonify({'error': 'Cadastro pendente de aprovação pelo administrador.'}), 403
            flash('Seu cadastro está aguardando confirmação do administrador. A criação e salvamento de planos será liberada após a aprovação.', 'aviso')
            return redirect(url_for('prof.dashboard'))
            
        return f(*args, **kwargs)
    return decorated_function
