from django.shortcuts import render,render_to_response,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from store.forms import *
from django.contrib.auth.decorators import login_required
from django.http import *
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')

    return HttpResponseRedirect('/accounts/login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def bookDetailView(request, bid):
    template_name='store/book_detail.html'
    
    # START YOUR CODE HERE
    objId = Book.objects.get(id = bid)
    value = 0.0
    try:
        book_copy = BookCopy.objects.get(book = objId)
        if book_copy.status:
            numBooks = 1
        else:
            numBooks = 0 
    except:
        BookCopy.objects.create(status=True, book = objId)
        numBooks = 1
    value = 0.0
    try:
        book_r = userRating.objects.get(bname=objId,user=request.user)
        value = book_r.value 
    except:
        userRating.objects.create(bname=objId,user=request.user)  
    context={
        'book':objId, # set this to an instance of the required book
        'num_available':numBooks, # set this 1 if any copy of this book is available, otherwise 0
        'book_copy':value
    }
    return render(request,template_name, context=context)


def bookListView(request):
    template_name='store/book_list.html'
    books = []
    for obj in Book.objects.all():
        books.append(obj)
    context={
        'books':books, # set here the list of required books upon filtering using the GET parameters
    }
    get_data=request.GET
    # START YOUR CODE HERE
    
    
    return render(request,template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name='store/loaned_books.html'
    books = []
    for book in BookCopy.objects.filter(status=False,borrower=request.user):
        books.append(book)
    context={
        'books': books,
    }
    '''
    The above key books in dictionary context should contain a list of instances of the 
    bookcopy model. Only those books should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    


    return render(request,template_name,context=context)

@csrf_exempt
@login_required
def loanBookView(request):  
    
    '''
    Check if an instance of the asked book is available.
    If yes, then set message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    #message = 'success'
    book_id = request.POST.get("bid") # get the book id from post data
    obj = Book.objects.get(id=book_id) #Book.objects.filter(id=book_id)
    book_copy = BookCopy.objects.get(book = obj)
    message = 0
    if book_copy.status == True:
        message =1
        book_copy.status = False
        book_copy.borrower = request.user
        book_copy.borrow_date = datetime.datetime.now().date()
        book_copy.save()
    response_data={
        'message': message,
    }
    return JsonResponse(response_data)
    

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    book_id = request.POST.get("bid")
    obj = Book.objects.get(id=book_id)
    book_copy = BookCopy.objects.get(book = book_id)
    book_copy.status = True
    book_copy.save()
    response_data={
        'messsage': 1
    }
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def returnRating(request):
    book_id = request.POST.get("bid")
    obj = Book.objects.get(id=book_id)
    book_r = userRating.objects.get(bname=book_id,user=request.user)
    rating = float(request.POST.get("rValue"))
    book_r.value=rating
    book_r.save()    
    number = 0
    obj.totalRating = obj.totalRating+rating
    obj.number = obj.number+1
    obj.save()
    if obj.number != 0:
        obj.rating = round(obj.totalRating/obj.number,2)
        obj.save()
    response_data={
        'messsage': 1
    }
    return JsonResponse(response_data)
