from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from apps.schemes.models import State, Category, Organization, Scheme, Policy
from apps.schemes.serializers import StateSerializer, CategorySerializer, OrganizationSerializer, SchemeSerializer, PolicySerializer

class SchemeListView(APIView):
    def get(self, request):
        qs = Scheme.objects.filter(is_active=True).select_related('organization', 'category', 'applicable_state').prefetch_related('rules')
        
        # State filter
        state_code = request.query_params.get('state')
        if state_code:
            if state_code == 'CENTRAL' or state_code == 'IN':
                qs = qs.filter(applicable_state__isnull=True)
            else:
                qs = qs.filter(Q(applicable_state__state_code=state_code) | Q(applicable_state__isnull=True))

        # Category filter
        category_name = request.query_params.get('category')
        if category_name:
            qs = qs.filter(category__category_name__iexact=category_name)

        # Organization / Scheme type filter
        scheme_type = request.query_params.get('type')
        if scheme_type:
            qs = qs.filter(scheme_type__iexact=scheme_type)

        # Search query
        q = request.query_params.get('q')
        if q:
            qs = qs.filter(
                Q(scheme_name__icontains=q) |
                Q(description__icontains=q) |
                Q(benefits__icontains=q) |
                Q(eligibility_info__icontains=q) |
                Q(organization__organization_name__icontains=q)
            )

        serializer = SchemeSerializer(qs, many=True)
        return Response(serializer.data)

class SchemeDetailView(APIView):
    def get(self, request, pk):
        try:
            scheme = Scheme.objects.select_related('organization', 'category', 'applicable_state').prefetch_related('rules').get(pk=pk)
            return Response(SchemeSerializer(scheme).data)
        except Scheme.DoesNotExist:
            return Response({'error': 'Scheme not found'}, status=status.HTTP_404_NOT_FOUND)

class PolicyListView(APIView):
    def get(self, request):
        qs = Policy.objects.filter(is_active=True).select_related('organization', 'category', 'applicable_state').prefetch_related('rules')
        
        category_name = request.query_params.get('category')
        if category_name:
            qs = qs.filter(category__category_name__iexact=category_name)

        policy_type = request.query_params.get('type')
        if policy_type:
            qs = qs.filter(policy_type__iexact=policy_type)

        q = request.query_params.get('q')
        if q:
            qs = qs.filter(
                Q(policy_name__icontains=q) |
                Q(description__icontains=q) |
                Q(benefits__icontains=q) |
                Q(key_exclusions__icontains=q)
            )

        serializer = PolicySerializer(qs, many=True)
        return Response(serializer.data)

class PolicyDetailView(APIView):
    def get(self, request, pk):
        try:
            policy = Policy.objects.select_related('organization', 'category', 'applicable_state').prefetch_related('rules').get(pk=pk)
            return Response(PolicySerializer(policy).data)
        except Policy.DoesNotExist:
            return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)

class CategoryListView(APIView):
    def get(self, request):
        cats = Category.objects.all()
        return Response(CategorySerializer(cats, many=True).data)

class StateListView(APIView):
    def get(self, request):
        states = State.objects.all()
        return Response(StateSerializer(states, many=True).data)

class StatsView(APIView):
    def get(self, request):
        return Response({
            "total_schemes": Scheme.objects.filter(is_active=True).count(),
            "total_policies": Policy.objects.filter(is_active=True).count(),
            "total_categories": Category.objects.count(),
            "states_supported": State.objects.count(),
            "ap_schemes_count": Scheme.objects.filter(applicable_state__state_code='AP').count(),
            "ts_schemes_count": Scheme.objects.filter(applicable_state__state_code='TS').count(),
            "central_schemes_count": Scheme.objects.filter(applicable_state__isnull=True).count(),
        })
