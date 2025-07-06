from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Food model with rich functionality.
    """

    list_display = [
        'name',
        'price',
        'available_status',
        'image_preview',
        'description_preview',
        'created_by_info',
        'created_info'
    ]

    list_filter = [
        'available',
        'price',
        'created_by',
        'created_at',
    ]

    search_fields = [
        'name',
        'description',
        'created_by__username',
        'created_by__email',
    ]

    ordering = ['name']

    fields = [
        'name',
        'description',
        'price',
        'available',
        'image',
        'image_preview_large',
        'created_by',
        'created_at',
        'updated_at'
    ]

    readonly_fields = ['image_preview_large',
                       'created_by', 'created_at', 'updated_at']

    list_per_page = 20

    actions = ['make_available', 'make_unavailable', 'duplicate_food']

    def available_status(self, obj):
        """
        Display availability status with colored badge.

        Args:
            obj: Food instance

        Returns:
            str: HTML formatted availability status
        """
        if obj.available:
            return format_html(
                '<span style="color: white; background-color: #28a745; padding: 3px 8px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">AVAILABLE</span>'
            )
        else:
            return format_html(
                '<span style="color: white; background-color: #dc3545; padding: 3px 8px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">UNAVAILABLE</span>'
            )
    available_status.short_description = 'Status'

    def image_preview(self, obj):
        """
        Display small image preview in list view.

        Args:
            obj: Food instance

        Returns:
            str: HTML formatted image or placeholder
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; '
                'border-radius: 8px; border: 2px solid #dee2e6;" />',
                obj.image.url
            )
        else:
            return format_html(
                '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #ff6b35, #f7931e); '
                'border-radius: 8px; display: flex; align-items: center; justify-content: center; '
                'color: white; font-size: 16px;">📷</div>'
            )
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        """
        Display large image preview in detail form.

        Args:
            obj: Food instance

        Returns:
            str: HTML formatted large image or placeholder
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; object-fit: cover; '
                'border-radius: 12px; border: 3px solid #dee2e6;" />',
                obj.image.url
            )
        else:
            return format_html(
                '<div style="width: 300px; height: 200px; background: linear-gradient(135deg, #ff6b35, #f7931e); '
                'border-radius: 12px; display: flex; align-items: center; justify-content: center; '
                'color: white; font-size: 48px;">📷</div>'
            )
    image_preview_large.short_description = 'Current Image'

    def description_preview(self, obj):
        """
        Display truncated description in list view.

        Args:
            obj: Food instance

        Returns:
            str: Truncated description
        """
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description
    description_preview.short_description = 'Description'

    def created_by_info(self, obj):
        """
        Display user who created the food item.

        Args:
            obj: Food instance

        Returns:
            str: HTML formatted user info
        """
        return format_html(
            '<div style="display: flex; align-items: center;">'
            '<div style="width: 30px; height: 30px; background: linear-gradient(135deg, #667eea, #764ba2); '
            'border-radius: 50%; display: flex; align-items: center; justify-content: center; '
            'color: white; font-weight: bold; margin-right: 8px;">{}</div>'
            '<div><strong>{}</strong><br><small style="color: #6c757d;">{}</small></div>'
            '</div>',
            obj.created_by.username[:1].upper(),
            obj.created_by.username,
            obj.created_at.strftime('%b %d, %Y')
        )
    created_by_info.short_description = 'Created By'

    def created_info(self, obj):
        """
        Display creation information.

        Args:
            obj: Food instance

        Returns:
            str: HTML formatted creation info
        """
        return format_html(
            '<small style="color: #6c757d;">ID: {}</small>',
            obj.id
        )
    created_info.short_description = 'ID'

    def make_available(self, request, queryset):
        """
        Admin action to mark selected foods as available.

        Args:
            request: HTTP request
            queryset: Selected Food objects
        """
        updated = queryset.update(available=True)
        self.message_user(
            request,
            f'{updated} food item(s) marked as available.'
        )
    make_available.short_description = "Mark selected foods as available"

    def make_unavailable(self, request, queryset):
        """
        Admin action to mark selected foods as unavailable.

        Args:
            request: HTTP request
            queryset: Selected Food objects
        """
        updated = queryset.update(available=False)
        self.message_user(
            request,
            f'{updated} food item(s) marked as unavailable.'
        )
    make_unavailable.short_description = "Mark selected foods as unavailable"

    def duplicate_food(self, request, queryset):
        """
        Admin action to duplicate selected food items.

        Args:
            request: HTTP request
            queryset: Selected Food objects
        """
        duplicated_count = 0
        for food in queryset:
            food.pk = None
            food.name = f"{food.name} (Copy)"
            food.save()
            duplicated_count += 1

        self.message_user(
            request,
            f'{duplicated_count} food item(s) duplicated successfully.'
        )
    duplicate_food.short_description = "Duplicate selected foods"

    class Media:
        """
        Add custom CSS for enhanced admin styling.
        """
        css = {
            'all': ('admin/css/custom_food_admin.css',)
        }


admin.site.site_header = "My Food Site Administration"
admin.site.site_title = "Food Admin"
admin.site.index_title = "Welcome to Food Administration"
