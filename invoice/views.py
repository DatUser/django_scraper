from django.shortcuts import render, redirect
from django.views import View
from . import scraper
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import InvoiceDB
import datetime

user = None


def register(request):
    global user
    user = None
    form = AuthenticationForm()
    return render(request, 'invoice/home.html', {'form' : form.as_p})

def create_invoice(invoice, user):
    InvoiceDB.objects.create(number=invoice.number,\
                            date=datetime.datetime.strptime(invoice.date, '%d/%m/%Y'),\
                            name=invoice.name, total_tcc=invoice.total_tcc, \
                            total_vat=invoice.total_vat, user=user)

def fill_database(invoices, user):
    InvoiceDB.objects.filter(user=user).delete()
    for invoiceValid in invoices[0]:
        create_invoice(invoiceValid, user)
    for invoiceDraft in invoices[1]:
        create_invoice(invoiceDraft, user)

class Home(View):
    """docstring for ."""

    def get(self, request):
        return register(request)

    def post(self, request):
        form = request.POST.copy()
        email = form.get('email')
        passw = form.get('password')
        email_split = email.split('@')
        username = email_split[0] + email_split[1]
        invoices = scraper.get_invoice(email, passw)
        global user
        user = authenticate(username=username, password=passw)
        if invoices is None:
            return register(request)
        else:
            if user is None:
                user = User.objects.create_user(username, email, passw)
            fill_database(invoices, user)
            return redirect('/table/'+ email)

class Table(View):
    def get(self, request, login=None):
        global user
        number = len(InvoiceDB.objects.filter(user=user))
        invoices = InvoiceDB.objects.filter(user=user)
        context = { 'invoices' : invoices, }
        if user is None or not user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'invoice/table.html', context)
