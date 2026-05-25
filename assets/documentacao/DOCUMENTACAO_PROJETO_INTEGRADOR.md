# SISTEMA DE GESTÃO DE NOTAS ACADÊMICAS

**Projeto Integrador: Laboratório de Programação**

---

**Universidade Santo Amaro – UNISA**
**Curso:** Análise e Desenvolvimento de Sistemas
**Disciplina:** Projeto Integrador – Laboratório de Programação
**Semestre:** 2025.1

---

## RESUMO

O presente trabalho apresenta o desenvolvimento de um sistema desktop para gestão de notas acadêmicas, utilizando a linguagem Python e a biblioteca CustomTkinter para construção da interface gráfica. O sistema foi desenvolvido como solução para o gerenciamento de notas de uma instituição de ensino, tendo como exemplo a UNISA. A aplicação contempla controle de acesso por perfil (aluno, professor e administrador), permitindo operações como matrícula em disciplinas, lançamento e edição de notas, geração de relatórios e backup de dados. A persistência dos dados é realizada em arquivo JSON, dispensando a necessidade de um servidor de banco de dados externo. O projeto integra conhecimentos adquiridos nas disciplinas de Lógica de Programação, Engenharia de Software e Análise de Dados, resultando em uma aplicação funcional, executável e sem erros.

**Palavras-chave:** gestão acadêmica. Python. CustomTkinter. notas. sistema desktop. JSON.

---

## 1. INTRODUÇÃO

A gestão de notas acadêmicas é uma atividade essencial em qualquer instituição de ensino. O controle manual ou por planilhas apresenta limitações como falta de segurança, dificuldade de acesso e ausência de validações automáticas. Diante dessa situação-problema, foi proposto o desenvolvimento de um sistema que centralize e automatize esse processo.

O projeto coloca em prática os conteúdos abordados durante o semestre nas disciplinas de Lógica de Programação, Engenharia de Software e Análise de Dados. A linguagem Python, trabalhada na disciplina de programação, foi escolhida como base do desenvolvimento. Através da biblioteca CustomTkinter, que estende o Tkinter nativo com componentes visuais modernos, foi construída uma interface desktop intuitiva e funcional.

Como cenário de aplicação, foi utilizada a própria UNISA como exemplo de instituição, simulando cursos, matérias, turmas, períodos e semestres reais. O sistema implementa toda uma governança de acesso, onde cada tipo de usuário possui permissões específicas e visualiza apenas as funcionalidades pertinentes ao seu perfil.

A motivação para a escolha deste tema está na vivência diária como estudante, onde a consulta de notas, o acompanhamento de aprovação e a comunicação com professores são atividades recorrentes que podem ser otimizadas por meio de um sistema bem estruturado.

---

## 2. OBJETIVOS

### 2.1 Objetivo Geral

Desenvolver um sistema desktop funcional para gestão de notas acadêmicas com controle de acesso por perfil, aplicando os conhecimentos adquiridos nas disciplinas do semestre.

### 2.2 Objetivos Específicos

- Implementar autenticação de usuários com validação de credenciais;
- Desenvolver interface gráfica moderna utilizando CustomTkinter;
- Criar funcionalidades de CRUD para cursos e matérias;
- Implementar sistema de matrícula com turma, período e semestre;
- Desenvolver módulo de lançamento e edição de notas (AVI, AVC, AVG);
- Calcular automaticamente médias e nota final com status de aprovação;
- Gerar relatórios estatísticos por matéria e por perfil;
- Implementar sistema de backup com geração de arquivo ZIP;
- Aplicar persistência de dados em arquivo JSON.

---

## 3. DESENVOLVIMENTO

### 3.1 Fundamentação Teórica

O desenvolvimento do sistema se baseia em conceitos fundamentais da programação orientada a objetos e programação estruturada. A linguagem Python foi escolhida por sua sintaxe clara, vasta documentação e ampla adoção no mercado (Van Rossum, 2023). A biblioteca CustomTkinter permite a criação de interfaces modernas sem a necessidade de frameworks web, mantendo a simplicidade de distribuição de uma aplicação desktop (Mayer, 2023).

A arquitetura do sistema segue o padrão de separação em camadas, onde a camada de serviço (Service) concentra toda a lógica de negócio e acesso a dados, enquanto a camada de visualização (View) é responsável exclusivamente pela interface gráfica. Essa separação facilita a manutenção e evolução do código (Sommerville, 2019).

A persistência em JSON foi adotada por dispensar instalação de banco de dados externo, simplificando a implantação e permitindo portabilidade do sistema (ECMA International, 2017).

### 3.2 Arquitetura do Sistema

O sistema foi organizado em duas camadas principais:

- **Service** — contém toda a lógica de negócio, validações e operações de leitura/escrita no banco de dados JSON.
- **View** — responsável pela interface gráfica, dividida em janelas (windows), popups e painéis (panels).

A Figura 1 apresenta a estrutura de diretórios do projeto.

```
LabProgramacao/
├── assets/sistema/              # Ícones e imagens
├── database/data.json           # Banco de dados JSON
├── src/
│   ├── main.py                  # Ponto de entrada
│   ├── service/
│   │   ├── database_service.py  # CRUD e regras de negócio
│   │   └── backup_service.py    # Geração de backup
│   └── view/
│       ├── utils.py             # Constantes e utilitários
│       ├── home_window.py       # Tela de login
│       ├── dashboard_window.py  # Tela principal com sidebar
│       ├── register_popup.py    # Popup de cadastro
│       ├── forgot_password_popup.py
│       └── panels/              # Painéis de conteúdo
├── requirements.txt
└── README.md
```
Fonte: Autor, 2025.

### 3.3 Modelo de Dados

O banco de dados é um arquivo JSON com a seguinte estrutura:

```json
{
  "users": [
    {
      "usuario": "string",
      "nome_completo": "string",
      "email": "string",
      "senha": "string",
      "nome_mae": "string",
      "tipo": "user | teacher | admin",
      "materias": [
        {
          "nome": "string",
          "semestre": "2025.1",
          "turma": "A",
          "periodo": "Manhã",
          "notas": {"avi": [], "avc": [], "avg": []}
        }
      ]
    }
  ],
  "system": {
    "semesters": ["2015.1", "...", "2035.2"],
    "courses": [
      {"nome": "string", "subjects": ["string"]}
    ]
  }
}
```
Fonte: Autor, 2025.

### 3.4 Perfis de Acesso

O sistema implementa três perfis com funcionalidades distintas:

| Perfil | Funcionalidades |
|--------|----------------|
| Aluno (user) | Consultar matérias, notas e situação |
| Professor (teacher) | Lançar notas, editar notas, relatórios |
| Administrador (admin) | Matricular, vincular professor, gerenciar cursos/matérias, relatórios, backup |

Fonte: Autor, 2025.

### 3.5 Regras de Negócio

As principais regras implementadas no sistema são:

- Cada avaliação (AVI, AVC, AVG) pode conter N notas; a média é calculada pela soma dividida pela quantidade;
- A nota final é sempre (média_AVI + média_AVC + média_AVG) / 3, independente de quantas avaliações possuem notas lançadas;
- Aprovação ocorre quando a nota final é igual ou superior a 6.0;
- Notas devem estar entre 0 e 10;
- Turmas disponíveis: A, B, C;
- Períodos disponíveis: Manhã, Noturno;
- Usuário, email e nome da mãe são armazenados em lowercase para evitar duplicatas.

### 3.6 Funcionalidades Implementadas

**Autenticação e Cadastro:**
- Login com usuário e senha;
- Cadastro de novos usuários com seleção de tipo (aluno ou professor);
- Recuperação de senha por validação do nome da mãe.

**Módulo do Aluno:**
- Visualização de matérias matriculadas com professor, turma e período;
- Consulta de notas por avaliação (AVI, AVC, AVG) com médias calculadas;
- Exibição da nota final e status de aprovação/reprovação.

**Módulo do Professor:**
- Lançamento de notas individuais por aluno, matéria e tipo de avaliação;
- Edição e remoção de notas já lançadas;
- Relatório por matéria vinculada com média geral, maior e menor nota.

**Módulo do Administrador:**
- Matrícula de alunos em matérias com turma, período e semestre;
- Vínculo de professores a matérias com turma, período e semestre;
- CRUD de cursos e matérias;
- Relatório geral com total de cursos, matérias e aprovados/reprovados;
- Geração de backup em arquivo ZIP com timestamp.

### 3.7 Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | 3.10+ | Linguagem principal |
| CustomTkinter | >= 5.2.0 | Interface gráfica moderna |
| Pillow | >= 10.0.0 | Carregamento de imagens |
| JSON (stdlib) | — | Persistência de dados |
| zipfile (stdlib) | — | Geração de backup |

Fonte: Autor, 2025.

### 3.8 Instalação e Execução

Para executar o sistema:

```bash
pip install -r requirements.txt
cd src
python main.py
```

Credenciais padrão do administrador:
- Usuário: `admin`
- Senha: `admin`

---

## 4. CONCLUSÃO

O objetivo proposto de desenvolver um sistema funcional para gestão de notas acadêmicas foi alcançado com sucesso. A aplicação integra os conhecimentos das disciplinas cursadas no semestre: a Lógica de Programação foi aplicada na estruturação dos algoritmos e fluxos de dados; a Engenharia de Software orientou a arquitetura em camadas e a separação de responsabilidades; e a Análise de Dados fundamentou os cálculos de médias e a geração de relatórios estatísticos.

O sistema demonstra que é possível construir uma aplicação desktop completa e funcional utilizando Python e bibliotecas de código aberto, sem dependência de servidores externos ou infraestrutura complexa. A persistência em JSON, embora simples, atende adequadamente ao escopo proposto e facilita a portabilidade da aplicação.

Como melhorias futuras, poderiam ser implementadas: criptografia de senhas, exportação de relatórios em PDF, integração com banco de dados relacional para ambientes com maior volume de dados e desenvolvimento de versão web para acesso remoto.

---

## REFERÊNCIAS

ECMA INTERNATIONAL. **The JSON Data Interchange Syntax**. ECMA-404. 2. ed. Genebra: ECMA International, 2017. Disponível em: https://www.ecma-international.org/publications-and-standards/standards/ecma-404/. Acesso em: 20 jan. 2025.

MAYER, T. **CustomTkinter Documentation**. 2023. Disponível em: https://customtkinter.tomschimansky.com/. Acesso em: 15 jan. 2025.

SOMMERVILLE, I. **Engenharia de Software**. 10. ed. São Paulo: Pearson, 2019.

VAN ROSSUM, G. **Python Documentation**. Python Software Foundation, 2023. Disponível em: https://docs.python.org/3/. Acesso em: 10 jan. 2025.
