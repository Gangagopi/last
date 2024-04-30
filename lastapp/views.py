from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from . models import Movie,Category,Review
from . forms import MovieForm, ReviewForm
from django.db.models import Q
# Create your views here.
def index(request):
    movie=Movie.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    if query:
        movie = movie.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category_filter:
        movie = movie.filter(category__name__icontains=category_filter)

    context={
        'movie_list':movie,
        'categories': categories
    }
    return render(request,'index.html',context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.movie = movie
            new_review.user = request.user
            new_review.save()
            return redirect('lastapp:detail', movie_id=movie_id)
    else:
        review_form = ReviewForm()
    return render(request, "detail.html", {'movie': movie, 'reviews': reviews, 'review_form': review_form})





def update(request,id):
    movie=Movie.objects.get(id=id)
    form=MovieForm(request.POST or None, request.FILES,instance=movie)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'form':form,'movie':movie})

def delete(request,id):
    if request.method=='POST':
        movie=Movie.objects.get(id=id)
        movie.delete()
        return redirect('/')
    return render(request,'delete.html')



def add_movie(request):
    categories = Category.objects.all()
    if request.method=="POST":
        title=request.POST.get('title',)
        description = request.POST.get('description', )
        release_date = request.POST.get('release_date', )
        actors = request.POST.get('actors', )
        poster = request.FILES['poster']

        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        movie=Movie(title=title,description=description,release_date=release_date,poster=poster,actors=actors,category=category)
        movie.save()

    return render(request,'add.html',{'categories':categories})