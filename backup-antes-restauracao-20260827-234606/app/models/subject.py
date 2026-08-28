from . import db

class Subject(db.Model):
	__tablename__ = 'subjects'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	education_level = db.Column(db.Enum('fundamental', 'medio', name='education_levels'), nullable=False)
	active = db.Column(db.Boolean, default=True)
	__table_args__ = (db.UniqueConstraint('name', 'education_level', name='uq_subject_level'),)
	documents = db.relationship('CurriculumDocument', back_populates='subject', lazy='dynamic', cascade='all, delete-orphan')
	lessons = db.relationship('ScopeLesson', back_populates='subject', lazy='dynamic', cascade='all, delete-orphan')
	plans = db.relationship('LessonPlan', back_populates='subject', lazy='dynamic')

	def to_dict(self):
		return {'id': self.id, 'name': self.name, 'education_level': self.education_level, 'active': self.active}
