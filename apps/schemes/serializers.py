from rest_framework import serializers
from apps.schemes.models import State, Category, Organization, Scheme, Policy, EligibilityRule

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'state_name', 'state_code']

class CategorySerializer(serializers.ModelSerializer):
    schemes_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'description', 'icon', 'schemes_count']

    def get_schemes_count(self, obj):
        return obj.schemes.count()

class OrganizationSerializer(serializers.ModelSerializer):
    org_type_display = serializers.CharField(source='get_organization_type_display', read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'organization_name', 'organization_type', 'org_type_display', 'official_website']

class EligibilityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityRule
        fields = ['id', 'condition_type', 'condition_description', 'value_criteria']

class SchemeSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.organization_name', read_only=True)
    organization_type = serializers.CharField(source='organization.get_organization_type_display', read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    state_name = serializers.SerializerMethodField()
    state_code = serializers.SerializerMethodField()
    rules = EligibilityRuleSerializer(many=True, read_only=True)

    class Meta:
        model = Scheme
        fields = [
            'id', 'scheme_name', 'description', 'organization', 'organization_name',
            'organization_type', 'category', 'category_name', 'category_icon',
            'applicable_state', 'state_name', 'state_code', 'scheme_type',
            'benefits', 'eligibility_info', 'required_documents', 'application_procedure',
            'official_source_url', 'last_verified_date', 'important_dates', 'is_active', 'rules'
        ]

    def get_state_name(self, obj):
        return obj.applicable_state.state_name if obj.applicable_state else 'All India (Central)'

    def get_state_code(self, obj):
        return obj.applicable_state.state_code if obj.applicable_state else 'IN'

class PolicySerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.organization_name', read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    state_name = serializers.SerializerMethodField()
    rules = EligibilityRuleSerializer(many=True, read_only=True)

    class Meta:
        model = Policy
        fields = [
            'id', 'policy_name', 'description', 'organization', 'organization_name',
            'category', 'category_name', 'applicable_state', 'state_name', 'policy_type',
            'benefits', 'eligibility_info', 'terms_conditions_summary', 'key_exclusions',
            'official_source_url', 'last_verified_date', 'is_active', 'rules'
        ]

    def get_state_name(self, obj):
        return obj.applicable_state.state_name if obj.applicable_state else 'All India'
