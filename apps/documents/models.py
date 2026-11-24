from django.db import models
from django.contrib.auth.models import User

class UploadedDocument(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Analysis'),
        ('processing', 'Processing Document'),
        ('completed', 'Analysis Completed'),
        ('failed', 'Analysis Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_documents')
    original_file = models.FileField(upload_to='uploads/%Y/%m/')
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(default=0, help_text='File size in bytes')
    page_count = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    processing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.file_name} ({self.get_processing_status_display()})"


class ExtractedClause(models.Model):
    IMPORTANCE_CHOICES = [
        ('High', 'High Review Priority'),
        ('Medium', 'Medium Review Priority'),
        ('Informational', 'Informational Notice'),
    ]

    POSITION_CHOICES = [
        ('top', 'Top of Page / Early Section'),
        ('middle', 'Middle Page / Dense Section'),
        ('final_pages', 'Final Pages / Back Matter'),
        ('footnote', 'Footnote / Bottom Margin'),
        ('table', 'Embedded Table / Fine Column'),
        ('appendix', 'Appendix / Annexure'),
    ]

    uploaded_document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='clauses')
    original_text = models.TextField(help_text='Exact verbatim clause extracted from the PDF')
    page_number = models.PositiveIntegerField(help_text='Exact 1-based page number')
    section_heading = models.CharField(max_length=255, blank=True, default='')
    clause_category = models.CharField(max_length=100, help_text='e.g. Additional Charges, Cancellation Penalty, Exclusions')
    
    font_size = models.FloatField(null=True, blank=True, help_text='Font size in points')
    body_font_size = models.FloatField(null=True, blank=True, help_text='Average body font size of document')
    is_small_font = models.BooleanField(default=False, help_text='True if font is unusually small (< 80% of body text)')
    
    document_position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='middle')
    importance_level = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='Medium')
    
    ai_explanation = models.TextField(help_text='Plain-language simplified explanation')
    te_explanation = models.TextField(blank=True, default='', help_text='Telugu simplified explanation')
    why_it_matters = models.TextField(help_text='Why this condition is important to the user')
    suggested_action = models.TextField(help_text='Question to ask the provider or checklist step before signing')
    confidence_score = models.FloatField(default=0.90)

    class Meta:
        ordering = ['page_number', '-importance_level']

    def __str__(self):
        return f"P.{self.page_number} [{self.importance_level}] {self.clause_category}"


class DocumentAnalysis(models.Model):
    uploaded_document = models.OneToOneField(UploadedDocument, on_delete=models.CASCADE, related_name='analysis')
    overall_summary = models.TextField(help_text='Comprehensive plain English summary of the entire document')
    overall_summary_te = models.TextField(blank=True, default='', help_text='Comprehensive Telugu summary')
    
    total_pages_analysed = models.PositiveIntegerField(default=0)
    total_conditions_detected = models.PositiveIntegerField(default=0)
    small_font_count = models.PositiveIntegerField(default=0)
    later_pages_count = models.PositiveIntegerField(default=0)
    
    high_risk_count = models.PositiveIntegerField(default=0)
    medium_risk_count = models.PositiveIntegerField(default=0)
    info_risk_count = models.PositiveIntegerField(default=0)
    
    difficult_terms = models.JSONField(default=list, blank=True, help_text='List of simplified jargon terms [{"term": "...", "simple": "...", "te": "..."}]')
    eligibility_summary = models.TextField(blank=True, default='')
    required_docs_summary = models.TextField(blank=True, default='')
    benefits_limitations_summary = models.TextField(blank=True, default='')
    
    analysis_status = models.CharField(max_length=20, default='completed')
    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis of {self.uploaded_document.file_name} ({self.total_conditions_detected} clauses found)"
