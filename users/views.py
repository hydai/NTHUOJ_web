'''
The MIT License (MIT)

Copyright (c) 2014 NTHUOJ team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template import RequestContext
from users.admin import UserCreationForm, AuthenticationForm

from index.views import custom_proc
from users.forms import UserProfileForm, UserLevelForm
from users.models import User
from utils.log_info import get_logger, get_client_ip
from utils.user_info import get_user_statistics
from users.templatetags.profile_filters import can_change_userlevel
# Create your views here.

logger = get_logger()

def list(request):
    users = User.objects.all()
    paginator = Paginator(users, 25)  # Show 25 users per page
    page = request.GET.get('page')

    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user = paginator.page(paginator.num_pages)

    return render(
        request,
        'users/userList.html',
        {'users': user},
        context_instance=RequestContext(request, processors=[custom_proc]))

def submit(request):
    return render(
        request,
        'users/submit.html', {},
        context_instance=RequestContext(request, processors=[custom_proc]))


def profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
        piechart_data = get_user_statistics(profile_user)

        render_data = {}
        render_data['profile_user'] = profile_user
        render_data['piechart_data'] = json.dumps(piechart_data)
        if request.user == profile_user:
            render_data['profile_form'] = UserProfileForm(instance=profile_user)
        if can_change_userlevel(request.user, profile_user):
            render_data['userlevel_form'] = UserLevelForm(instance=profile_user)

        if request.method == 'POST' and 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=profile_user)
            render_data['profile_form'] = profile_form
            if profile_form.is_valid() and request.user == profile_user:
                logger.info('User %s update profile' % username)
                profile_form.save()
                render_data['profile_message'] = 'Update successfully'

        if request.method == 'POST' and 'userlevel_form' in request.POST:
            userlevel_form = UserLevelForm(request.POST)
            if can_change_userlevel(request.user, profile_user):
                if userlevel_form.is_valid(request.user):
                    user_level = userlevel_form.cleaned_data['user_level']
                    logger.info('User %s update %s\'s user_level to %s' %
                        (request.user, username, user_level))
                    profile_user.user_level = user_level
                    profile_user.save()
                    render_data['userlevel_message'] = 'Update successfully'
                else:
                    user_level = userlevel_form.cleaned_data['user_level']
                    render_data['userlevel_message'] = 'You can\'t switch user %s to %s' % \
                        (profile_user, user_level)

        return render(
            request,
            'users/profile.html',
            render_data,
            context_instance=RequestContext(request, processors=[custom_proc]))

    except User.DoesNotExist:
        logger.warning('User %s does not exist' % username)
        return render(
            request,
            'index/500.html',
            {'error_message': 'User %s does not exist' % username})


def user_create(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            logger.info('user %s created' % str(user))
            login(request, user)
            return redirect(reverse('index:index'))
        else:
            return render(
                request, 'users/auth.html',
                {'form': user_form, 'title': 'Sign Up'},
                context_instance=RequestContext(request, processors=[custom_proc]))
    return render(
        request,
        'users/auth.html',
        {'form': UserCreationForm(), 'title': 'Sign Up'},
        context_instance=RequestContext(request, processors=[custom_proc]))


def user_logout(request):
    logger.info('user %s logged out' % str(request.user))
    logout(request)
    return redirect(reverse('index:index'))


def user_login(request):
    if request.user.is_authenticated():
        return redirect(reverse('index:index'))
    if request.method == 'POST':
        user_form = AuthenticationForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'])
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            ip = get_client_ip(request)
            logger.info('user %s @ %s logged in' % (str(user), ip))
            login(request, user)
            return redirect(reverse('index:index'))
        else:
            return render(
                request,
                'users/auth.html',
                {'form': user_form, 'title': 'Login'},
                context_instance=RequestContext(request, processors=[custom_proc]))
    return render(
        request,
        'users/auth.html',
        {'form': AuthenticationForm(), 'title': 'Login'},
        context_instance=RequestContext(request, processors=[custom_proc]))
