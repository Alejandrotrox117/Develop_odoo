# -*- coding: utf-8 -*-

from . import controllers
from . import models

from odoo import fields, api

import pytz
from datetime import datetime, time, timedelta

def create_update_bcv_job(cr, registry):
    job_name = 'Currency Rate: Update bcv dolar ves rate'
    job_interval = timedelta(days=1)
    job_time = time(hour=14, minute=0, second=0)

    # create the cron job
    env = api.Environment(cr, 1, {})

    model = env['ir.model'].sudo().search([('model', '=', 'res.currency.rate')])

    cron = env['ir.cron'].sudo().search([('name', '=', job_name)])

    if not cron:
        timezone = pytz.timezone('America/Caracas')
        local_time = timezone.localize(datetime.combine(fields.Date.today() + job_interval, job_time))
        utc_time = local_time.astimezone(pytz.utc)

        cron = env['ir.cron'].sudo().create({
            'name': job_name,
            'interval_number': job_interval.days,
            'interval_type': 'days',
            'numbercall': -1,
            'doall': False,
            'user_id': env.ref('base.user_root').id,
            'model_id': model.id,
            'code': 'model._update_bcv_dolar()',
            'priority': 10,
            'active': True,
            'nextcall': utc_time.strftime('%Y-%m-%d %H:%M:%S'),
        })
