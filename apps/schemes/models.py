from django.db import models

class State(models.Model):
    state_name = models.CharField(max_length=100, unique=True)
    state_code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['state_name']

    def __str__(self):
        return f"{self.state_name} ({self.state_code})"


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=50, default='layers', help_text='Lucide icon name')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['category_name']

    def __str__(self):
        return self.category_name


class Organization(models.Model):
    ORG_TYPE_CHOICES = [
        ('central', 'Central Government'),
        ('state', 'State Government'),
        ('public', 'Public-Sector Organization'),
        ('private', 'Private Company / Institution'),
    ]

    organization_name = models.CharField(max_length=200, unique=True)
    organization_type = models.CharField(max_length=50, choices=ORG_TYPE_CHOICES, default='central')
    official_website = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['organization_name']

    def __str__(self):
        return f"{self.organization_name} ({self.get_organization_type_display()})"


class Scheme(models.Model):
    SCHEME_TYPE_CHOICES = [
        ('Central', 'Central Government Scheme'),
        ('State', 'State Government Scheme'),
        ('Public', 'Public-Sector Scheme'),
        ('Private', 'Private Offering'),
    ]

    scheme_name = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='schemes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='schemes')
    applicable_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='schemes', help_text='Null if All-India / Central')
    scheme_type = models.CharField(max_length=50, choices=SCHEME_TYPE_CHOICES, default='Central')
    
    benefits = models.TextField(help_text='Detailed benefits provided by the scheme')
    eligibility_info = models.TextField(help_text='Who is eligible to apply')
    required_documents = models.TextField(help_text='Documents required for application')
    application_procedure = models.TextField(help_text='Step-by-step application process')
    official_source_url = models.URLField(max_length=500, help_text='Official portal link')
    last_verified_date = models.DateField(auto_now=True)
    important_dates = models.CharField(max_length=255, blank=True, default='Ongoing / Annual cycle')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheme_name']

    def __str__(self):
        state_str = self.applicable_state.state_code if self.applicable_state else 'Central'
        return f"[{state_str}] {self.scheme_name}"


class Policy(models.Model):
    POLICY_TYPE_CHOICES = [
        ('insurance', 'Insurance Policy'),
        ('loan', 'Education / Business Loan'),
        ('investment', 'Savings / Pension Policy'),
        ('other', 'Other Policy / Benefit'),
    ]

    policy_name = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='policies')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='policies')
    applicable_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='policies')
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPE_CHOICES, default='insurance')
    
    benefits = models.TextField(help_text='Key benefits and coverage details')
    eligibility_info = models.TextField(help_text='Eligibility requirements')
    terms_conditions_summary = models.TextField(help_text='Key terms, lock-in, renewal rules')
    key_exclusions = models.TextField(help_text='What is NOT covered or excluded')
    official_source_url = models.URLField(max_length=500)
    last_verified_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Policies'
        ordering = ['policy_name']

    def __str__(self):
        return f"{self.policy_name} ({self.organization.organization_name})"


class EligibilityRule(models.Model):
    CONDITION_TYPE_CHOICES = [
        ('min_age', 'Minimum Age'),
        ('max_age', 'Maximum Age'),
        ('max_income', 'Maximum Annual Income'),
        ('min_income', 'Minimum Annual Income'),
        ('occupation', 'Occupation / Profession'),
        ('state', 'State Residency'),
        ('gender', 'Gender Specific'),
        ('category', 'Social / Educational Category'),
        ('landholding', 'Landholding Size'),
        ('other', 'Other Condition'),
    ]

    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True, blank=True, related_name='rules')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True, blank=True, related_name='rules')
    condition_type = models.CharField(max_length=50, choices=CONDITION_TYPE_CHOICES)
    condition_description = models.CharField(max_length=255)
    value_criteria = models.CharField(max_length=255, help_text='Evaluation criterion, e.g. "farmer", "<=250000", ">=18"')

    def __str__(self):
        target = self.scheme.scheme_name if self.scheme else (self.policy.policy_name if self.policy else 'Generic')
        return f"{target} -> {self.condition_type}: {self.condition_description}"
