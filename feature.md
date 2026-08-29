tenha como base o projeto que sa iniciei em php'plano de aula'


# PAPEL DA IA

Você é um desenvolvedor Full Stack especializado em:

- Python
- Flask
- MySQL
- HTML5
- CSS3
- JavaScript

Sua tarefa é desenvolver um sistema web completo para criação, organização
e gerenciamento de planos de aula.

O sistema será utilizado por professores e deverá possuir autenticação,
controle de acesso, painel do professor, painel administrativo, banco de
dados MySQL, importação de documentos PDF e geração de planos em PDF.

O projeto deverá ser organizado, modular, seguro, responsivo e de fácil
manutenção.

Não altere as regras de negócio descritas neste documento sem informar
previamente.

Não gere todo o projeto de uma única vez.

Primeiro apresente:
1. arquitetura;
2. banco de dados;
3. relacionamentos;
4. estrutura de pastas;
5. rotas;
6. fluxo das páginas.

Somente depois comece a gerar os arquivos do projeto.


==================================================
# 1. OBJETIVO DO SISTEMA
==================================================

Criar um sistema web destinado a professores para:

- realizar cadastro;
- fazer login;
- acessar seu perfil;
- editar seus dados;
- criar planos de aula;
- consultar planos já criados;
- editar planos;
- excluir planos;
- visualizar planos;
- imprimir planos;
- gerar planos em PDF;
- organizar planos por bimestre.

Os planos deverão utilizar informações curriculares provenientes dos
PDFs do Guia do Currículo Priorizado.

Existe um PDF específico para cada componente curricular.

Esses PDFs possuem informações de Escopo-Sequência que deverão ser
extraídas previamente e armazenadas no banco de dados.

IMPORTANTE:

O PDF NÃO deverá ser processado novamente toda vez que o professor
criar um plano.

O fluxo correto deverá ser:

PDF
↓
Processamento pelo backend Python
↓
Extração do Escopo-Sequência
↓
Validação
↓
Armazenamento no MySQL
↓
Consulta dos dados pelo Gerador de Plano de Aula


==================================================
# 2. TECNOLOGIAS
==================================================

BACKEND

- Python
- Flask

FRONTEND

- HTML5
- CSS3
- JavaScript

BANCO DE DADOS

- MySQL

OUTROS RECURSOS

- biblioteca Python para leitura de PDFs;
- biblioteca para geração de PDFs;
- autenticação por sessão;
- ORM ou consultas parametrizadas;
- proteção CSRF;
- validação no backend e frontend.


==================================================
# 3. TIPOS DE USUÁRIOS
==================================================

O sistema deverá possuir dois tipos de usuário:

1. PROFESSOR
2. ADMINISTRADOR


==================================================
# 4. CADASTRO DO PROFESSOR
==================================================

Criar a página:

"Criar conta"

Campos obrigatórios:

- Nome completo
- E-mail
- Telefone
- Senha
- Confirmação de senha

O sistema deverá validar:

- preenchimento dos campos obrigatórios;
- formato do e-mail;
- existência prévia do e-mail;
- senha e confirmação de senha;
- impedir cadastro duplicado utilizando o mesmo e-mail.

Caso senha e confirmação sejam diferentes, apresentar uma mensagem
informando que as senhas não coincidem.

A senha nunca deverá ser armazenada em texto puro.

Utilizar hash seguro.

Depois da validação, criar o registro na tabela:

users

O usuário deverá receber:

role = professor

status = pendente


==================================================
# 5. APROVAÇÃO DO PROFESSOR
==================================================

IMPORTANTE:

O professor poderá fazer login mesmo enquanto seu cadastro estiver
com status "pendente".

Entretanto, enquanto não houver confirmação do administrador, o
professor NÃO poderá criar planos de aula.

Fluxo:

Cadastro
↓
status = pendente
↓
Professor pode fazer login
↓
Professor acessa a Home
↓
Sistema informa que o cadastro aguarda confirmação
↓
Administrador confirma o professor
↓
status = ativo
↓
Professor passa a poder criar planos de aula

Enquanto:

status = pendente

o professor poderá:

- fazer login;
- acessar sua Home;
- acessar Meu Perfil;
- editar seus dados;
- alterar sua senha;
- acessar a página de Planos de Aula.

Porém NÃO poderá:

- criar um novo plano de aula;
- salvar um novo plano.

O botão:

"Novo Plano"

deverá permanecer desabilitado ou indisponível enquanto o usuário
estiver pendente.

Mostrar uma mensagem como:

"Seu cadastro está aguardando confirmação do administrador.
Após a aprovação, a criação de planos de aula será liberada."

IMPORTANTE:

Essa restrição NÃO poderá existir somente no JavaScript.

O backend também deverá verificar:

status == ativo

antes de permitir acesso à rota de criação ou salvamento de um plano.

Mesmo que o usuário tente acessar manualmente a URL de criação,
o backend deverá impedir a operação caso seu status seja "pendente".


==================================================
# 6. CONFIRMAÇÃO PELO ADMINISTRADOR
==================================================

O administrador deverá possuir uma página para visualizar os professores
cadastrados.

Organizar os professores por status:

- Pendentes
- Ativos

Para professores pendentes, disponibilizar a ação:

"Aprovar cadastro"

Ao aprovar:

status = ativo

A partir desse momento o professor poderá criar planos de aula.

Também registrar, se possível:

- data da aprovação;
- administrador responsável pela aprovação.


==================================================
# 7. LOGIN DO PROFESSOR
==================================================

Criar a página:

"Acesse sua conta"

Campos:

- E-mail
- Senha

Fluxo:

1. Professor informa e-mail e senha.

2. Backend procura o usuário pelo e-mail.

3. Sistema verifica a senha utilizando o hash armazenado.

4. Se as credenciais estiverem corretas, criar uma sessão autenticada.

5. Armazenar na sessão pelo menos:

- user_id
- nome
- role
- status

6. Redirecionar para a Home do Professor.

O status "pendente" NÃO deverá impedir o login.

O status deverá controlar apenas as funcionalidades que exigem aprovação,
principalmente a criação de planos.

Caso o cadastro não exista ou o e-mail e/ou a senha sejam inválidos,
apresentar:

"E-mail ou senha inválidos."

Também apresentar:

"Ainda não possui cadastro? Criar conta"

Esse link deverá direcionar para:

/cadastro

Não informar separadamente se o problema ocorreu no e-mail ou na senha.


==================================================
# 8. LOGOUT
==================================================

Ao clicar em:

"Sair"

o sistema deverá:

1. encerrar a sessão;
2. remover os dados da sessão;
3. redirecionar para a página de login.


==================================================
# 9. HOME DO PROFESSOR
==================================================

A Home do Professor deverá possuir duas áreas:

1. MENU LATERAL FIXO À ESQUERDA
2. ÁREA DE CONTEÚDO À DIREITA

O menu lateral deverá permanecer fixo durante toda a navegação.


==================================================
# 10. MENU LATERAL
==================================================

Exibir:

- Meu Perfil
- Planos de Aula
- Sair

Quando uma opção for selecionada, alterar apenas o conteúdo exibido
na área direita.

O menu esquerdo deverá permanecer fixo.


==================================================
# 11. MEU PERFIL
==================================================

Quando clicar em:

"Meu Perfil"

carregar os dados do usuário autenticado.

Exibir:

- Nome completo
- E-mail
- Telefone

Permitir edição.

Criar botão:

"Salvar alterações"

Após clicar, atualizar o registro na tabela:

users


==================================================
# 12. ALTERAÇÃO DE SENHA
==================================================

Criar uma área específica contendo:

- Senha atual
- Nova senha
- Confirmação da nova senha

Regras:

- a senha cadastrada nunca deverá ser exibida;
- validar a senha atual;
- nova senha e confirmação precisam ser iguais;
- salvar utilizando novo hash seguro.


==================================================
# 13. PLANOS DE AULA — HOME
==================================================

Ao clicar em:

"Planos de Aula"

carregar:

- campo de busca;
- botão "Novo Plano";
- pasta 1º Bimestre;
- pasta 2º Bimestre;
- pasta 3º Bimestre;
- pasta 4º Bimestre.

Cada pasta deverá apresentar a quantidade de planos salvos naquele
bimestre.

Se:

status = pendente

o botão "Novo Plano" deverá permanecer bloqueado e deverá ser apresentada
a informação de que o cadastro ainda aguarda aprovação.

Se:

status = ativo

o botão deverá funcionar normalmente.


==================================================
# 14. PLANOS POR BIMESTRE
==================================================

Ao clicar em:

- 1º Bimestre
- 2º Bimestre
- 3º Bimestre
- 4º Bimestre

consultar o banco de dados.

Mostrar somente planos:

- pertencentes ao professor autenticado;
- pertencentes ao bimestre selecionado.

Cada plano deverá apresentar:

- Título
- Componente curricular
- Ano/Série
- Turma(s)
- Período
- Data de criação
- Data da última atualização

Disponibilizar ações:

- Visualizar
- Editar
- Excluir
- Gerar PDF


==================================================
# 15. BUSCA DE PLANOS
==================================================

No canto superior direito da página de Planos de Aula deverá existir
um campo de busca.

A pesquisa deverá consultar o banco de dados.

IMPORTANTE:

O professor somente poderá pesquisar seus próprios planos.

Permitir busca por:

- título;
- componente curricular;
- ano/série;
- turma;
- bimestre;
- conteúdo.


==================================================
# 16. NOVO PLANO
==================================================

O botão:

"Novo Plano"

deverá verificar:

status == ativo

Se estiver ativo:

abrir a página de criação.

Se estiver pendente:

não abrir a página e informar que é necessária a confirmação do
administrador.


==================================================
# 17. ORDEM DOS CAMPOS DO PLANO
==================================================

Organizar a página nesta sequência:

Professor
↓
Período
↓
Tipo de Ensino
↓
Componente Curricular
↓
Ano/Série
↓
Turma(s)
↓
Bimestre
↓
Aulas do Escopo-Sequência
↓
Dados preenchidos automaticamente
↓
Número de aulas
↓
Recursos didáticos
↓
Metodologia
↓
Instrumentos de avaliação
↓
Salvar


==================================================
# 18. PROFESSOR
==================================================

O nome do professor deverá ser preenchido automaticamente utilizando
os dados do usuário autenticado.

Não permitir alteração desse campo na página de criação do plano.

Utilizar campo somente leitura.


==================================================
# 19. PERÍODO
==================================================

Criar um calendário que permita selecionar um intervalo:

Data inicial
até
Data final

Exemplo:

03/08/2026 até 14/08/2026

Salvar separadamente:

start_date
end_date


==================================================
# 20. TIPO DE ENSINO
==================================================

Permitir selecionar:

- Ensino Fundamental
- Ensino Médio

Essa escolha deverá controlar dinamicamente os próximos campos.


==================================================
# 21. COMPONENTES — ENSINO FUNDAMENTAL
==================================================

Se o professor selecionar:

ENSINO FUNDAMENTAL

mostrar somente:

- Ciências
- Língua Portuguesa
- Arte
- Educação Física
- Língua Inglesa
- Matemática
- Geografia
- História


==================================================
# 22. COMPONENTES — ENSINO MÉDIO
==================================================

Se selecionar:

ENSINO MÉDIO

mostrar somente:

- Língua Portuguesa
- Arte
- Educação Física
- Língua Inglesa
- Matemática
- Geografia
- História
- Sociologia
- Filosofia
- Biologia
- Física
- Química


==================================================
# 23. ANO / SÉRIE
==================================================

ENSINO FUNDAMENTAL:

- 6º Ano
- 7º Ano
- 8º Ano
- 9º Ano

ENSINO MÉDIO:

- 1ª Série
- 2ª Série
- 3ª Série


==================================================
# 24. TURMAS
==================================================

Depois de selecionar Ano/Série, mostrar:

- A
- B
- C
- D
- E
- F

Combinar automaticamente:

Ano/Série + letra

Exemplos:

8º Ano + A = 8º A

1ª Série + C = 1ª C

Permitir selecionar mais de uma turma.

Exemplo:

8º A
8º B
8º C

Um mesmo plano poderá pertencer a várias turmas.


==================================================
# 25. BIMESTRE
==================================================

Permitir selecionar:

- 1º Bimestre
- 2º Bimestre
- 3º Bimestre
- 4º Bimestre


==================================================
# 26. CONSULTA AO ESCOPO-SEQUÊNCIA
==================================================

Depois de selecionar:

- Tipo de ensino
- Componente curricular
- Ano/Série
- Bimestre

consultar o banco de dados.

Exemplo:

Ensino Médio
+
Filosofia
+
1ª Série
+
2º Bimestre

↓ CONSULTA ↓

Retornar somente as aulas cadastradas para:

Filosofia
1ª Série
2º Bimestre


==================================================
# 27. AULAS DO ESCOPO-SEQUÊNCIA
==================================================

Criar uma área com barra de rolagem.

Mostrar somente:

- Número da aula
- Título da aula

Exemplo:

☐ Aula 1 – Desafios éticos nas relações intergeracionais
☐ Aula 2 – Diálogo e responsabilidade entre gerações
☐ Aula 3 – O olhar do outro nas relações intergeracionais
☐ Aula 4 – Aula desafio: relações intergeracionais

Permitir selecionar uma ou várias aulas.

Não mostrar inicialmente todos os conteúdos curriculares na lista.


==================================================
# 28. PREENCHIMENTO AUTOMÁTICO
==================================================

Quando o professor selecionar uma ou várias aulas, consultar o banco
e preencher automaticamente:

- Títulos das aulas
- Conteúdos
- Objetivos de aprendizagem
- Habilidades
- Aprendizagens Essenciais (AEs)

Esses dados deverão vir da tabela responsável pelo Escopo-Sequência.

O professor não deverá precisar digitá-los.


==================================================
# 29. DADOS REPETIDOS
==================================================

Não repetir habilidades iguais.

Exemplo:

Aula 1 → EM13CHS205
Aula 2 → EM13CHS205
Aula 3 → EM13CHS205

Resultado:

EM13CHS205

Aplicar a mesma regra para Aprendizagens Essenciais.


==================================================
# 30. CAMPOS MANUAIS
==================================================

O professor preencherá manualmente:

- Número de aulas
- Recursos didáticos
- Metodologia
- Instrumentos de avaliação

IMPORTANTE:

Número de aulas NÃO deverá ser calculado automaticamente com base no
número de aulas do Escopo selecionadas.

Exemplo:

3 aulas do Escopo podem ser desenvolvidas durante 6 aulas escolares.

Portanto, Número de aulas deverá permanecer editável.


==================================================
# 31. SALVAR PLANO
==================================================

Ao clicar em:

"Salvar"

verificar novamente no backend:

status == ativo

Somente professores ativos poderão salvar novos planos.

Salvar:

- user_id
- subject_id
- período inicial
- período final
- tipo de ensino
- ano/série
- turma(s)
- bimestre
- número de aulas
- aulas do Escopo selecionadas
- títulos
- conteúdos
- objetivos
- habilidades
- Aprendizagens Essenciais
- recursos didáticos
- metodologia
- instrumentos de avaliação
- created_at
- updated_at


==================================================
# 32. AÇÕES DO PLANO
==================================================

Depois de salvo, permitir:

- Visualizar
- Editar
- Salvar alterações
- Excluir
- Imprimir
- Gerar PDF


==================================================
# 33. EXCLUSÃO
==================================================

Antes de excluir, mostrar:

"Deseja realmente excluir este plano de aula?"

Botões:

[Cancelar]
[Excluir]

Somente excluir após confirmação.


==================================================
# 34. IMPORTAÇÃO DOS PDFs
==================================================

A importação será exclusiva do administrador.

Criar opção:

"Importar PDF"

Fluxo:

1. Administrador seleciona o PDF.
2. Backend Python lê o PDF.
3. Identifica o componente curricular.
4. Identifica o tipo de ensino.
5. Localiza o Escopo-Sequência.
6. Extrai os dados.
7. Organiza os registros.
8. Valida os registros.
9. Mostra uma prévia.
10. Administrador confirma.
11. Dados são armazenados no MySQL.


==================================================
# 35. DADOS EXTRAÍDOS DO PDF
==================================================

Extrair sempre que disponíveis:

- Tipo de ensino
- Componente curricular
- Ano/Série
- Bimestre
- Número da aula
- Título da aula
- Conteúdo
- Objetivos de aprendizagem
- Habilidades
- Código da Aprendizagem Essencial
- Aprendizagem Essencial


==================================================
# 36. VALIDAÇÃO DA IMPORTAÇÃO
==================================================

Antes de gravar:

- verificar componente;
- verificar tipo de ensino;
- verificar Ano/Série;
- verificar Bimestre;
- verificar Número da aula;
- procurar duplicidades;
- impedir a importação da mesma aula duas vezes;
- mostrar prévia ao administrador.

Somente armazenar após confirmação.


==================================================
# 37. BANCO DE DADOS
==================================================

Criar inicialmente as tabelas:

users
subjects
curriculum_documents
scope_lessons
lesson_plans
lesson_plan_lessons
lesson_plan_classes


==================================================
# 38. TABELA users
==================================================

Campos sugeridos:

id
name
email
phone
password_hash
role
status
approved_at
approved_by
created_at
updated_at

role:

- professor
- admin

status:

- pendente
- ativo


==================================================
# 39. TABELA subjects
==================================================

Campos:

id
name
education_level
active


==================================================
# 40. TABELA curriculum_documents
==================================================

Campos:

id
subject_id
document_year
file_name
imported_at
status


==================================================
# 41. TABELA scope_lessons
==================================================

Campos:

id
subject_id
education_level
grade
bimester
lesson_number
title
content
learning_objectives
skills
essential_learning_code
essential_learning
year


==================================================
# 42. TABELA lesson_plans
==================================================

Campos:

id
user_id
subject_id
education_level
grade
bimester
start_date
end_date
number_of_lessons
resources
methodology
evaluation
created_at
updated_at


==================================================
# 43. TABELA lesson_plan_lessons
==================================================

Campos:

id
lesson_plan_id
scope_lesson_id


==================================================
# 44. TABELA lesson_plan_classes
==================================================

Campos:

id
lesson_plan_id
class_name


==================================================
# 45. RELACIONAMENTOS
==================================================

users
│
└── lesson_plans
      │
      ├── lesson_plan_classes
      │
      └── lesson_plan_lessons
                │
                └── scope_lessons
                         │
                         └── subjects
                               │
                               └── curriculum_documents


==================================================
# 46. SEGURANÇA
==================================================

Implementar:

- hash seguro das senhas;
- sessão autenticada;
- proteção CSRF;
- validações no backend;
- ORM ou consultas parametrizadas;
- proteção contra SQL Injection;
- proteção contra XSS;
- controle de acesso por usuário;
- controle de acesso por perfil;
- controle por status do professor;
- validação de upload;
- aceitar apenas PDF;
- limitar tamanho dos arquivos;
- impedir que um professor acesse planos pertencentes a outro professor;
- impedir professor pendente de criar ou salvar novos planos.

Nunca confiar apenas no JavaScript.

Toda restrição deverá ser validada novamente pelo backend.


==================================================
# 47. INTERFACE
==================================================

Criar uma interface:

- profissional;
- moderna;
- limpa;
- responsiva;
- adequada ao ambiente educacional;
- simples de utilizar.

Manter identidade visual consistente em todas as páginas.

A Home do Professor deverá possuir menu lateral fixo.


==================================================
# 48. ESTRUTURA DO PROJETO
==================================================

Utilizar uma organização semelhante a:

project/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── uploads/
├── migrations/
├── config.py
├── requirements.txt
├── run.py
└── README.md


Separar módulos de:

- autenticação;
- usuários;
- administrador;
- aprovação de professores;
- planos;
- componentes;
- Escopo-Sequência;
- importação de PDFs;
- processamento de PDFs;
- geração de PDF.


==================================================
# 49. COMUNICAÇÃO COM O BANCO
==================================================

NÃO utilizar:

JavaScript
↓
MySQL

Utilizar:

HTML / JavaScript
↓
Python / Flask
↓
MySQL


==================================================
# 50. REGRA DOS PDFs
==================================================

NÃO UTILIZAR:

Professor escolhe Filosofia
↓
Sistema abre o PDF
↓
Sistema processa o PDF
↓
Sistema retorna aulas


UTILIZAR:

ADMINISTRADOR

PDF
↓
Python
↓
Extração
↓
Validação
↓
MySQL


DEPOIS:

PROFESSOR

Ensino
+
Componente
+
Ano/Série
+
Bimestre
↓
Consulta ao MySQL
↓
Aulas disponíveis


==================================================
# 51. FLUXO DO PROFESSOR
==================================================

CADASTRO
↓
status = pendente
↓
LOGIN PERMITIDO
↓
HOME DO PROFESSOR
↓
MEU PERFIL DISPONÍVEL
↓
PLANOS DE AULA
↓
NOVO PLANO BLOQUEADO
↓
ADMINISTRADOR APROVA
↓
status = ativo
↓
NOVO PLANO LIBERADO
↓
PERÍODO
↓
TIPO DE ENSINO
↓
COMPONENTE
↓
ANO/SÉRIE
↓
TURMA(S)
↓
BIMESTRE
↓
CONSULTA scope_lessons
↓
SELEÇÃO DAS AULAS
↓
PREENCHIMENTO AUTOMÁTICO
↓
PREENCHIMENTO MANUAL
↓
SALVAR
↓
VISUALIZAR / EDITAR / EXCLUIR / GERAR PDF


==================================================
# 52. ORDEM DE DESENVOLVIMENTO
==================================================

Desenvolver nesta ordem:

1. Arquitetura Flask
2. Configuração do MySQL
3. Banco de dados
4. Models
5. Cadastro
6. Login
7. Sessões
8. Sistema de status pendente/ativo
9. Home do Professor
10. Meu Perfil
11. Painel Administrativo
12. Aprovação de professores
13. Planos por bimestre
14. Cadastro dos componentes
15. Estrutura scope_lessons
16. Importação de PDFs
17. Extração do Escopo-Sequência
18. Novo Plano
19. Consultas dinâmicas
20. Salvamento
21. Edição
22. Exclusão
23. Busca
24. Impressão
25. Geração de PDF
26. Testes de segurança
27. Testes gerais


==================================================
# 53. FORMA DE ENTREGA DO CÓDIGO
==================================================

Antes de gerar código, apresentar:

1. Arquitetura
2. Estrutura de pastas
3. Modelo do banco
4. Relacionamentos
5. Rotas
6. Fluxo de autenticação
7. Fluxo de aprovação
8. Fluxo de importação
9. Fluxo de criação do plano

Depois gerar os arquivos gradualmente.

Para cada arquivo:

- informar o caminho exato;
- fornecer o código completo;
- explicar sua função;
- indicar dependências.

Não fornecer apenas trechos sem indicar onde devem ser inseridos.

Quando um arquivo existente precisar ser alterado, fornecer
preferencialmente o arquivo completo atualizado.

Não alterar as regras de negócio sem informar.





==================================================
# PAINEL DO ADMINISTRADOR
==================================================

O sistema deverá possuir uma área administrativa independente da área
do professor.

O administrador será responsável por:

- acompanhar professores cadastrados;
- aprovar novos professores;
- consultar planos criados pelos professores;
- pesquisar e filtrar planos;
- importar os PDFs do Guia do Currículo Priorizado;
- consultar arquivos já importados;
- gerenciar seu próprio perfil;
- alterar sua senha.


==================================================
# 1. CONTA INICIAL DO ADMINISTRADOR
==================================================

O sistema deverá possuir pelo menos uma conta inicial de administrador.

Essa conta deverá ser criada durante a configuração inicial do projeto.

Não armazenar e-mail ou senha administrativa diretamente no código-fonte.

Utilizar variáveis de ambiente:

ADMIN_EMAIL
ADMIN_INITIAL_PASSWORD

Essas informações deverão ficar no arquivo:

.env

O arquivo .env deverá obrigatoriamente ser incluído no:

.gitignore

A senha deverá ser armazenada na tabela users utilizando hash seguro.

O usuário deverá possuir:

role = admin
status = ativo

Na configuração inicial do projeto, fornecer instruções claras para
definir:

- e-mail inicial do administrador;
- senha inicial do administrador.

Opcionalmente, exigir alteração da senha no primeiro acesso.


==================================================
# 2. LOGIN DO ADMINISTRADOR
==================================================

Criar uma página de login para administrador.

Campos:

- E-mail
- Senha

Fluxo:

1. Administrador informa e-mail e senha.

2. Backend procura o usuário na tabela users.

3. Verificar se:

role = admin

4. Comparar a senha informada com o hash armazenado.

5. Se estiver correta, criar sessão autenticada.

6. Armazenar na sessão:

- user_id
- nome
- role

7. Redirecionar para:

/admin

Caso as credenciais sejam inválidas, mostrar:

"E-mail ou senha inválidos."

Não informar separadamente se o problema está no e-mail ou na senha.


==================================================
# 3. ESQUECI MINHA SENHA
==================================================

Na página de login deverá existir:

"Esqueci minha senha"

IMPORTANTE:

O sistema nunca deverá mostrar ou recuperar a senha antiga.

A senha armazenada deverá possuir hash e somente poderá ser redefinida.

Fluxo:

1. Administrador clica em "Esqueci minha senha".

2. Informa seu e-mail.

3. O sistema verifica internamente se existe uma conta correspondente.

4. Independentemente da existência do e-mail, mostrar uma mensagem genérica:

"Se o e-mail estiver cadastrado, você receberá as instruções
para redefinir sua senha."

5. Se o e-mail existir, gerar um token aleatório e seguro.

6. Armazenar somente o hash do token no banco de dados.

7. Definir prazo de validade para o token.

Sugestão:

30 minutos.

8. Enviar ao e-mail do administrador um link contendo o token.

Exemplo:

/redefinir-senha?token=...

9. Ao abrir o link, apresentar:

- Nova senha
- Confirmação da nova senha

10. Verificar se as duas senhas são iguais.

11. Atualizar password_hash.

12. Invalidar imediatamente o token utilizado.

13. Não permitir reutilização do token.


==================================================
# 4. HOME DO ADMINISTRADOR
==================================================

A página principal do administrador deverá possuir:

- menu lateral fixo à esquerda;
- área de conteúdo à direita.

O menu lateral deverá permanecer sempre visível.


==================================================
# 5. MENU LATERAL DO ADMINISTRADOR
==================================================

Exibir as opções:

- Início
- Perfil
- Professores
- Arquivos
- Cadastros de Professores
- Sair

Ao selecionar qualquer opção, manter o menu lateral fixo e alterar
somente o conteúdo da área direita.


==================================================
# 6. DASHBOARD PRINCIPAL
==================================================

Ao acessar a página inicial do administrador, apresentar no topo três
indicadores simples:

PROFESSORES CADASTRADOS
Quantidade total de professores cadastrados.

ARQUIVOS IMPORTADOS
Quantidade total de PDFs curriculares importados.

CADASTROS PENDENTES
Quantidade de professores aguardando aprovação.

Os indicadores deverão ser obtidos diretamente do banco de dados.

Não utilizar números fixos no HTML.


==================================================
# 7. LISTA DE PROFESSORES NA HOME
==================================================

Abaixo dos indicadores principais, apresentar todos os professores
cadastrados no formato de pastas ou cartões.

Cada professor deverá possuir uma pasta própria.

Exemplo:

[ Professor: João Silva ]

Componentes com planos:
- Ciências
- Matemática
- Tecnologia

Total de planos:
18

As informações deverão ser calculadas a partir dos planos existentes
no banco de dados.

Se o professor ainda não tiver criado nenhum plano, informar:

"Nenhum plano criado."


==================================================
# 8. PASTA DO PROFESSOR
==================================================

Ao clicar na pasta de um professor, abrir uma página contendo todos
os seus planos.

Organizar inicialmente por bimestre:

1º Bimestre
2º Bimestre
3º Bimestre
4º Bimestre

Cada pasta deverá apresentar a quantidade de planos existentes.


==================================================
# 9. ORGANIZAÇÃO INTERNA DOS PLANOS
==================================================

Dentro de cada bimestre, separar os planos por:

ENSINO FUNDAMENTAL

e

ENSINO MÉDIO

Dentro de cada tipo de ensino, organizar os planos por componente
curricular.

Exemplo:

PROFESSOR
João Silva

└── 1º Bimestre

    ├── Ensino Fundamental
    │
    │   ├── Ciências
    │   │   ├── Plano 1
    │   │   └── Plano 2
    │   │
    │   └── Matemática
    │       └── Plano 3
    │
    └── Ensino Médio

        ├── Biologia
        │   └── Plano 4
        │
        └── Física
            └── Plano 5


==================================================
# 10. VISUALIZAÇÃO DOS PLANOS
==================================================

Para cada plano, exibir de forma resumida:

- Título
- Professor
- Componente curricular
- Tipo de ensino
- Ano/Série
- Turma(s)
- Bimestre
- Período
- Número de aulas
- Data de criação
- Data da última alteração

Permitir ao administrador abrir o plano completo.

O administrador poderá visualizar os planos de qualquer professor.

Não permitir que um professor comum utilize essa funcionalidade.


==================================================
# 11. FILTROS
==================================================

Na parte superior da página de consulta dos planos, criar uma área
de filtros.

Permitir filtrar por:

- Professor
- Tipo de ensino
- Ano/Série
- Turma
- Período

Tipo de ensino:

- Ensino Fundamental
- Ensino Médio

Ano/Série:

Ensino Fundamental:
- 6º Ano
- 7º Ano
- 8º Ano
- 9º Ano

Ensino Médio:
- 1ª Série
- 2ª Série
- 3ª Série

Permitir selecionar:

Data inicial
até
Data final

para o filtro de período.

Os filtros poderão ser combinados.

Exemplo:

Professor:
João Silva

Ensino:
Ensino Fundamental

Ano:
8º Ano

Turma:
B

Período:
01/08/2026 até 31/08/2026

O backend deverá realizar a consulta correspondente no MySQL.

Adicionar também botão:

"Limpar filtros"


==================================================
# 12. PERFIL DO ADMINISTRADOR
==================================================

Ao clicar em:

"Perfil"

exibir:

- Nome
- E-mail

Permitir alteração dos dados permitidos.

Criar uma área separada:

ALTERAR SENHA

Campos:

- Senha atual
- Nova senha
- Confirmação da nova senha

A senha atual deverá ser validada antes da alteração.

Nunca exibir a senha existente.


==================================================
# 13. PROFESSORES
==================================================

Ao clicar em:

"Professores"

apresentar uma lista com todos os professores cadastrados.

Exibir:

- Nome
- E-mail
- Telefone
- Status
- Data de cadastro
- Quantidade de planos

Permitir busca pelo nome do professor.


==================================================
# 14. CADASTROS DE PROFESSORES
==================================================

Ao clicar em:

"Cadastros de Professores"

mostrar prioritariamente professores com:

status = pendente

Para cada cadastro apresentar:

- Nome
- E-mail
- Telefone
- Data do cadastro

Disponibilizar:

[Aprovar cadastro]

Ao aprovar:

status = ativo

Registrar também:

approved_at
approved_by

Após a aprovação, o professor poderá criar planos de aula.

O professor pendente continuará podendo fazer login, acessar sua Home
e alterar seu perfil, porém não poderá criar planos.


==================================================
# 15. ARQUIVOS
==================================================

Ao clicar em:

"Arquivos"

mostrar os PDFs do Guia do Currículo Priorizado já importados.

Exibir:

- Nome do arquivo
- Componente curricular
- Tipo de ensino
- Ano do documento
- Data de importação
- Status da importação

Criar botão:

"Importar PDF"


==================================================
# 16. IMPORTAÇÃO DE PDF
==================================================

Ao clicar em:

"Importar PDF"

permitir selecionar um arquivo PDF.

Fluxo:

PDF
↓
Python
↓
Leitura
↓
Identificação do componente
↓
Identificação do tipo de ensino
↓
Identificação do Escopo-Sequência
↓
Extração
↓
Validação
↓
Prévia
↓
Confirmação do administrador
↓
MySQL

Não salvar automaticamente sem apresentar a prévia ao administrador.


==================================================
# 17. INDICADOR DE IMPORTAÇÃO
==================================================

Depois da importação, informar:

- quantidade de aulas identificadas;
- quantidade de registros válidos;
- quantidade de duplicidades;
- quantidade de erros encontrados.

Somente depois da confirmação deverão ser gravados os novos registros.


==================================================
# 18. SEGURANÇA DO PAINEL ADMINISTRATIVO
==================================================

Todas as rotas administrativas deverão verificar no backend:

role == admin

Um professor que tente acessar manualmente:

/admin

deverá receber acesso negado ou ser redirecionado.

Não confiar somente em esconder links no frontend.

Também implementar:

- sessões autenticadas;
- proteção CSRF;
- proteção contra SQL Injection;
- proteção contra XSS;
- hash seguro de senhas;
- validação de uploads;
- limitação de tamanho dos PDFs;
- encerramento seguro de sessão.


==================================================
# 19. FLUXO RESUMIDO DO ADMINISTRADOR
==================================================

LOGIN
↓
HOME ADMIN
↓
INDICADORES

Professores cadastrados
Arquivos importados
Cadastros pendentes

↓
PASTAS DOS PROFESSORES
↓
PROFESSOR
↓
BIMESTRE
↓
ENSINO FUNDAMENTAL / ENSINO MÉDIO
↓
COMPONENTE CURRICULAR
↓
PLANOS DE AULA


MENU FIXO:

Início
Perfil
Professores
Arquivos
Cadastros de Professores
Sair


==================================================
# 20. REGRAS IMPORTANTES
==================================================

1. O administrador poderá visualizar os planos de todos os professores.

2. O professor somente poderá visualizar seus próprios planos.

3. O administrador será responsável pela aprovação dos professores.

4. Professores pendentes poderão fazer login.

5. Professores pendentes não poderão criar novos planos.

6. A aprovação deverá alterar:

status = pendente

para:

status = ativo

7. PDFs somente poderão ser importados pelo administrador.

8. As informações dos PDFs deverão ser processadas uma única vez e
armazenadas no MySQL.

9. As telas administrativas deverão obter informações reais do banco.

10. Não utilizar dados simulados depois que o banco estiver integrado.
==================================================
# 54. OBJETIVO FINAL
==================================================

O sistema final deverá ser:

- funcional;
- seguro;
- organizado;
- modular;
- responsivo;
- fácil de manter;
- simples para professores;
- preparado para diferentes componentes curriculares;
- preparado para atualizações anuais do Guia do Currículo Priorizado;
- preparado para novos PDFs sem necessidade de reconstrução do sistema.