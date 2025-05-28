from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

class Students(models.Model):
	status_list = [
		("pre-inscrito", "Pré-inscrito"),
		("matriculado", "Matriculado"),
		("desmatriculado", "Desmatriculado"),
		("rematriculado", "Rematriculado")
		]
	_name = 'students.data'
	_description = 'The personal data from the Students.'
	_rec_name = 'name'

	name = fields.Char(string="Nome Completo")
	birth_date = fields.Date(string="Data de Nascimento")
	age = fields.Float(string="Idade",compute="_calculate_age", store=True)
	minor_bool = fields.Boolean(string="É menor de idade", 
								help="Esse valor será verdadeiro se uma pessoa tiver menos de 18 anos, e falso se ela tiver mais.",
								compute="_calculate_is_minor", store=True, default=True)
	
	cpf_apl = fields.Char(string='CPF do Aplicante')
	rg_apl = fields.Char(string='RG do Aplicante')
	tel_apl = fields.Char(string='Telefone do Aplicante')
	tel_emer = fields.Char(string='Telefone de Emergência')
	nome_emer = fields.Char(string="Quem é o contato de emergência", help="O nome do contato, seguido do seu grau de parentesco")
	nome_resp =  fields.Char(string="Nome do Responsável")
	cpf_resp = fields.Char(string='CPF do Responsável')
	rg_resp = fields.Char(string='RG do Responsável')
	tel_resp = fields.Char(string='Telefone do Responsável')
	parent_resp = fields.Char(string="Grau de Parentesco do Responsável")
	status = fields.Selection(selection=status_list)
	vinculed_grades = fields.Many2many('grade.data', 
									   'student_grade_rel',
									   'student_id', 
									   'grade_id',
										string="Grades Matriculadas")
	# CRIAR 
	# GRUPO - Saúde
	# condicao_medica
	# descricao
	# deficiencia
	# descricao_def

	#Webhooks parte -> enviar informações do forms para o odoo, pelo payload

	@api.onchange('cpf_apl', 'cpf_resp')
	def _check_cpf_format(self):
		def is_valid_cpf(cpf):
			if cpf and not re.match(r'^\d{11}$', cpf):
				raise ValidationError("CPF inválido. Verifique se o formato contém apenas números e possui 11 caracteres")
		for record in self:
			is_valid_cpf(record.cpf_apl)
			is_valid_cpf(record.cpf_resp)
				
	@api.onchange('rg_apl', 'rg_resp')
	def _check_rg_format(self):
		def is_valid_rg(cpf):
			if cpf and not re.match(r'^\d{9}$', cpf):
				raise ValidationError("CPF inválido. Verifique se o formato contém apenas números e possui 9 caracteres")
		for record in self:
			is_valid_rg(record.rg_apl)
			is_valid_rg(record.rg_resp)

	@api.depends('birth_date')
	def _calculate_age(self):
		for rec in self:
			if rec.birth_date:
				rec.age = relativedelta(datetime.now().date(), rec.birth_date).years
			else:
				rec.age = 0

	@api.depends('age')
	def _calculate_is_minor(self):
		for rec in self:
			if rec.age and rec.age >= 18:
				rec.minor_bool = False
			elif rec.age and rec.age < 18 :
				rec.minor_bool = True