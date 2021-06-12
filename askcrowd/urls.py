from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from askcrowd.views import home, ask_form, detail, tag, save_comment, save_upvote, save_downvote, Update_Answer, Del_Answer, update_question, del_question
urlpatterns = [

    path('ask', home, name='ask'),
    path('ask/ask-question', ask_form, name = 'ask-question'),
    path('ask/detail/<int:id>', detail, name = 'detail'),
    path('ask/tag/<str:tag>', tag , name='tag'),
    path('ask/detail/save-comment', save_comment, name = 'save-comment'),
    path('ask/detail/save-upvote', save_upvote, name = 'save-upvote'),
    path('ask/detail/save-downvote', save_downvote, name = 'save-downvote'),
    path('ask/update/<int:id>', Update_Answer, name = 'update_answer'),
    path('ask/detail/delete/<int:id>', Del_Answer, name = 'Del-Ans'),
    path('ask/ask-question/<int:id>', update_question, name = 'update-question'),
    path('ask/<int:id>', del_question, name = 'delete_question')

]