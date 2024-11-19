from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework import serializers

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from .models import MCQuestion, MCQAnswer, Question, Answer, FillQuestions, FillAnswers, Feedback, CheckStatement, TrueFalse,UploadedImage, Folder,File,Tag
from .serializers import (
    CheckStatementOnlySerializer, MCQuestionSerializer, MCQAnswerSerializer,
    QuestionSerializer, AnswerSerializer,
    MCQuestionOnlySerializer, MCQAnswerOnlySerializer,
    AnswersOnlySerializer, QuestionsOnlySerializer,
    FillQuestionsSerializer, FillAnswersSerializer,
    FillQuestionOnlySerializer, FillAnswerOnlySerializer,
    CheckStatementSerializer, TrueFalseOnlySerializer, TrueFalseSerializer,
    CreateFolderSerializer, CreateSubfolderSerializer,FolderSerializer,FileSerializer,
    UploadedImageSerializer,TagSerializer)

def home(request):
    return render(request, 'home.html')

def cards(request):
    return render(request, 'cards.html')

def flashcard(request):
    return render(request, 'flashcard.html')

class MCQuestionViewSet(viewsets.ModelViewSet):
    queryset = MCQuestion.objects.all()
    serializer_class = MCQuestionSerializer

    @action(detail=False, methods=['get'])
    def get_questions(self, request):
        questions = MCQuestion.objects.all()
        serializer = MCQuestionOnlySerializer(questions, many=True)
        return Response(serializer.data)

class MCQAnswerViewSet(viewsets.ModelViewSet):
    queryset = MCQAnswer.objects.all()
    serializer_class = MCQAnswerSerializer

    @action(detail=False, methods=['get'])
    def get_answers(self, request):
        answers = MCQAnswer.objects.all()
        serializer = MCQAnswerOnlySerializer(answers, many=True)
        return Response(serializer.data)

class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class FillQuestionViewSet(viewsets.ModelViewSet):
    queryset = FillQuestions.objects.all()
    serializer_class = FillQuestionsSerializer

class FillAnswerViewSet(viewsets.ModelViewSet):
    queryset = FillAnswers.objects.all()
    serializer_class = FillAnswersSerializer

class CheckStatementViewSet(viewsets.ModelViewSet):
    queryset = CheckStatement.objects.all()
    serializer_class = CheckStatementSerializer

class TrueFalseViewSet(viewsets.ModelViewSet):
    queryset = TrueFalse.objects.all()
    serializer_class = TrueFalseSerializer

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    parser_classes = (MultiPartParser, FormParser)



class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    @action(detail=True, methods=['post'], url_path='create_folder')
    def create_folder(self, request, pk=None):
        parent_folder = self.get_object()
        data = request.data.copy()
        data['parent'] = parent_folder.id
        data['type'] = 'folder'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='create_subfolder')
    def create_subfolder(self, request, pk=None):
        parent_folder = self.get_object()
        data = request.data.copy()
        data['parent'] = parent_folder.id
        data['type'] = 'subfolder'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='create_subfolder_in_subfolder')
    def create_subfolder_in_subfolder(self, request, pk=None):
        parent_folder = self.get_object()
        data = request.data.copy()
        data['parent'] = parent_folder.id
        data['type'] = 'subfolder'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

@api_view(['GET'])
def folder_detail(request, pk):
    try:
        folder = Folder.objects.get(pk=pk)
    except Folder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FolderSerializer(folder)
    return Response(serializer.data)

class DirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def list(self, request, *args, **kwargs):
        parent_id = request.query_params.get('parent', None)
        if parent_id:
            queryset = Folder.objects.filter(parent_id=parent_id)
        else:
            queryset = Folder.objects.filter(parent=None)
        serializer = FolderSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def contents(self, request, pk=None):
        folder = self.get_object()
        files = folder.files.all()
        mc_questions = folder.mc_questions.all()
        mcq_answers = folder.mcq_answers.all()
        questions = folder.questions.all()
        answers = folder.answers.all()
        fill_questions = folder.fill_questions.all()
        fill_answers = folder.fill_answers.all()
        check_statements = folder.check_statements.all()
        true_false = folder.true_false.all()

        return Response({
            'files': FileSerializer(files, many=True).data,
            'mc_questions': MCQuestionOnlySerializer(mc_questions, many=True).data,
            'mcq_answers': MCQAnswerOnlySerializer(mcq_answers, many=True).data,
            'questions': QuestionsOnlySerializer(questions, many=True).data,
            'answers': AnswersOnlySerializer(answers, many=True).data,
            'fill_questions': FillQuestionOnlySerializer(fill_questions, many=True).data,
            'fill_answers': FillAnswerOnlySerializer(fill_answers, many=True).data,
            'check_statements': CheckStatementOnlySerializer(check_statements, many=True).data,
            'true_false': TrueFalseOnlySerializer(true_false, many=True).data,
        })



def mcq_questions(request):
    questions = MCQuestion.objects.all()
    serializer = MCQuestionOnlySerializer(questions, many=True)
    return JsonResponse(serializer.data, safe=False)

def mcq_answers(request):
    answers = MCQAnswer.objects.all()
    serializer = MCQAnswerOnlySerializer(answers, many=True)
    return JsonResponse(serializer.data, safe=False)

def mcq_question_by_id(request, pk=None):
    try:
        question = MCQuestion.objects.get(pk=pk)
    except MCQuestion.DoesNotExist:
        raise Http404("Question does not exist")
    serializer = MCQuestionOnlySerializer(question)
    return JsonResponse(serializer.data)

def mcq_answer_by_id(request, pk=None):
    try:
        answer = MCQAnswer.objects.get(pk=pk)
    except MCQAnswer.DoesNotExist:
        raise Http404("Answer does not exist")
    serializer = MCQAnswerOnlySerializer(answer)
    return JsonResponse(serializer.data)


def FillupQuestions(request):
    question = FillQuestions.objects.all()
    serializer = FillQuestionOnlySerializer(question, many=True)
    return JsonResponse(serializer.data, safe=False)

def FillupAnswers(request):
    answer = FillAnswers.objects.all()
    serializer = FillAnswerOnlySerializer(answer, many=True)
    return JsonResponse(serializer.data, safe=False)

def all_mcq_questions_and_answers(request):
    mcq_questions = MCQuestion.objects.all()
    mcq_question_serializer = MCQuestionSerializer(mcq_questions, many=True)
    
    data = {
        'mcq_questions': mcq_question_serializer.data,
    }
    
    return JsonResponse(data)

def all_fill_questions_and_answers(request):
    fill_questions = FillQuestions.objects.all()
    fill_question_serializer = FillQuestionsSerializer(fill_questions, many=True)
    
    data = {
        'fill_questions_answers': fill_question_serializer.data
    }
    
    return JsonResponse(data)

def Fill_question_by_id(request, pk=None):
    try:
        questions = FillQuestions.objects.get(pk=pk)
    except FillQuestions.DoesNotExist:
        raise Http404("Answer does not exist")
    serializer = FillQuestionOnlySerializer(questions)
    return JsonResponse(serializer.data)

def Fill_answer_by_id(request, pk=None):
    try:
        answers = FillAnswers.objects.get(pk=pk)
    except FillAnswers.DoesNotExist:
        raise Http404("Answer does not exist")
    serializer = FillAnswerOnlySerializer(answers)
    return JsonResponse(serializer.data)

def get_feedback(request):
    feedback = Feedback.objects.all()
    data = [{'id': fb.id, 'easily_recalled': fb.easily_recalled, 'skip': fb.skip, 'partially_recalled': fb.partially_recalled, 'forgot': fb.forgot} for fb in feedback]
    return JsonResponse(data, safe=False)

@require_POST
def handle_feedback(request):
    data = request.POST
    feedback_id = data.get('feedback_id')
    feedback = Feedback.objects.get(id=feedback_id)
    feedback.easily_recalled = data.get('easily_recalled', False)
    feedback.skip = data.get('skip', False)
    feedback.partially_recalled = data.get('partially_recalled', False)
    feedback.forgot = data.get('forgot', False)
    feedback.save()
    return JsonResponse({'message': 'Feedback received successfully'})


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

from rest_framework import generics
from .models import MCQuestion, FillQuestions, TrueFalse, CheckStatement
from .serializers import CombinedQuestionSerializer

class CombinedQuestionsByFolderAPIView(generics.ListAPIView):
    serializer_class = CombinedQuestionSerializer

    def get_queryset(self):
        folder_id = self.kwargs['folder_id']  # Assuming the folder_id is passed as a URL parameter
        mcqs = MCQuestion.objects.filter(folder_id=folder_id)
        fill_questions = FillQuestions.objects.filter(folder_id=folder_id)
        true_false = TrueFalse.objects.filter(folder_id=folder_id)
        check_statements = CheckStatement.objects.filter(folder_id=folder_id)

        combined_queryset = list(mcqs) + list(fill_questions) + list(true_false) + list(check_statements)
        return combined_queryset

@api_view(['GET'])
def get_questions_by_subfolder(request, subfolder_id):
    mc_questions = MCQuestion.objects.filter(folder_id=subfolder_id)
    fill_questions = FillQuestions.objects.filter(folder_id=subfolder_id)
    true_false_questions = TrueFalse.objects.filter(folder_id=subfolder_id)
    check_statements = CheckStatement.objects.filter(folder_id=subfolder_id)

    mc_question_serializer = MCQuestionSerializer(mc_questions, many=True)
    fill_question_serializer = FillQuestionsSerializer(fill_questions, many=True)
    true_false_serializer = TrueFalseSerializer(true_false_questions, many=True)
    check_statement_serializer = CheckStatementSerializer(check_statements, many=True)

    combined_data = {
        'mc_questions': mc_question_serializer.data,
        'fill_questions': fill_question_serializer.data,
        'true_false_questions': true_false_serializer.data,
        'check_statements': check_statement_serializer.data
    }

    return Response(combined_data)
