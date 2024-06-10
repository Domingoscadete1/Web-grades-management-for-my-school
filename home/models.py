from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# Create your models here.
CATEGORY=(
    ('Escrita','Escrita'),
    ('Oral','Oral'),
    ('Pratica','Pratica'),
    ('Defesa_trabalho','Defesa_trabalho'),
)
CLASSES=(
    ('Iniciação','Iniciação'),
    ('1ª','1ª'),
    ('2ª','2ª'),
    ('3ª','3ª'),
    ('4ª','4ª'),
    ('5ª','5ª'),
    ('6ª','6ª'),
    ('7ª','7ª'),
    ('8ª','8ª'),
    ('9ª','9ª'),
    ('10ª','10ª'),
    ('11ª','11ª'),
    ('12ª','12ª'),
    ('13ª','13ª'),
     
 )
GENERO=(
    ('Masculino','Masculino'),
    ('Feminino','Feminino'),

)
ESTADO=(
    ('Solterio','Solteiro'),
    ('Casado','Casado')
)
class User(AbstractUser):
    is_admin=models.BooleanField('Is admin',default=False)
    is_professor=models.BooleanField('Is professor',default=False)
    is_aluno=models.BooleanField('Is aluno',default=False)

class Aluno(models.Model):
    ano_lectivo=models.CharField(max_length=50)
    n_processo=models.CharField(max_length=70)
    nome=models.CharField(max_length=255)
    
    idade=models.PositiveIntegerField()
    data_nascimento=models.DateField()
    n_bi=models.CharField(max_length=80)
    data_emissao=models.DateField()
    foto=models.ImageField(upload_to='imagens_aluno/')
    estado_civil=models.CharField(max_length=50,choices=ESTADO)
    genero=models.CharField(max_length=50,choices=GENERO)
    nacionalidade=models.CharField(max_length=100)
    nome_pai=models.CharField(max_length=255)
    nome_mae=models.CharField(max_length=255)
    profissao_pai=models.CharField(max_length=150)
    profissao_mae=models.CharField(max_length=150)
    obs=models.TextField()
    def __str__(self) -> str:
        return f'{self.nome}'
    

class  Classe(models.Model):
    nome=models.CharField(max_length=55,choices=CLASSES)
    nivel=models.CharField(max_length=100)
    descricao=models.TextField()
    obs=models.TextField()
    def __str__(self) -> str:
        return f'{self.nome}'
    




class Curso (models.Model):
    nome=models.CharField(max_length=255)
    nivel=models.CharField(max_length=100)
    descricao=models.TextField()
    objectivo=models.TextField()
    programa=models.TextField()
    def __str__(self) -> str:
        return f'{self.nome}'


class Professor(models.Model):
    nome=models.CharField(max_length=255)
    bi=models.CharField(max_length=50)
    data_nascimento=models.DateField()
    nivel_escolaridade=models.CharField(max_length=100)
    habilitacoes=models.TextField()
    experiencia=models.TextField()
    estado_civil=models.CharField(max_length=70,choices=ESTADO)
    foto=models.ImageField(upload_to='imagens_professor/',null=True)
    genero=models.CharField(max_length=40,choices=GENERO)
    nacionalidade=models.CharField(max_length=60)
    obs=models.TextField()
    def __str__(self) -> str:
        return f'{self.nome}'


class Disciplina(models.Model):
    nome=models.CharField(max_length=255)
    nivel=models.CharField(max_length=60)
    descricao=models.TextField()
    programa=models.TextField()
    objectivo=models.TextField()
    obs=models.TextField()
    def __str__(self) -> str:
        return f'{self.nome}'

class Turma(models.Model):
    nome=models.CharField(max_length=255)
    n_alunos=models.PositiveIntegerField()
    n_max_alunos=models.PositiveIntegerField()
    
    classe_id=models.ForeignKey(Classe,on_delete=models.CASCADE,null=False)
    sala=models.CharField(max_length=50)
    curso_id=models.ForeignKey(Curso,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.nome}'


class ProfessorDisciplina(models.Model):
    disciplina_id=models.ForeignKey(Disciplina,on_delete=models.CASCADE,null=False)
    professor_id=models.ForeignKey(Professor,on_delete=models.CASCADE,null=False)
    def __str__(self) -> str:
        return f'disciplina :{self.disciplina_id.nome}-- professor :{self.professor_id.nome}'


class CursoDisciplina(models.Model):
    disciplina_id=models.ForeignKey(Disciplina,on_delete=models.CASCADE,null=False)
    curso_id=models.ForeignKey(Curso,on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return f'disciplina :{self.disciplina_id.nome}-- curso :{self.curso_id.nome}'

class CursoClasse (models.Model):
    classe_id=models.ForeignKey(Classe,on_delete=models.CASCADE,null=False)
    curso_id=models.ForeignKey(Curso,on_delete=models.CASCADE,null=False)
    def __str__(self) -> str:
        return f'classe id:{self.classe_id}-- Curso id:{self.curso_id}'


class  ProfessorTurma  (models. Model):
    professor_id=models.ForeignKey(Professor,on_delete=models.CASCADE,null=False)
    turma_id=models.ForeignKey(Turma,on_delete=models.CASCADE,null=False)
    def __str__(self) -> str:
        return f'professor :{self.professor_id.nome} -- Turma :{self.turma_id.nome}'
    


class ClasseDisciplina (models.Model):
    disciplina_id=models.ForeignKey(Disciplina,on_delete=models.CASCADE,null=False)
    classe_id=models.ForeignKey(Classe,on_delete=models.CASCADE,null=False)
    def __str__(self) -> str:
        return f'disciplina :{self.disciplina_id.nome}-- classe :{self.classe_id.nome}'

class Matricula(models.Model):
    aluno_id=models.ForeignKey(Aluno,on_delete=models.CASCADE,null=False)
    turma_id=models.ForeignKey(Turma,on_delete=models.CASCADE,null=False)
    @property
    def classe_id(self):
        return self.turma.classe_id.id
    
TRIMESTRE=(
    ('Primeiro trimeste','Primeiro trimestre'),
    ('Segundo trimeste','Segundo trimestre'),
    ('Terceiro trimeste','Terceiro trimestre')
)
class Nota(models.Model): 
    tipo_prova=models.CharField(max_length=50,choices=CATEGORY)
    valor=models.FloatField()
    data_prova=models.DateField()
    trimestre=models.CharField(max_length=90,choices=TRIMESTRE)
    aluno_id=models.ForeignKey(Aluno,on_delete=models.CASCADE,null=False)
    disciplina_id=models.ForeignKey(Disciplina,on_delete=models.CASCADE,null=False)
    def __str__(self) -> str:
        return f'disciplina :{self.disciplina_id.nome}-- aluno :{self.aluno_id.nome}'

class MediaNota(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    media = models.FloatField()

    def __str__(self):
        return f"{self.aluno.nome} - {self.disciplina.nome}: {self.media}"

