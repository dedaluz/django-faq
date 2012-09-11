from django.contrib import admin
from models import Question, Topic, Faq

class QuestionInlineAdmin(admin.TabularInline):
    model = Question
    fields = ('text', 'position', 'status', )
    # define the sortable
    sortable_field_name = "position"
    extra = 0

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name",)} 
    
    inlines = [QuestionInlineAdmin]

class TopicInlineAdmin(admin.TabularInline):
    model = Topic
    fields = ('name', 'position', )
    # define the sortable
    sortable_field_name = "position"
    extra = 0

class FaqAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name",)} 
    
    inlines = [TopicInlineAdmin]
    
class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("text",)} 

    def save_model(self, request, obj, form, change): 
        '''
        Update created-by / modified-by fields.
        
        The date fields are upadated at the model layer, but that's not got
        access to the user.
        '''
        # If the object's new update the created_by field.
        if not change:
            obj.created_by = request.user
        
        # Either way update the updated_by field.
        obj.updated_by = request.user

        # Let the superclass do the final saving.
        return super(QuestionAdmin, self).save_model(request, obj, form, change)

admin.site.register(Faq, FaqAdmin)
admin.site.register(Topic, TopicAdmin)        
admin.site.register(Question, QuestionAdmin)

