import os
import sys
import json
from pathlib import Path

# Adicionar pasta raiz ao PATH
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.models import db, User, Subject, ScopeLesson, CurriculumDocument, LessonPlan, LessonPlanClass, LessonPlanLesson
from app.routes.api import FUNDAMENTAL_SUBJECTS, MEDIO_SUBJECTS

def seed_database():
    app = create_app()
    with app.app_context():
        print("Criando tabelas no MySQL...")
        db.create_all()
        print("Tabelas verificadas/criadas com sucesso.")

        # 1. Cadastrar Disciplinas (Ensino Fundamental e Médio)
        for name in FUNDAMENTAL_SUBJECTS:
            if not Subject.query.filter_by(name=name, education_level='fundamental').first():
                db.session.add(Subject(name=name, education_level='fundamental', active=True))

        for name in MEDIO_SUBJECTS:
            if not Subject.query.filter_by(name=name, education_level='medio').first():
                db.session.add(Subject(name=name, education_level='medio', active=True))

        db.session.commit()
        print("Disciplinas cadastradas com sucesso.")

        # 2. Criar Administrador Inicial
        admin_email = app.config.get('ADMIN_EMAIL')
        admin_pass = app.config.get('ADMIN_INITIAL_PASSWORD')
        admin_name = app.config.get('ADMIN_NAME', 'Administrador do Sistema')

        if not admin_email or not admin_pass:
            raise RuntimeError('Defina ADMIN_EMAIL e ADMIN_INITIAL_PASSWORD no arquivo .env antes de executar o seed.')

        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                name=admin_name,
                email=admin_email,
                role='admin',
                status='ativo'
            )
            admin.set_password(admin_pass)
            db.session.add(admin)
            db.session.commit()
            print(f"Administrador criado: {admin_email} / {admin_pass}")

        # 3. Criar Professor de Exemplo (Ativo)
        prof_email = 'professor@escola.sp.gov.br'
        prof = User.query.filter_by(email=prof_email).first()
        if not prof:
            prof = User(
                name='Prof. Carlos Eduardo',
                email=prof_email,
                phone='(11) 98765-4321',
                role='professor',
                status='ativo'
            )
            prof.set_password('Prof@123456')
            db.session.add(prof)
            db.session.commit()
            print(f"Professor de teste criado: {prof_email} / Prof@123456")

        # 4. Criar Professor Pendente de Teste
        prof_pendente = User.query.filter_by(email='mariana.silva@escola.sp.gov.br').first()
        if not prof_pendente:
            prof_pendente = User(
                name='Profa. Mariana Silva',
                email='mariana.silva@escola.sp.gov.br',
                phone='(11) 91234-5678',
                role='professor',
                status='pendente'
            )
            prof_pendente.set_password('Mariana@123')
            db.session.add(prof_pendente)
            db.session.commit()
            print("Professor pendente de teste criado.")

        # 5. Inserir dados oficiais do PDF do Guia do Currículo Priorizado (Filosofia - 1ª Série Ensino Médio 2026)
        subj_filo = Subject.query.filter_by(name='Filosofia', education_level='medio').first()
        if subj_filo:
            # Lista completa das 52 aulas extraídas das tabelas do PDF oficial de Filosofia EM 1ª Série
            filosofia_aulas = [
                # 1º Bimestre (Aulas 1 a 14)
                {
                    'bimester': 1, 'lesson_number': 1,
                    'title': 'Por que filosofia?',
                    'content': 'A filosofia e a formação para a cidadania.',
                    'learning_objectives': '• Identificar e situar a filosofia na formação geral básica.\n• Descrever as expectativas em torno desse componente curricular.\n• Reconhecer a importância do diálogo para a formação filosófica do cidadão.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 2,
                    'title': 'Origens da filosofia',
                    'content': '• As origens da filosofia.\n• Hipóteses sobre o nascimento da filosofia.',
                    'learning_objectives': '• Discutir o espanto e a indagação como condições subjetivas para o desenvolvimento da reflexão filosófica.\n• Problematizar as hipóteses convencionais sobre o contexto histórico do nascimento da filosofia.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 3,
                    'title': 'Atitude filosófica: a exigência pela argumentação',
                    'content': '• A atitude filosófica: a exigência pela argumentação.\n• O diálogo como forma de expressão da filosofia.\n• A argumentação nos diálogos filosóficos.',
                    'learning_objectives': '• Identificar a importância dos argumentos no contexto filosófico.\n• Compreender o diálogo como forma de expressão filosófica.\n• Distinguir tese e argumentos no contexto de um diálogo filosófico.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 4,
                    'title': 'A atitude filosófica: a análise dos argumentos',
                    'content': '• A atitude filosófica: a análise dos argumentos.\n• Lógica e discurso argumentativo.\n• Falácias formais e informais.',
                    'learning_objectives': '• Compreender a construção de argumentos visando o convencimento.\n• Analisar a força dos argumentos.\n• Identificar falácias formais e informais.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 5,
                    'title': 'Mito e Filosofia',
                    'content': 'A narrativa mitológica e o discurso filosófico.',
                    'learning_objectives': '• Distinguir Logos e Mythos.\n• Comparar a narrativa mitológica e o discurso filosófico para compreender aproximações e rupturas entre modos de pensar.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 6,
                    'title': 'Períodos da História da Filosofia',
                    'content': 'Períodos da história da Filosofia.',
                    'learning_objectives': '• Identificar marcadores que permitem uma periodização da história da filosofia.\n• Analisar como a filosofia se desenvolve em diálogo com seu contexto de produção, reconhecendo a influência mútua entre ideias e escolas filosóficas, processos e eventos históricos.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 7,
                    'title': 'Campos de investigação da Filosofia',
                    'content': 'Campos de investigação da Filosofia.',
                    'learning_objectives': '• Identificar os principais campos de investigação da filosofia.\n• Reconhecer a filosofia como uma atividade interdisciplinar.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 8,
                    'title': 'Escola de Atenas',
                    'content': 'A filosofia de Platão e Aristóteles na obra "Escola de Atenas".',
                    'learning_objectives': '• Compreender as bases do pensamento de Platão e Aristóteles tendo como ponto de partida a obra Escola de Atenas.\n• Analisar o pensamento filosófico de Platão a partir da alegoria da caverna.',
                    'skills': 'EM13CHS101', 'essential_learning_code': 'AE1',
                    'essential_learning': 'AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.'
                },
                {
                    'bimester': 1, 'lesson_number': 9,
                    'title': 'A arte pode motivar a reflexão filosófica?',
                    'content': '• A arte como objeto e como motivação da reflexão filosófica.\n• Estética como campo de investigação filosófica.',
                    'learning_objectives': '• Compreender a Estética como campo de investigação da Filosofia.\n• Reconhecer a obra de arte como oportunidade para a reflexão filosófica.',
                    'skills': 'EM13CHS104', 'essential_learning_code': 'AE2',
                    'essential_learning': 'AE2 - Analisar a produção artística, compreendendo a formação do gosto e exercitando a atitude crítica diante de padrões estéticos, conhecimentos e valores historicamente construídos.'
                },
                {
                    'bimester': 1, 'lesson_number': 10,
                    'title': 'O belo, o feio e o gosto',
                    'content': 'Os conceitos fundamentais da Estética.',
                    'learning_objectives': '• Reconhecer conceitos fundamentais da Estética, como o belo, o feio e o gosto.\n• Problematizar a possibilidade de um gosto universal.',
                    'skills': 'EM13CHS104', 'essential_learning_code': 'AE2',
                    'essential_learning': 'AE2 - Analisar a produção artística, compreendendo a formação do gosto e exercitando a atitude crítica diante de padrões estéticos, conhecimentos e valores historicamente construídos.'
                },
                {
                    'bimester': 1, 'lesson_number': 11,
                    'title': 'A atitude crítica: ponto comum entre a reflexão filosófica e a reflexão estética',
                    'content': '• O conceito de crítica.\n• A atitude crítica em filosofia.',
                    'learning_objectives': '• Identificar elementos da atitude crítica.\n• Analisar a incorporação do conceito de crítica à filosofia, no século XVIII.',
                    'skills': 'EM13CHS104', 'essential_learning_code': 'AE2',
                    'essential_learning': 'AE2 - Analisar a produção artística, compreendendo a formação do gosto e exercitando a atitude crítica diante de padrões estéticos, conhecimentos e valores historicamente construídos.'
                },
                {
                    'bimester': 1, 'lesson_number': 12,
                    'title': 'Breves considerações sobre a reflexão estética',
                    'content': 'Reflexão filosófica e experiência estética.',
                    'learning_objectives': 'Analisar obras de arte identificando possibilidades de sentido a partir da experiência estética.',
                    'skills': 'EM13CHS104', 'essential_learning_code': 'AE2',
                    'essential_learning': 'AE2 - Analisar a produção artística, compreendendo a formação do gosto e exercitando a atitude crítica diante de padrões estéticos, conhecimentos e valores historicamente construídos.'
                },
                {
                    'bimester': 1, 'lesson_number': 13,
                    'title': 'A arte em diálogo com o mundo contemporâneo',
                    'content': 'A produção de significados e a reflexão estética.',
                    'learning_objectives': 'Analisar significados produzidos por manifestações artísticas contemporâneas de diferentes linguagens.',
                    'skills': 'EM13CHS104', 'essential_learning_code': 'AE2',
                    'essential_learning': 'AE2 - Analisar a produção artística, compreendendo a formação do gosto e exercitando a atitude crítica diante de padrões estéticos, conhecimentos e valores historicamente construídos.'
                },
                {
                    'bimester': 1, 'lesson_number': 14,
                    'title': 'Análise crítica de obra de arte',
                    'content': 'Organização e produção de uma análise crítica sobre obra de arte.',
                    'learning_objectives': '• Analisar significados produzidos por manifestações artísticas;\n• Organizar argumentos na análise crítica de uma obra de arte.',
                    'skills': 'EM13CHS104', 'essential_learning_code': 'AE2',
                    'essential_learning': 'AE2 - Analisar a produção artística, compreendendo a formação do gosto e exercitando a atitude crítica diante de padrões estéticos, conhecimentos e valores historicamente construídos.'
                },

                # 2º Bimestre (Aulas 1 a 14)
                {
                    'bimester': 2, 'lesson_number': 1,
                    'title': 'Desafios éticos nas relações intergeracionais',
                    'content': '• Estereótipos geracionais e etarismo na sociedade contemporânea.\n• Desafios éticos na convivência entre diferentes gerações.\n• Os valores éticos do respeito à alteridade e da empatia.',
                    'learning_objectives': '• Refletir criticamente sobre os estereótipos geracionais, o etarismo e suas manifestações na sociedade contemporânea.\n• Reconhecer desafios éticos da convivência entre diferentes gerações e delinear possibilidades de superação.',
                    'skills': 'EM13CHS205', 'essential_learning_code': 'AE3',
                    'essential_learning': 'AE3 - Analisar as relações intergeracionais no Brasil e no mundo contemporâneo, problematizando estereótipos e a prática do etarismo, e reconhecendo a importância dos estatutos de proteção às diferentes fases da vida.'
                },
                {
                    'bimester': 2, 'lesson_number': 2,
                    'title': 'Diálogo e responsabilidade entre gerações',
                    'content': '• As condições e as possibilidades de convívio intergeracional: contribuições da filosofia contemporânea.\n• Marcos legais: Estatutos da Criança e do Adolescente, da Juventude e da Pessoa Idosa.',
                    'learning_objectives': '• Mobilizar repertório sobre a ideia de cidadania identificando seus princípios fundamentais.\n• Identificar as contribuições de Hannah Arendt para refletir sobre a responsabilidade entre gerações.',
                    'skills': 'EM13CHS205', 'essential_learning_code': 'AE3',
                    'essential_learning': 'AE3 - Analisar as relações intergeracionais no Brasil e no mundo contemporâneo, problematizando estereótipos e a prática do etarismo, e reconhecendo a importância dos estatutos de proteção às diferentes fases da vida.'
                },
                {
                    'bimester': 2, 'lesson_number': 3,
                    'title': 'O olhar do outro nas relações intergeracionais',
                    'content': '• A noção de olhar do outro segundo Jean Paul Sartre.\n• O olhar do outro nas relações intergeracionais.',
                    'learning_objectives': '• Compreender o conceito sartreano de olhar do outro.\n• Analisar e avaliar o olhar "do outro" no contexto das relações intergeracionais.',
                    'skills': 'EM13CHS205', 'essential_learning_code': 'AE3',
                    'essential_learning': 'AE3 - Analisar as relações intergeracionais no Brasil e no mundo contemporâneo, problematizando estereótipos e a prática do etarismo, e reconhecendo a importância dos estatutos de proteção às diferentes fases da vida.'
                },
                {
                    'bimester': 2, 'lesson_number': 4,
                    'title': 'Aula desafio: campanha relações intergeracionais',
                    'content': '• O protagonismo juvenil na promoção de relações intergeracionais éticas.\n• Orientações para produção de uma campanha de promoção de relações éticas.',
                    'learning_objectives': '• Análises e reflexões de produções de campanhas envolvendo os marcos legais de proteção das fases da vida.\n• Desenvolver propostas para a efetivação cotidiana dos Estatutos.',
                    'skills': 'EM13CHS205', 'essential_learning_code': 'AE3',
                    'essential_learning': 'AE3 - Analisar as relações intergeracionais no Brasil e no mundo contemporâneo, problematizando estereótipos e a prática do etarismo, e reconhecendo a importância dos estatutos de proteção às diferentes fases da vida.'
                },
                {
                    'bimester': 2, 'lesson_number': 5,
                    'title': 'Contribuições do pensamento filosófico para a análise da violência',
                    'content': 'Análises filosóficas do fenômeno da violência: contribuições de Hannah Arendt.',
                    'learning_objectives': '• Compreender a violência a partir das contribuições de Hannah Arendt.\n• Analisar a violência no mundo contemporâneo.',
                    'skills': 'EM13CHS503', 'essential_learning_code': 'AE4',
                    'essential_learning': 'AE4 - Identificar formas de violência, suas causas e significados, avaliando mecanismos de enfrentamento com base em argumentos éticos.'
                },
                {
                    'bimester': 2, 'lesson_number': 6,
                    'title': 'A ideia de dignidade humana como princípio fundamental dos Direitos Humanos',
                    'content': '• A ideia de dignidade humana: contribuições de Pico della Mirandola e Immanuel Kant.\n• A dignidade humana como princípio dos Direitos Humanos e Constituição brasileira.',
                    'learning_objectives': '• Compreender a noção de dignidade humana a partir de Pico della Mirandola e Kant.\n• Discutir a dignidade humana como princípio dos Direitos Humanos.',
                    'skills': 'EM13CHS503', 'essential_learning_code': 'AE4',
                    'essential_learning': 'AE4 - Identificar formas de violência, suas causas e significados, avaliando mecanismos de enfrentamento com base em argumentos éticos.'
                },
                {
                    'bimester': 2, 'lesson_number': 7,
                    'title': 'O republicanismo e sua relação com a democracia e os direitos humanos',
                    'content': '• O ideal de liberdade republicana (liberdade como não-dominação).\n• As virtudes cívicas e a participação política.',
                    'learning_objectives': '• Compreender o conceito de republicanismo com foco na liberdade como não-dominação.\n• Analisar a importância das virtudes cívicas.',
                    'skills': 'EM13CHS503', 'essential_learning_code': 'AE4',
                    'essential_learning': 'AE4 - Identificar formas de violência, suas causas e significados, avaliando mecanismos de enfrentamento com base em argumentos éticos.'
                },
                {
                    'bimester': 2, 'lesson_number': 8,
                    'title': 'Autoritarismo e desigualdade como desafios à democracia e aos Direitos Humanos',
                    'content': '• O autoritarismo e a desigualdade como desafio às instituições democráticas.\n• A importância de valores éticos na vida política: Emmanuel Lévinas.',
                    'learning_objectives': '• Analisar o autoritarismo e a banalização das desigualdades.\n• Discutir a Ética da alteridade de Emmanuel Lévinas.',
                    'skills': 'EM13CHS503', 'essential_learning_code': 'AE4',
                    'essential_learning': 'AE4 - Identificar formas de violência, suas causas e significados, avaliando mecanismos de enfrentamento com base em argumentos éticos.'
                },
                {
                    'bimester': 2, 'lesson_number': 9,
                    'title': 'Filosofia e desafios contemporâneos à Democracia e aos Direitos Humanos – Aula complementar',
                    'content': 'Síntese e reflexões sobre "violência e ética", "dignidade humana", "republicanismo" e "desafios à democracia".',
                    'learning_objectives': 'Sistematizar os conhecimentos desenvolvidos nas aulas anteriores.',
                    'skills': 'EM13CHS503', 'essential_learning_code': 'AE4',
                    'essential_learning': 'AE4 - Identificar formas de violência, suas causas e significados, avaliando mecanismos de enfrentamento com base em argumentos éticos.'
                },
                {
                    'bimester': 2, 'lesson_number': 10,
                    'title': 'Quais são as condições da legitimidade do poder soberano?',
                    'content': '• O conceito de poder soberano.\n• O problema filosófico da legitimidade do poder soberano.',
                    'learning_objectives': '• Analisar o conceito de poder soberano.\n• Discutir a legitimação do poder soberano.',
                    'skills': 'EM13CHS603', 'essential_learning_code': 'AE5',
                    'essential_learning': 'AE5 - Analisar a formação do Estado e a legitimidade do poder político, aplicando o conceito de soberania a partir de pensadores do contratualismo, liberalismo e republicanismo clássicos.'
                },
                {
                    'bimester': 2, 'lesson_number': 11,
                    'title': 'Teoria do direito divino e contratualismo',
                    'content': '• A teoria do direito divino ao poder.\n• A teoria do contrato social: Thomas Hobbes.',
                    'learning_objectives': '• Analisar os elementos centrais do direito divino ao poder.\n• Analisar o contratualismo de Thomas Hobbes.',
                    'skills': 'EM13CHS603', 'essential_learning_code': 'AE5',
                    'essential_learning': 'AE5 - Analisar a formação do Estado e a legitimidade do poder político, aplicando o conceito de soberania a partir de pensadores do contratualismo, liberalismo e republicanismo clássicos.'
                },
                {
                    'bimester': 2, 'lesson_number': 12,
                    'title': 'O papel do Estado e a liberdade individual',
                    'content': '• O contratualismo frente ao absolutismo: John Locke.\n• O liberalismo: os direitos individuais e a limitação do poder do Estado.',
                    'learning_objectives': '• Analisar as críticas de John Locke ao Estado Absolutista.\n• Destacar a relevância da proteção aos direitos individuais.',
                    'skills': 'EM13CHS603', 'essential_learning_code': 'AE5',
                    'essential_learning': 'AE5 - Analisar a formação do Estado e a legitimidade do poder político, aplicando o conceito de soberania a partir de pensadores do contratualismo, liberalismo e republicanismo clássicos.'
                },
                {
                    'bimester': 2, 'lesson_number': 13,
                    'title': 'Vontade geral e soberania popular',
                    'content': '• O contratualismo frente ao absolutismo: Jean-Jacques Rousseau.\n• Os conceitos republicanos de vontade geral e soberania popular.',
                    'learning_objectives': '• Analisar as críticas de Rousseau ao absolutismo.\n• Destacar a relevância da participação política dos cidadãos.',
                    'skills': 'EM13CHS603', 'essential_learning_code': 'AE5',
                    'essential_learning': 'AE5 - Analisar a formação do Estado e a legitimidade do poder político, aplicando o conceito de soberania a partir de pensadores do contratualismo, liberalismo e republicanismo clássicos.'
                },
                {
                    'bimester': 2, 'lesson_number': 14,
                    'title': 'Um olhar da atualidade para o contratualismo clássico - Aula complementar',
                    'content': 'Reflexões sobre o contratualismo clássico (Hobbes, Locke, Rousseau) a partir da atualidade.',
                    'learning_objectives': 'Mobilizar teses centrais do contratualismo para apresentar indícios desse legado na atualidade.',
                    'skills': 'EM13CHS603', 'essential_learning_code': 'AE5',
                    'essential_learning': 'AE5 - Analisar a formação do Estado e a legitimidade do poder político, aplicando o conceito de soberania a partir de pensadores do contratualismo, liberalismo e republicanismo clássicos.'
                },

                # 3º Bimestre (Aulas 1 a 12)
                {
                    'bimester': 3, 'lesson_number': 1,
                    'title': 'Identidade e produção filosófica',
                    'content': 'A Filosofia e o filosofar: diferentes modos de ser e de estar no mundo.',
                    'learning_objectives': '• Reconhecer a multiplicidade de perspectivas filosóficas sobre a existência humana.\n• Compreender o eurocentrismo como obstáculo ao reconhecimento de outras produções.',
                    'skills': 'EM13CHS601', 'essential_learning_code': 'AE6',
                    'essential_learning': 'AE6 - Analisar a produção filosófica, considerando o contexto de exclusão e inclusão precária de povos indígenas e populações afrodescendentes na ordem social e econômica, a fim de reconhecer o valor filosófico de produções vinculadas a matrizes culturais não europeias.'
                },
                {
                    'bimester': 3, 'lesson_number': 2,
                    'title': 'Filosofias de matriz africana',
                    'content': '• A filosofia Ubuntu.\n• Filósofos negros do Brasil contemporâneo.',
                    'learning_objectives': '• Identificar elementos característicos da filosofia Ubuntu.\n• Analisar desafios contemporâneos a partir da obra de filósofos brasileiros de matriz africana.',
                    'skills': 'EM13CHS601', 'essential_learning_code': 'AE6',
                    'essential_learning': 'AE6 - Analisar a produção filosófica, considerando o contexto de exclusão e inclusão precária de povos indígenas e populações afrodescendentes na ordem social e econômica, a fim de reconhecer o valor filosófico de produções vinculadas a matrizes culturais não europeias.'
                },
                {
                    'bimester': 3, 'lesson_number': 3,
                    'title': 'Protagonismo e cidadania dos povos indígenas',
                    'content': '• Protagonismo e cidadania dos povos indígenas do Brasil.\n• Filósofos indígenas: Davi Kopenawa Yanomami e Ailton Krenak.',
                    'learning_objectives': '• Identificar a produção filosófica como expressão do protagonismo indígena.\n• Analisar as contribuições de Kopenawa e Krenak.',
                    'skills': 'EM13CHS601', 'essential_learning_code': 'AE6',
                    'essential_learning': 'AE6 - Analisar a produção filosófica, considerando o contexto de exclusão e inclusão precária de povos indígenas e populações afrodescendentes na ordem social e econômica, a fim de reconhecer o valor filosófico de produções vinculadas a matrizes culturais não europeias.'
                },
                {
                    'bimester': 3, 'lesson_number': 4,
                    'title': 'A reflexão filosófica como fundamento da conduta ética',
                    'content': 'A reflexão filosófica como fundamento da conduta ética.',
                    'learning_objectives': '• Identificar na reflexão filosófica as condições da ação ética.\n• Reconhecer a reflexão ética como esforço de fundamentação das regras humanas.',
                    'skills': 'EM13CHS501', 'essential_learning_code': 'AE7',
                    'essential_learning': 'AE7 - Analisar a fundamentação ética das ações humanas com base em diferentes teorias filosóficas a fim de promover a autonomia, o respeito à diversidade e a defesa da equidade e dos direitos humanos.'
                },
                {
                    'bimester': 3, 'lesson_number': 5,
                    'title': 'A ação humana e sua iniciativa criadora: liberdade ou determinismo',
                    'content': '• A ação humana: liberdade ou determinismo.\n• As posições de Jean Paul Sartre e Louis Althusser.',
                    'learning_objectives': '• Identificar as posições antagônicas de Sartre e Althusser.\n• Comparar os argumentos de ambos sobre a ação humana e transformação da realidade.',
                    'skills': 'EM13CHS501', 'essential_learning_code': 'AE7',
                    'essential_learning': 'AE7 - Analisar a fundamentação ética das ações humanas com base em diferentes teorias filosóficas a fim de promover a autonomia, o respeito à diversidade e a defesa da equidade e dos direitos humanos.'
                },
                {
                    'bimester': 3, 'lesson_number': 6,
                    'title': 'Ética e democracia',
                    'content': 'Os valores democráticos e solidários, respeito à diversidade e direitos humanos: Jürgen Habermas.',
                    'learning_objectives': '• Compreender a legitimação dos valores democráticos.\n• Analisar a fundamentação filosófica segundo Habermas.',
                    'skills': 'EM13CHS501', 'essential_learning_code': 'AE7',
                    'essential_learning': 'AE7 - Analisar a fundamentação ética das ações humanas com base em diferentes teorias filosóficas a fim de promover a autonomia, o respeito à diversidade e a defesa da equidade e dos direitos humanos.'
                },
                {
                    'bimester': 3, 'lesson_number': 7,
                    'title': 'Há uma moral válida para todos?',
                    'content': '• O debate sobre o universalismo moral na Filosofia contemporânea.\n• As posições de Habermas e Michel Foucault.',
                    'learning_objectives': '• Problematizar o universalismo moral nos debates contemporâneos.\n• Analisar as posições de Habermas e Foucault.',
                    'skills': 'EM13CHS501', 'essential_learning_code': 'AE7',
                    'essential_learning': 'AE7 - Analisar a fundamentação ética das ações humanas com base em diferentes teorias filosóficas a fim de promover a autonomia, o respeito à diversidade e a defesa da equidade e dos direitos humanos.'
                },
                {
                    'bimester': 3, 'lesson_number': 8,
                    'title': 'Existe conflito entre ciência e religião?',
                    'content': '• Características dos discursos religioso e científico.\n• A relação entre ciência e religião em diferentes períodos.',
                    'learning_objectives': '• Analisar elementos do discurso religioso e científico.\n• Problematizar a interação entre ciência e religião.',
                    'skills': 'EM13CHS504', 'essential_learning_code': 'AE8',
                    'essential_learning': 'AE8 - Analisar reflexões filosóficas sobre a produção de conhecimento, discutindo os impasses ético-políticos implicados em práticas científicas de diferentes períodos, a fim de reconhecer os limites do conhecimento científico.'
                },
                {
                    'bimester': 3, 'lesson_number': 9,
                    'title': 'O rompimento com a tradição: empirismo e racionalismo na modernidade',
                    'content': '• Ruptura com a escolástica e valorização da razão/experiência.\n• Empirismo e racionalismo e o domínio técnico da natureza.',
                    'learning_objectives': '• Caracterizar a visão de mundo medieval e escolástica.\n• Analisar o empirismo e o racionalismo moderno.',
                    'skills': 'EM13CHS504', 'essential_learning_code': 'AE8',
                    'essential_learning': 'AE8 - Analisar reflexões filosóficas sobre a produção de conhecimento, discutindo os impasses ético-políticos implicados em práticas científicas de diferentes períodos, a fim de reconhecer os limites do conhecimento científico.'
                },
                {
                    'bimester': 3, 'lesson_number': 10,
                    'title': 'Impasses ético-políticos do problema do conhecimento',
                    'content': '• O ceticismo de David Hume e o desafio à causalidade.\n• A filosofia crítica de Kant como resposta ao desafio cético.',
                    'learning_objectives': '• Analisar o ceticismo de Hume e o problema da causalidade.\n• Analisar as consequências ético-políticas segundo Kant.',
                    'skills': 'EM13CHS504', 'essential_learning_code': 'AE8',
                    'essential_learning': 'AE8 - Analisar reflexões filosóficas sobre a produção de conhecimento, discutindo os impasses ético-políticos implicados em práticas científicas de diferentes períodos, a fim de reconhecer os limites do conhecimento científico.'
                },
                {
                    'bimester': 3, 'lesson_number': 11,
                    'title': 'O mito da certeza e da neutralidade da ciência',
                    'content': 'O mito da certeza e da neutralidade da ciência.',
                    'learning_objectives': '• Analisar o conceito de neutralidade científica.\n• Reconhecer as contribuições de Karl Popper e Thomas Kuhn.',
                    'skills': 'EM13CHS504', 'essential_learning_code': 'AE8',
                    'essential_learning': 'AE8 - Analisar reflexões filosóficas sobre a produção de conhecimento, discutindo os impasses ético-políticos implicados em práticas científicas de diferentes períodos, a fim de reconhecer os limites do conhecimento científico.'
                },
                {
                    'bimester': 3, 'lesson_number': 12,
                    'title': 'Bioética e os limites à dominação humana da natureza',
                    'content': 'O conceito de bioética; Dilemas bioéticos contemporâneos.',
                    'learning_objectives': '• Conhecer o conceito de bioética e princípios em situações práticas.\n• Analisar dilemas da manipulação da vida e inovação científica.',
                    'skills': 'EM13CHS504', 'essential_learning_code': 'AE8',
                    'essential_learning': 'AE8 - Analisar reflexões filosóficas sobre a produção de conhecimento, discutindo os impasses ético-políticos implicados em práticas científicas de diferentes períodos, a fim de reconhecer os limites do conhecimento científico.'
                },

                # 4º Bimestre (Aulas 1 a 12)
                {
                    'bimester': 4, 'lesson_number': 1,
                    'title': 'Uma discrepância prometeica',
                    'content': '• A inovação tecnológica e os efeitos socioambientais.\n• Os desafios da sociedade tecnológica segundo Günther Anders.',
                    'learning_objectives': '• Analisar o diagnóstico de Anders sobre o poderio e a sensibilidade humana.\n• Problematizar práticas que levam a futuros distópicos.',
                    'skills': 'EM13CHS301', 'essential_learning_code': 'AE9',
                    'essential_learning': 'AE9 - Analisar o papel do Estado, da sociedade e do indivíduo nos processos de produção e consumo, à luz de críticas à noção convencional de desenvolvimento, a fim de problematizar as responsabilidades socioambientais de cada agente.'
                },
                {
                    'bimester': 4, 'lesson_number': 2,
                    'title': 'A ética da responsabilidade na sociedade tecnológica',
                    'content': '• A ética da responsabilidade de Hans Jonas.\n• Os objetivos de desenvolvimento sustentável (ODS).',
                    'learning_objectives': '• Relacionar os ODS da ONU aos desafios éticos e ambientais.\n• Compreender a ética da responsabilidade.',
                    'skills': 'EM13CHS301', 'essential_learning_code': 'AE9',
                    'essential_learning': 'AE9 - Analisar o papel do Estado, da sociedade e do indivíduo nos processos de produção e consumo, à luz de críticas à noção convencional de desenvolvimento, a fim de problematizar as responsabilidades socioambientais de cada agente.'
                },
                {
                    'bimester': 4, 'lesson_number': 3,
                    'title': 'O contrato natural',
                    'content': '• Contrato natural (Michel Serres).\n• Consumo sustentável e redução da geração de resíduos (ODS 12).',
                    'learning_objectives': '• Compreender o contrato natural de Michel Serres.\n• Reconhecer a demanda por consumo sustentável como desafio ético.',
                    'skills': 'EM13CHS301', 'essential_learning_code': 'AE9',
                    'essential_learning': 'AE9 - Analisar o papel do Estado, da sociedade e do indivíduo nos processos de produção e consumo, à luz de críticas à noção convencional de desenvolvimento, a fim de problematizar as responsabilidades socioambientais de cada agente.'
                },
                {
                    'bimester': 4, 'lesson_number': 4,
                    'title': 'Críticas e alternativas à concepção convencional de desenvolvimento',
                    'content': 'Críticas e alternativas à noção convencional de desenvolvimento a partir de saberes de diferentes matrizes (Ailton Krenak e Antônio Bispo dos Santos).',
                    'learning_objectives': 'Analisar o pensamento de Krenak e Bispo sobre o modelo consumista e excludente.',
                    'skills': 'EM13CHS301', 'essential_learning_code': 'AE9',
                    'essential_learning': 'AE9 - Analisar o papel do Estado, da sociedade e do indivíduo nos processos de produção e consumo, à luz de críticas à noção convencional de desenvolvimento, a fim de problematizar as responsabilidades socioambientais de cada agente.'
                },
                {
                    'bimester': 4, 'lesson_number': 5,
                    'title': 'A sociedade disciplinar',
                    'content': 'O conceito de sociedade disciplinar em Michel Foucault; O esquema de poder no Panóptico de Bentham.',
                    'learning_objectives': '• Reconhecer o conceito de sociedade disciplinar em situações práticas.\n• Expressar opinião fundamentada sobre o controle social.',
                    'skills': 'EM13CHS103', 'essential_learning_code': 'AE10',
                    'essential_learning': 'AE10 - Analisar as características das sociedades contemporâneas a partir de diagnósticos filosóficos do momento presente, a fim de elaborar hipóteses e compor argumentos sobre as transformações nas formas de poder, subjetividade e organização social.'
                },
                {
                    'bimester': 4, 'lesson_number': 6,
                    'title': 'A Condição pós-moderna: o fim das grandes narrativas',
                    'content': '• A condição pós-moderna de Jean-François Lyotard.\n• Crítica às grandes narrativas e elevação dos saberes locais.',
                    'learning_objectives': '• Reconhecer a condição pós-moderna em diferentes gêneros textuais.\n• Compor argumentos utilizando referencial filosófico.',
                    'skills': 'EM13CHS103', 'essential_learning_code': 'AE10',
                    'essential_learning': 'AE10 - Analisar as características das sociedades contemporâneas a partir de diagnósticos filosóficos do momento presente, a fim de elaborar hipóteses e compor argumentos sobre as transformações nas formas de poder, subjetividade e organização social.'
                },
                {
                    'bimester': 4, 'lesson_number': 7,
                    'title': 'A sociedade hipermoderna',
                    'content': 'Sociedade hipermoderna segundo Gilles Lipovetsky; O papel da moda e o império do efêmero.',
                    'learning_objectives': 'Problematizar o caráter efêmero das experiências e a moda a partir de Lipovetsky.',
                    'skills': 'EM13CHS103', 'essential_learning_code': 'AE10',
                    'essential_learning': 'AE10 - Analisar as características das sociedades contemporâneas a partir de diagnósticos filosóficos do momento presente, a fim de elaborar hipóteses e compor argumentos sobre as transformações nas formas de poder, subjetividade e organização social.'
                },
                {
                    'bimester': 4, 'lesson_number': 8,
                    'title': 'A sociedade do cansaço',
                    'content': 'O conceito de sociedade do cansaço segundo Byung-Chul Han; Formas contemporâneas de alienação.',
                    'learning_objectives': 'Problematizar as formas contemporâneas de alienação a partir da obra de Byung-Chul Han.',
                    'skills': 'EM13CHS103', 'essential_learning_code': 'AE10',
                    'essential_learning': 'AE10 - Analisar as características das sociedades contemporâneas a partir de diagnósticos filosóficos do momento presente, a fim de elaborar hipóteses e compor argumentos sobre as transformações nas formas de poder, subjetividade e organização social.'
                },
                {
                    'bimester': 4, 'lesson_number': 9,
                    'title': 'A seguridade social e os direitos humanos',
                    'content': '• A dimensão ética dos desafios impostos à seguridade social.\n• A seguridade no contexto dos Direitos Humanos.',
                    'learning_objectives': '• Reconhecer a seguridade social na Declaração Universal dos Direitos Humanos.\n• Compreender a dimensão ética dos desafios.',
                    'skills': 'EM13CHS403', 'essential_learning_code': 'AE11',
                    'essential_learning': 'AE11 - Analisar desafios ético-políticos contemporâneos relacionados aos direitos sociais, ao reconhecimento das diferenças e à luta por justiça redistributiva, a fim de compreender o papel do Estado na garantia de direitos e fortalecer o exercício crítico da cidadania.'
                },
                {
                    'bimester': 4, 'lesson_number': 10,
                    'title': 'O Estado de bem-estar social, suas promessas e seus desafios',
                    'content': 'O Estado de bem-estar social, suas promessas e desafios contemporâneos segundo Jürgen Habermas.',
                    'learning_objectives': '• Identificar os fundamentos éticos do Estado de bem-estar social.\n• Analisar fatores contemporâneos que desafiam o Estado de bem-estar.',
                    'skills': 'EM13CHS403', 'essential_learning_code': 'AE11',
                    'essential_learning': 'AE11 - Analisar desafios ético-políticos contemporâneos relacionados aos direitos sociais, ao reconhecimento das diferenças e à luta por justiça redistributiva, a fim de compreender o papel do Estado na garantia de direitos e fortalecer o exercício crítico da cidadania.'
                },
                {
                    'bimester': 4, 'lesson_number': 11,
                    'title': 'Conflitos sociais e luta por reconhecimento',
                    'content': 'Conflitos sociais e luta por reconhecimento segundo Axel Honneth.',
                    'learning_objectives': '• Identificar situações de desigualdades decorrentes da ausência de reconhecimento.\n• Analisar o diagnóstico dos conflitos sociais contemporâneos.',
                    'skills': 'EM13CHS403', 'essential_learning_code': 'AE11',
                    'essential_learning': 'AE11 - Analisar desafios ético-políticos contemporâneos relacionados aos direitos sociais, ao reconhecimento das diferenças e à luta por justiça redistributiva, a fim de compreender o papel do Estado na garantia de direitos e fortalecer o exercício crítico da cidadania.'
                },
                {
                    'bimester': 4, 'lesson_number': 12,
                    'title': 'A ideia de justiça redistributiva',
                    'content': 'A ideia de justiça redistributiva segundo Nancy Fraser.',
                    'learning_objectives': 'Analisar o diagnóstico dos conflitos sociais e as possibilidades de emancipação propostas por Nancy Fraser.',
                    'skills': 'EM13CHS403', 'essential_learning_code': 'AE11',
                    'essential_learning': 'AE11 - Analisar desafios ético-políticos contemporâneos relacionados aos direitos sociais, ao reconhecimento das diferenças e à luta por justiça redistributiva, a fim de compreender o papel do Estado na garantia de direitos e fortalecer o exercício crítico da cidadania.'
                }
            ]

            # Inserir aulas de Filosofia no banco
            for aula_data in filosofia_aulas:
                existente = ScopeLesson.query.filter_by(
                    subject_id=subj_filo.id,
                    education_level='medio',
                    grade='1ª Série',
                    bimester=aula_data['bimester'],
                    lesson_number=aula_data['lesson_number'],
                    year=2026
                ).first()

                if not existente:
                    nova_aula = ScopeLesson(
                        subject_id=subj_filo.id,
                        education_level='medio',
                        grade='1ª Série',
                        bimester=aula_data['bimester'],
                        lesson_number=aula_data['lesson_number'],
                        title=aula_data['title'],
                        content=aula_data['content'],
                        learning_objectives=aula_data['learning_objectives'],
                        skills=aula_data['skills'],
                        essential_learning_code=aula_data['essential_learning_code'],
                        essential_learning=aula_data['essential_learning'],
                        year=2026
                    )
                    db.session.add(nova_aula)

            # Registrar documento de Filosofia
            if not CurriculumDocument.query.filter_by(subject_id=subj_filo.id, grade='1ª Série').first():
                doc = CurriculumDocument(
                    subject_id=subj_filo.id,
                    education_level='medio',
                    grade='1ª Série',
                    document_year=2026,
                    file_name='Guia_Curriculo_Priorizado_EM_Filosofia_1Serie.pdf',
                    file_path='uploads/Guia_Curriculo_Priorizado_EM_Filosofia_1Serie.pdf',
                    total_lessons=len(filosofia_aulas),
                    status='processado'
                )
                db.session.add(doc)

            db.session.commit()
            print(f"52 Aulas oficiais de Filosofia (1ª Série EM) inseridas com sucesso!")

        # 6. Importar dados adicionais de Biologia / Ciências do JSON existente caso exista
        json_path = Path(__file__).resolve().parent.parent.parent / 'public' / 'data' / 'escopo.json'
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    dados_json = json.load(f)
                    
                subj_bio = Subject.query.filter_by(name='Biologia', education_level='medio').first()
                if subj_bio and dados_json:
                    contador_bio = 0
                    for item in dados_json:
                        if 'Biologia' in item.get('componente', ''):
                            bim_str = item.get('bimestre', '1').replace('°', '').replace('º', '')
                            try:
                                bim = int(bim_str)
                                num_aula = int(item.get('aula', 1))
                            except ValueError:
                                continue

                            existente = ScopeLesson.query.filter_by(
                                subject_id=subj_bio.id,
                                education_level='medio',
                                grade='3ª Série',
                                bimester=bim,
                                lesson_number=num_aula,
                                year=2026
                            ).first()

                            if not existente:
                                nova_aula = ScopeLesson(
                                    subject_id=subj_bio.id,
                                    education_level='medio',
                                    grade='3ª Série',
                                    bimester=bim,
                                    lesson_number=num_aula,
                                    title=item.get('titulo', f'Aula {num_aula}'),
                                    content=item.get('conteudo', ''),
                                    learning_objectives=item.get('objetivos', ''),
                                    skills=item.get('habilidade', ''),
                                    essential_learning_code='',
                                    essential_learning='',
                                    year=2026
                                )
                                db.session.add(nova_aula)
                                contador_bio += 1

                    if contador_bio > 0:
                        doc_bio = CurriculumDocument(
                            subject_id=subj_bio.id,
                            education_level='medio',
                            grade='3ª Série',
                            document_year=2026,
                            file_name='Guia_Curriculo_Priorizado_EM_Biologia_3Serie.pdf',
                            file_path='uploads/Guia_Curriculo_Priorizado_EM_Biologia_3Serie.pdf',
                            total_lessons=contador_bio,
                            status='processado'
                        )
                        db.session.add(doc_bio)
                        db.session.commit()
                        print(f"{contador_bio} Aulas de Biologia (3ª Série EM) importadas do acervo!")
            except Exception as e:
                print(f"Nota: Não foi possível importar dados secundários do JSON: {e}")

        # 7. Criar 2 Planos de Aula de exemplo para o Professor de Teste
        if prof and subj_filo:
            if LessonPlan.query.filter_by(user_id=prof.id).count() == 0:
                from datetime import date
                plano1 = LessonPlan(
                    user_id=prof.id,
                    subject_id=subj_filo.id,
                    education_level='medio',
                    grade='1ª Série',
                    bimester=1,
                    start_date=date(2026, 2, 9),
                    end_date=date(2026, 2, 27),
                    number_of_lessons=6,
                    selected_lesson_titles="Aula 1 - Por que filosofia?\nAula 2 - Origens da filosofia\nAula 3 - Atitude filosófica: a exigência pela argumentação",
                    contents="• A filosofia e a formação para a cidadania.\n• As origens da filosofia e o espanto.\n• A atitude filosófica e o diálogo.",
                    objectives="• Situar a filosofia na formação geral básica.\n• Discutir o espanto e a indagação como condições da reflexão filosófica.\n• Identificar a importância dos argumentos no contexto filosófico.",
                    skills="EM13CHS101",
                    essential_learnings="AE1 - Analisar as origens da Filosofia, seus campos de investigação e as características da atitude filosófica, considerando a importância do diálogo e da argumentação fundamentada.",
                    resources="Projetor multimídia, slides da SEDUC, caderno do aluno, textos impressos de apoio.",
                    methodology="Aula expositiva dialogada inicial introduzindo os conceitos de espanto e atitude filosófica. Leitura e debate em grupos sobre situações cotidianas que exigem fundamentação racional.",
                    evaluation="Participação ativa nos debates em sala de aula, produção de pequeno texto reflexivo individual e resolução de questões conceituais."
                )
                plano1.classes.append(LessonPlanClass(class_name='1ª A'))
                plano1.classes.append(LessonPlanClass(class_name='1ª B'))
                
                # Associar as 3 primeiras aulas do escopo
                aulas_1a3 = ScopeLesson.query.filter(
                    ScopeLesson.subject_id == subj_filo.id,
                    ScopeLesson.bimester == 1,
                    ScopeLesson.lesson_number.in_([1, 2, 3])
                ).all()
                for al in aulas_1a3:
                    plano1.lessons.append(LessonPlanLesson(scope_lesson_id=al.id))

                db.session.add(plano1)
                db.session.commit()
                print("Plano de aula de demonstração criado com sucesso!")

        print("\n=== BANCO DE DADOS POPULADO E PRONTO PARA USO! ===")

if __name__ == '__main__':
    seed_database()

