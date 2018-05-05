from django.contrib import admin

from .models import SiteDetail, SiteArticle


class SiteDetailAdmin(admin.ModelAdmin):
    model = SiteDetail
    list_display = ('company_name', 'logo', 'support_email', 'jobs_email', 'info_email')


class SiteArticleAdmin(admin.ModelAdmin):
    model = SiteArticle


admin.site.register(SiteDetail, SiteDetailAdmin)
admin.site.register(SiteArticle, SiteArticleAdmin)
