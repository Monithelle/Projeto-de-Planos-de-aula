from datetime import datetime
import re
from . import db


def format_class_name(class_name: str, education_level: str) -> str:
    if not class_name:
        return class_name
    if education_level == 'medio' and re.match(r'^\d+[ªº] [A-F]$', class_name):
        return class_name.replace('ª ', 'ª Série ').replace('º ', 'º Série ')
    if education_level == 'fundamental' and re.match(r'^\d+[ªº] [A-F]$', class_name):
        return class_name.replace('ª ', 'ª Ano ').replace('º ', 'º Ano ')
    return class_name

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
    
    # Preenchimentos automáticos / agregados
    selected_lesson_titles = db.Column(db.Text, nullable=True)
    contents = db.Column(db.Text, nullable=True)
    objectives = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    essential_learnings = db.Column(db.Text, nullable=True)
    
    # Preenchimentos manuais do professor
    resources = db.Column(db.Text, nullable=True)
    methodology = db.Column(db.Text, nullable=True)
    evaluation = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='plans')
    subject = db.relationship('Subject', back_populates='plans')
    classes = db.relationship('LessonPlanClass', back_populates='plan', cascade='all, delete-orphan')
    lessons = db.relationship('LessonPlanLesson', back_populates='plan', cascade='all, delete-orphan')

    @property
    def classes_formatted(self) -> str:
        return ', '.join(
            format_class_name(class_item.class_name, self.education_level)
            for class_item in self.classes
        )

    @property
    def period_formatted(self) -> str:
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%d/%m/%Y')} até {self.end_date.strftime('%d/%m/%Y')}"
        return ""

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'professor_name': self.user.name if self.user else '',
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else '',
            'education_level': self.education_level,
            'grade': self.grade,
            'bimester': self.bimester,
            'turmas': [
                format_class_name(class_item.class_name, self.education_level)
                for class_item in self.classes
            ],
            'turmas_texto': self.classes_formatted,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else '',
            'periodo': self.period_formatted,
            'number_of_lessons': self.number_of_lessons,
            'selected_lesson_titles': self.selected_lesson_titles or '',
            'contents': self.contents or '',
            'objectives': self.objectives or '',
            'skills': self.skills or '',
            'essential_learnings': self.essential_learnings or '',
            'resources': self.resources or '',
            'methodology': self.methodology or '',
            'evaluation': self.evaluation or '',
            'selected_lesson_ids': [l.scope_lesson_id for l in self.lessons],
            'created_at': self.created_at.strftime('%d/%m/%Y') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M') if self.updated_at else ''
        }


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

