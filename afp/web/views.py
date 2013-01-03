from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from afp.web.models import *
import datetime

def home(request):
    return render_to_response('home.html')

def funds_by_administrator(request, slug):
    administrator = get_object_or_404(Administrator, name=slug)
    funds = Fund.objects.filter(administrator = administrator)
    return render_to_response('funds_by_administrator.html', locals())

def fund_chart_data(request):
    fund_id = request.GET.get('id')
    date = datetime.datetime.now() - datetime.timedelta(days=365)
    fund = get_object_or_404(Fund, pk=fund_id)
    data = fund.get_line_data(date)
    return HttpResponse(data)

def funds_by_name(request, slug):
    funds = Fund.objects.filter(name = slug)
    return render_to_response('funds_by_name.html', locals())
