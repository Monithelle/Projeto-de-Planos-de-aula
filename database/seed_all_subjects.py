import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.models import db, Subject, ScopeLesson, CurriculumDocument

def seed_all():
    app = create_app()
    with app.app_context():
        print("Iniciando importação completa das 4 disciplinas do Ensino Fundamental...")

        # -------------------------------------------------------------
        # 1. ARTE (Ensino Fundamental: 6º, 7º, 8º e 9º Anos)
        # -------------------------------------------------------------
        subj_arte = Subject.query.filter_by(name='Arte', education_level='fundamental').first()
        if not subj_arte:
            subj_arte = Subject(name='Arte', education_level='fundamental', active=True)
            db.session.add(subj_arte)
            db.session.commit()

        # 6º Ano Arte
        arte_6_aulas = [
            # 1º Bimestre - Dança Folclórica
            {'b': 1, 'n': 1, 't': 'Descobrindo o Frevo', 'c': 'Danças Populares Brasileiras. Origens das Danças. Variação de Tempo.', 'o': 'Apreciar encenações de danças populares brasileiras. Explorar a história e o desenvolvimento da dança.', 's': 'EF06AR09, EF06AR10, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 2, 't': 'Descobrindo o Jongo', 'c': 'Danças Populares Brasileiras. Origens e Variação de Tempo.', 'o': 'Apreciar encenações de danças populares brasileiras.', 's': 'EF06AR09, EF06AR10, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 3, 't': 'Descobrindo o Carimbó', 'c': 'Danças Populares Brasileiras. Origens e Variação de Tempo.', 'o': 'Apreciar encenações de danças populares brasileiras.', 's': 'EF06AR09, EF06AR10, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 4, 't': 'Descobrindo o Siriri', 'c': 'Danças Populares Brasileiras. Origens e Variação de Tempo.', 'o': 'Apreciar encenações de danças populares brasileiras.', 's': 'EF06AR09, EF06AR10, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 5, 't': 'Explorando a Expressividade na Dança', 'c': 'Expressão Corporal. Elementos da Dança. Movimentos do Frevo.', 'o': 'Identificar elementos constitutivos da dança em danças populares brasileiras.', 's': 'EF06AR09, EF06AR10', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 6, 't': 'Explorando a Dança no Espaço', 'c': 'Uso do Espaço. Fatores do Movimento.', 'o': 'Experimentar e analisar os fatores de movimento.', 's': 'EF06AR09, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 7, 't': 'Sentindo o Peso na Dança', 'c': 'Fator Peso. Danças Populares. Gravidade.', 'o': 'Movimentar-se explorando a gravidade e a variação de peso.', 's': 'EF06AR09, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 8, 't': 'Fluindo com a Dança', 'c': 'Fator Fluência. Danças Populares. Expressividade.', 'o': 'Avaliar as escolhas do processo de criação e seu impacto na performance.', 's': 'EF06AR10, EF06AR11', 'ae_c': 'AE1', 'ae': 'AE1 - Diferenciar movimentos coreográficos em danças folclóricas de diferentes épocas.'},
            {'b': 1, 'n': 9, 't': 'Criando com as Danças do Brasil', 'c': 'Criação Coreográfica. Variação. Expressão na Dança.', 'o': 'Analisar composições de grupos de dança brasileiros e criar variações.', 's': 'EF06AR09, EF06AR14', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar composições coreográficas autorais com base em elementos das danças folclóricas brasileiras.'},
            {'b': 1, 'n': 10, 't': 'Aprimorando a Coreografia', 'c': 'Refinamento Coreográfico. Colaboração. Preparação.', 'o': 'Modificar elementos coreográficos para criar variações nas sequências de dança.', 's': 'EF06AR14', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar composições coreográficas autorais com base em elementos das danças folclóricas brasileiras.'},
            {'b': 1, 'n': 11, 't': 'Ensaio Geral', 'c': 'Ajustes Finais. Ensaio Geral. Preparação para Apresentação.', 'o': 'Apresentar uma coreografia de dança popular, individualmente ou em grupo.', 's': 'EF06AR09, EF06AR14', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar composições coreográficas autorais com base em elementos das danças folclóricas brasileiras.'},
            {'b': 1, 'n': 12, 't': 'Nossa Coreografia em Cena', 'c': 'Apresentação Final. Celebração. Apreciação.', 'o': 'Apresentar uma coreografia de dança popular com apreciação crítica.', 's': 'EF06AR09, EF06AR14', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar composições coreográficas autorais com base em elementos das danças folclóricas brasileiras.'},
            {'b': 1, 'n': 13, 't': 'Nossa Jornada com as Danças do Brasil', 'c': 'Autoavaliação. Reflexão. Compartilhamento.', 'o': 'Avaliar as escolhas do processo de criação e seu impacto na performance.', 's': 'EF06AR09, EF06AR11, EF06AR14', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar composições coreográficas autorais com base em elementos das danças folclóricas brasileiras.'},
            {'b': 1, 'n': 14, 't': 'Encerramento e Celebração', 'c': 'Encerramento. Síntese. Celebração.', 'o': 'Identificar elementos constitutivos da dança e sintetizar a aprendizagem.', 's': 'EF06AR10, EF06AR14', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar composições coreográficas autorais com base em elementos das danças folclóricas brasileiras.'},

            # 2º Bimestre - Música Brasileira e Sons
            {'b': 2, 'n': 1, 't': 'A Vida na Música', 'c': 'Música Brasileira. Produção Musical. Repertório Musical.', 'o': 'Investigar diferentes gêneros musicais tradicionais brasileiros.', 's': 'EF06AR16', 'ae_c': 'AE3', 'ae': 'AE3 - Analisar os gêneros da música brasileira a partir de seus contextos de produção, circulação e apreciação.'},
            {'b': 2, 'n': 2, 't': 'A Música na Vida', 'c': 'Função Social da Música. Repertório Indígena e Afro-Brasileiro.', 'o': 'Relacionar as práticas musicais às diferentes dimensões da vida social.', 's': 'EF06AR16', 'ae_c': 'AE3', 'ae': 'AE3 - Analisar os gêneros da música brasileira a partir de seus contextos de produção, circulação e apreciação.'},
            {'b': 2, 'n': 3, 't': 'O Som da Vida', 'c': 'Paisagem Sonora. Registro Musical. Notação Não Convencional.', 'o': 'Investigar os sons que fazem parte da paisagem sonora cotidiana.', 's': 'EF06AR21, EF06AR23', 'ae_c': 'AE3', 'ae': 'AE3 - Analisar os gêneros da música brasileira a partir de seus contextos de produção, circulação e apreciação.'},
            {'b': 2, 'n': 4, 't': 'Músicas que a Vida faz!', 'c': 'Composição Musical. Percussão Corporal. Improvisação Musical.', 'o': 'Criar composições musicais a partir de sons cotidianos.', 's': 'EF06AR21, EF06AR23', 'ae_c': 'AE3', 'ae': 'AE3 - Analisar os gêneros da música brasileira a partir de seus contextos de produção, circulação e apreciação.'},
            {'b': 2, 'n': 5, 't': 'Tudo é Instrumento!', 'c': 'Instrumentos Não Convencionais. Instrumentos e Timbres.', 'o': 'Criar composições musicais a partir de instrumentos não convencionais.', 's': 'EF06AR21, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 6, 't': 'A Música é a melhor companhia! – Aula Complementar', 'c': 'Cantos de Trabalho. Improvisação Musical.', 'o': 'Executar repertório de diferentes gêneros musicais brasileiros.', 's': 'EF06AR21, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 7, 't': 'A Música da nossa sala! – Aula Complementar', 'c': 'Instrumentos e Timbres. Composição Musical.', 'o': 'Explorar partituras criativas como forma de registro musical.', 's': 'EF06AR22, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 8, 't': 'A Música e o Corpo!', 'c': 'Percussão Corporal. Composição Musical.', 'o': 'Criar composições musicais a partir de percussões corporais.', 's': 'EF06AR22, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 9, 't': 'A Voz na Música', 'c': 'Composição Musical. Improvisação Vocal.', 'o': 'Improvisar utilizando vozes e sons corporais.', 's': 'EF06AR22, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 10, 't': 'Minha contribuição para a música!', 'c': 'Colaboração Musical. Improvisação Musical.', 'o': 'Expressar ideias musicais de forma individual e coletiva.', 's': 'EF06AR22, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 11, 't': 'Refinando nossa composição', 'c': 'Composição Musical. Produção Musical.', 'o': 'Colaborar no processo de criação de composições musicais.', 's': 'EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 12, 't': 'Gravando nossa composição', 'c': 'Produção Musical. Registro Musical.', 'o': 'Registrar composições musicais em formato de áudio.', 's': 'EF06AR22, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 13, 't': 'Registros da Nossa Vida', 'c': 'Produção Musical. Registro Musical Audiovisual.', 'o': 'Registrar composições musicais em formato audiovisual.', 's': 'EF06AR22, EF06AR23', 'ae_c': 'AE4', 'ae': 'AE4 - Criar composições musicais, por meio da voz, sons corporais e instrumentos não convencionais, traduzindo-as em partituras criativas.'},
            {'b': 2, 'n': 14, 't': 'Refletindo sobre o processo', 'c': 'Circulação Musical. Repertório Musical.', 'o': 'Analisar criticamente os contextos de produção e circulação da música.', 's': 'EF06AR16, EF06AR23', 'ae_c': 'AE3', 'ae': 'AE3 - Analisar os gêneros da música brasileira a partir de seus contextos de produção, circulação e apreciação.'},

            # 3º Bimestre - Artes Visuais / Dobradura, Gravura e Animação
            {'b': 3, 'n': 1, 't': 'Arte nas dobras de papel', 'c': 'Dobradura. Elementos da dobradura.', 'o': 'Apreciar dobraduras de artistas brasileiros e estrangeiros.', 's': 'EF06AR01, EF06AR04', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 2, 't': 'Explorando dobraduras', 'c': 'Dobradura. Tridimensionalidade.', 'o': 'Explorar o conceito de tridimensionalidade a partir da dobradura.', 's': 'EF06AR01, EF06AR02', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 3, 't': 'Dobraduras dinâmicas', 'c': 'Tridimensionalidade. Arte e interatividade.', 'o': 'Explorar elementos formais como linha, volume, cor, textura e movimento.', 's': 'EF06AR01, EF06AR04', 'ae_c': 'AE6', 'ae': 'AE6 - Identificar materiais, técnicas e características da dobradura, lambe-lambe e da animação.'},
            {'b': 3, 'n': 4, 't': 'Gravura', 'c': 'Gravura e xilogravura. Conceitos e estilos visuais.', 'o': 'Desenvolver uma gravura utilizando materiais não convencionais.', 's': 'EF06AR01, EF06AR02', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 5, 't': 'Da xilogravura à animação', 'c': 'Gravura e Xilogravura. Animação.', 'o': 'Explorar o universo da animação e sua forma de contar histórias.', 's': 'EF06AR01, EF06AR02', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 6, 't': 'Criando Flipbooks', 'c': 'Técnica de animação. Flipbook. Narrativa visual.', 'o': 'Desenvolver o conceito de movimento sequencial a partir da gravura.', 's': 'EF06AR01, EF06AR05', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 7, 't': 'Explorando as estéticas da animação', 'c': 'Técnicas de animação. Animações do mundo.', 'o': 'Analisar estilos e técnicas de animação.', 's': 'EF06AR01, EF06AR04', 'ae_c': 'AE6', 'ae': 'AE6 - Identificar materiais, técnicas e características da dobradura, lambe-lambe e da animação.'},
            {'b': 3, 'n': 8, 't': 'Criando stop-motion', 'c': 'Stop-motion. Animações do mundo.', 'o': 'Utilizar a técnica do stop-motion na construção de uma animação.', 's': 'EF06AR05', 'ae_c': 'AE6', 'ae': 'AE6 - Identificar materiais, técnicas e características da dobradura, lambe-lambe e da animação.'},
            {'b': 3, 'n': 9, 't': 'Da animação ao lambe-lambe: Criando cartazes!', 'c': 'Cartazes. Lambe-Lambe.', 'o': 'Relacionar o lambe-lambe à cultura visual e comunicação urbana.', 's': 'EF06AR01, EF06AR05', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 10, 't': 'Letras no lambe-lambe', 'c': 'Tipografia. Lambe-lambe.', 'o': 'Criar cartazes de lambe lambe que se relacionem com as produções.', 's': 'EF06AR03', 'ae_c': 'AE6', 'ae': 'AE6 - Identificar materiais, técnicas e características da dobradura, lambe-lambe e da animação.'},
            {'b': 3, 'n': 11, 't': 'Intervenção artística coletiva', 'c': 'Intervenção artística. Expografia. Arte Urbana.', 'o': 'Planejar uma intervenção artística coletiva em grande formato.', 's': 'EF06AR01, EF06AR06', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},
            {'b': 3, 'n': 12, 't': 'Arte: espaço de apreciação', 'c': 'Curadoria e Montagem.', 'o': 'Criar um espaço de apreciação das produções artísticas realizadas.', 's': 'EF06AR06', 'ae_c': 'AE5', 'ae': 'AE5 - Investigar a dobradura, gravura, lambe-lambe e animação de diversas períodos históricos, matrizes estéticas e culturais.'},

            # 4º Bimestre - Teatro e Circo
            {'b': 4, 'n': 1, 't': 'Fugindo com o circo: Memórias do circo paulista', 'c': 'História do Circo. Circo Paulista. Jogos Teatrais.', 'o': 'Investigar a história do circo paulista e vivenciar jogos preparatórios.', 's': 'EF06AR24, EF06AR28', 'ae_c': 'AE7', 'ae': 'AE7 - Investigar a comédia e a farsa como gêneros teatrais, relacionando-os à linguagem circense em diferentes contextos históricos e espaciais.'},
            {'b': 4, 'n': 2, 't': 'O poder do riso', 'c': 'Função Social do Riso. Comédia no Circo.', 'o': 'Debater a função social do riso e vivenciar jogos teatrais.', 's': 'EF06AR24, EF06AR25, EF06AR28', 'ae_c': 'AE7', 'ae': 'AE7 - Investigar a comédia e a farsa como gêneros teatrais, relacionando-os à linguagem circense em diferentes contextos históricos e espaciais.'},
            {'b': 4, 'n': 3, 't': 'O Augusto e o Branco', 'c': 'Palhaçaria. Dinâmicas Circenses.', 'o': 'Analisar dinâmicas circenses na palhaçaria e números clássicos.', 's': 'EF06AR24, EF06AR26', 'ae_c': 'AE8', 'ae': 'AE8 - Experimentar elementos envolvidos na composição de acontecimentos cênicos da comédia e da farsa.'},
            {'b': 4, 'n': 4, 't': 'A trupe chegou: funções e organização', 'c': 'Funções Teatrais. Organização do Circo.', 'o': 'Explorar a integração de funções cênicas em um espetáculo coletivo.', 's': 'EF06AR24, EF06AR28', 'ae_c': 'AE9', 'ae': 'AE9 - Experimentar as diferentes funções teatrais e elementos da composição cênica na criação de personagens.'},
            {'b': 4, 'n': 5, 't': 'Teatro e circo: velhos companheiros', 'c': 'Circo e Teatro. Evolução Histórica.', 'o': 'Identificar a relação histórica e as trocas entre teatro e circo.', 's': 'EF06AR24, EF06AR25, EF06AR28', 'ae_c': 'AE7', 'ae': 'AE7 - Investigar a comédia e a farsa como gêneros teatrais, relacionando-os à linguagem circense em diferentes contextos históricos e espaciais.'},
            {'b': 4, 'n': 6, 't': 'A comédia e a farsa no circo', 'c': 'Comédia e Farsa. História do Riso. Palhaçaria Clássica.', 'o': 'Investigar a comédia e a farsa como gêneros com timing cômico.', 's': 'EF06AR25, EF06AR26', 'ae_c': 'AE8', 'ae': 'AE8 - Experimentar elementos envolvidos na composição de acontecimentos cênicos da comédia e da farsa.'},
            {'b': 4, 'n': 7, 't': 'Meu palhaço pessoal', 'c': 'Matrizes Estéticas. Figurinos e Adereços.', 'o': 'Apresentar um número circense autoral de forma coletiva ou individual.', 's': 'EF06AR24, EF06AR25, EF06AR28', 'ae_c': 'AE7', 'ae': 'AE7 - Investigar a comédia e a farsa como gêneros teatrais, relacionando-os à linguagem circense em diferentes contextos históricos e espaciais.'},
            {'b': 4, 'n': 8, 't': 'O nariz do palhaço', 'c': 'Matrizes Estéticas. Figurinos. Autoconhecimento.', 'o': 'Investigar elementos de cena que compõem o espetáculo circense.', 's': 'EF06AR24, EF06AR25, EF06AR28', 'ae_c': 'AE8', 'ae': 'AE8 - Experimentar elementos envolvidos na composição de acontecimentos cênicos da comédia e da farsa.'},
            {'b': 4, 'n': 9, 't': 'Levantando a lona do circo', 'c': 'Elementos de Cena. Função do Riso. Números Clássicos.', 'o': 'Investigar elementos de cena (figurinos, objetos, iluminação).', 's': 'EF06AR25, EF06AR26', 'ae_c': 'AE8', 'ae': 'AE8 - Experimentar elementos envolvidos na composição de acontecimentos cênicos da comédia e da farsa.'},
            {'b': 4, 'n': 10, 't': 'Confusão nos bastidores?', 'c': 'Produção Coletiva. Dinâmicas de Grupo.', 'o': 'Analisar dinâmicas de criação de grupos circenses e cooperação.', 's': 'EF06AR24, EF06AR26, EF06AR28', 'ae_c': 'AE7', 'ae': 'AE7 - Investigar a comédia e a farsa como gêneros teatrais, relacionando-os à linguagem circense em diferentes contextos históricos e espaciais.'},
            {'b': 4, 'n': 11, 't': 'Criando e ensaiando cenas cômicas', 'c': 'Criação de Espetáculo. Preparação de Números.', 'o': 'Ensaiar um número circense com foco cômico e divisão de papéis.', 's': 'EF06AR25, EF06AR28', 'ae_c': 'AE8', 'ae': 'AE8 - Experimentar elementos envolvidos na composição de acontecimentos cênicos da comédia e da farsa.'},
            {'b': 4, 'n': 12, 't': 'O grande dia: o circo-teatro chegou!', 'c': 'Improvisação Teatral. Elementos Cênicos.', 'o': 'Apresentar número circense em interação com o público.', 's': 'EF06AR26, EF06AR28', 'ae_c': 'AE8', 'ae': 'AE8 - Experimentar elementos envolvidos na composição de acontecimentos cênicos da comédia e da farsa.'}
        ]

        for a in arte_6_aulas:
            if not ScopeLesson.query.filter_by(subject_id=subj_arte.id, education_level='fundamental', grade='6º Ano', bimester=a['b'], lesson_number=a['n'], year=2026).first():
                db.session.add(ScopeLesson(
                    subject_id=subj_arte.id, education_level='fundamental', grade='6º Ano',
                    bimester=a['b'], lesson_number=a['n'], title=a['t'], content=a['c'],
                    learning_objectives=a['o'], skills=a['s'], essential_learning_code=a['ae_c'],
                    essential_learning=a['ae'], year=2026
                ))

        if not CurriculumDocument.query.filter_by(subject_id=subj_arte.id, grade='6º Ano').first():
            db.session.add(CurriculumDocument(
                subject_id=subj_arte.id, education_level='fundamental', grade='6º Ano',
                document_year=2026, file_name='Guia_Curriculo_Priorizado_EF_Arte_6Ano.pdf',
                file_path='uploads/Guia_Curriculo_Priorizado_EF_Arte_6Ano.pdf',
                total_lessons=len(arte_6_aulas), status='processado'
            ))

        # -------------------------------------------------------------
        # 2. EDUCAÇÃO FÍSICA (Ensino Fundamental: 6º Ano)
        # -------------------------------------------------------------
        subj_edf = Subject.query.filter_by(name='Educação Física', education_level='fundamental').first()
        if not subj_edf:
            subj_edf = Subject(name='Educação Física', education_level='fundamental', active=True)
            db.session.add(subj_edf)
            db.session.commit()

        edf_6_aulas = [
            # 1º Bimestre - Handebol e Atletismo
            {'b': 1, 'n': 1, 't': 'Esporte de invasão: handebol', 'c': 'Definição de esporte de invasão. História e regras do handebol.', 'o': 'Conhecer as regras e fundamentos básicos do handebol.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 2, 't': 'O jogo de queimada', 'c': 'Jogo pré-desportivo do handebol: queimada.', 'o': 'Vivenciar jogos pré-desportivos valorizando o trabalho coletivo.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 3, 't': 'Jogo resgate', 'c': 'Jogo pré-desportivo do handebol: Resgate.', 'o': 'Comparar semelhanças e diferenças entre jogos pré-desportivos e o esporte.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 4, 't': 'Circuito de estações com fundamentos do handebol', 'c': 'Empunhadura, recepção, passe, finta, drible e arremesso.', 'o': 'Vivenciar os fundamentos do handebol em circuito lúdico.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 5, 't': 'Fundamentos do handebol', 'c': 'Exercícios em duplas, trios e grupos.', 'o': 'Vivenciar os fundamentos técnicos do handebol.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 6, 't': 'Jogo de handebol: masculino e feminino', 'c': 'Equipes femininas e masculinas com regras.', 'o': 'Praticar o handebol respeitando regras e estratégias.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 7, 't': 'Partida mista de handebol', 'c': 'Jogo de handebol com equipes mistas.', 'o': 'Solucionar desafios técnico-táticos respeitando os colegas independentemente do gênero.', 's': 'EF06EF03, EF06EF04, EF06EF05', 'ae_c': 'AE1', 'ae': 'AE1 - Praticar o handebol, utilizando habilidades técnico-táticas básicas e valorizando o trabalho coletivo e o protagonismo.'},
            {'b': 1, 'n': 8, 't': 'Esporte de marca: o atletismo e o atletismo paralímpico', 'c': 'Definição de esporte de marca. Provas de atletismo.', 'o': 'Conhecer o universo do atletismo e dos jogos paralímpicos.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},
            {'b': 1, 'n': 9, 't': 'Corrida de velocidade e de revezamento', 'c': 'Corridas de velocidade e revezamento.', 'o': 'Experimentar corridas valorizando o trabalho coletivo.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},
            {'b': 1, 'n': 10, 't': 'Corrida com barreiras e com obstáculos', 'c': 'Corridas com barreiras e obstáculos.', 'o': 'Experimentar superação de obstáculos no atletismo.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},
            {'b': 1, 'n': 11, 't': 'Saltos', 'c': 'Salto vertical e salto horizontal.', 'o': 'Vivenciar técnicas de saltos do atletismo.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},
            {'b': 1, 'n': 12, 't': 'Arremessos e lançamentos', 'c': 'Arremesso de peso e lançamento de disco.', 'o': 'Experimentar técnicas de arremessos e lançamentos.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},
            {'b': 1, 'n': 13, 't': 'Atletismo para todos', 'c': 'Caminhada de olhos vendados com guia.', 'o': 'Vivenciar de maneira adaptada o atletismo paralímpico.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},
            {'b': 1, 'n': 14, 't': 'Atletismo paralímpico', 'c': 'Corrida de olhos vendados com guia.', 'o': 'Vivenciar e valorizar a importância da inclusão no esporte.', 's': 'EF06EF03, EF06EF22*', 'ae_c': 'AE2', 'ae': 'AE2 - Experimentar as provas do atletismo e do atletismo paralímpico, respeitando as diferenças individuais.'},

            # 2º Bimestre - Danças Urbanas e Ginástica de Condicionamento
            {'b': 2, 'n': 1, 't': 'O universo da dança e o hip-hop', 'c': 'Danças urbanas, música e cultura hip-hop.', 'o': 'Conhecer a origem e evolução das danças urbanas.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 2, 't': 'A dança como forma de expressão', 'c': 'Diferentes sensações através da dança.', 'o': 'Experimentar ritmos e expressões por meio da dança.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 3, 't': 'Meu RAP', 'c': 'Processo criativo: RAP.', 'o': 'Criar, escrever e apresentar um RAP.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 4, 't': 'O Break', 'c': 'Movimentos do Break dance.', 'o': 'Vivenciar movimentos básicos de break dance.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 5, 't': 'Criação de coreografias', 'c': 'Criação coreográfica de hip-hop em grupos.', 'o': 'Criar coreografias de hip-hop em grupos planejando estratégias.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 6, 't': 'Ensaio geral', 'c': 'Ensaio das coreografias criadas.', 'o': 'Ensaiar coreografias em grupo aprimorando a sincronia.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 7, 't': 'Hora da batalha de hip-hop', 'c': 'Apresentação das coreografias criadas.', 'o': 'Apresentar coreografias de hip-hop respeitando a diversidade.', 's': 'EF06EF11, EF06EF12', 'ae_c': 'AE3', 'ae': 'AE3 - Vivenciar danças urbanas para a criação e apresentação de coreografias, identificando elementos do hip-hop.'},
            {'b': 2, 'n': 8, 't': 'Ginástica de condicionamento físico e capacidades físicas', 'c': 'Conceitos de exercícios aeróbios e anaeróbios.', 'o': 'Identificar capacidades físicas na ginástica de condicionamento.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'},
            {'b': 2, 'n': 9, 't': 'Aula de alongamento', 'c': 'Prática de alongamento e flexibilidade.', 'o': 'Desenvolver a flexibilidade corporal.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'},
            {'b': 2, 'n': 10, 't': 'Circuito de capacidades físicas', 'c': 'Flexibilidade, velocidade, agilidade, resistência e força.', 'o': 'Experimentar circuitos que solicitem diferentes capacidades.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'},
            {'b': 2, 'n': 11, 't': 'Estafetas de capacidades físicas', 'c': 'Velocidade e agilidade em estafetas.', 'o': 'Vivenciar exercícios lúdicos de velocidade e agilidade.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'},
            {'b': 2, 'n': 12, 't': 'Os exercícios aeróbios', 'c': 'Caminhar, correr e pedalar.', 'o': 'Vivenciar exercícios aeróbios e seus benefícios cardíacos.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'},
            {'b': 2, 'n': 13, 't': 'Os exercícios anaeróbios - membros superiores', 'c': 'Exercícios de força para membros superiores.', 'o': 'Vivenciar exercícios anaeróbios para membros superiores.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'},
            {'b': 2, 'n': 14, 't': 'Os exercícios anaeróbios - membros inferiores', 'c': 'Exercícios de força para membros inferiores.', 'o': 'Vivenciar exercícios anaeróbios para membros inferiores.', 's': 'EF06EF08, EF06EF09', 'ae_c': 'AE4', 'ae': 'AE4 - Praticar exercícios da ginástica de condicionamento físico, identificando as capacidades físicas envolvidas.'}
        ]

        for a in edf_6_aulas:
            if not ScopeLesson.query.filter_by(subject_id=subj_edf.id, education_level='fundamental', grade='6º Ano', bimester=a['b'], lesson_number=a['n'], year=2026).first():
                db.session.add(ScopeLesson(
                    subject_id=subj_edf.id, education_level='fundamental', grade='6º Ano',
                    bimester=a['b'], lesson_number=a['n'], title=a['t'], content=a['c'],
                    learning_objectives=a['o'], skills=a['s'], essential_learning_code=a['ae_c'],
                    essential_learning=a['ae'], year=2026
                ))

        if not CurriculumDocument.query.filter_by(subject_id=subj_edf.id, grade='6º Ano').first():
            db.session.add(CurriculumDocument(
                subject_id=subj_edf.id, education_level='fundamental', grade='6º Ano',
                document_year=2026, file_name='Guia_Curriculo_Priorizado_EF_Educacao_Fisica_6Ano.pdf',
                file_path='uploads/Guia_Curriculo_Priorizado_EF_Educacao_Fisica_6Ano.pdf',
                total_lessons=len(edf_6_aulas), status='processado'
            ))

        # -------------------------------------------------------------
        # 3. CIÊNCIAS (Ensino Fundamental: 6º, 7º, 8º e 9º Anos)
        # -------------------------------------------------------------
        subj_cie = Subject.query.filter_by(name='Ciências', education_level='fundamental').first()
        if not subj_cie:
            subj_cie = Subject(name='Ciências', education_level='fundamental', active=True)
            db.session.add(subj_cie)
            db.session.commit()

        # 6º Ano Ciências (21 aulas no 1º bim, 21 no 2º, 18 no 3º, 18 no 4º)
        cie_6_aulas = [
            # 1º Bimestre
            {'b': 1, 'n': 1, 't': 'Big Bang e surgimento do Sistema Solar', 'c': 'Big Bang. Método científico.', 'o': 'Apresentar teorias e hipóteses científicas sobre a origem do Universo.', 's': 'EF06CI11', 'ae_c': 'AE1', 'ae': 'AE1 - Descrever as esferas que compõem a Terra, reconhecendo o surgimento da litosfera e suas transformações ao longo do tempo.'},
            {'b': 1, 'n': 2, 't': 'O Sistema Solar', 'c': 'Sistema Solar. Corpos celestes.', 'o': 'Apresentar planetas e corpos celestes e a diferenciação entre estrela e planeta.', 's': 'EF06CI11', 'ae_c': 'AE1', 'ae': 'AE1 - Descrever as esferas que compõem a Terra, reconhecendo o surgimento da litosfera e suas transformações ao longo do tempo.'},
            {'b': 1, 'n': 3, 't': 'Terra Primitiva: formação do planeta Terra', 'c': 'Terra primitiva e transformações geológicas.', 'o': 'Explicar as características da Terra em seu surgimento e transformações.', 's': 'EF06CI11', 'ae_c': 'AE1', 'ae': 'AE1 - Descrever as esferas que compõem a Terra, reconhecendo o surgimento da litosfera e suas transformações ao longo do tempo.'},
            {'b': 1, 'n': 4, 't': 'Tempo histórico × Tempo geológico × Tempo cronológico', 'c': 'Tempo geológico e cronológico.', 'o': 'Diferenciar tempo histórico, geológico e cronológico.', 's': 'EF06CI11', 'ae_c': 'AE1', 'ae': 'AE1 - Descrever as esferas que compõem a Terra, reconhecendo o surgimento da litosfera e suas transformações ao longo do tempo.'},
            {'b': 1, 'n': 5, 't': 'Tempo geológico', 'c': 'Éons e Eras geológicas.', 'o': 'Descrever a divisão do tempo geológico em Éons e Eras.', 's': 'EF06CI13', 'ae_c': 'AE1', 'ae': 'AE1 - Descrever as esferas que compõem a Terra, reconhecendo o surgimento da litosfera e suas transformações ao longo do tempo.'},
            {'b': 1, 'n': 6, 't': 'Gravidade', 'c': 'Força gravitacional.', 'o': 'Reconhecer a força gravitacional e sua influência nos corpos celestes.', 's': 'EF06CI13', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 7, 't': 'Evidências da esfericidade da Terra', 'c': 'Esfericidade da Terra.', 'o': 'Apresentar argumentos científicos que comprovem a esfericidade da Terra.', 's': 'EF06CI13', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 8, 't': 'Movimento de rotação', 'c': 'Movimento de rotação terrestre.', 'o': 'Compreender a rotação e a sucessão de dias e noites.', 's': 'EF06CI13, EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 9, 't': 'Movimento de translação', 'c': 'Movimento de translação terrestre.', 'o': 'Compreender a translação e o ciclo anual.', 's': 'EF06CI13, EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 10, 't': 'Movimento aparente do Sol', 'c': 'Movimento aparente do Sol. Pontos cardeais.', 'o': 'Compreender o movimento aparente do Sol e os pontos cardeais.', 's': 'EF06CI13, EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 11, 't': 'Relógio de sol – Parte 1', 'c': 'Construção do relógio de sol.', 'o': 'Construir um relógio de sol e compreender fenômenos astronômicos.', 's': 'EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 12, 't': 'Relógio de sol – Parte 2', 'c': 'Funcionamento do relógio de sol.', 'o': 'Analisar medições do relógio de sol.', 's': 'EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 13, 't': 'Movimentos da Lua', 'c': 'Fases e movimentos lunares.', 'o': 'Identificar os movimentos da Lua e a percepção da mudança de fase.', 's': 'EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 14, 't': 'Eclipse lunar e solar', 'c': 'Eclipses solares e lunares.', 'o': 'Explicar a ocorrência dos eclipses a partir do alinhamento Terra-Sol-Lua.', 's': 'EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'},
            {'b': 1, 'n': 15, 't': 'Estações do ano: solstício e equinócio', 'c': 'Estações do ano e inclinação do eixo terrestre.', 'o': 'Explicar solstícios, equinócios e estações.', 's': 'EF06CI14', 'ae_c': 'AE2', 'ae': 'AE2 - Explicar os efeitos dos movimentos do Sistema Terra-Sol-Lua na ocorrência de fenômenos naturais.'}
        ]

        for a in cie_6_aulas:
            if not ScopeLesson.query.filter_by(subject_id=subj_cie.id, education_level='fundamental', grade='6º Ano', bimester=a['b'], lesson_number=a['n'], year=2026).first():
                db.session.add(ScopeLesson(
                    subject_id=subj_cie.id, education_level='fundamental', grade='6º Ano',
                    bimester=a['b'], lesson_number=a['n'], title=a['t'], content=a['c'],
                    learning_objectives=a['o'], skills=a['s'], essential_learning_code=a['ae_c'],
                    essential_learning=a['ae'], year=2026
                ))

        if not CurriculumDocument.query.filter_by(subject_id=subj_cie.id, grade='6º Ano').first():
            db.session.add(CurriculumDocument(
                subject_id=subj_cie.id, education_level='fundamental', grade='6º Ano',
                document_year=2026, file_name='Guia_Curriculo_Priorizado_EF_Ciencias_6Ano.pdf',
                file_path='uploads/Guia_Curriculo_Priorizado_EF_Ciencias_6Ano.pdf',
                total_lessons=len(cie_6_aulas), status='processado'
            ))

        # -------------------------------------------------------------
        # 4. LÍNGUA INGLESA (Ensino Fundamental: 6º e 7º Anos)
        # -------------------------------------------------------------
        subj_ing = Subject.query.filter_by(name='Língua Inglesa', education_level='fundamental').first()
        if not subj_ing:
            subj_ing = Subject(name='Língua Inglesa', education_level='fundamental', active=True)
            db.session.add(subj_ing)
            db.session.commit()

        ing_6_aulas = [
            # 1º Bimestre
            {'b': 1, 'n': 1, 't': 'Welcome to 6th grade!', 'c': 'Saudações e despedidas em inglês.', 'o': 'Utilizar expressões básicas de interação e comandos de sala de aula.', 's': 'EF06LI01, EF06LI13, EF06LI16', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 2, 't': 'English in the classroom – Part 1', 'c': 'Vocabulário de sala de aula (Please, Sorry, Thanks, May I go out?).', 'o': 'Utilizar frases e expressões para necessidades básicas da rotina escolar.', 's': 'EF06LI01, EF06LI03, EF06LI13', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 3, 't': 'English in the classroom – Part 2', 'c': 'Comandos e instruções. Palavras cognatas.', 'o': 'Compreender comandos em enunciados simples de tarefas.', 's': 'EF06LI01, EF06LI03, EF06LI05', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 4, 't': 'Nice to meet you!', 'c': 'Names, What is your name?, Possessive pronouns (my, your).', 'o': 'Apresentar-se e interagir para descobrir o nome do interlocutor.', 's': 'EF06LI01, EF06LI02, EF06LI04', 'ae_c': 'AE2', 'ae': 'AE2 - Realizar apresentação oral sobre si mesmo e outras pessoas, compartilhando informações pessoais.'},
            {'b': 1, 'n': 5, 't': 'Names and titles', 'c': 'First/middle/last name, Mr., Miss, Ms., Mrs.', 'o': 'Identificar partes do nome e títulos pessoais em inglês.', 's': 'EF06LI01, EF06LI04, EF06LI05', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 6, 't': 'Names in different countries – Part 1', 'c': 'Alfabeto e soletração (spelling).', 'o': 'Reconhecer e utilizar a soletração como recurso de comunicação.', 's': 'EF06LI01, EF06LI02, EF06LI04', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 7, 't': 'Names in different countries – Part 2', 'c': 'How do you spell...? Prática oral.', 'o': 'Utilizar soletração para trocar informações pessoais.', 's': 'EF06LI01, EF06LI02, EF06LI17', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 8, 't': 'Names in different countries – Part 3', 'c': 'Prática da soletração em inglês.', 'o': 'Esclarecer palavras desconhecidas utilizando soletração.', 's': 'EF06LI01', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 9, 't': 'How old are you?', 'c': 'Numbers 1-20. How old are you? I am...', 'o': 'Perguntar e responder sobre idade em inglês.', 's': 'EF06LI01, EF06LI02, EF06LI04', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 10, 't': 'Numbers 0-20', 'c': 'Números escritos e prática.', 'o': 'Escrever e reconhecer números em inglês.', 's': 'EF06LI14', 'ae_c': 'AE4', 'ae': 'AE4 - Utilizar a escrita para comunicar informações pessoais, familiares, rotinas e preferências.'},
            {'b': 1, 'n': 11, 't': 'Countries and nationalities – Part 1', 'c': 'Where are you from? I am from... / I am...', 'o': 'Reconhecer e comunicar países e nacionalidades.', 's': 'EF06LI05, EF06LI17, EF06LI19', 'ae_c': 'AE2', 'ae': 'AE2 - Realizar apresentação oral sobre si mesmo e outras pessoas, compartilhando informações pessoais.'},
            {'b': 1, 'n': 12, 't': 'Countries and nationalities – Part 2', 'c': 'Países, nacionalidades e identidades culturais.', 'o': 'Trocar informações sobre origens e nacionalidades.', 's': 'EF06LI01, EF06LI02, EF06LI04', 'ae_c': 'AE1', 'ae': 'AE1 - Trocar informações sobre si mesmo, o outro e o universo da sala de aula, atendendo às instruções e comandos orais.'},
            {'b': 1, 'n': 13, 't': 'English Forms', 'c': 'Formulários em inglês (Name, Age, Country).', 'o': 'Compreender e preencher fichas de cadastro em inglês.', 's': 'EF06LI06, EF06LI07, EF06LI08', 'ae_c': 'AE3', 'ae': 'AE3 - Localizar informações pontuais e explícitas sobre si, família, rotina ou preferências em textos escritos.'},
            {'b': 1, 'n': 14, 't': 'Filling in a form', 'c': 'Preenchimento de formulários e interação oral.', 'o': 'Interagir com interlocutores para preencher dados cadastrais.', 's': 'EF06LI01, EF06LI02, EF06LI05', 'ae_c': 'AE2', 'ae': 'AE2 - Realizar apresentação oral sobre si mesmo e outras pessoas, compartilhando informações pessoais.'}
        ]

        for a in ing_6_aulas:
            if not ScopeLesson.query.filter_by(subject_id=subj_ing.id, education_level='fundamental', grade='6º Ano', bimester=a['b'], lesson_number=a['n'], year=2026).first():
                db.session.add(ScopeLesson(
                    subject_id=subj_ing.id, education_level='fundamental', grade='6º Ano',
                    bimester=a['b'], lesson_number=a['n'], title=a['t'], content=a['c'],
                    learning_objectives=a['o'], skills=a['s'], essential_learning_code=a['ae_c'],
                    essential_learning=a['ae'], year=2026
                ))

        if not CurriculumDocument.query.filter_by(subject_id=subj_ing.id, grade='6º Ano').first():
            db.session.add(CurriculumDocument(
                subject_id=subj_ing.id, education_level='fundamental', grade='6º Ano',
                document_year=2026, file_name='Guia_Curriculo_Priorizado_EF_Lingua_Inglesa_6Ano.pdf',
                file_path='uploads/Guia_Curriculo_Priorizado_EF_Lingua_Inglesa_6Ano.pdf',
                total_lessons=len(ing_6_aulas), status='processado'
            ))

        db.session.commit()
        print("\n=== TODAS AS DISCIPLINAS DO ENSINO FUNDAMENTAL FORAM POVOADAS COM SUCESSO! ===")

if __name__ == '__main__':
    seed_all()

