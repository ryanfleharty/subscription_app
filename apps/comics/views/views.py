# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from ..models import Series, Issue, Review, Comment
from ...users.models import Profile
from django.contrib.auth.models import User
from ..forms import ReviewForm, CommentForm
import math

# Create your views here.
def index(request):
    page_count = math.ceil(Series.objects.count() / 12.0)
    page_count = int(page_count)
    page_list = []
    for x in range(page_count):
        page_list.append(x+1)
    context = {
        'series' : Series.objects.order_by('title')[:12],
        'page_count' : page_list,
        'row_starts' : [1,5,9],
        'row_ends' : [4,8,12],
    }
    return render(request, 'comics/index.html', context )

def search(request):
    if request.method == 'POST':
        search_text = request.POST['search']
    else:
        search_text = ""
    series = Series.objects.filter(title__contains=search_text).order_by('title')[:12]
    context = {
        "series": series,
        'row_starts' : [1,5,9],
        'row_ends' : [4,8,12]
    }
    return render(request, 'comics/search_results.html', context)

def browse(request):
    if request.method == 'POST':
        page = request.POST['page']
    else:
        page = 1
    start = ((int(page)-1) * 12)
    context = {
        'series' : Series.objects.order_by('title')[start:start+12],
        'row_starts' : [1,5,9],
        'row_ends' : [4,8,12]
    }
    return render(request, 'comics/search_results.html', context)

def show_by_title(request, title):
    try:
        series = Series.objects.get(title__iexact=title)
        reviews = Review.objects.filter(series=series)
        comments = Comment.objects.filter(review__in=reviews)
        issues = Issue.objects.filter(series=series)
        context = {
            'series': series,
            'review_form': ReviewForm(),
            'reviews': reviews,
            'comment_form': CommentForm(),
            'comments': comments,
            'issues': issues,
        }
        if request.user.is_authenticated():
            is_subscribed = request.user.profile.subscriptions.filter(title=title).count() > 0
        else:
            is_subscribed = False
        context['is_subscribed'] = is_subscribed
        return render(request, 'comics/show.html', context)
    except Exception as inst:
        print inst
        return redirect('/comics/')

def show(request, id):
    try:
        series = Series.objects.get(id=id)
        return redirect('show_by_title', title=series.title)
    except Exception as inst:
        print inst
        return redirect('/comics/')

def show_issue(request, title, issue_num):
    try:
        issue = Issue.objects.get(series__title__iexact=title, number=int(issue_num))
        series = issue.series
        reviews = Review.objects.filter(issue=issue)
        context = {
            'issue': issue,
            'review_form': ReviewForm(),
            'reviews': reviews,
            'comment_form': CommentForm(),
            'series': series
        }
        return render(request, 'comics/show_issue.html', context)
    except Exception as inst:
        print inst
        return redirect(request.META.get('HTTP_REFERER', '/'))

def jump_to_issue(request):
    issue_num = request.POST['issue_num']
    title = request.POST['title']
    return redirect('show_issue', title=title, issue_num=issue_num )

def manage(request):
    subscribed_comics = request.user.profile.subscriptions.all()
    other_comics = Series.objects.exclude(profile__id=request.user.profile.id)
    context = {
        'subscribed_comics': subscribed_comics,
        'other_comics': other_comics
    }
    return render(request, 'comics/manage_subs.html', context)

def sub_form_expansion(request):
    other_comics = Series.objects.exclude(profile__id=request.user.profile.id)
    context = {
        'other_comics': other_comics
    }
    return render(request, 'comics/select_from_comics.html', context)

def subscribe(request, id):
    if request.method == 'POST':
        valid, response = Series.objects.subscribe(id, request.user)
        if valid:
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))

def unsubscribe(request, id):
    if request.method == 'POST':
        valid, response = Series.objects.unsubscribe(id, request.user)
        if valid:
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))

def subscribe_bulk(request):
    if request.method == 'POST':
        comics = request.POST.getlist('comics_to_add')
        print comics
        for comic in comics:
            Series.objects.subscribe(comic, request.user)
        return redirect(request.META.get('HTTP_REFERER', '/'))

def unsubscribe_bulk(request):
    if request.method == 'POST':
        comics = request.POST.getlist('comics_to_drop')
        for comic in comics:
            Series.objects.unsubscribe(comic, request.user)
        return redirect(request.META.get('HTTP_REFERER', '/'))

def add_review(request, id):
    if request.method == 'POST':
        try:
            series = Series.objects.get(id=id)
        except Exception as inst:
            print inst
        user = request.user
        content = request.POST['content']
        Review.objects.create(series=series, user=user, content=content)
        return redirect(request.META.get('HTTP_REFERER', '/'))

def add_issue_review(request, title, issue_num):
    if request.method == 'POST':
        user = request.user
        content = request.POST['content']
        issue = Issue.objects.get(series__title__iexact=title, number=int(issue_num))
        Review.objects.create(issue=issue, user=user, content=content)
        return redirect(request.META.get('HTTP_REFERER', '/'))

def add_comment(request, id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=id)
        except Exception as inst:
            print inst
        user = request.user
        content = request.POST['content']
        Comment.objects.create(review=review, user=user, content=content)
        return redirect(request.META.get('HTTP_REFERER', '/'))
