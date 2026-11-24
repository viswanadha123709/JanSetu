from django.contrib import admin
from apps.documents.models import UploadedDocument, ExtractedClause, DocumentAnalysis

class ExtractedClauseInline(admin.TabularInline):
    model = ExtractedClause
    extra = 0
    readonly_fields = ('page_number', 'clause_category', 'importance_level', 'font_size', 'is_small_font', 'document_position', 'original_text')

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'user', 'page_count', 'processing_status', 'upload_date')
    list_filter = ('processing_status', 'upload_date')
    search_fields = ('file_name',)
    inlines = [ExtractedClauseInline]

@admin.register(ExtractedClause)
class ExtractedClauseAdmin(admin.ModelAdmin):
    list_display = ('uploaded_document', 'page_number', 'clause_category', 'importance_level', 'is_small_font', 'document_position')
    list_filter = ('importance_level', 'is_small_font', 'document_position', 'clause_category')
    search_fields = ('original_text', 'ai_explanation', 'clause_category')

@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('uploaded_document', 'total_pages_analysed', 'total_conditions_detected', 'high_risk_count', 'small_font_count', 'analysis_date')
