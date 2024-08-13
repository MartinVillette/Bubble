from django.shortcuts import render, redirect
from users.models import Group, Profile, QuoteTag
from .models import Quote
from .forms import QuoteForm
import json

# Create your views here.
def typing(request):
    profile = Profile.objects.get(user=request.user)
    if profile:
        if request.method == 'POST':
            quotes = json.loads(request.POST['quotes'])
            for quote in quotes:
                quote_elem = Quote.objects.get(id=quote['id'])
                quote_profile = profile.quotes.get(quote=quote_elem)
                quote_profile.counter = quote['counter']
                quote_profile.save()

        return render(request, 'french/typing.html', {'profile':profile})
    return redirect('home')

def learning(request):
    profile = Profile.objects.get(user=request.user)
    if profile:
        return render(request, 'french/learning.html', {'profile':profile})
    return redirect('home')

def quotes(request):
    profile = Profile.objects.get(user=request.user)
    if profile:
        if request.method == 'POST':
            quotes = json.loads(request.POST['quotes'])
            quote_elems = []
            quote_tags = []
            for quote in quotes:
                quoteElem = Quote.objects.get(id=quote['id'])
                quote_elems.append(quoteElem)
                quoteProfile = profile.quotes.filter(quote=quoteElem)[0]
                quoteProfile.active = quote['active']
                for id,value in quote['groups'].items():
                    groupProfile = Group.objects.get(id=id)
                    if value:
                        groupProfile.quotes.add(quoteElem)
                    else:
                        groupProfile.quotes.remove(quoteElem)
                    for user in groupProfile.users.all():
                        if value:
                            quoteElem.access.add(user)
                        else:
                            quoteElem.access.remove(user)

                for tag in quote['tags']:
                    quote_tag = QuoteTag.objects.filter(user=request.user, tag=tag)
                    if quote_tag:
                        if not quote_tag[0] in quote_tags:
                            quote_tags.append(quote_tag[0])
                    if not quoteProfile.tags.filter(tag=tag):
                        if quote_tag:
                            quoteProfile.tags.add(quote_tag[0])
                        else:
                            new_quote = QuoteTag(user=request.user, tag=tag)
                            new_quote.save()
                            quoteProfile.tags.add(new_quote)
                            quote_tags.append(new_quote)
                
                for tag in quoteProfile.tags.all():
                    if not tag.tag in quote['tags']:
                        quoteProfile.tags.remove(tag)                

                quoteProfile.save()
                groupProfile.save()

            for tag in QuoteTag.objects.filter(user=request.user):
                if not tag in quote_tags:
                    tag.delete()

            for quote_profile in profile.quotes.all():
                quote = quote_profile.quote
                if not quote in quote_elems:
                    quote.delete()
        else:
            groups = Group.objects.filter(admins=request.user.id)
            tags = QuoteTag.objects.filter(user=request.user.id)
            return render(request, 'french/quotes.html', {'profile':profile,'groups':groups, 'tags':tags})
    return redirect('home')

def lesson(request):
    profile = Profile.objects.get(user=request.user)
    if profile:
        groups = Group.objects.filter(admins=request.user.id)
        quotes = profile.quotes.filter(active=True)
        return render(request, 'french/lesson.html', {'profile':profile,'groups':groups,'quotes':quotes})
    return redirect('home')

def add_quote(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.user.id)
        if profile:
            form = QuoteForm(request.POST)
            if form.is_valid():
                author = form.cleaned_data['author']
                quote = form.cleaned_data['quote']
                page = form.cleaned_data['page']
                quoteElem = Quote.objects.filter(author=author,quote=quote,page=page)
                if quoteElem:
                    new_quote = quoteElem[0]
                else:
                    new_quote = Quote()
                    new_quote.author = author
                    new_quote.quote = quote
                    new_quote.page = page
                    new_quote.admin = request.user
                    new_quote.save()
                    new_quote.access.add(request.user)
                profile.quotes.create(quote=new_quote)
            elif request.POST['quotes']:
                quotes = json.loads(request.POST['quotes'])
                for quote_id in quotes:
                    quote_elem = Quote.objects.get(id=quote_id)
                    if quote_elem:
                        quote_elem.admin = request.user
                        profile.quotes.create(quote=quote_elem)
            return redirect('add-quote')
    else:
        if request.user.is_authenticated:
            quotes = Quote.objects.filter(access=request.user.id).exclude(admin=request.user.id)
            form = QuoteForm()
            return render(request, 'french/add_quote.html', {'quotes':quotes,'form':form})
    return redirect('home')

def quote_share(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    if quote:
        if request.user.is_authenticated:
            quotes = Quote.objects.filter(access=request.user.id)
            form = QuoteForm({'author':quote.author,'quote':quote.quote,'page':quote.page})
            return render(request, 'french/add_quote.html', {'quotes':quotes,'form':form})
    return redirect('home')