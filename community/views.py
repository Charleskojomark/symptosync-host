from django.shortcuts import render, redirect
from .models import Group
from userauth.models import UserProfile
from .forms import JoinGroupForm, PostForm
from django.contrib.auth.decorators import login_required


def group_list(request):
    groups = Group.objects.all()
    return render(request, 'community/group_list.html', {'groups': groups})


def join_group(request):
    if request.method == 'POST':
        form = JoinGroupForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            user_profile = UserProfile.objects.get(user=request.user)
            group.members.add(user_profile)
            return redirect('community:group_list')
    else:
        form = JoinGroupForm()
    return render(request, 'community/join_group.html', {'form': form})


def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    posts = group.post_set.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = UserProfile.objects.get(user=request.user)
            post.group = group
            post.save()
            return redirect('community:group_detail', group_id=group.id)
    else:
        form = PostForm()
    return render(request, 'community/group_detail.html', {'group': group, 'posts': posts, 'form': form})


