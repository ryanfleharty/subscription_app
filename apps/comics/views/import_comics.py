from django.contrib.auth.decorators import permission_required
from ..forms import ImportComicForm
from ..models import Issue, Series
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files import File
import os
import csv
import datetime
import urllib
import tinify
tinify.key = settings.TINIFY_API_KEY

@permission_required('comics.add_series')
def import_comics(request):
    if request.method == 'POST':
        spreadsheet = request.FILES['comics']
        reader = csv.reader(spreadsheet)
        reader.next()
        issues_uploaded = 0
        for row in reader:
            (description, stock_no, title,
            series_code, issue_number, publisher,
            ship_date, price, artist,
            writer, colorist, cover_image_link
            ) = row
            series_title = title.split(' #')[0]
            issue_title = series_title + " #" + issue_number
            ship_date = datetime.datetime.strptime(ship_date, "%m/%d/%Y")
            if Series.objects.filter(series_code=series_code).count() > 0:
                print "SERIES ALREADY EXISTS, REGULAR UPDATE"
                series = Series.objects.get(series_code=series_code)
            else:
                print "CREATING A SERIES"
                series = Series.objects.create(publisher=publisher,title=series_title, series_code=series_code)
            if Issue.objects.filter(series_code=series_code, number=issue_number).count() > 0:
                print "ISSUE ALREADY EXISTS, DONT CREATE IT"
                continue
            else:
                new_issue = Issue.objects.create(title=issue_title, description=description, ship_date=ship_date,
                                                series=series, number=issue_number, price=price, artist=artist,
                                                publisher=publisher, series_code=series_code, writer=writer)
            cover_image = urllib.urlretrieve(cover_image_link)
            new_issue.cover_image = File(open(cover_image[0], 'rb'))
            new_issue.cover_image.name = title + '.jpg'
            new_issue.save()
            source = tinify.from_url(cover_image_link)
            source.to_file(File(open(settings.BASE_DIR + new_issue.cover_image.url, 'wb')))
            new_issue.save()
            issues_uploaded += 1
            if issues_uploaded > 10:
                break;
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        context = {
            'form': ImportComicForm()
        }
        return render(request, 'comics/import.html', context)
