from django.contrib import admin
from .models import Proposal, ProposalData, ProposalConfig


class ProposalDataInline(admin.TabularInline):
    model = ProposalData
    extra = 0
    readonly_fields = ('value',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProposalAdmin(admin.ModelAdmin):
    inlines = [ProposalDataInline]
    list_display = ('id', 'status', 'human_analysis')
    list_filter = ('status', 'human_analysis')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.human_analysis:
            readonly_fields = tuple()
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj and obj.human_analysis:
            return False
        return super().has_delete_permission(request, obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if (
            form.instance.status == 'Aprovado'
            or form.instance.status == 'Negada'
        ):
            form.instance.human_analysis = False
            form.instance.save()

    def save_model(self, request, obj, form, change):
        if (
            obj.status == 'Negada' or obj.status == 'Aprovada'
        ):
            obj.human_analysis = False
        super().save_model(request, obj, form, change)


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalData)
admin.site.register(ProposalConfig)
