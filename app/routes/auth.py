import secrets
import hashlib
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User
from app.services.auth_service import login_user, logout_user, get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('prof.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('prof.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('senha', '')

        if not email or not password:
            flash('Por favor, informe o e-mail e a senha.', 'erro')
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('E-mail ou senha inválidos.', 'erro')
            return render_template('auth/login.html')

        # Realizar Login
        login_user(user)

        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('prof.dashboard'))

    return render_template('auth/login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        telefone = request.form.get('telefone', '').strip()
        senha = request.form.get('senha', '')
        confirmacao = request.form.get('confirmacao', '')

        # Validações
        if not nome or not email or not senha:
            flash('Preencha todos os campos obrigatórios.', 'erro')
            return redirect(url_for('auth.login') + '#cadastrar')

        if confirmacao and senha != confirmacao:
            flash('A senha e a confirmação de senha não coincidem.', 'erro')
            return redirect(url_for('auth.login') + '#cadastrar')

        # Verificar duplicidade de e-mail
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado no sistema.', 'erro')
            return redirect(url_for('auth.login') + '#cadastrar')

        # Criar professor pendente
        novo_usuario = User(
            name=nome,
            email=email,
            phone=telefone,
            role='professor',
            status='pendente'
        )
        novo_usuario.set_password(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Seu acesso foi criado com status pendente de aprovação pelo administrador.', 'sucesso')
        return redirect(url_for('auth.login', cadastro='enviado'))

    return redirect(url_for('auth.login') + '#cadastrar')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Você saiu do sistema com segurança.', 'sucesso')
    return redirect(url_for('auth.login'))

@auth_bp.route('/esqueci-senha', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        user = User.query.filter_by(email=email).first()
        if user:
            # Gerar token seguro
            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            user.reset_token_hash = token_hash
            user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
            
            # Link de redefinição
            reset_url = url_for('auth.reset_password', token=raw_token, _external=True)
            # Em ambiente de dev / log
            print(f"[AUTH] Link de redefinição para {email}: {reset_url}")
            flash(f'Instruções enviadas! (Em ambiente local, use o link: {reset_url})', 'sucesso')
        else:
            flash('Se o e-mail estiver cadastrado, você receberá as instruções para redefinir sua senha.', 'aviso')
            
        return render_template('auth/forgot_password.html', enviado=True)

    return render_template('auth/forgot_password.html')

@auth_bp.route('/redefinir-senha', methods=['GET', 'POST'])
def reset_password():
    raw_token = request.args.get('token') or request.form.get('token')
    if not raw_token:
        flash('Token de redefinição ausente ou inválido.', 'erro')
        return redirect(url_for('auth.login'))

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    user = User.query.filter(
        User.reset_token_hash == token_hash,
        User.reset_token_expires_at > datetime.utcnow()
    ).first()

    if not user:
        flash('O link de redefinição de senha expirou ou é inválido.', 'erro')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha', '')
        confirmacao = request.form.get('confirmacao', '')

        if not nova_senha or len(nova_senha) < 6:
            flash('A nova senha deve ter no mínimo 6 caracteres.', 'erro')
            return render_template('auth/reset_password.html', token=raw_token)

        if nova_senha != confirmacao:
            flash('A confirmação de senha não coincide.', 'erro')
            return render_template('auth/reset_password.html', token=raw_token)

        user.set_password(nova_senha)
        user.reset_token_hash = None
        user.reset_token_expires_at = None
        db.session.commit()

        flash('Senha redefinida com sucesso! Você já pode fazer login.', 'sucesso')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=raw_token)

