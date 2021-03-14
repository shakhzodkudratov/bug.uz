from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import quote
import re

from django.urls import reverse

from core.models import Url, UrlStat

url_regex = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:%_\+.~#?&\/\/=' \
            r' ]*)'


def index(request):
    # context = {'latest_question_list': latest_question_list}
    post = request.POST

    if post:
        url = post.get('url')

        if url:
            regex_result = re.search(url_regex, url)

            if regex_result:
                groups = regex_result.groups()
                url = groups[0] + quote(groups[2])
                url = url[0:1024]

                url_object = Url.objects.create(url=url)

                return redirect(reverse('stats', args=(url_object.private_name,)))

    return render(request, 'index.html')


def stats(request, name):
    url = get_object_or_404(Url, private_name=name)

    return render(request, 'stats.html', {
        'url': url,
    })


def short_url(request, url):
    url = get_object_or_404(Url, name=url)

    meta = request.META
    ip_address = meta.get('REMOTE_ADDR')
    referer = meta.get('HTTP_REFERER')
    user_agent = meta.get('HTTP_USER_AGENT')

    UrlStat.objects.create(
        url=url,
        ip_address=ip_address,
        referer=referer,
        user_agent=user_agent,
    )

    return redirect(url.url)
