from django import forms
from django.forms import inlineformset_factory
from .models import Survey, Question, Choice


class SurveyCreateForm(forms.ModelForm):
    """Kullanıcının kendi anketini oluşturması için form"""
    class Meta:
        model = Survey
        fields = ['title', 'description', 'category', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Anket başlığınızı girin...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Kısa bir açıklama yazın (isteğe bağlı)...',
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'thumbnail': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '🗳️',
                'style': 'font-size:1.5rem; width:80px',
            }),
        }
        labels = {
            'title': 'Anket Başlığı *',
            'description': 'Açıklama',
            'category': 'Kategori',
            'thumbnail': 'Emoji',
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'order']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sorunuzu buraya yazın...',
            }),
            'order': forms.HiddenInput(),
        }
        labels = {'text': 'Soru Metni'}


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'icon', 'order']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seçenek metni...',
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control text-center',
                'placeholder': '✅',
                'style': 'width:60px; font-size:1.2rem',
            }),
            'order': forms.HiddenInput(),
        }
        labels = {'text': '', 'icon': ''}


ChoiceFormSet = inlineformset_factory(
    Question, Choice,
    form=ChoiceForm,
    extra=4,
    min_num=2,
    validate_min=True,
    can_delete=True,
    fields=['text', 'icon', 'order']
)
