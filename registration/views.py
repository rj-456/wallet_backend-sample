from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserRegistration, Expense
from .serializer import RegistrationSerializer, ExpenseSerializer

# --- API: FOR MOBILE APP (JSON) ---

@api_view(['POST'])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = UserRegistration.objects.get(email=email)
        if user.password == password: 
            return Response({
                "user_id": user.id, 
                "name": user.first_name
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    except UserRegistration.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def expense_list(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        if user_id:
            expenses = Expense.objects.filter(user=user_id).order_by('-date')
        else:
            expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- WEB: FOR BROWSER (HTML) ---

def login_view(request):
    # If user clicked "Login" button (POST request)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if user exists
            user = UserRegistration.objects.get(email=email)
            if user.password == password:
                # Success! Redirect to users list
                # We use session to remember who logged in
                request.session['user_id'] = user.id
                request.session['user_name'] = user.first_name
                return redirect('registration:users_html')
            else:
                messages.error(request, "Invalid password")
        except UserRegistration.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, 'registration/login.html')

def logout_view(request):
    request.session.flush() # Clear session
    return redirect('registration:login_html')

def users_html(request):
    # Check if logged in
    if 'user_id' not in request.session:
        return redirect('registration:login_html')
    
    # Get all users to display in the list
    users = UserRegistration.objects.all()
    return render(request, 'registration/users_list.html', {
        'users': users,
        'current_user': request.session.get('user_name')
    })