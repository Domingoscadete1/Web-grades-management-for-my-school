from django.contrib import admin

# Register your models here.
from .models import *


# Register your models here.
admin.site.register(User)
admin.site.site_header='Notas management'

admin.site.register(Aluno)
admin.site.register(Matricula)
admin.site.register(Disciplina)
admin.site.register(Curso)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Classe)
admin.site.register(Nota)
admin.site.register(CursoDisciplina)

admin.site.register(ProfessorDisciplina)
admin.site.register(ProfessorTurma)

admin.site.register(CursoClasse)
admin.site.register(ClasseDisciplina)
