from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView, UpdateView,
)


from authentication.models import User
from .models import Profile


@method_decorator([login_required], name='dispatch')
class ProfileDetailView(TemplateView):
    """
    Show the profile.
    """
    model = Profile
    template_name = 'user_profile/profile.html'

    def get_context_data(self, **kwargs):
        """
        Pass the context to the template.
        """
        context = super(ProfileDetailView, self).get_context_data(**kwargs) # 此步获取 url 后面的 user_id
        user_id = self.kwargs.get('user_id')
        context['user'] = User.objects.get(id=user_id)
        context['profile'] = Profile.objects.get(user_id=user_id)
        return context


@method_decorator([login_required], name='dispatch')
class UpdateProfileView(UpdateView):
    """
    Update the profile.
    """
    model = Profile
    fields = ['avatar', 'url', 'location', 'job_title']
    template_name = 'user_profile/profile_update.html'

    def get_object(self, queryset=None):
        """
        指定 Profile 对象
        :param queryset:
        :return:
        """
        return Profile.objects.get(user_id=self.kwargs.get('user_id'))

    def form_valid(self, form):
        """
        Do something before save the profile.
        """
        profile = form.save(commit=False)
        profile.save()
        form.save_m2m()
        return redirect('user_profile:profile', self.kwargs.get('user_id'))

    def get_success_url(self):
        return reverse('user_profile:profile', self.kwargs.get('user_id'))


@login_required
def setpassword(request):
    title = 'Change Password'
    # username = request.user.username
    user = request.user
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword','')
        newpassword = request.POST.get('newpassword','')
        if user.check_password(oldpassword):
            user.set_password(newpassword)
            user.save()
            tips = ''
            # time.sleep(3)
            return redirect('home')
        else:
            tips = '原密码输入有误，修改失败。若修改成功，将自动跳转到登录界面'

    return render(request,'user_profile/setpassword.html',locals())


