from django.template.loader import get_template
from django.conf import settings

from tempfile import NamedTemporaryFile
from tempfile import gettempdir

import cups
from pdf2image import convert_from_bytes
from xhtml2pdf import pisa
from PIL import Image

import os
from threading import Thread

from .models import Order

def print_file(file, title, printer_name=settings.PRINTER_NAME):
    conn = cups.Connection()
    conn.printFile(printer=printer_name, filename=file, title=title, options={})

def pdf2png(file, width=241):
    output_path = None

    images = convert_from_bytes(
        open(file, 'rb').read(),
        output_folder=gettempdir(),
        size=(width, None),
        fmt='ppm'
    )

    if len(images) > 1:

        _, heights = zip(*(i.size for i in images))

        new_im = Image.new('RGB', (width, sum(heights)))
        y_offset = 0
        for im in images:
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

        output_path = os.path.join(gettempdir(), os.path.basename(file).split(".")[0] + ".ppm")
        new_im.save(output_path)

        for im in images:
            os.remove(im.filename)

    else:
        output_path = images[0].filename

    return output_path

def print_receipt(order_id):
    template_path = 'receipt.html'

    order = Order.objects.get(id=order_id)
    order_items = order.items.select_related('product')
    context = {'order': order, 'items': order_items}
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    with NamedTemporaryFile(suffix=".pdf", mode="w+b", delete=False) as result_file:
        pisa_status = pisa.CreatePDF(
           html, dest=result_file, encoding='UTF-8')
    image_filename = pdf2png(result_file.name)
    print_file(file=image_filename, title="Order {}".format(order_id))
    os.remove(image_filename)
    os.remove(result_file.name)

def print_receipt_task(order_id):
    Thread(target=print_receipt, args=[order_id]).start()
