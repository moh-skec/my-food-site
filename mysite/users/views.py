from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import RegisterForm, LoginForm

FOOD_LIST_URL = 'food:list'


class RegisterView(CreateView):
    """
    User registration view that handles user account creation.
    """
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(FOOD_LIST_URL)

    def form_valid(self, form):
        """
        Handle successful form submission.

        Args:
            form: The validated form instance

        Returns:
            HttpResponseRedirect: Redirect to success URL
        """
        response = super().form_valid(form)

        user = form.save()
        login(self.request, user)

        messages.success(
            self.request,
            f'Welcome {user.username}! Your account has been created successfully.'
        )

        return response

    def form_invalid(self, form):
        """
        Handle form submission with validation errors.

        Args:
            form: The form instance with errors

        Returns:
            HttpResponse: Rendered template with form errors
        """
        messages.error(
            self.request,
            'Please correct the errors below and try again.'
        )
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Handle request dispatch. Redirect authenticated users.

        Args:
            request: The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponse: Either redirect or normal view response
        """
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return HttpResponseRedirect(reverse_lazy(FOOD_LIST_URL))

        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """
    Custom login view with enhanced styling and user experience.
    """
    template_name = 'users/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Return the URL to redirect to after successful login.

        Returns:
            str: Success URL
        """
        return reverse_lazy(FOOD_LIST_URL)

    def form_valid(self, form):
        """
        Handle successful form submission.

        Args:
            form: The validated form instance

        Returns:
            HttpResponseRedirect: Redirect to success URL
        """
        username = form.cleaned_data.get('username')
        messages.success(
            self.request,
            f'Welcome back, {username}! You have been logged in successfully.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle form submission with validation errors.

        Args:
            form: The form instance with errors

        Returns:
            HttpResponse: Rendered template with form errors
        """
        messages.error(
            self.request,
            'Invalid username or password. Please try again.'
        )
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Handle request dispatch. Redirect authenticated users.

        Args:
            request: The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponse: Either redirect or normal view response
        """
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return HttpResponseRedirect(reverse_lazy(FOOD_LIST_URL))

        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    """
    Custom logout view with enhanced user experience and messaging.
    """

    def get_next_page(self):
        """
        Return the URL to redirect to after successful logout.

        Returns:
            str: Next page URL
        """
        return reverse_lazy(FOOD_LIST_URL)

    def dispatch(self, request):
        """
        Handle both GET and POST requests for logout.

        Arg:
            request: The HTTP request

        Returns:
            HttpResponse: Redirect response after logout
        """
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.success(
                request,
                f'Goodbye, {username}! You have been logged out successfully.'
            )
        else:
            messages.info(request, 'You were not logged in.')

        return HttpResponseRedirect(self.get_next_page())
