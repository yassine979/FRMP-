from django.shortcuts import render
from django.urls import path
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Actualite, concours , Club, ContactMessage, Profile
from .forms import ProfileForm
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def index(request):
    actualites = Actualite.objects.all()[:9]  # Limiter à 9 actualités
    # Diviser les actualités en groupes de 3
    actualites_vitrine = [actualites[i:i+3] for i in range(0, len(actualites), 3)]
    return render(request, 'pages/index.html', {'actualites_vitrine': actualites_vitrine})
#@login_required
def liste_concours(request):
    concours_list = concours.objects.all().order_by('-date_debut')
    paginator = Paginator(concours_list, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/concours.html', {'page_obj': page_obj})
def about(request):
    return render(request, 'pages/about.html', {})
#@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a bien été envoyé.")
            return redirect('contact')  # Remplace 'contact' par le nom de l’URL
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def service(request):
    return render(request, 'pages/service.html', {})
#@login_required
def page_actualite(request):
    # 1. Base queryset, trié par date décroissante
    qs = Actualite.objects.order_by('-date_pub')

    # 2. Récupération des paramètres GET
    q         = request.GET.get('q', '').strip()
    date_from = request.GET.get('date_from', '')
    date_to   = request.GET.get('date_to', '')

    # 3. Application des filtres
    if q:
        qs = qs.filter(
            Q(titre__icontains=q) |
            Q(contenu__icontains=q)
        )
    if date_from:
        qs = qs.filter(date_pub__gte=date_from)
    if date_to:
        qs = qs.filter(date_pub__lte=date_to)

    # 4. Pagination : 15 actualités par page
    paginator   = Paginator(qs, 15)
    page_number = request.GET.get('page')
    actualites  = paginator.get_page(page_number)

    # 5. Rendu du template avec le contexte
    context = {
        'actualites': actualites,
        'q':          q,
        'date_from':  date_from,
        'date_to':    date_to,
    }
    return render(request, 'pages/lactualite.html', context)

#@login_required
def detail_actualite(request, pk):
    act = get_object_or_404(Actualite, pk=pk)
    # Exemple : 3 dernières actus de la même ligue (hors celle-ci)
    if act.ligue:
        related = Actualite.objects.filter(
            ligue=act.ligue
        ).exclude(pk=act.pk)[:3]
    else:
        related = Actualite.objects.exclude(pk=act.pk).order_by('-date_pub')[:3]
    return render(request, 'pages/detail_actualite.html', {
        'act': act,
        'related_actualites': related,
    })
@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Remplacez 'profile' par le nom de votre URL
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile/profile.html', {'form': form})
