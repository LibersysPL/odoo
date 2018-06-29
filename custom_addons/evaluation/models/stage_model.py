# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StageModel(models.Model):
	_name = 'libersys.evaluation.stage'
	_order = 'id'
	
	name = fields.Char(string = "Status", required = True)