from django.urls import path,include
from authy.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile,VerificationView, report

from django.contrib.auth import views as authViews
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView



urlpatterns = [
   	
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	path('', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
   	path('passwordreset/done', PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
   	path('passwordreset/complete/', PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
	path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('report', report, name='report_issue')

]