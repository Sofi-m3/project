from django.urls import path
from .views import (
    TestListView, TestCreateView, TestEditView, TestDeleteView,
    QuestionAddView, AnswerAddView, TestTakeView, TestResultsView,
    AllResultsView, TestSelectView
)

urlpatterns = [
    path('', TestListView.as_view(), name='test_list'),
    path('create/', TestCreateView.as_view(), name='test_create'),
    path('<int:test_id>/edit/', TestEditView.as_view(), name='test_edit'),
    path('<int:test_id>/delete/', TestDeleteView.as_view(), name='test_delete'),
    path('<int:test_id>/questions/add/', QuestionAddView.as_view(), name='question_add'),
    path('questions/<int:question_id>/answers/add/', AnswerAddView.as_view(), name='answer_add'),
    path('select/', TestSelectView.as_view(), name='test_select'),
    path('<int:test_id>/take/', TestTakeView.as_view(), name='test_take'),
    path('<int:test_id>/results/', TestResultsView.as_view(), name='test_results'),
    path('results/all/', AllResultsView.as_view(), name='all_results'),
]