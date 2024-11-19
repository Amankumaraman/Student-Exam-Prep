from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Flash import views
from rest_framework.routers import DefaultRouter
from .views import (MCQuestionViewSet, MCQAnswerViewSet, QuestionsViewSet,AnswersViewSet, 
FillQuestionViewSet, FillAnswerViewSet,CheckStatementViewSet,TrueFalseViewSet,UploadedImageViewSet)




router = DefaultRouter()
router.register(r'mcquestions', views.MCQuestionViewSet, basename='mcquestion')
router.register(r'mcqanswers', views.MCQAnswerViewSet)
router.register(r'question', views.QuestionsViewSet, basename='question')
router.register(r'answer', views.AnswersViewSet)
router.register(r'fillquestions', views.FillQuestionViewSet, basename='fillquestion')
router.register(r'fillanswers', views.FillAnswerViewSet)
router.register(r'check-statements', views.CheckStatementViewSet)
router.register(r'folders', views.FolderViewSet)
router.register(r'files', views.FileViewSet)
router.register(r'true-false', views.TrueFalseViewSet)
router.register(r'images', UploadedImageViewSet)
router.register(r'directory', views.DirectoryViewSet, basename='directory')
router.register(r'tags', views.TagViewSet, basename='tag')


urlpatterns = [
    path('', include(router.urls)),
    path('subfolders/<int:pk>/create_subfolder/', views.FolderViewSet.as_view({'post': 'create_subfolder_by_subfolder_id'})),
    path('folders/<int:pk>/create_subfolder/', views.FolderViewSet.as_view({'post': 'create_subfolder_by_subfolder_id'}), name='create-subfolder'),
    path('mcq_questions/', views.mcq_questions, name='mcq_questions'),
    path('subfolder/<int:subfolder_id>/questions/', views.get_questions_by_subfolder, name='get-questions-by-subfolder'),
    path('mcq_questions/<int:pk>/', views.mcq_question_by_id, name='mcq_question_by_id'),
    path('mcq_answers/', views.mcq_answers, name='mcq_answers'),
    path('mcq_answers/<int:pk>/', views.mcq_answer_by_id, name='mcq_answer_by_id'),
    path('Fill_question_by_id/<int:pk>/', views.Fill_question_by_id, name='Fill_question_by_id'),
    path('Fill_answer_by_id/<int:pk>/', views.Fill_answer_by_id, name='Fill_answer_by_id'),
    path('FillupQuestions/', views.FillupQuestions, name='FillupQuestions'),
    path('FillupAnswers/', views.FillupAnswers, name='FillupAnswers'),
    path('home/', views.home, name='home'),
    path('all_mcq_questions_and_answers/', views.all_mcq_questions_and_answers, name='all_mcq_questions_and_answers'),
    path('all_fill_questions_and_answers/', views.all_fill_questions_and_answers, name='all_fill_questions_and_answers'),
    path('cards/', views.cards, name='cards'),
    path('flashcard/', views.flashcard, name='flashcard'),
    path('get_feedback/', views.get_feedback, name='get_feedback'),
    path('handle_feedback/', views.handle_feedback, name='handle_feedback'),
    path('questions/combined/<int:folder_id>/', views.CombinedQuestionsByFolderAPIView.as_view(), name='combined-questions-by-folder'),
]

