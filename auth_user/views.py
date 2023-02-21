from django import dispatch
from django.contrib.auth import login, REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, FormView, UpdateView

from .forms import MyUserCreationForm, ProfileForm
from .models import CustomModelUser, UserProfile
from .token_generator import account_activation_token

my_signal = dispatch.Signal()


def home(request):
    return render(request, "auth_user/main_page.html")


class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'auth_user/signup.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('auth_user/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                "We've sent you an email, please confirm your email address to complete registration")
        else:
            return self.form_invalid(form)


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        my_signal.send(sender=user)

        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'auth_user/login.html'

    # def form_valid(self, form):
    #     user = form.get_user()
    #     login(self.request, user)
    #     return super().form_valid(form)


class MyLogoutView(LogoutView):
    pass


class UpdateProfile(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'auth_user/user_profile.html'
    success_url = reverse_lazy('home')

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     print(request.user.id)
    #     print(self.object.user_id)
    #     request.user.id = self.object.user_id
    #     return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     print(request.user.id)
    #     print(self.object.user_id)
    #     return super().post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     pass
    #     user = self.request.user
    #     print(f"methoddd form_valid:: {user}")
    #     user.profile.phone = form.cleaned_data.get('phone')
    #     user.profile.birthday = form.cleaned_data.get('birthday')
    #     if 'photo' in self.request.FILES:
    #         print('found it')
    #         user.profile.photo = self.request.FILES['photo']
    #
    #     print(self.request.FILES)
    #     print(user.profile.photo)
    #     user.save()
    #     return super(UpdateProfile, self).form_valid(form)
