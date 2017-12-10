from django.utils.safestring import mark_safe
import markdown
from django.db.models import Count
from django import template
register = template.Library()
from ..models import Post


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# @register.assignment_tag
# def get_most_commented_posts(count=5):
#     return Post.published.annotate(
#         total_comments=Count('comments')
#     ).order_by('-total_comments')[:count]


@register.filter(name='mymarkdown')
def markdown_format(text):
    options = {'input': None, 'term_action': 'e', 'port': 8222, 'output': None, 'safe_mode': False, 'extensions': ['footnotes', 'attr_list', 'def_list', 'abbr', 'pymdownx.github', 'pymdownx.extrarawhtml'], 'encoding': None, 'output_format': 'xhtml1', 'lazy_ol': True}

    markdown_processor = markdown.Markdown(**options)

    return mark_safe(markdown_processor.reset().convert(text))

    # return mark_safe(markdown.markdown(text))
