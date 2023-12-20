from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import pytz

from .models import Bins
from django.contrib.auth.decorators import login_required
@login_required
def create_note(request):
    if request.method == 'GET':

        return render(request, 'bins/create.html', {'content': '', 'code_bins': return_all_unexpired()})

    else:
        print(request.POST)
        Bins.objects.create(
            code=f'''{request.POST['codeContent']}''',
            expiry_policy=request.POST['duration']
        )

        return JsonResponse({'Status': 'Success!'})


def note(request, uuid):
    try:
        code_bin = Bins.objects.get(uuid=uuid)
    except Bins.DoesNotExist:
        return HttpResponse('Site error: no bin by that uuid.')

    expired = False if code_bin.expires_on > datetime.now(pytz.timezone('UTC')) else True

    if not expired:
        return render(request, 'bins/read.html',
                      {
                          'code': code_bin.code,
                          'expires': code_bin.expiry_policy,
                          'code_display': highlight_code(code_bin.code, 'python'),
                          'code_bins': Bins.objects.all()
                      }
                      )
    else:
        return HttpResponse('Sorry this bin no longer exists.')


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def highlight_code(code, language):
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter(linenos=False, cssclass="source")
    return highlight(code, lexer, formatter)


def return_all_unexpired():

    return [x for x in Bins.objects.all() if not x.is_expired()]
