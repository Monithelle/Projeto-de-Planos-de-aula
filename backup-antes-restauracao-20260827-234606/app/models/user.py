from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(191), unique=True, nullable=False, index=True)
	phone = db.Column(db.String(30), nullable=True)
	password_hash = db.Column(db.String(255), nullable=False)
	role = db.Column(db.Enum('admin', 'professor', name='user_roles'), default='professor', nullable=False)
	status = db.Column(db.Enum('pendente', 'ativo', name='user_statuses'), default='pendente', nullable=False)
	reset_token_hash = db.Column(db.String(255), nullable=True)
	reset_token_expires_at = db.Column(db.DateTime, nullable=True)
	approved_at = db.Column(db.DateTime, nullable=True)
	approved_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	plans = db.relationship('LessonPlan', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
	approver = db.relationship('User', remote_side=[id], backref='approved_users')

	def set_password(self, password: str):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)

	@property
	def is_admin(self) -> bool:
		return self.role == 'admin'

	@property
	def is_active_prof(self) -> bool:
		return self.role == 'professor' and self.status == 'ativo'

	def to_dict(self):
		return {
			'id': self.id, 'name': self.name, 'email': self.email, 'phone': self.phone,
			'role': self.role, 'status': self.status,
			'created_at': self.created_at.strftime('%d/%m/%Y') if self.created_at else '',
			'approved_at': self.approved_at.strftime('%d/%m/%Y %H:%M') if self.approved_at else ''
		}
