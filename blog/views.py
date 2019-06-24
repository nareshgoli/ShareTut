from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import PostModelForm, TutModelForm, UserRegisterForm
from .models import Technology, Tutorial


def list_tech(request):
    technologies = Technology.objects.all()
    context = {
        'technologies': technologies
    }
    return render(request, 'blog/tech_list.html', context)


def tech_detail(request, pk):
    technology = get_object_or_404(Technology, pk=pk)
    tutorials = Tutorial.objects.filter(tech=technology)
    return render(request, 'blog/tech_detail.html', {'technology': technology, 'tutorials': tutorials})


def tech_create(request):
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/tech/')
    context = {
        'form' : form
    }
    return render(request, "blog/tech_create.html", context)


def tut_list(request):
    tutorials = Tutorial.objects.all()
    context = {
        'tutorials' : tutorials
    }
    return render(request, 'blog/tut_list.html', context)


def tut_create(request):
    form = TutModelForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            var = form.save(commit = False)
            var.users = request.user
            var.save()
            a = var.tech.id
            return redirect('tech_detail',pk=a)
    context = {
        'form' : form
    }
    return render(request, "blog/tut_create.html", context)

def tut_upvote(request, pk):
    tutorial = get_object_or_404(Tutorial, pk=pk)
    tutorial.upvote +=1
    tutorial.save()
    return redirect("tech_detail", pk = tutorial.tech.pk)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('/login/')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})
    











