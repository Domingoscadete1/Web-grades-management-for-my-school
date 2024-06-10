from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.http.response import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_,logout
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from.forms import *
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import EmailChangeForm

# Create your views here.

def registro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        is_aluno = request.POST.get('is_student') == 'on'
        is_professor = request.POST.get('is_teacher') == 'on'

        user = User.objects.filter(username=username).first()

        if user:
            return render(request, 'alert.html', {'message': 'Já existe um usuário com esse username.', 'redirect_url': '/register/'})

        if is_aluno:
            aluno = Aluno.objects.filter(nome=username).first()
            if not aluno:
                return render(request, 'alert.html', {'message': 'Não existe um aluno com esse username.', 'redirect_url': '/register/'})

        if is_professor:
            professor = Professor.objects.filter(nome=username).first()
            if not professor:
                return render(request, 'alert.html', {'message': 'Não existe um professor com esse username.', 'redirect_url': '/register/'})

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.is_aluno = is_aluno
        user.is_professor = is_professor
        user.save()

        

        return redirect('login')
def custom_404(request, exception):
    return redirect('login')

def home_view(request):
    
    if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin-dashboard')
            elif request.user.is_aluno:
                return redirect('dashboard-aluno') 
            elif request.user.is_professor:
                return redirect('home-professor') 
    else:
        return render(request,'home/home.html')


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('admin-dashboard')
            elif request.user.is_aluno:
                return redirect('dashboard-aluno') 
            elif request.user.is_professor:
                return redirect('home-professor') 
        return render(request, 'login.html')
    
    username = request.POST.get('username')
    senha = request.POST.get('senha')

    user = authenticate(request, username=username, password=senha)

    if user is not None:
        login_(request, user)
        return redirect('plataforma')
    else:
        return render(request, 'alert.html', {'message': 'Email ou senha incorretos.', 'redirect_url': '/login/'})
def logout_view(request):
    logout(request)
    return redirect('login')
def plataforma(request):
    if request.user.is_authenticated:
        if request.user.is_aluno:
            aluno=Aluno.objects.filter(nome__iexact=request.user.username).first()
            #if aluno:
            return redirect('dashboard-aluno')
            #else:
                #return render(request, 'alert.html', {'message': 'Não existe nenhum aluno com este username .', 'redirect_url': ''})



           
            
        elif request.user.is_professor:
            professor=Professor.objects.filter(nome__iexact=request.user.username).first()
            #if professor:
            return redirect('home-professor')
            #else:
                #return render(request, 'alert.html', {'message': 'Não existe nenhum professor com este username .', 'redirect_url': ''})
                #professor=Professor.objects.create(nome=request.user.username)
                #professor.save()
                #return redirect('home-professor')

        elif request.user.is_admin:
            return redirect('admin-dashboard')
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})

def teste(request):
    return render(request,'P.F/index.html')

@login_required
def AdminView(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            context={
                'turmas':Turma.objects.all(),
                'alunos':Aluno.objects.all(),
                'professores':Professor.objects.all(),
                'cursos':Curso.objects.all(),
                'disciplinas':Disciplina.objects.all(),
                'classes':Classe.objects.all(),

            }
            return render(request,'admin_list.html',context)
        return render(request, 'alert.html', {'message': 'Você precisa ser um admin para acessar esta página.', 'redirect_url': '/login/'})
    
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})
@login_required
def AdminProfessores(request):
    professores=Professor.objects.all()
    professores_paginator=Paginator(professores,4)
    page_num=request.GET.get('page')
    page=professores_paginator.get_page(page_num)
    
   
    
    disciplinas=ProfessorDisciplina.objects.all()
    turmas = ProfessorTurma.objects.all()
        

    context={
        'page':page,
        'disciplinas':disciplinas,
        'turmas':turmas,
        'professores':professores
    }
    return render(request,'home/admin_professor_list.html',context)
"""disciplinas views inicio"""
@login_required
def AdminDisciplinas(request):
    disciplina=Disciplina.objects.all()

    form_disciplina=DisciplinaForm()
    disciplinas_paginator=Paginator(disciplina,4)
    page_num=request.GET.get('page')
    page=disciplinas_paginator.get_page(page_num)
    
   
    
   
    
    professores=ProfessorDisciplina.objects.all()
    
    cursos=CursoDisciplina.objects.all()
    classes=ClasseDisciplina.objects.all()
        

    context={
        'page':page,
        'professores':professores,
        'disciplinas':Disciplina.objects.all(),
        'professores1':Professor.objects.all(),
        'classes1':Classe.objects.all(),

        'cursos':cursos,
        'classes':classes,
        'form_disciplina':form_disciplina,

    }
    return render(request,'home/disciplina_list.html',context)

class DisciplinaCreate(LoginRequiredMixin,CreateView):
    model = Disciplina
    fields = ['nome', 'nivel', 'descricao', 'programa', 'objectivo', 'obs']
    success_url = reverse_lazy('admin-dashboard')
    login_url = 'login'
    


    def form_valid(self, form):
        disciplina = form.cleaned_data['nome']
        if Disciplina.objects.filter(nome__iexact=disciplina).exists():
            form.add_error(None, 'Esta disciplina já existe.')
            return self.form_invalid(form)
        return super().form_valid(form)

    


class DisciplinaCursoCreate(LoginRequiredMixin,CreateView):
    model=CursoDisciplina
    fields=['disciplina_id','curso_id']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
    def form_valid(self, form):
       
        disciplina_id = form.cleaned_data['disciplina_id']
        curso_id = form.cleaned_data['curso_id']
        
        if curso_id:  
            if CursoDisciplina.objects.filter(disciplina_id=disciplina_id, curso_id=curso_id).exists():
                form.add_error(None, 'Esta associação de disciplina e curso já existe.')
                return self.form_invalid(form)
        else:
            
            form.instance.curso_id = None

        return super().form_valid(form)
class DisciplinaClasseCreate(LoginRequiredMixin,CreateView):
    model=ClasseDisciplina
    fields=['disciplina_id','classe_id']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    def form_valid(self, form):
       
        disciplina_id = form.cleaned_data['disciplina_id']
        classe_id = form.cleaned_data['classe_id']
        
        if ClasseDisciplina.objects.filter(disciplina_id=disciplina_id, classe_id=classe_id).exists():
            form.add_error(None, 'Esta associação de disciplina e classe já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)

class DisciplinaUpdate(LoginRequiredMixin,UpdateView):
   
    model=Disciplina
    context_object_name='disciplinas'
    fields=['nome','nivel','descricao','programa','objectivo','obs']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class DisciplinaDelete(LoginRequiredMixin,DeleteView):
   
    model=Disciplina
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    

"""disciplanas views fim"""


"""professores views inicio"""
@login_required
def ProfessorView(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
        
    
            professores=Professor.objects.filter(nome__iexact=request.user.username).first()
    
   
    
            disciplinas=ProfessorDisciplina.objects.filter(professor_id=professores).all()
            turmas = ProfessorTurma.objects.all()
            turmas1=ProfessorTurma.objects.filter(professor_id=professores).all()
        

            context={
            'professores':professores,
            'disciplinas':disciplinas,
            'turmas':turmas,
            'turmas1':turmas1.count(),
            'disciplinas1':disciplinas.count(),
            }
            return render(request,'professor_list.html',context)
        return render(request, 'alert.html', {'message': 'Você precisa ser um professor para acessar esta página.', 'redirect_url': '/login/'})
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})
@login_required
def ProfessorPerfil(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
        
    
            professores=Professor.objects.filter(nome__iexact=request.user.username).first()
    
   
    
            disciplinas=ProfessorDisciplina.objects.all()
            turmas = ProfessorTurma.objects.all()
        

            context={
            'professores':professores,
            'disciplinas':disciplinas,
            'turmas':turmas,
             
            }
            return render(request,'professor_perfil.html',context)
        return HttpResponse('você precisa ser um professor para acessar está pagina')
    return HttpResponse('você precisa estar logado para acessar esta página')
class ProfessorDisciplinaCreate(LoginRequiredMixin,CreateView):
    model=ProfessorDisciplina
    fields=['disciplina_id','professor_id']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
    def form_valid(self, form):
       
        disciplina_id = form.cleaned_data['disciplina_id']
        professor_id = form.cleaned_data['professor_id']
        
        if ProfessorDisciplina.objects.filter(disciplina_id=disciplina_id, professor_id=professor_id).exists():
            
            form.add_error(None, 'Esta associação de professor e disciplina já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)
class ProfessorDisciplinaDelete(LoginRequiredMixin,DeleteView):
    model=ProfessorDisciplina
   
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
class ProfessorTurmaCreate(CreateView):
    model=ProfessorTurma
    fields=['turma_id','professor_id']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
    def form_valid(self, form):
        
        turma_id = form.cleaned_data['turma_id']
        professor_id = form.cleaned_data['professor_id']
        
        if ProfessorTurma.objects.filter(turma_id=turma_id, professor_id=professor_id).exists():
            form.add_error(None, 'Esta associação de professor e turma já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)
class ProfessorTurmaUpdate(LoginRequiredMixin,UpdateView):
    model=ProfessorTurma
    fields=['turma_id','professor_id']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class ProfessorTurmaDelete(LoginRequiredMixin,DeleteView):
    model=ProfessorTurma
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class ProfessorDelete(LoginRequiredMixin,DeleteView):
    model=Professor
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
    

class ProfessorCreate(LoginRequiredMixin,CreateView):
    model=Professor
    fields=['nome','bi','data_nascimento','nivel_escolaridade','habilitacoes','experiencia','estado_civil','genero','foto','nacionalidade','obs']
    success_url=reverse_lazy('create-professor-disciplina')
    login_url = 'login'
    
    def form_valid(self, form):
        professor = form.cleaned_data['nome']
        
        
        if Professor.objects.filter(nome__iexact=professor).exists():
            form.add_error(None, 'Este professor já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)
    
from django.urls import reverse_lazy, reverse

class ProfessorUpdate(LoginRequiredMixin, UpdateView):
    model = Professor
    fields = ['nome', 'bi', 'data_nascimento', 'nivel_escolaridade', 'habilitacoes', 'experiencia', 'estado_civil', 'foto', 'genero', 'nacionalidade', 'obs']
    login_url = 'login'

    def get_success_url(self):
        # Verifique se o usuário é um professor
        if hasattr(self.request.user, 'is_professor') and self.request.user.is_professor:
            return reverse('home-professor')
        else:
            return reverse('admin-dashboard')
class ProfessorUpdate1(LoginRequiredMixin,UpdateView):
    model=Professor
    fields=['nome','bi','data_nascimento','nivel_escolaridade','habilitacoes','experiencia','estado_civil','foto','genero','nacionalidade','obs']
    
    success_url=reverse_lazy('perfil-professor')
    login_url = 'login'
"""professores views  fim"""

"""classes views inicio"""
@login_required
def AdminClasses(request):
    
    classes=Classe.objects.all()
    classes_paginator=Paginator(classes,4)
    page_num=request.GET.get('page')
    page=classes_paginator.get_page(page_num)
    
   
    
   
    turmas=Turma.objects.all()
    disciplinas=ClasseDisciplina.objects.all()
    cursos=CursoClasse.objects.all()
    
        

    context={
        'disciplinas':disciplinas,
        'cursos':cursos,
        'page':page,
        'turmas':turmas,
        'classes':classes,

    }
    return render(request,'home/classe_list.html',context)
class ClasseCreate(LoginRequiredMixin,CreateView):
   
    model=Classe
    context_object_name='Classes'
    fields=['nome','nivel','descricao','obs']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
    def form_valid(self, form):
       
        classe = form.cleaned_data['nome']
        
        
        if Classe.objects.filter(nome__iexact=classe).exists():
            
            form.add_error(None, 'Esta classe já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)
class ClasseUpdate(LoginRequiredMixin,UpdateView):
   
    model=Classe
    context_object_name='Classes'
    fields=['nome','nivel','descricao','obs']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class ClasseDelete(LoginRequiredMixin,DeleteView):
   
    model=Classe
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class CursoClasseCreate(LoginRequiredMixin,CreateView):
    model = CursoClasse
    fields = ['classe_id', 'curso_id']
    success_url = reverse_lazy('admin-dashboard')
    login_url = 'login'
    

    def form_valid(self, form):
        classe = form.cleaned_data['classe_id']
        curso = form.cleaned_data['curso_id']
        
        
        restricted_classes = ['1ª', '2ª', '3ª', '4ª', '5ª', '6ª', '7ª', '8ª', '9ª']
        
        
        if classe.nome in restricted_classes:
            form.add_error('classe_id', 'Classes dos anos [1ª, 2ª, 3ª, 4ª, 5ª, 6ª, 7ª, 8ª, 9ª] não podem ser associadas a um curso.')
            return self.form_invalid(form)
        
        
        if CursoClasse.objects.filter(classe_id=classe, curso_id=curso).exists():
            form.add_error(None, 'Esta associação de classe e curso já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)
"""classe views fim"""
@login_required
def AdminAluno(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            context={
                'turmas':Turma.objects.all()
            }
            return render(request,'form_turma.html',context)
@login_required
def AlunosList(request):
    if request.method=='POST':
        turma=request.POST.get('turma')
        
        context={
            'turma':Turma.objects.filter(nome__iexact=turma).first(),
            'matriculas':Matricula.objects.all(),
            'alunos':Aluno.objects.all(),
            'matriculas1':Matricula.objects.filter(turma_id=Turma.objects.filter(nome__iexact=turma).first()).all(),
        }
        return render(request,'alunos_list.html',context)
    return redirect('admin-dashboard-alunos')
    
class MatriculaCreate(LoginRequiredMixin,CreateView):
    model=Matricula
    fields=['aluno_id','turma_id']  
    success_url=reverse_lazy('admin-dashboard') 
    login_url = 'login'

    def form_valid(self, form):
       
        aluno= form.cleaned_data['aluno_id']
        if Matricula.objects.filter(aluno_id=aluno,).exists():
            form.add_error(None, 'Esta matricula já existe.')
            return self.form_invalid(form)
        return super().form_valid(form)
class MatriculaUpdate(LoginRequiredMixin, UpdateView):
    model = Matricula
    fields = ['aluno_id', 'turma_id']
    success_url = reverse_lazy('admin-dashboard')
    login_url = 'login'

    def form_valid(self, form):
        aluno = form.cleaned_data['aluno_id']
        turma = form.cleaned_data['turma_id']
        classe = form.cleaned_data['classe_id']

        if Matricula.objects.filter(aluno_id=aluno, turma_id=turma).exists():
            form.add_error(None, 'Esta matrícula já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class AlunoCreate(LoginRequiredMixin,CreateView):
    model=Aluno
    fields=['ano_lectivo','n_processo','nome','idade','data_nascimento','n_bi','data_emissao','foto','estado_civil','genero','nacionalidade','nome_pai','nome_mae','profissao_pai','profissao_mae','obs']
    success_url=reverse_lazy('create-matricula')
    login_url = 'login'
    def form_valid(self, form):
       
        nome = form.cleaned_data['nome']
        n_processo = form.cleaned_data['n_processo']
        if Aluno.objects.filter(nome=nome,n_processo=n_processo).exists():
            form.add_error(None, 'Este aluno já existe.')
            return self.form_invalid(form)
        return super().form_valid(form)
class AlunoDelete(LoginRequiredMixin,DeleteView):
    model=Aluno
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'



"""turmas views inicio"""
@login_required
def AdminTurmas(request):
    
    curso=Curso.objects.all()
    turmas=Turma.objects.all()
    classes=Classe.objects.all()

    turmas_paginator=Paginator(turmas,4)
    page_num=request.GET.get('page')
    page=turmas_paginator.get_page(page_num)
    
   
    
   
    
    
    
        

    context={
        
        'classes':classes,
        'page':page,
        'cursos':curso,
        'turmas':turmas,

    }
    return render(request,'home/turma_list.html',context)


class TurmaCreate(LoginRequiredMixin, CreateView):
    model = Turma
    context_object_name = 'Classes'
    fields = ['nome', 'n_alunos', 'n_max_alunos', 'sala', 'classe_id', 'curso_id']
    success_url = reverse_lazy('admin-dashboard')
    login_url = 'login'

    CLASSES_SEM_CURSO = ['Iniciação', '1ª', '2ª', '3ª', '4ª', '5ª', '6ª', '7ª', '8ª', '9ª']

    def form_valid(self, form):
        turma_nome = form.cleaned_data['nome']
        sala = form.cleaned_data['sala']
        classe = form.cleaned_data['classe_id']
        curso = form.cleaned_data['curso_id']
        
      
        if Turma.objects.filter(nome__iexact=turma_nome).exists():
            form.add_error(None, 'Esta turma já existe.')
            return self.form_invalid(form)

        
        if Turma.objects.filter(sala=sala).exists():
            form.add_error('sala', 'Já existe uma turma com esta sala.')
            return self.form_invalid(form)
        
        
        if classe.nome in self.CLASSES_SEM_CURSO and curso:
            form.add_error('curso_id', 'Turmas das classes da Iniciação até a 9ª não devem ter um curso associado.')
            return self.form_invalid(form)
        
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    
class TurmaUpdate(LoginRequiredMixin,UpdateView):
   
    model=Turma
    context_object_name='Classes'
    fields=['nome','n_alunos','n_max_alunos','sala','classe_id','curso_id']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    CLASSES_SEM_CURSO = ['Iniciação', '1ª', '2ª', '3ª', '4ª', '5ª', '6ª', '7ª', '8ª', '9ª']

    def form_valid(self, form):
        turma_nome = form.cleaned_data['nome']
        classe = form.cleaned_data['classe_id']
        curso = form.cleaned_data['curso_id']
        sala = form.cleaned_data['sala']
        
        
        if Turma.objects.filter(nome__iexact=turma_nome).exclude(pk=self.object.pk).exists():
            form.add_error(None, 'Esta turma já existe.')
            return self.form_invalid(form)
        
        if Turma.objects.filter(sala=sala).exists():
            form.add_error('sala', 'Já existe uma turma com esta sala.')
            return self.form_invalid(form)
        
        if classe.nome in self.CLASSES_SEM_CURSO and curso:
            form.add_error('curso_id', 'Turmas das classes de Iniciação até a 9ª não devem ter um curso associado.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
class TurmaDelete(LoginRequiredMixin,DeleteView):
   
    model=Turma
       
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
"""turmas views fim"""
        

    
"""curso views"""
@login_required
def AdminCurso(request):
    
    classes=CursoClasse.objects.all()
    turmas=Turma.objects.all()
    disciplinas=CursoDisciplina.objects.all()

    
    
   
    
    cursos=Curso.objects.all()

    cursos_paginator=Paginator(cursos,4)
    page_num=request.GET.get('page')
    page=cursos_paginator.get_page(page_num)
    
   
    
        

    context={
        
        'page':page,
        'classes':classes,
        'turmas':turmas,
        'disciplinas':disciplinas,
        'cursos':cursos,
        

    }
    return render(request,'home/curso_list.html',context)

class CursoUpdate(LoginRequiredMixin,UpdateView):
   
    model=Curso
    context_object_name='Classes'
    fields=['nome','nivel','descricao','objectivo','programa']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class CursoDelete(LoginRequiredMixin,DeleteView):
    model=Curso
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
   
class CursoClasseDelete(LoginRequiredMixin,DeleteView):
   
    model=CursoClasse
    
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
class CursoCreate(LoginRequiredMixin,CreateView):
   
    model=Curso
    context_object_name='Classes'
    fields=['nome','nivel','descricao','objectivo','programa']
    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'
    
    def form_valid(self, form):
       
        turma = form.cleaned_data['nome']
        
        
        if Turma.objects.filter(nome__iexact=turma).exists():
            
            form.add_error(None, 'Esta turma já existe.')
            return self.form_invalid(form)

        return super().form_valid(form)

    


"""Views De Gerenciamento de notas na ótica do professor """
@login_required
def ProfessorTurmasDisciplinas(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
        
    
            professores=Professor.objects.filter(nome__iexact=request.user.username).first()
            turmas=ProfessorTurma.objects.all()
            disciplinas=ProfessorDisciplina.objects.all()
            context={
                'professores':professores,
                'turmas':turmas,
                'disciplinas':disciplinas,

            }
            return render(request,'professores/disciplinas.html',context)
        else:
            return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})
    
@login_required
def AlunosDaturma(request):
    if request.method=="POST":
        turma=request.POST.get('turma')
        disciplina=request.POST.get('disciplina')
        matricula=Matricula.objects.all()
        context={
            'turma':turma,
            'disciplina':disciplina,
            'matriculas':matricula,
            'notas':Nota.objects.all(),
        }
        return render(request,'professores/alunosSelect.html',context)
    else:
        return render(request,'professores/alunosSelect.html')


@login_required
def AlunosSelect(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
            professores = Professor.objects.filter(nome__iexact=request.user.username).first()
            if request.method == "POST":
                aluno = request.POST.get('aluno')
                disciplina = request.POST.get('disciplina')
                alunos = Aluno.objects.filter(nome__iexact=aluno).first()
                disciplinas = Disciplina.objects.filter(nome__iexact=disciplina).first()
                data = request.POST.get('data')
                tipo = request.POST.get('tipo')
                valor = request.POST.get('valor')
                turma = request.POST.get('turma')
                trimestre = request.POST.get('trimestre')
                matricula = Matricula.objects.all()
                
                if aluno and disciplina:
                    notas_existentes = Nota.objects.filter(aluno_id=alunos, disciplina_id=disciplinas, trimestre=trimestre).count()
                    
                    
                    try:
                        valor = float(valor)
                        if valor < 0 or valor > 20:
                            context = {
                                'message': 'O valor da nota deve estar entre 0 e 20.',
                                'turma': turma,
                                'aluno': aluno,
                                'matriculas': Matricula.objects.all(),
                                'redirect_url':'/notas-disciplinas-professor/',
                            }
                            return render(request, 'alert.html', context)
                    except ValueError:
                        context = {
                            'message': 'O valor da nota deve ser um número.',
                            'turma': turma,
                            'aluno': aluno,
                            'matriculas': Matricula.objects.all(),
                            'redirect_url':'/notas-disciplinas-professor/',
                            
                        }
                        return render(request, 'alert.html', context)
                    if data=='':
                        context = {
                            'message': 'Preecha a data da prova.',
                            'turma': turma,
                            'aluno': aluno,
                            'matriculas': Matricula.objects.all(),
                            'redirect_url':'/notas-disciplinas-professor/',
                            
                        }
                        return render(request, 'alert.html', context)

                    
                    if notas_existentes < 3:
                        Nota.objects.create(
                            aluno_id=alunos,
                            disciplina_id=disciplinas,
                            data_prova=data,
                            tipo_prova=tipo,
                            valor=valor,
                            trimestre=trimestre
                        )
                        notas = Nota.objects.all()
                        context = {
                            'notas': notas,
                            'turma': turma,
                            'aluno': aluno,
                            'matriculas': matricula,
                        }
                        return redirect('home-professor')
                    else:
                        context = {
                            'message': 'O aluno já possui 3 notas para esta disciplina neste trimestre.',
                            'turma': turma,
                            'aluno': aluno,
                            'matriculas': Matricula.objects.all(),
                            'redirect_url':'/notas-disciplinas-professor/',
                        }
                        return render(request, 'alert.html', context)
                else:
                    return render(request, 'professores/notas.html', context)
            else:
                return redirect('home-professor')
        
        return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})
    
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})


class NotaUpdate(LoginRequiredMixin, UpdateView):
    model = Nota
    context_object_name = 'nota'
    fields = ['valor', 'tipo_prova', 'data_prova', 'trimestre']
    success_url = reverse_lazy('home-professor')
    login_url = 'login'

    def form_valid(self, form):
        valor = form.cleaned_data['valor']
        trimestre = form.cleaned_data['trimestre']
        data=form.cleaned_data['data_prova']
        aluno_id = self.get_object().aluno_id
        disciplina_id = self.get_object().disciplina_id

        
        try:
            valor = float(valor)
            if valor < 0 or valor > 20:
                context = self.get_context_data()
                context['message'] = 'O valor da nota deve estar entre 0 e 20.'
                context['redirect_url'] = '/notas-disciplinas-professor/'
                return render(self.request, 'alert.html', context)
        except ValueError:
            context = self.get_context_data()
            context['message'] = 'O valor da nota deve ser um número.'
            context['redirect_url'] = '/notas-disciplinas-professor/'
            return render(self.request, 'alert.html', context)
        if data=='':
                    context = {
                            'message': 'Preecha a data da prova.',
                            
                            'matriculas': Matricula.objects.all(),
                            'redirect_url':'/notas-disciplinas-professor/',
                            
                        }
                    return render(self.request, 'alert.html', context)

        
        notas_existentes = Nota.objects.filter(aluno_id=aluno_id, disciplina_id=disciplina_id, trimestre=trimestre).exclude(pk=self.object.pk).count()
        if notas_existentes >= 3:
            context = self.get_context_data()
            context['message'] = 'O aluno já possui 3 notas para esta disciplina neste trimestre.'
            context['redirect_url'] = '/notas-disciplinas-professor/'
            return render(self.request, 'alert.html', context)

        return super().form_valid(form)
class NotaDelete(LoginRequiredMixin,DeleteView):
    model = Nota
    success_url = reverse_lazy('home-professor')
    context_object_name = 'nota'
    login_url = 'login'

"""Fim Das Views De Gerenciamento de notas na ótica do professor"""

"""Inicio Das views de Gerenciamento de notas na ótica do aluno"""


@login_required
def AlunoPlataforma(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'is_aluno') and request.user.is_aluno:
            aluno = Aluno.objects.filter(nome__iexact=request.user.username).first()
            matriculas = Matricula.objects.filter(aluno_id=aluno)
            classes = Classe.objects.all()
            disciplinas = ClasseDisciplina.objects.all()
            curso_disciplinas = CursoDisciplina.objects.all()
            turmas = Turma.objects.all()

            trimestre_selecionado = request.GET.get('trimestre')
            notas = Nota.objects.filter(aluno_id=aluno)
            if trimestre_selecionado:
                notas = notas.filter(trimestre=trimestre_selecionado)

            medias_disciplinas = {}
            for disciplina in disciplinas:
                notas_disciplina = notas.filter(disciplina_id=disciplina.disciplina_id.id)
                total = sum(nota.valor for nota in notas_disciplina)
                count = notas_disciplina.count()
                media = total / count if count == 3 else 'Sem Media'
                medias_disciplinas[disciplina.disciplina_id.id] = media

            trimestres = Nota.objects.values_list('trimestre', flat=True).distinct()
            
            context = {
                'aluno': aluno,
                'matriculas': matriculas,
                'classes': classes,
                'disciplinas': disciplinas,
                'disciplinas1':disciplinas.count(),
                'curso_disciplinas': curso_disciplinas,
                'notas': notas,
                'turmas': turmas,
                'medias_disciplinas': medias_disciplinas,
                'trimestres': trimestres,
                'trimestre_selecionado': trimestre_selecionado,
            }

            return render(request, 'aluno_dashboard.html', context)
        return render(request, 'alert.html', {'message': 'Você precisa estar logado como aluno para acessar esta página.', 'redirect_url': '/login/'})
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})


@login_required      
def AlunoPerfil(request):
    if request.user.is_authenticated:
        if request.user.is_aluno:
        
    
            alunos=Aluno.objects.filter(nome__iexact=request.user.username).first()
            matriculas = Matricula.objects.filter(aluno_id=alunos)

   
    
            disciplinas=ProfessorDisciplina.objects.all()
            turmas = ProfessorTurma.objects.all()
            turmas_n1=turmas.count()
            turmas1 = Turma.objects.all()

        

            context={
            'alunos':alunos,
            'disciplinas':disciplinas,
            'turmas1':turmas,
            'matriculas': matriculas,
            'turmas_n1':turmas_n1,
            'turmas':turmas1,
            }
            return render(request,'aluno_perfil.html',context)
        else:
          
            return render(request, 'alert.html', {'message': 'Você precisa estar logado como aluno para acessar esta página.', 'redirect_url': '/login/'})
    else:

        return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/login/'})

class AlunoUpdate(LoginRequiredMixin,UpdateView):
    model=Aluno
    context_object_name='alunos'
    fields=['ano_lectivo','n_processo','nome','idade','data_nascimento','n_bi','data_emissao','foto','estado_civil','genero','nacionalidade','nome_pai','nome_mae','profissao_pai','profissao_mae','obs']

    success_url=reverse_lazy('admin-dashboard')
    login_url = 'login'


"""Fim Das views de Gerenciamento de notas na ótica do aluno"""
    
def not_found(request,exception):
    return render(request,'home/not_found.html',status=404)





@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu email foi alterado com sucesso.')
           
            if request.user.is_admin:
                return redirect('admin-dashboard')  
            elif request.user.is_professor:
                return redirect('home-professor')  
            elif request.user.is_aluno:
                return redirect('dashboard-aluno')  
            else:
                return redirect('profile')  
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, 'registration/email_change_form.html', {'form': form})