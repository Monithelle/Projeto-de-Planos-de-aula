# Projeto Planos de Aula

Ambiente de desenvolvimento Python configurado.

## Estrutura do Projeto

```
Projeto/
│
├── .venv/               # Ambiente virtual Python (isolado)
├── .vscode/             # Configurações do VS Code / Antigravity
│   └── settings.json
├── src/                 # Código-fonte principal
├── .env.example         # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos e pastas ignorados pelo Git
├── requirements.txt     # Dependências do projeto
├── main.py              # Ponto de entrada da aplicação
└── README.md            # Documentação
```

## Como Usar

### 1. Ativar o Ambiente Virtual
No terminal PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
Ou no CMD:
```cmd
.\.venv\Scripts\activate.bat
```

### 2. Instalar Dependências
```powershell
pip install -r requirements.txt
```

### 3. Executar o Projeto
```powershell
python main.py
```

