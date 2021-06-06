from django.shortcuts import render, redirect
from django.views.generic import View
from .form import ContactForm
from .models import Profile, Work
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap


# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.all()
        work_data = Work.objects.all()
        if profile_data.exists():
            profile_data = profile_data.order_by("-id")[0]
            work_data = work_data.order_by("-id")
        return render(
            request,
            "app/index.html",
            {
                "profile_data": profile_data,
                "work_data": work_data,
            },
        )


class DetailView(View):
    def get(self, request, *args, **kwargs):
        work_data = Work.objects.get(id=self.kwargs["pk"])
        return render(
            request,
            "app/detail.html",
            {
                "work_data": work_data,
            },
        )


class AboutView(View):
    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.all()
        work_data = Work.objects.all()
        if profile_data.exists():
            profile_data = profile_data.order_by("-id")[0]
        return render(
            request,
            "app/about.html",
            {
                "profile_data": profile_data,
            },
        )


class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        return render(
            request,
            "app/contact.html",
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            subject = "お問い合わせ"
            contact = textwrap.dedent(
                """
                ※このメールはシステムからの自動返信です。

                {name} 様

                お問い合わせありがとうございます。
                以下の内容でお問い合わせを受付いたしました。
                内容を確認させていただき、ご返信させて頂きますので、少々お待ちください。

                --------------------
                ■お名前
                {name}

                ■メールアドレス
                {email}

                ■メッセージ内容
                {message}
                --------------------
                """
            ).format(
                name=name,
                email=email,
                message=message,
            )
            recipient_list = [email]
            from_email = settings.EMAIL_HOST_USER
            bcc = [settings.EMAIL_HOST_USER]
            try:
                message = EmailMessage(
                    subject, contact, from_email, recipient_list, bcc
                )
                message.send()
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました")

            return redirect("thanks")

        return render(
            request,
            "app/contact.html",
            {
                "form": form,
            },
        )


class ThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "app/thanks.html")
