from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm, ReportForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile, Report_Issue
from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator

from django.urls import resolve
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token



# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
		'follow_status':follow_status,
		'url_name':url_name,
	}

	return HttpResponse(template.render(context, request))

def UserProfileFavorites(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	
	posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile_favorite.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user=User.objects.create_user(username=username, email=email, password=password)
			user.is_active=False
			user.save()
			uidb64=urlsafe_base64_encode(force_bytes(user.pk))
			domain=get_current_site(request).domain
			link=reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
			activate_url='http://'+domain+link
			email_subject='Account Activation Email'
			email_body='Hi '+user.username+','+'\n\n JUST ONE MORE STEP AHEAD\n\nPlease use this link to verify your account\n\n'+ activate_url +' Thank You for Registering.\n\nYour sincerely,\n\nThe Crowd Team.'
			email = EmailMessage(
				email_subject,
				email_body,
				'noreply@Crowd-admin.com',
				[email],

			)
			email.send(fail_silently=False)


			messages.success(request,f'We have sent you an email to verify your account.')
			return redirect('signup')
	else:
		form = SignupForm()

	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')



@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			 posts = Post.objects.all().filter(user=following)[:25]

			 with transaction.atomic():
			 	for post in posts:
			 		stream = Stream(post=post, user=request.user, date=post.posted, following=following)
			 		stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))

class VerificationView(View):
	def get(self, request, uidb64, token):
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)

			if not account_activation_token.check_token(user, token):
				return redirect('login' + '?message=' + 'User already activated')

			if user.is_active:
				return redirect('login')
			user.is_active = True
			user.save()

			messages.success(request, 'Account activated successfully')
			return redirect('login')

		except Exception as ex:
			pass

		return redirect('login')


def report(request):

	form = ReportForm
	if request.method == 'POST':
		reportForm = ReportForm(request.POST, request.FILES)
		if reportForm.is_valid():
			reportForm = reportForm.save(commit=False)
			reportForm.user = request.user
			reportForm.save()
			return HttpResponseRedirect('/post/')
	return render(request, 'report.html',{'form':form})