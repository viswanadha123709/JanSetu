from rest_framework import serializers
from apps.documents.models import UploadedDocument, ExtractedClause, DocumentAnalysis

class ExtractedClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedClause
        fields = [
            'id', 'page_number', 'section_heading', 'clause_category',
            'original_text', 'font_size', 'body_font_size', 'is_small_font',
            'document_position', 'importance_level', 'ai_explanation',
            'te_explanation', 'why_it_matters', 'suggested_action', 'confidence_score'
        ]

class DocumentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAnalysis
        fields = [
            'id', 'overall_summary', 'overall_summary_te', 'total_pages_analysed',
            'total_conditions_detected', 'small_font_count', 'later_pages_count',
            'high_risk_count', 'medium_risk_count', 'info_risk_count',
            'difficult_terms', 'eligibility_summary', 'required_docs_summary',
            'benefits_limitations_summary', 'analysis_status', 'analysis_date'
        ]

class UploadedDocumentSerializer(serializers.ModelSerializer):
    analysis = DocumentAnalysisSerializer(read_only=True)
    clauses_count = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedDocument
        fields = [
            'id', 'file_name', 'file_size', 'page_count', 'upload_date',
            'processing_status', 'error_message', 'file_url', 'analysis', 'clauses_count'
        ]

    def get_clauses_count(self, obj):
        return obj.clauses.count()

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.original_file:
            if request:
                return request.build_absolute_uri(obj.original_file.url)
            return obj.original_file.url
        return ''
