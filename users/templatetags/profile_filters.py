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
from django import template
from users.models import User
from datetime import datetime
from utils.user_info import validate_user

register = template.Library()


@register.filter()
def can_change_userlevel(user, profile_user):
    '''Test if the user can change user_level
    of profile_user
    Args:
        submission: a Submission object
        user: an User object
    Returns:
        a boolean of the judgement
    '''
    user = validate_user(user)
    # admin can change user to all levels
    if user.has_admin_auth():
        return True
    # judge can change user to sub-judge, user
    user_level = profile_user.user_level
    if user.has_judge_auth() and \
        (user_level == User.SUB_JUDGE or user_level == User.USER):
        return True

    return False

