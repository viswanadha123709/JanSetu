from django.contrib import admin
from apps.schemes.models import State, Category, Organization, Scheme, Policy, EligibilityRule

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'state_code')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'icon')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'organization_type', 'official_website')
    list_filter = ('organization_type',)

class EligibilityRuleInline(admin.TabularInline):
    model = EligibilityRule
    extra = 1

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('scheme_name', 'organization', 'category', 'applicable_state', 'scheme_type', 'last_verified_date', 'is_active')
    list_filter = ('scheme_type', 'applicable_state', 'category')
    search_fields = ('scheme_name', 'description', 'benefits')
    inlines = [EligibilityRuleInline]

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_name', 'organization', 'category', 'policy_type', 'last_verified_date', 'is_active')
    list_filter = ('policy_type', 'category')
    search_fields = ('policy_name', 'description', 'key_exclusions')
    inlines = [EligibilityRuleInline]
