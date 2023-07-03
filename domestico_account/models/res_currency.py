from odoo import models, api

from bs4 import BeautifulSoup
import requests


class CurrencyRate(models.Model):
    _inherit = 'res.currency.rate'
    
    def _get_bcv_dolar(self):
        webSite = "https://monitordolarvenezuela.com/"

        webResult = requests.get(webSite)
        dataWeb = BeautifulSoup(webResult.content, 'html.parser')

        divElements = dataWeb.find_all('div', 'col-12 col-sm-4 col-md-2 col-lg-2')

        dolar_bcv = next(div.find('p').text if div.find('h4', class_="title-prome")
                        and "BCV" in div.find('h4', class_="title-prome").text.upper() else "" for div in divElements)

        dolar = dolar_bcv.split('=')[-1].strip().replace(',', '.')

        return float(dolar)
    
    @api.model
    def _update_bcv_dolar(self):

        moneda = self.env['res.currency'].search([('name', '=', 'VES')])
        if not moneda:
            raise ValueError("La moneda no existe.")
        
        dolar = self._get_bcv_dolar()

        rate = {
            'company_rate': dolar,
            'currency_id': moneda.id
        }
        
        self.create(rate)