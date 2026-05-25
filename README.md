# Sistema de Gestão de Notas - LabProgramacao

Sistema de gestão de notas acadêmicas desenvolvido em Python com interface gráfica CustomTkinter.

## 📋 Funcionalidades

### Para Alunos
- Login na plataforma
- Consultar matérias, notas e situação (aprovado/reprovado)
- Visualizar professor, turma e período de cada matéria

### Para Professores
- Lançamento de notas (AVI, AVC, AVG)
- Edição e remoção de notas lançadas
- Relatórios por matéria vinculada (média, maior/menor nota)

### Para Administradores
- Matricular alunos em matérias (com turma, período e semestre)
- Vincular professores a matérias
- Gerenciar cursos e matérias (criar, editar, remover)
- Relatório geral (aprovados/reprovados por matéria)
- Gerar backup do banco de dados

### Funções do Sistema
- Validação de cadastro (usuário único)
- Recuperação de senha (nome da mãe)
- Cálculo de médias e nota final
- Gerar backup em ZIP com timestamp

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação
1. Clone ou baixe o projeto
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução
```bash
cd src
python main.py
```

### Usuário padrão
- Usuário: `admin`
- Senha: `admin`
