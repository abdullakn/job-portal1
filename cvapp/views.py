from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.


from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from io import BytesIO,StringIO



# def load_cv(request):
#     template_path = 'employee/cv_template.html'
#     context = {'myvar': 'this is your template context'}
#     # Create a Django response object, and specify content_type as pdf
#     # response = HttpResponse(content_type='application/pdf')
#     # response['Content-Disposition'] = 'filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#     response=BytesIO()
#     print(html)
#     pdfpage=pisa.pisaDocument(BytesIO(html.encode("UTF-8")),response)
#     print(pdfpage)
#     if not pdfpage.err:
#         return HttpResponse(response.getvalue(),content_type="application/pdf")

#     else:
#         return HttpResponse("error")    


