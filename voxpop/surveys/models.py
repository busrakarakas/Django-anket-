import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Kategori', max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField('İkon', max_length=10, default='📊')
    description = models.TextField('Açıklama', blank=True)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['name']

    def __str__(self):
        return f"{self.icon} {self.name}"


class Survey(models.Model):
    TYPE_CHOICES = [
        ('hazir', '📋 Hazır Anket'),
        ('ozel', '✏️ Özel Anket'),
    ]
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('closed', 'Kapalı'),
        ('draft', 'Taslak'),
    ]

    title = models.CharField('Başlık', max_length=200)
    description = models.TextField('Açıklama', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='surveys')
    survey_type = models.CharField('Tür', max_length=10, choices=TYPE_CHOICES, default='ozel')
    status = models.CharField('Durum', max_length=10, choices=STATUS_CHOICES, default='active')
    thumbnail = models.CharField('Emoji', max_length=10, default='🗳️')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='surveys')
    created_at = models.DateTimeField('Oluşturulma', auto_now_add=True)
    updated_at = models.DateTimeField('Güncelleme', auto_now=True)
    is_featured = models.BooleanField('Öne Çıkar', default=False)

    class Meta:
        verbose_name = 'Anket'
        verbose_name_plural = 'Anketler'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def is_active(self):
        return self.status == 'active'

    def total_votes(self):
        return Vote.objects.filter(question__survey=self).count()

    def question_count(self):
        return self.questions.count()

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.created_at <= now

    was_created_recently.boolean = True
    was_created_recently.short_description = 'Son 7 günde?'


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Soru', max_length=400)
    order = models.PositiveIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Soru'
        verbose_name_plural = 'Sorular'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text[:60]

    def total_votes(self):
        return Vote.objects.filter(question=self).count()

    def winner_choice(self):
        return self.choices.order_by('-votes').first()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField('Seçenek', max_length=200)
    icon = models.CharField('İkon', max_length=10, blank=True)
    votes = models.IntegerField('Oy', default=0)
    order = models.PositiveIntegerField('Sıra', default=0)

    class Meta:
        verbose_name = 'Seçenek'
        verbose_name_plural = 'Seçenekler'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.icon} {self.text}".strip()

    def vote_percentage(self):
        total = self.question.total_votes()
        if total == 0:
            return 0
        return round((self.votes / total) * 100, 1)


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='vote_records')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='vote_records')
    session_key = models.CharField('Oturum', max_length=40)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Oy'
        verbose_name_plural = 'Oylar'
        unique_together = [['question', 'session_key']]

    def __str__(self):
        return f"{self.session_key[:8]}→{self.choice}"
