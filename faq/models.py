import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from managers import QuestionManager

class Faq(models.Model):
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ's")

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150)
    faq = models.ForeignKey(Faq, verbose_name=_('faq'), related_name='topics')
    position = models.PositiveSmallIntegerField(_('sort order'), default=0, help_text=_('The order you would like the topic to be displayed.'))

    def get_absolute_url(self):
        return '/faq/' + self.slug

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['position', 'name']

    def __unicode__(self):
        return self.name

class Question(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE,    _('Active')),
        (INACTIVE,  _('Inactive')),
        (HEADER,    _('Group Header')),
    )
    
    text = models.TextField(_('question'), help_text=_('The actual question itself.'))
    answer = models.TextField(_('answer'), blank=True, help_text=_('The answer text.'))
    topic = models.ForeignKey(Topic, verbose_name=_('topic'), related_name='questions')
    slug = models.SlugField(_('slug'), max_length=100)
    status = models.IntegerField(_('status'),
        choices=STATUS_CHOICES, default=INACTIVE, 
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed. Questions marked as 'Group Header' are treated "
                    "as such by views and templates that are set up to use them."))
    
    protected = models.BooleanField(_('is protected'), default=False,
        help_text=_("Set true if this question is only visible by authenticated users."))
        
    position = models.PositiveSmallIntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, related_name="+")
    updated_by = models.ForeignKey(User, verbose_name=_('updated by'), null=True, related_name="+")  
    
    objects = QuestionManager()
    
    class Meta:
        verbose_name = _("Frequent asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['position', 'created']


    def __unicode__(self):
        return self.text

    def is_header(self):
        return self.status == Question.HEADER

    def is_active(self):
        return self.status == Question.ACTIVE
