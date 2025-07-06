from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q, Min, Max
import os

from .models import Food


@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(LoginRequiredMixin, ListView):
    """
    Admin dashboard showing key statistics and metrics.
    """
    model = Food
    template_name = 'food/admin/dashboard.html'
    context_object_name = 'recent_foods'

    def get_queryset(self):
        """Get recent food items for dashboard."""
        return Food.objects.all()[:5]

    def get_context_data(self, **kwargs):
        """Add dashboard statistics to context."""
        context = super().get_context_data(**kwargs)

        total_foods = Food.objects.count()
        available_foods = Food.objects.filter(available=True).count()
        unavailable_foods = total_foods - available_foods

        total_users = User.objects.count()
        staff_users = User.objects.filter(is_staff=True).count()

        if total_foods > 0:
            price_stats = Food.objects.aggregate(
                avg_price=Avg('price'),
                min_price=Min('price'),
                max_price=Max('price'),
            )
        else:
            price_stats = {
                'avg_price': 0,
                'min_price': 0,
                'max_price': 0,
            }

        context.update({
            'total_foods': total_foods,
            'available_foods': available_foods,
            'unavailable_foods': unavailable_foods,
            'total_users': total_users,
            'staff_users': staff_users,
            'regular_users': total_users - staff_users,
            'avg_price': price_stats['avg_price'] or 0,
            'min_price': price_stats['min_price'] or 0,
            'max_price': price_stats['max_price'] or 0,
        })

        return context


@method_decorator(staff_member_required, name='dispatch')
class AdminFoodListView(LoginRequiredMixin, ListView):
    """
    Admin view for managing all food items with advanced filtering.
    """
    model = Food
    template_name = 'food/admin/food_list.html'
    context_object_name = 'foods'
    paginate_by = 15

    def get_queryset(self):
        """Filter foods based on admin parameters."""
        queryset = Food.objects.all().order_by('-id')

        availability = self.request.GET.get('availability')
        if availability == 'available':
            queryset = queryset.filter(available=True)
        elif availability == 'unavailable':
            queryset = queryset.filter(available=False)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        """Add filtering context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'current_availability': self.request.GET.get('availability', ''),
            'current_search': self.request.GET.get('search', ''),
            'current_min_price': self.request.GET.get('min_price', ''),
            'current_max_price': self.request.GET.get('max_price', ''),
        })
        return context


@method_decorator(staff_member_required, name='dispatch')
class AdminUserListView(LoginRequiredMixin, ListView):
    """
    Admin view for managing users.
    """
    model = User
    template_name = 'food/admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        """Filter users based on admin parameters."""
        queryset = User.objects.all().order_by('-date_joined')

        user_type = self.request.GET.get('user_type')
        if user_type == 'staff':
            queryset = queryset.filter(is_staff=True)
        elif user_type == 'regular':
            queryset = queryset.filter(is_staff=False)
        elif user_type == 'active':
            queryset = queryset.filter(is_active=True)
        elif user_type == 'inactive':
            queryset = queryset.filter(is_active=False)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )

        return queryset

    def get_context_data(self, **kwargs):
        """Add filtering context."""
        context = super().get_context_data(**kwargs)
        context.update({
            'current_user_type': self.request.GET.get('user_type', ''),
            'current_search': self.request.GET.get('search', ''),
        })
        return context


@method_decorator(staff_member_required, name='dispatch')
class AdminAnalyticsView(LoginRequiredMixin, DetailView):
    """
    Admin analytics view with charts and detailed statistics.
    """
    template_name = 'food/admin/analytics.html'

    def get_object(self):
        """Return None as this is not tied to a specific object."""
        return None

    def get_context_data(self, **kwargs):
        """Add comprehensive analytics data."""
        context = super().get_context_data(**kwargs)

        foods_by_availability = Food.objects.values('available').annotate(
            count=Count('id')
        )

        price_ranges = [
            ('$0-$10', Food.objects.filter(price__lt=10).count()),
            ('$10-$20', Food.objects.filter(price__gte=10, price__lt=20).count()),
            ('$20-$30', Food.objects.filter(price__gte=20, price__lt=30).count()),
            ('$30+', Food.objects.filter(price__gte=30).count()),
        ]

        user_stats = User.objects.aggregate(
            total=Count('id'),
            staff_count=Count('id', filter=Q(is_staff=True)),
            active_count=Count('id', filter=Q(is_active=True)),
        )

        context.update({
            'foods_by_availability': list(foods_by_availability),
            'price_ranges': price_ranges,
            'user_stats': user_stats,
        })

        return context


def safe_delete_file(file_field):
    """
    Safely delete a file from the file system.

    Args:
        file_field: Django FileField or ImageField instance

    Returns:
        bool: True if file was deleted successfully, False otherwise
    """
    if not file_field:
        return False

    try:
        if hasattr(file_field, 'path') and file_field.path:
            if os.path.isfile(file_field.path):
                os.remove(file_field.path)
                return True
            else:
                return False
    except (OSError, AttributeError):
        return False

    return False


class FoodListView(ListView):
    model = Food
    template_name = 'food/food_list.html'
    context_object_name = 'foods'


class FoodDetailView(LoginRequiredMixin, DetailView):
    model = Food
    template_name = 'food/food_detail.html'
    context_object_name = 'food'


FOOD_SUCCESS_URL = '/food/'


class FoodCreateView(LoginRequiredMixin, CreateView):
    model = Food
    template_name = 'food/food_form.html'
    fields = ['name', 'description', 'price', 'available', 'image']
    success_url = FOOD_SUCCESS_URL

    def form_valid(self, form):
        """Set the created_by field to the current user."""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FoodUpdateView(LoginRequiredMixin, UpdateView):
    model = Food
    template_name = 'food/food_form.html'
    fields = ['name', 'description', 'price', 'available', 'image']
    success_url = FOOD_SUCCESS_URL

    def get_queryset(self):
        """Allow users to edit only their own foods, or allow staff to edit any."""
        if self.request.user.is_staff:
            return Food.objects.all()
        return Food.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        old_image = None
        if self.object.pk and self.object.image:
            old_image = self.object.image

        response = super().form_valid(form)

        if old_image and self.object.image != old_image:
            safe_delete_file(old_image)

        return response


class FoodDeleteView(LoginRequiredMixin, DeleteView):
    model = Food
    template_name = 'food/food_confirm_delete.html'
    success_url = FOOD_SUCCESS_URL

    def get_queryset(self):
        """Allow users to delete only their own foods, or allow staff to delete any."""
        if self.request.user.is_staff:
            return Food.objects.all()
        return Food.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.image:
            safe_delete_file(obj.image)

        return super().delete(request, *args, **kwargs)
