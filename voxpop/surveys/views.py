from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib.auth.models import User

from .models import Survey, Question, Choice, Vote, Category
from .forms import SurveyCreateForm

EMOJI_LIST = ['🗳️','💻','📱','🔐','🌐','📊','🤖','☁️','🔧','📡','🎯','🧠','💡','🔬','📚','🎮','⚙️','🚀','🔒','💾']
QUICK_ICONS = ['✅','❌','⭐','🔥','💡','🤔','👍','👎','🟢','🟡','🔴','🟣','🔵','⚡','🏆','📊','💻','🌐','🔐','☁️','🤖','📱']


class IndexView(generic.TemplateView):
    template_name = 'surveys/index.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['hazir_surveys'] = Survey.objects.filter(status='active', survey_type='hazir').select_related('category')[:6]
        ctx['ozel_surveys'] = Survey.objects.filter(status='active', survey_type='ozel').select_related('category','created_by')[:6]
        ctx['categories'] = Category.objects.annotate(sc=Count('surveys', filter=Q(surveys__status='active')))
        ctx['total_surveys'] = Survey.objects.filter(status='active').count()
        ctx['total_votes'] = Vote.objects.count()
        ctx['total_users'] = Survey.objects.filter(survey_type='ozel', status='active').values('created_by').distinct().count()
        return ctx


class SurveyListView(generic.ListView):
    model = Survey
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'
    paginate_by = 12
    def get_queryset(self):
        qs = Survey.objects.filter(status='active').select_related('category','created_by')
        tip = self.request.GET.get('tip','')
        if tip in ['hazir','ozel']: qs = qs.filter(survey_type=tip)
        cat = self.request.GET.get('kategori','')
        if cat: qs = qs.filter(category__slug=cat)
        ara = self.request.GET.get('ara','')
        if ara: qs = qs.filter(Q(title__icontains=ara)|Q(description__icontains=ara))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['search_query'] = self.request.GET.get('ara','')
        ctx['tip'] = self.request.GET.get('tip','')
        ctx['kategori'] = self.request.GET.get('kategori','')
        return ctx


class SurveyDetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'
    def get_queryset(self):
        return Survey.objects.filter(status__in=['active','closed']).prefetch_related('questions__choices')
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        survey = self.object
        session_key = self.request.session.session_key
        voted_questions = set()
        if session_key:
            voted_questions = set(Vote.objects.filter(question__survey=survey, session_key=session_key).values_list('question_id', flat=True))
        ctx['voted_questions'] = voted_questions
        ctx['is_active'] = survey.is_active()
        ctx['total_votes'] = survey.total_votes()
        ctx['all_voted'] = len(voted_questions) == survey.question_count() and survey.question_count() > 0
        return ctx


class ResultsView(generic.DetailView):
    model = Survey
    template_name = 'surveys/results.html'
    context_object_name = 'survey'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        questions_data = []
        for q in self.object.questions.prefetch_related('choices'):
            total = q.total_votes()
            choices_data = [{'choice': c, 'percentage': c.vote_percentage()} for c in q.choices.all()]
            questions_data.append({'question': q, 'total': total, 'choices': choices_data, 'winner': q.winner_choice() if total > 0 else None})
        ctx['questions_data'] = questions_data
        ctx['survey_total'] = self.object.total_votes()
        return ctx


def vote(request, survey_pk, question_pk):
    survey = get_object_or_404(Survey, pk=survey_pk, status='active')
    question = get_object_or_404(Question, pk=question_pk, survey=survey)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    if Vote.objects.filter(question=question, session_key=session_key).exists():
        messages.warning(request, '⚠️ Bu soruya zaten oy verdiniz!')
        return redirect('surveys:survey_detail', pk=survey_pk)
    if request.method != 'POST':
        return redirect('surveys:survey_detail', pk=survey_pk)
    choice_id = request.POST.get('choice')
    if not choice_id:
        messages.error(request, '❌ Lütfen bir seçenek seçin.')
        return redirect('surveys:survey_detail', pk=survey_pk)
    try:
        choice = question.choices.get(pk=choice_id)
    except Choice.DoesNotExist:
        messages.error(request, '❌ Geçersiz seçenek.')
        return redirect('surveys:survey_detail', pk=survey_pk)
    choice.votes += 1
    choice.save()
    Vote.objects.create(question=question, choice=choice, session_key=session_key, ip_address=request.META.get('REMOTE_ADDR'))
    messages.success(request, f'✅ Oyunuz kaydedildi: <strong>{choice}</strong>')
    questions = list(survey.questions.order_by('order','id'))
    idx = next((i for i, q in enumerate(questions) if q.pk == question_pk), -1)
    if idx == len(questions) - 1:
        messages.info(request, '🎉 Anketi tamamladınız!')
        return redirect('surveys:results', pk=survey_pk)
    return redirect('surveys:survey_detail', pk=survey_pk)


@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyCreateForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.survey_type = 'ozel'
            survey.status = 'draft'
            survey.save()
            messages.success(request, '✅ Anket oluşturuldu! Sorularınızı ekleyin.')
            return redirect('surveys:add_question', pk=survey.pk)
    else:
        form = SurveyCreateForm()
    return render(request, 'surveys/create_survey.html', {'form': form, 'emoji_list': EMOJI_LIST})


@login_required
def add_question(request, pk):
    survey = get_object_or_404(Survey, pk=pk, created_by=request.user)
    questions = survey.questions.prefetch_related('choices').all()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_question':
            q_text = request.POST.get('question_text','').strip()
            if q_text:
                order = survey.questions.count() + 1
                q = Question.objects.create(survey=survey, text=q_text, order=order)
                for i in range(1, 7):
                    c_text = request.POST.get(f'choice_{i}','').strip()
                    c_icon = request.POST.get(f'icon_{i}','').strip()
                    if c_text:
                        Choice.objects.create(question=q, text=c_text, icon=c_icon, order=i)
                messages.success(request, f'✅ Soru eklendi!')
            else:
                messages.error(request, '❌ Soru metni boş olamaz.')
        elif action == 'delete_question':
            Question.objects.filter(pk=request.POST.get('question_id'), survey=survey).delete()
            messages.info(request, '🗑️ Soru silindi.')
        elif action == 'publish':
            if survey.questions.count() == 0:
                messages.error(request, '❌ En az bir soru ekleyin.')
            else:
                survey.status = 'active'
                survey.save()
                messages.success(request, '🚀 Anketiniz yayınlandı!')
                return redirect('surveys:survey_detail', pk=survey.pk)
        elif action == 'delete_survey':
            survey.delete()
            messages.info(request, '🗑️ Anket silindi.')
            return redirect('surveys:my_surveys')
        return redirect('surveys:add_question', pk=survey.pk)
    return render(request, 'surveys/add_question.html', {'survey': survey, 'questions': questions, 'quick_icons': QUICK_ICONS})


@login_required
def my_surveys(request):
    surveys = Survey.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'surveys/my_surveys.html', {'surveys': surveys})


@login_required
def delete_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk, created_by=request.user)
    if request.method == 'POST':
        survey.delete()
        messages.success(request, '🗑️ Anket silindi.')
    return redirect('surveys:my_surveys')
