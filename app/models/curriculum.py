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

    def to_dict(self):
        return {
            'id': self.id,
            'subject_name': self.subject.name if self.subject else '',
            'education_level': self.education_level,
            'grade': self.grade,
            'document_year': self.document_year,
            'file_name': self.file_name,
            'total_lessons': self.total_lessons,
            'status': self.status,
            'imported_at': self.imported_at.strftime('%d/%m/%Y %H:%M') if self.imported_at else ''
        }


class ScopeLesson(db.Model):
    __tablename__ = 'scope_lessons'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    education_level = db.Column(db.Enum('fundamental', 'medio', name='education_levels'), nullable=False)
    grade = db.Column(db.String(50), nullable=False)           # Ex: '1ª Série', '8º Ano'
    bimester = db.Column(db.Integer, nullable=False)            # 1, 2, 3, 4
    lesson_number = db.Column(db.Integer, nullable=False)       # 1, 2, 3...
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    learning_objectives = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(255), nullable=True)           # Ex: 'EM13CHS101'
    essential_learning_code = db.Column(db.String(50), nullable=True) # Ex: 'AE1'
    essential_learning = db.Column(db.Text, nullable=True)      # Texto descritivo da AE
    year = db.Column(db.Integer, nullable=False, default=2026)

    __table_args__ = (
        db.UniqueConstraint(
            'subject_id', 'education_level', 'grade', 'bimester', 'lesson_number', 'year',
            name='uq_scope_lesson_entry'
        ),
    )

    subject = db.relationship('Subject', back_populates='lessons')
    plan_lessons = db.relationship('LessonPlanLesson', back_populates='scope_lesson', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else '',
            'education_level': self.education_level,
            'grade': self.grade,
            'bimester': self.bimester,
            'lesson_number': self.lesson_number,
            'title': self.title,
            'content': self.content,
            'learning_objectives': self.learning_objectives,
            'skills': self.skills or '',
            'essential_learning_code': self.essential_learning_code or '',
            'essential_learning': self.essential_learning or '',
            'year': self.year
        }

