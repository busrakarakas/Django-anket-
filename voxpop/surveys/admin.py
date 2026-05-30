from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Survey, Question, Choice, Vote

admin.site.site_header = '🗳️ AnketApp Yönetim Paneli'
admin.site.site_title = 'AnketApp'
admin.site.index_title = 'Anket Yönetim Merkezi'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ['order', 'icon', 'text', 'votes']
    readonly_fields = ['votes']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'survey_type', 'category', 'status_badge',
                    'created_by', 'total_votes_display', 'created_at']
    list_filter = ['survey_type', 'status', 'category', 'is_featured']
    search_fields = ['title']
    inlines = [QuestionInline]
    actions = ['make_active', 'make_closed']

    def status_badge(self, obj):
        colors = {'active': '#28a745', 'draft': '#ffc107', 'closed': '#dc3545'}
        labels = {'active': '✅ Aktif', 'draft': '📝 Taslak', 'closed': '🔒 Kapalı'}
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:10px;font-size:11px">{}</span>',
            colors.get(obj.status, '#999'), labels.get(obj.status, obj.status)
        )
    status_badge.short_description = 'Durum'

    def total_votes_display(self, obj):
        return format_html('🗳️ <b>{}</b>', obj.total_votes())
    total_votes_display.short_description = 'Oy'

    @admin.action(description='✅ Aktif Yap')
    def make_active(self, request, queryset):
        queryset.update(status='active')

    @admin.action(description='🔒 Kapat')
    def make_closed(self, request, queryset):
        queryset.update(status='closed')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'survey', 'order']
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'votes']
    readonly_fields = ['votes']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['choice', 'question', 'voted_at']
    readonly_fields = ['question', 'choice', 'session_key', 'ip_address', 'voted_at']
    def has_add_permission(self, request): return False
