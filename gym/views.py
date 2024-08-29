from rest_framework import generics, viewsets, permissions, status
# from django.contrib.auth.models import User
from .models import MembershipPlan, Member, FitnessClass, Booking, GymUser, Instructor
from .serializers import UserSerializer, MembershipPlanSerializer, MemberSerializer, FitnessClassSerializer, BookingSerializer, UserLoginSerializer, BookingHistorySerializer, InstructorSerializer
from .permissions import IsAdminOrStaffOrReadOnly, IsOwnerOrAdminOrReadOnly
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

# User = get_user_model()

""" class UserRegistrationView(generics.CreateAPIView):
    queryset = GymUser.objects.all()
    serializer_class = UserSerializer """

class UserRegistrationView(generics.CreateAPIView):
    queryset = GymUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate token and confirmation link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://zymzoo.onrender.com//activate/{uid}/{token}/"

            # Send confirmation email
            email_subject = "Confirm your email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Check your email for confirmation.", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = GymUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, GymUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')  
    else:
        return redirect('register') 

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                'token': token.key, 
                'user_id': user.id, 
                'is_staff': user.is_staff,  # or use 'is_staff_member' if using custom field
                'first_name': user.first_name,
                'last_name': user.last_name
            }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response("Logged out successfully", status=status.HTTP_200_OK)

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # permission_classes = [IsOwnerOrAdminOrReadOnly]
    permission_classes = [IsAdminOrStaffOrReadOnly]

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        fitness_class_id = self.request.query_params.get('id', None)
        if fitness_class_id is not None:
            queryset = queryset.filter(id=fitness_class_id)
        return queryset

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingHistoryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def booking_history(self, request):
        user = request.user
        bookings = Booking.objects.filter(member__user=user)
        serializer = BookingHistorySerializer(bookings, many=True)
        return Response(serializer.data)
    
def fitness_classes_view(request):
    fitness_classes = FitnessClass.objects.all()
    return render(request, 'fitness_classes.html', {'fitness_classes': fitness_classes})

def booking_history_view(request):
    bookings = Booking.objects.filter(member__user=request.user)
    return render(request, 'booking_history.html', {'bookings': bookings})