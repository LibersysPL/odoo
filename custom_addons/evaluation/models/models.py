# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class evaluation(models.Model):
	_name = 'libersys.evaluation'
	
	contacts = []
	
	subject = fields.Char(string="Subject", required=True)
	partner = fields.Many2one('res.partner', string="Account", required=True, domain=[('customer', '=', True)])
	assigned_to = fields.Many2one('res.users', string="Assigned To", required=True)
	project = fields.Many2many('project.project', string="Projects")
	documents = fields.Many2many('ir.attachment', string="Documents")
	contact_person = fields.Many2many('res.partner', string="Contact Person")
	sales_person = fields.Many2one('res.users', string="Sales Person", required=True)
	internal_notes = fields.Text(String="Internal Notes")
	priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default = 'low', string = "Priority", required=True)
	deadline = fields.Date(compute='_get_eval_deadline', string = "Evaluation Deadline", required=True)
	
	@api.one
	def assigned_progressbar(self):
		self.write({
			'state': '2'
			})
		
	@api.one
	def pending_progressbar(self):
		self.write({
			'state': '3'
			})

	@api.one
	def uclosed_progressbar(self):
		self.write({
			'state': '4'
			})
	
	@api.one
	def sclosed_progressbar(self):
		self.write({
			'state': '5'
			})
		
	@api.onchange('partner')
	def _get_contact_person(self):
		choices = ()
		for p in self.partner:
			choices = p.child_ids
		self.contact_person = choices
		
	@api.model
	def _read_group_stage_ids(self,stages,domain,order):
		stage_ids = self.env['libersys.evaluation.stage'].search([])
		return stage_ids

	state = fields.Many2one('libersys.evaluation.stage', default=1 ,group_expand='_read_group_stage_ids')
	
	@api.depends('priority')
	def _get_eval_deadline(self):
		date_today = datetime.datetime.today()
		if self.priority == 'low':
			self.deadline = date_today + datetime.timedelta(days=14)
		elif self.priority == 'medium':
			self.deadline = date_today + datetime.timedelta(days=7)
		else:
			self.deadline = date_today + datetime.timedelta(days=2)
		