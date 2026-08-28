from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .subject import Subject
from .curriculum import CurriculumDocument, ScopeLesson
from .lesson_plan import LessonPlan, LessonPlanClass, LessonPlanLesson

