from django.contrib import admin


class ModelAdminCustom(admin.ModelAdmin):
    list_per_page = 12

    def __init__(self, *args, **kwargs):
        super(ModelAdminCustom, self).__init__(*args, **kwargs)
        self.exclude = ['created_at', 'created_by', 'updated_at', 'updated_by']