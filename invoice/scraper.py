import re
import requests as rq
from bs4 import BeautifulSoup as bs

class Invoice():

    def __init__(self, number, date, name, total_tcc=None, total_vat=None):
        self.number = number
        self.date = date
        self.name = name
        self.total_tcc = total_tcc
        self.total_vat = total_vat

    def listValidArgs(self):
        return [self.number, self.date, self.name, self.total_tcc, self.total_vat]

    def listDraftArgs(self):
        return [self.number, self.date, self.name]

def connect(login, password):
    url = 'https://app.factomos.com/connexion'
    payload = {
        'email' : login,
        'password' : password,
        "csrfmiddlewaretoken": "<CSRF_TOKEN>"
    }
    res = r.post(url, data=payload, headers=dict(referer=url))

    url_data = 'https://app.factomos.com/mes-factures'
    res_data = r.get(url_data, headers=dict(referer=url))

    res_bis = r.get(url_data, auth=(login, password))
    res_bis.raise_for_status()


def is_draft(soupInvoice):
    return soupInvoice.find('span', attrs='draft_number') is not None


def connect_page(login, password):
    session = rq.Session()
    payload = {
        'username' : login,
        'password' : password
        }
    session.post('https://app.factomos.com/connexion', data=payload)
    return session.get('https://app.factomos.com/mes-factures')

def get_table(page):
    soup = bs(page.text, 'html.parser')
    table = soup.find('tbody', id='invoiceListBody')
    return table.find_all('tr') if table else None

def create_invoice(table_line):
    number_soup = table_line.find('td', attrs='ITEM-NUMBER')
    isDraft = is_draft(number_soup)

    number = (number_soup.find('span') if isDraft else number_soup).text.strip()
    date = table_line.find('td', attrs='ITEM-DATE').text.strip()
    name = table_line.find('td', attrs='ITEM-CLIENT').find('a').text.strip()
    ttc = float(re.sub("[^0-9\\.]", "", table_line.find('td', attrs='ITEM-TOT-TTC').text.strip()))
    vat = float(re.sub("[^0-9\\.]", "", table_line.find('td', attrs='ITEM-TOT-TVA').text.strip()))

    return (Invoice(number, date, name), isDraft) if isDraft else (Invoice(number, date, name, ttc, vat), isDraft)

def extract_data(table):
    invoice_validated, invoice_draft = [], []

    for elt in table:
        (invoice, isDraft) = create_invoice(elt)

        if isDraft:
            invoice_draft.append(invoice)
        else:
            invoice_validated.append(invoice)

    return (invoice_validated, invoice_draft)

'''
    Returns a 2 lists with invoices if the connection succeeded, None otherwise
'''
def get_invoice(login, password):
    page = connect_page(login, password)
    if page.url != 'https://app.factomos.com/mes-factures':
        return None
    table = get_table(page)
    return extract_data(table) if table else ([], [])
