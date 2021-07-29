from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

import logging
from django.urls import reverse_lazy
from django.views import generic

from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
import csv
from .forms import InquiryForm, ThreadCreateForm
from .models import thread
import os
from django.http import FileResponse
from portfolio.settings_common import BASE_DIR

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
    paginate_by = 5

    def get_queryset(self):
        # threads = thread.objects.filter(
        #     user=self.request.user).order_by('-created_at')
        threads = thread.objects.order_by('-created_at')
        return threads


class ThreadDetailView(LoginRequiredMixin, generic.DetailView):
    model = thread
    template_name = "thread_detail.html"


class ThreadCreateView(LoginRequiredMixin, generic.CreateView):
    model = thread
    template_name = "thread_create.html"
    form_class = ThreadCreateForm
    success_url = reverse_lazy('Threader:thread_list')

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.user = self.request.user
        thread.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'スレッドの作成に失敗しました。')
        return super().form_invalid(form)


class ThreadUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = thread
    template_name = "thread_update.html"
    form_class = ThreadCreateForm
    success_url = reverse_lazy('Threader:thread_list')

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.user = self.request.user
        thread.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'スレッドの作成に失敗しました。')
        return super().form_invalid(form)


class ThreadDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = thread
    template_name = "thread_delete.html"
    form_class = ThreadCreateForm
    success_url = reverse_lazy('Threader:thread_list')

    def delete(self, request, *args, **kargs):
        messages.error(self.request, 'スレッドを削除しました。')
        return super().delete(request, *args, **kargs)


def OutputCsv(request):
    """
    ユーザー情報およびユーザーが投稿したスレッド内容を
    csvファイルに一括出力。
    """

    output_path = os.getcwd()
    output_name = '_billing.csv'

    # 検索対象レコードの抽出
    start_date = date.today().replace(day=1) - relativedelta(months=1)  # 前月の1日を取得
    end_date = date.today().replace(day=1) - timedelta(1)  # 前月の最終日を取得

    thread_list = thread.objects.all()

    # CSV出力処理開始
    with open(r"C:\Users\10387.SACTYO03\Documents\portfolio_threader\portfolio\static\test\_billing.csv", 'w', encoding='cp932', newline='') as csvfile:
        # 1行目にヘッダーを書き込む
        header = ['ユーザー', 'Email', 'タイトル', '内容', '作成日']
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(header)

        user = request.user

        for threads in thread_list:
            user_name = user.username
            user_email = user.email
            title = threads.title
            content = threads.content
            created_at = threads.created_at

            row = []
            row += [user_name, user_email, title, content, created_at]

            writer.writerow(row)

    file_path = r"C:\Users\10387.SACTYO03\Documents\portfolio_threader\portfolio\static\test"
    filename = r"\_billing.csv"
    file_name = file_path + filename

    return FileResponse(open(file_name, "rb"), as_attachment=True, filename=filename)
