from django.core.paginator import Paginator
from django.contrib import messages

def show_message(request,data,name):
    if len(data)<=0:
        messages.warning(request,f" No results found for {name} ")
    else:
        messages.warning(request,f" showing results for {name} ")

def get_paginated_data(request,queryset,page_size=20):
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj