from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from apps.eligibility.models import Conversation
from apps.eligibility.ai_engine import EligibilityAdvisor

class ChatAdvisorView(APIView):
    def post(self, request):
        question = request.data.get('question', '').strip()
        if not question:
            return Response({'error': 'Please provide a question or requirement.'}, status=status.HTTP_400_BAD_REQUEST)

        session_id = request.data.get('session_id') or str(uuid.uuid4())
        language = request.data.get('language', 'en')
        
        user_profile = None
        user = request.user if request.user.is_authenticated else None
        if user and hasattr(user, 'profile'):
            user_profile = user.profile

        # Evaluate eligibility via AI advisor
        answer = EligibilityAdvisor.evaluate_eligibility(
            query_text=question,
            user_profile=user_profile,
            language=language
        )

        conv = Conversation.objects.create(
            user=user,
            session_id=session_id,
            question=question,
            answer=answer,
            language=language,
        )

        return Response({
            'session_id': session_id,
            'question': question,
            'answer': answer,
            'language': language,
            'timestamp': conv.timestamp.isoformat()
        })

class ConversationHistoryView(APIView):
    def get(self, request):
        session_id = request.query_params.get('session_id')
        user = request.user if request.user.is_authenticated else None

        qs = Conversation.objects.none()
        if user:
            qs = Conversation.objects.filter(user=user)
        elif session_id:
            qs = Conversation.objects.filter(session_id=session_id)

        history = [
            {
                'id': c.id,
                'question': c.question,
                'answer': c.answer,
                'language': c.language,
                'timestamp': c.timestamp.isoformat(),
            }
            for c in qs.order_by('timestamp')
        ]
        return Response(history)
