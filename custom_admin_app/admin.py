from datetime import date

from django.contrib import admin
from django.template.defaulttags import url

from custom_admin_app.models import Messages


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    change_list_template = "chat/index.html"
    # change_form_template = "chat/index.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['test'] = "Hello world"
        return super(MessagesAdmin, self).changelist_view(request, extra_context)

