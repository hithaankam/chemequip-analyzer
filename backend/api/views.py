from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import io
import os
from analysis.orchestrator import analyze_equipment_data
from .models import DatasetUpload

@method_decorator(csrf_exempt, name='dispatch')
class EquipmentAnalysisView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            uploaded_file = request.FILES['file']
            
            if not uploaded_file.name.endswith('.csv'):
                return Response(
                    {'error': 'File must be a CSV'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            file_content = uploaded_file.read()
            file_obj = io.StringIO(file_content.decode('utf-8'))
            
            analysis_results = analyze_equipment_data(file_obj)
            
            dataset_record = DatasetUpload.objects.create(
                user=request.user,
                filename=uploaded_file.name,
                file_size=uploaded_file.size,
                equipment_count=analysis_results['dataset_info']['cleaned_size'],
                summary_data=analysis_results
            )
            
            DatasetUpload.cleanup_old_records_for_user(request.user)
            
            response_data = {
                'upload_id': dataset_record.id,
                'analysis_results': analysis_results
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DatasetHistoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user_datasets = DatasetUpload.objects.filter(user=request.user)[:5]
            history_data = []
            
            for dataset in user_datasets:
                summary_stats = dataset.get_summary_stats()
                history_data.append({
                    'id': dataset.id,
                    'filename': dataset.filename,
                    'upload_date': dataset.upload_date.isoformat(),
                    'file_size': dataset.file_size,
                    'equipment_count': dataset.equipment_count,
                    'summary_stats': summary_stats
                })
            
            return Response({
                'count': len(history_data),
                'datasets': history_data,
                'user': request.user.username
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': 'Failed to retrieve history'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DatasetDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, dataset_id):
        try:
            dataset = DatasetUpload.objects.get(id=dataset_id, user=request.user)
            return Response({
                'id': dataset.id,
                'filename': dataset.filename,
                'upload_date': dataset.upload_date.isoformat(),
                'file_size': dataset.file_size,
                'equipment_count': dataset.equipment_count,
                'analysis_results': dataset.summary_data
            }, status=status.HTTP_200_OK)
            
        except DatasetUpload.DoesNotExist:
            return Response(
                {'error': 'Dataset not found or access denied'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to retrieve dataset'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
class AuthLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

@method_decorator(csrf_exempt, name='dispatch')
class AuthRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
