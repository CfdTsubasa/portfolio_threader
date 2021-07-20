from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

import logging
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm
from .models import thread

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('Threader:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, message='メッセージを送信しました。')
        logger.info('Inquiry send by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class ThreadListView(LoginRequiredMixin, generic.ListView):
    model = thread
    template_name = "thread_list.html"
    paginate_by = 2

    def get_queryset(self):
        threads = thread.objects.filter(
            user=self.request.user).order_by('-created_at')
        return threads


class ThreadDetailView(LoginRequiredMixin, generic.DetailView):
    model = thread
    template_name = "thread_detail.html"
