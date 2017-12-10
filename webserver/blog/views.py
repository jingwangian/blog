from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.http import JsonResponse,HttpResponse

from taggit.models import Tag

import markdown
import codecs

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

MARKDOWN_EXT = ('footnotes', 'attr_list', 'def_list', 'abbr','pymdownx.github', 'pymdownx.extrarawhtml')
md = markdown.Markdown(extensions=MARKDOWN_EXT)

@login_required(login_url='/admin/login/')
def user_login(request):
    # return HttpResponse('You have login')
    return redirect('/admin')


def user_logout(request):
    logout(request)
    return redirect('/blog')
    # return HttpResponse('You have logout')

@login_required(login_url='/admin/login/')
def markdown_edit(request):
    context = {'in_action':'hello',
                'out_action':'hello world',
                'html_head': 'html_head',
                'vim_mode': False,
                'markdown_input':'markdown_input'}
                
    return render(request, 'blog/post/markdown_edit.html', context)

def ajax_preview(request):
    print('request -->:', request)
    if request.method == 'POST':
        post_content = request.POST
        print('post_content -->:', post_content)
        print('body-->:',request.body)
        print('content-type:',request.content_type)

        input_text = request.body.decode()

        # mid_text = codecs.getreader('utf8')(input_text).read()

        output_text = md.reset().convert(input_text)

        print('input_text -->',input_text)
        # print('mid_text -->',mid_text)
        print('output_text -->',output_text)

        return HttpResponse(output_text)
    else:
        return HttpResponse('Error: request mothod is not Post')

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'user_login':0,
                'page': page,
                'posts': posts,
                'tag': tag}
    return render(request, 'blog/post/list.html', context)

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {'user_login':1,
                'post': post,
                'comments': comments,
                'comment_form': comment_form,
                'similar_posts': None}

    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
