from datetime import datetime
from . import db

class LessonPlan(db.Model):
	__tablename__ = 'lesson_plans'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
	subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='RESTRICT'), nullable=False)
	education_level = db.Column(db.Enum('fundamental', 'medio', name='education_levels'), nullable=False)
	grade = db.Column(db.String(50), nullable=False)
	bimester = db.Column(db.Integer, nullable=False)
	start_date = db.Column(db.Date, nullable=False)
	end_date = db.Column(db.Date, nullable=False)
	number_of_lessons = db.Column(db.Integer, nullable=False, default=1)
	selected_lesson_titles = db.Column(db.Text, nullable=True)
	contents = db.Column(db.Text, nullable=True)
	objectives = db.Column(db.Text, nullable=True)
	skills = db.Column(db.Text, nullable=True)
	essential_learnings = db.Column(db.Text, nullable=True)
	resources = db.Column(db.Text, nullable=True)
	methodology = db.Column(db.Text, nullable=True)
	evaluation = db.Column(db.Text, nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
	user = db.relationship('User', back_populates='plans')
	subject = db.relationship('Subject', back_populates='plans')
	classes = db.relationship('LessonPlanClass', back_populates='plan', cascade='all, delete-orphan')
	lessons = db.relationship('LessonPlanLesson', back_populates='plan', cascade='all, delete-orphan')

class LessonPlanClass(db.Model):
	__tablename__ = 'lesson_plan_classes'
	id = db.Column(db.Integer, primary_key=True)
	lesson_plan_id = db.Column(db.Integer, db.ForeignKey('lesson_plans.id', ondelete='CASCADE'), nullable=False)
	class_name = db.Column(db.String(20), nullable=False)
	plan = db.relationship('LessonPlan', back_populates='classes')

class LessonPlanLesson(db.Model):
	__tablename__ = 'lesson_plan_lessons'
	id = db.Column(db.Integer, primary_key=True)
	lesson_plan_id = db.Column(db.Integer, db.ForeignKey('lesson_plans.id', ondelete='CASCADE'), nullable=False)
	scope_lesson_id = db.Column(db.Integer, db.ForeignKey('scope_lessons.id', ondelete='RESTRICT'), nullable=False)
	plan = db.relationship('LessonPlan', back_populates='lessons')
	scope_lesson = db.relationship('ScopeLesson', back_populates='plan_lessons')
