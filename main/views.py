from django.shortcuts import render
from django.views.generic import TemplateView


class MainIndexView(TemplateView):
    template_name = 'layouts/base.html'
