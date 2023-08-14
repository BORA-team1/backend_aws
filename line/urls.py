from django.contrib import admin
from django.urls import path
from .views import *

app_name='line'      

urlpatterns = [
        path('<int:post_pk>/',MyLineView.as_view()),
        path('<int:post_pk>/com/',MyLineComView.as_view()),
        path('<int:post_pk>/qna/',MyLineQnAView.as_view()),
        path('<int:post_pk>/emo/',MyLineEmoView.as_view()),
        path('delete/<int:line_pk>/',MyLineDeleteView.as_view()),
        path('com/<int:line_pk>/',LineComView.as_view()),
        path('com/del/<int:linecom_pk>/',DeleteComView.as_view()),
        path('com/like/<int:linecom_pk>/',LineComLikeView.as_view()),
        path('comcom/<int:linecom_pk>/',NewLineComComView.as_view()),
        path('comcomdelete/<int:linecomcom_pk>/',DeleteComComView.as_view()),
        path('qna/<int:line_pk>/',LineQnAView.as_view()),
        path('qnadelete/<int:question_pk>/',DeleteQueView.as_view()),
        path('ans/<int:question_pk>/',AnswerView.as_view()),
        path('emo/<int:line_pk>/',EmoView.as_view()),
        path('com/w/<int:post_pk>/',LineCom2View.as_view()),
        path('qna/w/<int:post_pk>/',LineQnA2View.as_view()),
        path('emo/w/<int:post_pk>/',LineEmo2View.as_view()),
]