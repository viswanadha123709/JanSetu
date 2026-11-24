from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import os
import shutil
from django.conf import settings
from apps.documents.models import UploadedDocument, ExtractedClause, DocumentAnalysis
from apps.documents.serializers import UploadedDocumentSerializer, ExtractedClauseSerializer
from apps.documents.analyzer import DocumentAnalyzer, DocumentQAService

class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file uploaded. Please upload a PDF document.'}, status=status.HTTP_400_BAD_REQUEST)

        if not file_obj.name.lower().endswith('.pdf'):
            return Response({'error': 'Invalid file format. Please upload a PDF file.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user if request.user.is_authenticated else None

        doc = UploadedDocument.objects.create(
            user=user,
            original_file=file_obj,
            file_name=file_obj.name,
            file_size=file_obj.size,
            processing_status='pending'
        )

        # Trigger analysis
        analyzer = DocumentAnalyzer(doc.id)
        analyzer.analyze()
        doc.refresh_from_db()

        serializer = UploadedDocumentSerializer(doc, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DocumentSampleLoadView(APIView):
    def post(self, request):
        sample_type = request.data.get('sample_type', 'health')
        user = request.user if request.user.is_authenticated else None

        if sample_type == 'loan':
            sample_rel = 'sample_docs/Sample_Loan_Agreement.pdf'
            name = 'Sample_Personal_Loan_Agreement.pdf'
        else:
            sample_rel = 'sample_docs/Sample_Health_Insurance_Policy.pdf'
            name = 'Sample_Health_Insurance_Policy.pdf'

        source_abs = os.path.join(settings.BASE_DIR, sample_rel)
        if not os.path.exists(source_abs):
            return Response({'error': 'Sample file not found on server.'}, status=status.HTTP_404_NOT_FOUND)

        dest_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'samples')
        os.makedirs(dest_dir, exist_ok=True)
        dest_abs = os.path.join(dest_dir, name)
        shutil.copyfile(source_abs, dest_abs)

        rel_media_path = os.path.join('uploads', 'samples', name).replace('\\', '/')

        doc = UploadedDocument.objects.create(
            user=user,
            original_file=rel_media_path,
            file_name=name,
            file_size=os.path.getsize(dest_abs),
            processing_status='pending'
        )

        analyzer = DocumentAnalyzer(doc.id)
        analyzer.analyze()
        doc.refresh_from_db()

        serializer = UploadedDocumentSerializer(doc, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DocumentDetailView(APIView):
    def get(self, request, pk):
        try:
            doc = UploadedDocument.objects.select_related('analysis').get(pk=pk)
            serializer = UploadedDocumentSerializer(doc, context={'request': request})
            return Response(serializer.data)
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

class DocumentClausesView(APIView):
    def get(self, request, pk):
        try:
            doc = UploadedDocument.objects.get(pk=pk)
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

        qs = doc.clauses.all()

        level = request.query_params.get('level')
        if level:
            qs = qs.filter(importance_level__iexact=level)

        is_small = request.query_params.get('is_small')
        if is_small is not None:
            qs = qs.filter(is_small_font=(is_small.lower() == 'true'))

        pos = request.query_params.get('position')
        if pos:
            qs = qs.filter(document_position__iexact=pos)

        category = request.query_params.get('category')
        if category:
            qs = qs.filter(clause_category__icontains=category)

        serializer = ExtractedClauseSerializer(qs, many=True)
        return Response(serializer.data)

class DocumentQAView(APIView):
    def post(self, request, pk):
        try:
            doc = UploadedDocument.objects.get(pk=pk)
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

        question = request.data.get('question', '').strip()
        language = request.data.get('language', 'en')
        if not question:
            return Response({'error': 'Please provide a question.'}, status=status.HTTP_400_BAD_REQUEST)

        result = DocumentQAService.answer_question(doc, question, language=language)
        return Response(result)

class DocumentListView(APIView):
    def get(self, request):
        qs = UploadedDocument.objects.all().select_related('analysis')[:20]
        serializer = UploadedDocumentSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
