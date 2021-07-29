from django import forms
from django.core.mail import EmailMessage
from .models import thread


class InquiryForm(forms.Form):
    name = forms.CharField(label='name', max_length=30)
    email = forms.EmailField(label='email')
    title = forms.CharField(label='title', max_length=30)
    message = forms.CharField(label='message', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-7'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を記入してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-7'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを記入してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-7'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルを記入してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-7'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを記入してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ{}'.format(title)
        message = '送信者:{0}\nメールアドレス:{1}\nメッセージ{2}:'.format(
            name, email, message)

        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message,
                               from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = thread
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3',)

        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
