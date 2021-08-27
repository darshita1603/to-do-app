from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase
 
from django.http import HttpResponse
from xhtml2pdf import pisa  
from django.template.loader import get_template
#difine render_to_pdf() function
 
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
    
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     with open(f'media/pdf_files/task_history_pdf.pdf','w+b') as f:
        # result_file = open("test.pdf", "w+b")
        #This part will create the pdf.
        pisa_status = pisa.CreatePDF(
                html,                   # the HTML to convert
                dest=f            # file handle to recieve result
        )
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None