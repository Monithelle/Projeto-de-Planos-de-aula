from datetime import datetime
from . import db

class CurriculumDocument(db.Model):
	__tablename__ = 'curriculum_documents'
	id = db.Column(db.Integer, primary_key=True)
	subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
	education_level = db.Column(db.Enum('fundamental', 'medio', name='education_levels'), nullable=False)
	grade = db.Column(db.String(50), nullable=False)
	document_year = db.Column(db.Integer, nullable=False, default=2026)
	file_name = db.Column(db.String(255), nullable=False)
	file_path = db.Column(db.String(500), nullable=False)
	total_lessons = db.Column(db.Integer, default=0)
	status = db.Column(db.Enum('processado', 'erro', name='document_statuses'), default='processado')
	imported_at = db.Column(db.DateTime, default=datetime.utcnow)
	subject = db.relationship('Subject', back_populates='documents')

class ScopeLesson(db.Model):
	__tablename__ = 'scope_lessons'
	id = db.Column(db.Integer, primary_key=True)
	subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
	education_level = db.Column(db.Enum('fundamental', 'medio', name='education_levels'), nullable=False)
	grade = db.Column(db.String(50), nullable=False)
	bimester = db.Column(db.Integer, nullable=False)
	lesson_number = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(255), nullable=False)
	content = db.Column(db.Text, nullable=False)
	learning_objectives = db.Column(db.Text, nullable=False)
	skills = db.Column(db.String(255), nullable=True)
	essential_learning_code = db.Column(db.String(50), nullable=True)
	essential_learning = db.Column(db.Text, nullable=True)
	year = db.Column(db.Integer, nullable=False, default=2026)
	subject = db.relationship('Subject', back_populates='lessons')
	plan_lessons = db.relationship('LessonPlanLesson', back_populates='scope_lesson', lazy='dynamic')
