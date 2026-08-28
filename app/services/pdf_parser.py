import re
import os
from typing import Dict, List, Any, Optional
import pdfplumber
from pypdf import PdfReader

# Disciplinas mapeadas
SUBJECT_NAMES = [
    # Ensino Fundamental & Médio
    'Filosofia', 'Sociologia', 'Biologia', 'Física', 'Química',
    'História', 'Geografia', 'Matemática', 'Língua Portuguesa',
    'Arte', 'Educação Física', 'Língua Inglesa', 'Ciências'
]

class CurriculumPdfParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_text = ""
        self.pages_text = []
        
    def _read_pdf_text(self):
        self.pages_text = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                self.pages_text.append(text)
        self.raw_text = "\n".join(self.pages_text)

    def detect_metadata(self) -> Dict[str, Any]:
        """Detecta o componente curricular, nível de ensino, série e ano do documento"""
        if not self.pages_text:
            self._read_pdf_text()

        # Primeiras 5 páginas são capa e sumário
        header_text = "\n".join(self.pages_text[:5])
        
        # 1. Detectar Componente
        detected_subject = "Filosofia"
        for sub in SUBJECT_NAMES:
            if re.search(rf"\b{re.escape(sub)}\b", header_text, re.IGNORECASE):
                detected_subject = sub
                break

        # 2. Detectar Nível de Ensino
        detected_level = "medio"
        if re.search(r"Ensino\s+Fundamental|Anos\s+Finais", header_text, re.IGNORECASE):
            detected_level = "fundamental"
        elif re.search(r"Ensino\s+M[ée]dio", header_text, re.IGNORECASE):
            detected_level = "medio"

        # 3. Detectar Série / Ano
        detected_grade = "1ª Série" if detected_level == "medio" else "6º Ano"
        if "1ª s" in header_text.lower() or "1ª série" in header_text.lower() or "1a serie" in header_text.lower():
            detected_grade = "1ª Série"
        elif "2ª s" in header_text.lower() or "2ª série" in header_text.lower() or "2a serie" in header_text.lower():
            detected_grade = "2ª Série"
        elif "3ª s" in header_text.lower() or "3ª série" in header_text.lower() or "3a serie" in header_text.lower():
            detected_grade = "3ª Série"
        elif "6º" in header_text or "6o" in header_text or "6º ano" in header_text.lower():
            detected_grade = "6º Ano"
        elif "7º" in header_text or "7o" in header_text or "7º ano" in header_text.lower():
            detected_grade = "7º Ano"
        elif "8º" in header_text or "8o" in header_text or "8º ano" in header_text.lower():
            detected_grade = "8º Ano"
        elif "9º" in header_text or "9o" in header_text or "9º ano" in header_text.lower():
            detected_grade = "9º Ano"

        # 4. Ano letivo
        year_match = re.search(r"202[4-9]", header_text)
        detected_year = int(year_match.group(0)) if year_match else 2026

        return {
            'subject_name': detected_subject,
            'education_level': detected_level,
            'grade': detected_grade,
            'document_year': detected_year
        }

    def extract_essential_learnings(self) -> Dict[str, str]:
        """Extrai o mapeamento de AE1..AE20 e suas descrições completas"""
        if not self.pages_text:
            self._read_pdf_text()

        aes = {}
        pattern = re.compile(r'(AE\d+)\s*[-–—]\s*([^\n\r]+(?:\n(?!(?:AE\d+|Não há|Habilidade|1º|2º|3º|4º|Sumário|Governador))[^\n\r]+)*)', re.IGNORECASE)
        
        for text in self.pages_text:
            matches = pattern.findall(text)
            for code, desc in matches:
                clean_code = code.upper().strip()
                clean_desc = " ".join(desc.split()).strip()
                if clean_code not in aes or len(clean_desc) > len(aes[clean_code]):
                    aes[clean_code] = f"{clean_code} - {clean_desc}"
                    
        return aes

    def extract_scope_lessons(self, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extrai todas as aulas estruturadas das tabelas de Escopo-Sequência"""
        if not self.pages_text:
            self._read_pdf_text()

        meta = metadata or self.detect_metadata()
        aes_dict = self.extract_essential_learnings()
        lessons = []

        with pdfplumber.open(self.file_path) as pdf:
            current_bimester = 1

            for page_idx, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                
                # Detectar se a página pertence ao Escopo-Sequência
                if "Escopo" not in page_text and "Sequência" not in page_text and "Sequencia" not in page_text:
                    # Se não tiver a palavra-chave no texto, pula se não for tabela de escopo
                    continue

                # Atualizar Bimestre corrente com base no cabeçalho da página
                bim_match = re.search(r'([1-4])º\s*Bimestre', page_text, re.IGNORECASE)
                if bim_match:
                    current_bimester = int(bim_match.group(1))

                # Extrair tabelas estruturadas
                tables = page.extract_tables()
                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    # Identificar cabeçalho da tabela
                    header_row = [str(c).replace('\n', ' ').strip().lower() for c in table[0] if c is not None]
                    header_str = " ".join(header_row)

                    if not ('aula' in header_str or 'conteúdo' in header_str or 'conteudo' in header_str or 'objetivo' in header_str):
                        # Pode ser a segunda linha se a primeira for título mesclado
                        if len(table) > 2:
                            header_row = [str(c).replace('\n', ' ').strip().lower() for c in table[1] if c is not None]
                            header_str = " ".join(header_row)
                            if 'aula' in header_str or 'conteúdo' in header_str or 'conteudo' in header_str:
                                rows_to_process = table[2:]
                            else:
                                continue
                        else:
                            continue
                    else:
                        rows_to_process = table[1:]

                    for row in rows_to_process:
                        if not row or len(row) < 3:
                            continue

                        # Limpar células
                        row_cells = [str(c).strip() if c is not None else "" for c in row]
                        
                        # Procurar número da aula
                        col0 = row_cells[0]
                        # Pode vir "1 \n Por que filosofia?" ou número isolado
                        lesson_num_match = re.search(r'^\s*(\d+)\b', col0)
                        
                        lesson_num = None
                        title = ""
                        content = ""
                        objectives = ""
                        skills = ""
                        ae_code = ""
                        ae_text = ""

                        if lesson_num_match:
                            lesson_num = int(lesson_num_match.group(1))
                            # O título pode estar na mesma célula ou na seguinte
                            rest_col0 = col0[lesson_num_match.end():].strip()
                            if rest_col0:
                                title = rest_col0
                            elif len(row_cells) > 1 and not re.match(r'^[•\-\*]', row_cells[1]) and len(row_cells) >= 5:
                                title = row_cells[1]
                        else:
                            # Tentar na segunda coluna se a primeira for em branco
                            if len(row_cells) > 1 and re.search(r'^\s*(\d+)\b', row_cells[1]):
                                m = re.search(r'^\s*(\d+)\b', row_cells[1])
                                lesson_num = int(m.group(1))
                                title = row_cells[1][m.end():].strip()

                        if lesson_num is None:
                            continue

                        # Mapear colunas de acordo com o tamanho da linha
                        if len(row_cells) >= 5:
                            # Formato clássico: [Aula/Título, Conteúdo, Objetivos, Habilidades, Aprendizagem Essencial]
                            # Ou [Aula, Título, Conteúdo, Objetivos, Habilidades, Aprendizagem Essencial]
                            if len(row_cells) == 5:
                                if not title:
                                    # Se a coluna 0 era só o número, o título pode estar na primeira linha do conteúdo
                                    title = f"Aula {lesson_num}"
                                content = row_cells[1]
                                objectives = row_cells[2]
                                skills = row_cells[3]
                                ae_col = row_cells[4]
                            elif len(row_cells) >= 6:
                                if not title:
                                    title = row_cells[1]
                                content = row_cells[2]
                                objectives = row_cells[3]
                                skills = row_cells[4]
                                ae_col = row_cells[5]

                            # Extrair código e texto da AE
                            ae_code_match = re.search(r'(AE\d+)', ae_col, re.IGNORECASE)
                            if ae_code_match:
                                ae_code = ae_code_match.group(1).upper()
                                ae_text = ae_col
                            elif ae_col:
                                ae_text = ae_col

                            # Se o texto da AE for curto, buscar na tabela de AEs do próprio PDF
                            if ae_code and ae_code in aes_dict and len(aes_dict[ae_code]) > len(ae_text):
                                ae_text = aes_dict[ae_code]

                        elif len(row_cells) == 4:
                            content = row_cells[1]
                            objectives = row_cells[2]
                            skills = row_cells[3]
                            if not title:
                                title = f"Aula {lesson_num}"

                        # Limpar formatações
                        title = title.replace('\n', ' ').strip()
                        if not title:
                            title = f"Aula {lesson_num}"
                        
                        # Extrair código de habilidade do campo de habilidades
                        skills_codes = re.findall(r'(EM\d+[A-Z\d]+|EF\d+[A-Z\d]+)', skills)
                        clean_skills = ", ".join(dict.fromkeys(skills_codes)) if skills_codes else skills.replace('\n', ' ').strip()

                        # Salvar aula estruturada
                        lessons.append({
                            'education_level': meta['education_level'],
                            'grade': meta['grade'],
                            'bimester': current_bimester,
                            'lesson_number': lesson_num,
                            'title': title,
                            'content': content.strip(),
                            'learning_objectives': objectives.strip(),
                            'skills': clean_skills,
                            'essential_learning_code': ae_code,
                            'essential_learning': ae_text.strip(),
                            'year': meta['document_year']
                        })

        # Ordenar por bimestre e número da aula
        lessons.sort(key=lambda x: (x['bimester'], x['lesson_number']))
        
        # Remover eventuais duplicatas exatas
        unique_lessons = []
        seen = set()
        for l in lessons:
            key = (l['bimester'], l['lesson_number'])
            if key not in seen:
                seen.add(key)
                unique_lessons.append(l)

        return unique_lessons

