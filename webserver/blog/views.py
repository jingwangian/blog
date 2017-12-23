from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone

from django.http import JsonResponse, HttpResponse

from taggit.models import Tag

import markdown
import codecs

from .models import Post, Comment
from .models import VisitorStat, TitleStat
from .forms import EmailPostForm, CommentForm

MARKDOWN_EXT = ('footnotes', 'attr_list', 'def_list', 'abbr', 'pymdownx.github', 'pymdownx.extrarawhtml')
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
def create_new_post(request):
    return markdown_edit(request)


def markdown_edit(request, title=''):
    markdown_input = ''
    if request.method == 'GET':
        if len(title) > 0:
            object_list = Post.objects.filter(title=title)
            if len(object_list) > 0:
                post = object_list[0]
                markdown_input = post.body

        context = {'in_actions': 'save',
                   'out_actions': 'preview',
                   'html_head': 'html_head',
                   'vim_mode': False,
                   'title': title,
                   'markdown_input': markdown_input}

        return render(request, 'blog/post/markdown_edit.html', context)
    elif request.method == 'POST':
        post_content = request.POST

        title = request.POST.get('title')
        # slug = request.POST.get('slug')
        slug = title.replace(' ', '-')
        body_text = request.POST.get('markdown_text')

        # print('title -->', title)
        # print('slug -->', slug)
        # print('body_text -->', body_text)

        if len(title) == 0:
            return HttpResponse('title should not empty!')

        # Save the text into datbase
        save_text_into_database(request, title, slug, body_text)
        return HttpResponse('Submit successfully!')


def save_text_into_database(request, title, slug, body_text):
    object_list = Post.objects.filter(title=title)

    # print('object_list --->', object_list)

    if len(object_list) == 0:
        # print('new topic')
        post = Post(title=title, slug=slug, body=body_text, author=request.user, status='published')

        post.save()
    else:
        post = object_list[0]
        post.body = body_text
        post.save()
        # print('old topic')


def ajax_preview(request):
    print('request -->:', request)
    if request.method == 'POST':
        post_content = request.POST
        # print('post_content -->:', post_content)
        # print('body-->:', request.body)
        # print('content-type:', request.content_type)

        input_text = request.body.decode()

        # mid_text = codecs.getreader('utf8')(input_text).read()

        output_text = md.reset().convert(input_text)

        # print('input_text -->', input_text)
        # print('output_text -->', output_text)

        return HttpResponse(output_text)
    else:
        return HttpResponse('Error: request mothod is not Post')


def post_list(request, tag_slug=None):
    user_name = 'None'
    if not request.user.is_authenticated:
        user_login = 0
    else:
        user_login = 1
        user_name = request.user.username

    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'user_login': user_login,
               'page': page,
               'posts': posts,
               'tag': tag,
               'is_detail': False}
    return render(request, 'blog/post/list.html', context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    meta_dict = request.META
    client_addr = 'unknown'
    user_agent = 'unknown'
    http_referer = 'unknown'
    request_path = 'unknown'
    last_visit_date = timezone.now()

    try:
        client_addr = meta_dict.get('REMOTE_ADDR', 'unknown').strip()
        user_agent = meta_dict.get('HTTP_USER_AGENT', 'unknown').strip()
        http_referer = meta_dict.get('HTTP_REFERER', 'unknown').strip()
        request_path = request.path.strip()
    except KeyError:
        pass
    except Exception as e:
        print("Error in post_detail --> {}".format(e))

    # print('client_addr')

    object_list = VisitorStat.objects.filter(ip_addr=client_addr)
    # visitor_object
    if len(object_list) == 0:
        obj = VisitorStat(ip_addr=client_addr,
                          user_agent=user_agent,
                          referrer=http_referer,
                          total_visit_count=1,
                          today_visit_count=1,
                          last_visit_date=last_visit_date)
    else:
        obj = object_list[0]
        obj.user_agent = user_agent
        obj.referrer = http_referer
        obj.total_visit_count += 1
        obj.today_visit_count += 1
        obj.last_visit_date = last_visit_date

    obj.save()

    user_name = 'None'
    if not request.user.is_authenticated:
        user_login = 0
    else:
        user_login = 1
        user_name = request.user.username

    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    title_object_list = TitleStat.objects.filter(title=post.title)
    if len(title_object_list) == 0:
        title_obj = TitleStat(title=post.title,
                              request_path=request_path,
                              total_visit_count=1,
                              today_visit_count=1,
                              last_visit_date=last_visit_date)
    else:
        title_obj = title_object_list[0]
        title_obj.total_visit_count += 1
        title_obj.today_visit_count += 1
        title_obj.last_visit_date = last_visit_date

    title_obj.save()

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

    context = {'user_login': user_login,
               'post': post,
               'is_detail': True,
               'comments': comments,
               'comment_form': comment_form,
               'similar_posts': None}

    return render(request, 'blog/post/detail.html', context)


@login_required(login_url='/admin/login/')
def post_update(request, slug):
    '''
    Updated the existing post text
    '''
    user_name = 'None'
    if not request.user.is_authenticated:
        user_login = 0
    else:
        user_login = 1
        user_name = request.user.username

    post = get_object_or_404(Post, slug=slug)

    print('post.title is ', post.title)

    return markdown_edit(request, post.title)


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
