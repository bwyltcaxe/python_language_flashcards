"""Views functions for language flashcards service"""
from django.shortcuts import render, redirect
from .forms import CardForm
from .models import Collection, Card

def home(request):
    """Greeting page rendering"""
    return render(request, 'index.html')

def cards_list(request):
    """
    Display a list of cards with respect to filter.
    """
    collection_id = request.GET.get('collection_id')

    if collection_id and collection_id != 'all':
        selected_collection = Collection.objects.get(id=collection_id)
        cards = Card.objects.filter(collection=selected_collection)
    else:
        selected_collection = 'Все карточки'
        cards = Card.objects.all()

    return render(request, 'cards/list.html', {
        "collections": Collection.objects.all(),
        "cards": cards,
        "selected_collection": selected_collection
    })

def add_card(request):
    """
    Handle the creation of a new card.
    The whole validation exists in forms.
    """
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            explanation = form.cleaned_data['explanation']
            collection = form.cleaned_data['collection']
            new_collection = form.cleaned_data['new_collection']

            if new_collection:
                collection, _ = Collection.objects.get_or_create(
                    name=new_collection
                )

            Card.objects.create(
                word=word,
                explanation=explanation,
                collection=collection
            )
            return redirect('add-card')
    else:
        form = CardForm()

    return render(request, 'cards/add.html', {
        'form': form,
        'collections': Collection.objects.all()
    })

def edit_card(request, card_id):
    """
    Edit an already existing card's word or explanation.
    """
    card = Card.objects.get(id=card_id)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card.word = form.cleaned_data['word']
            card.explanation = form.cleaned_data['explanation']
            card.save()
            return redirect('cards-list')
    else:
        form = CardForm()

    return render(request, 'cards/edit.html', {
        'form': form,
        'card': card
    })

def exam_collections(request):
    """
    Display a list of collections to choose one for an exam.
    """
    collections = Collection.objects.all()
    return render(request, 'exam/exam_collections.html', {
        'collections': collections
    })

def exam_session(request, collection_id):
    """
    Run an exam's session. Show cards.
    """
    selected_collection = Collection.objects.get(id=collection_id)
    cards = list(Card.objects.filter(collection=selected_collection))

    return render(request, 'exam/exam_session.html', {
        'collection': selected_collection,
        'cards': cards
    })
