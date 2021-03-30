from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from main.models import Post, Comment, Subscribe,Category
from main.forms import PostForm, CommentForm, SubscribeForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
# from .filters import OrderFilter
from django.core.mail import send_mail
# Create your views here.

class AdvertView(TemplateView):
    template_name = 'blog/advert.html'


def newsletter_subscribe(request):
    form = SubscribeForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if Subscribe.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Your email already exists', 'alert alert-warning alert-dismissible')
        else:
            instance.save()
            messages.success(request, 'Your email has been submitted ','alert alert-success alert-dismissible')
    context = {'form':form}

    return render(request, 'blog/subscribe.html', context)


def news_unsub(request):
    form = SubscribeForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if Subscribe.objects.filter(email=instance.email).exists():
            Subscribe.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your email has been removed', 'alert alert-warning alert-dismissible')
        else:
            messages.warning(request, 'Sorry your email is not in our database ','alert alert-success alert-dismissible')

    context = {'form':form}

    return render(request, 'blog/unsubscribe.html', context)





import datetime
class PostListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 21


    def get_queryset(self):
        return Post.objects.filter(published_date__lte=now()).order_by("-published_date")

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        cat_menu = Category.objects.all()
        # recent = datetime.date.today() - datetime.timedelta(days=7)

        # myfilter = OrderFilter(request.GET)
        list_post = Post.objects.all()
        query = self.request.GET.get('src')
        if query:
            list_post = list_post.filter(Q(title__icontains=query) | Q(text__icontains=query))
        paginator = Paginator(list_post, self.paginate_by)
        page = self.request.GET.get('src')

        try:
            li_posts = paginator.page(page)
        except PageNotAnInteger:
            li_posts = paginator.page(1)
        except EmptyPage:
            li_posts = paginator.page(paginator.num_pages)

        context['list_post']  = li_posts
        context['cat_menu']= cat_menu


        # context['myfilter']= myfilter
        return context

class PostDetailView(DetailView):
    
    model = Post
    template_name = 'blog/post_detail.html'

    ordering = ["-published_date"]

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['cat_menu'] = cat_menu
        return context



class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    template_name = 'blog/post_form.html'
    model = Post

def contact(request):
    if request.method == "POST":
        massage_name = request.POST['massage_name']
        massage_email = request.POST['email']
        massage = request.POST['massage']
        #send mai
        send_mail = (
            massage_name,
            massage_email,
            massage,['arizonatymothy@gmail.com','timzonatimothy@gamil.com']
        )
        return render(request, 'blog/contact.html', {'massage_name':massage_name,'massage_email':massage_email,'massage':massage})

    else:
        return render(request, 'blog/contact.html', {})


def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=post.pk)

class UpdatePostView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    template_name = 'blog/post_form.html'
    form_class = PostForm

    model = Post




class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

def CategoryView(request,cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'blog/categories.html',{'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})



def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request,'blog/category_list.html',{'cat_menu_list':cat_menu_list})


class AddCategoryView(LoginRequiredMixin,CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'


# class DraftListView(LoginRequiredMixin,ListView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_list.html'
#     model = Post
#     template_name = 'blog/post_draft_list.html'
#     def get_queryset(self):
#         return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html',{'form':form})






