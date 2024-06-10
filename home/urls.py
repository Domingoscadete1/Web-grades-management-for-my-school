from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',registro,name='cadastro' ),
    path('',home_view,name='home' ),
    path('login/',login_view,name='login' ),
    path('logout/', logout_view, name='logout'),
    path('plataforma/',plataforma,name='plataforma' ),
    path('teste/',teste,name='teste' ),
    path('home-professor/',ProfessorView,name='home-professor' ),
    path('perfil-professor/',ProfessorPerfil,name='perfil-professor' ),
    path('update-professor/<int:pk>', ProfessorUpdate.as_view(),name='update-professor'),
    path('delete-professor/<int:pk>', ProfessorDelete.as_view(),name='delete-professor'),
    path('update-professor1/<int:pk>', ProfessorUpdate1.as_view(),name='update-professor1'),
    path('update-professor-turma/<int:pk>/', ProfessorTurmaUpdate.as_view(),name='update-professor-turma'),
    path('delete-professor-turma/<int:pk>/', ProfessorTurmaDelete.as_view(),name='delete-professor-turma'),
    path('create-professor/', ProfessorCreate.as_view(),name='create-professor'),
    path('create-professor-disciplina/', ProfessorDisciplinaCreate.as_view(),name='create-professor-disciplina'),
    path('delete-professor-disciplina/<int:pk>', ProfessorDisciplinaDelete.as_view(),name='delete-professor-disciplina'),
    path('create-professor-turma/', ProfessorTurmaCreate.as_view(),name='create-professor-turma'),
    path('admin-dashboard/', AdminView,name='admin-dashboard'),
    path('admin-dashboard-professores/', AdminProfessores,name='admin-dashboard-professores'),
    path('admin-dashboard-disciplinas/', AdminDisciplinas,name='admin-dashboard-disciplinas'),
    path('update-disciplina/<int:pk>', DisciplinaUpdate.as_view(),name='update-disciplina'),
    path('delete-disciplina/<int:pk>', DisciplinaDelete.as_view(),name='delete-disciplina'),
    path('create-disciplina/', DisciplinaCreate.as_view(),name='create-disciplina'),
    path('create-disciplina-curso/', DisciplinaCursoCreate.as_view(),name='create-disciplina-curso'),
    path('create-disciplina-classe/', DisciplinaClasseCreate.as_view(),name='create-disciplina-classe'),

    path('admin-dashboard-classes/', AdminClasses,name='admin-dashboard-classes'),
    path('update-classe/<int:pk>', ClasseUpdate.as_view(),name='update-classe'),
    path('delete-classe/<int:pk>', ClasseDelete.as_view(),name='delete-classe'),
    path('create-classe-curso/', CursoClasseCreate.as_view(),name='create-classe-curso'),
    path('create-classe/', ClasseCreate.as_view(),name='create-classe'),
    path('admin-dashboard-turmas/', AdminTurmas,name='admin-dashboard-turmas'),
    path('update-turma/<int:pk>', TurmaUpdate.as_view(),name='update-turma'),
    path('delete-turma/<int:pk>', TurmaDelete.as_view(),name='delete-turma'),
    path('create-turma/', TurmaCreate.as_view(),name='create-turma'),
    path('admin-dashboard-curso/', AdminCurso,name='admin-dashboard-curso'),
    path('update-curso/<int:pk>', CursoUpdate.as_view(),name='update-curso'),
    path('create-curso/', CursoCreate.as_view(),name='create-curso'),
    path('delete-curso/<int:pk>', CursoDelete.as_view(),name='delete-curso'),
    path('delete-curso-classe/<int:pk>', CursoClasseDelete.as_view(),name='delete-curso-classe'),
    
    path('admin-dashboard-alunos/', AdminAluno,name='admin-dashboard-alunos'),
    path('admin-dashboard-alunos-list/', AlunosList,name='admin-dashboard-alunos-list'),
    path('create-aluno/', AlunoCreate.as_view(),name='create-aluno'),
    path('delete-aluno/<int:pk>', AlunoDelete.as_view(),name='delete-aluno'),
    path('create-matricula/', MatriculaCreate.as_view(),name='create-matricula'),
    path('matricula/<int:pk>/update/', MatriculaUpdate.as_view(), name='matricula-update'),

    

    path('notas-disciplinas-professor/',ProfessorTurmasDisciplinas,name='notas_disciplinas_professor'),
    path('alunos_turma_professor/',AlunosDaturma,name='alunos-da-turma'),
    path('alunos_turma_professor_Select/',AlunosSelect,name='alunos_da_turma_nota'),
    path('aluno-nota-update/<int:pk>',NotaUpdate.as_view(),name='update-nota'),
    path('aluno-nota-delete/<int:pk>',NotaDelete.as_view(),name='delete-nota'),
    path('dashboard-aluno/', AlunoPlataforma,name='dashboard-aluno'),
    path('perfil-aluno/',AlunoPerfil,name='perfil-aluno' ),
    path('aluno-update/<int:pk>',AlunoUpdate.as_view(),name='update-aluno'),




    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    


    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),


    path('email_change/', email_change, name='email_change'),

   



]
