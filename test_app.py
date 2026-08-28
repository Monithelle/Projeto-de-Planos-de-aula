import io
import unittest
from datetime import date
from app import create_app
from app.models import db, User, Subject, ScopeLesson, LessonPlan, LessonPlanClass, LessonPlanLesson
from app.services.pdf_exporter import generate_lesson_plan_pdf
from app.services.pdf_parser import CurriculumPdfParser

class TestPlanoDeAula(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_database_and_seeds(self):
        """Verifica se as tabelas e dados iniciais foram criados"""
        admin = User.query.filter_by(role='admin').first()
        self.assertIsNotNone(admin)
        self.assertTrue(admin.check_password('Admin@123456'))

        prof = User.query.filter_by(email='professor@escola.sp.gov.br').first()
        self.assertIsNotNone(prof)
        self.assertEqual(prof.status, 'ativo')

        # Verificar aulas de Filosofia no Escopo
        filo_aulas = ScopeLesson.query.filter_by(education_level='medio', grade='1ª Série').all()
        self.assertGreater(len(filo_aulas), 0)
        print(f"[TEST] Total de aulas de Filosofia carregadas: {len(filo_aulas)}")

    def test_auth_routes(self):
        """Testa fluxos de autenticação"""
        # Login com credenciais válidas
        res = self.client.post('/login', data={'email': 'professor@escola.sp.gov.br', 'senha': 'Prof@123456'}, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn('/prof', res.headers['Location'])

        # Deslogar antes do próximo teste
        self.client.get('/logout')

        # Login com senha incorreta
        res_fail = self.client.post('/login', data={'email': 'professor@escola.sp.gov.br', 'senha': 'errada'}, follow_redirects=True)
        self.assertIn('E-mail ou senha', res_fail.data.decode('utf-8'))

    def test_api_escopo_and_details(self):
        """Testa os endpoints de consulta do escopo e agregação de dados"""
        subj = Subject.query.filter_by(name='Filosofia', education_level='medio').first()
        self.assertIsNotNone(subj)

        # GET /api/escopo
        res = self.client.get(f'/api/escopo?subject_id={subj.id}&grade=1ª Série&bimester=1&education_level=medio')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertGreater(len(data), 0)
        print(f"[TEST] /api/escopo retornou {len(data)} aulas para o 1º Bimestre de Filosofia")

        # POST /api/detalhes-aulas
        lesson_ids = [data[0]['id'], data[1]['id']]
        res_details = self.client.post('/api/detalhes-aulas', json={'lesson_ids': lesson_ids})
        self.assertEqual(res_details.status_code, 200)
        detalhes = res_details.get_json()
        self.assertIn('Aula 1', detalhes['titulos'])
        self.assertIn('EM13CHS101', detalhes['habilidades'])
        self.assertIn('AE1', detalhes['aes'])

    def test_pdf_export(self):
        """Testa a geração de PDF oficial com ReportLab"""
        plan = LessonPlan.query.first()
        self.assertIsNotNone(plan)

        pdf_io = generate_lesson_plan_pdf(plan)
        self.assertIsInstance(pdf_io, io.BytesIO)
        pdf_bytes = pdf_io.getvalue()
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertTrue(pdf_bytes.startswith(b'%PDF'))
        print(f"[TEST] PDF do plano de aula gerado com sucesso! Tamanho: {len(pdf_bytes)} bytes")

    def test_pending_user_restrictions(self):
        """Verifica restrição no backend para professor com status pendente"""
        # Login como professor pendente
        self.client.post('/login', data={'email': 'mariana.silva@escola.sp.gov.br', 'senha': 'Mariana@123'}, follow_redirects=True)
        
        # Tentar acessar rota de novo plano
        res_novo = self.client.get('/planos/novo', follow_redirects=False)
        self.assertEqual(res_novo.status_code, 302)
        self.assertIn('/prof', res_novo.headers['Location'])
        print("[TEST] Professor pendente bloqueado com sucesso de acessar /planos/novo!")

if __name__ == '__main__':
    unittest.main()

