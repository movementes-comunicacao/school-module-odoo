from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Grade(models.Model):
	_name = 'grade.data'
	_description = "All the elements that form a grade of a class"
	_rec_name = 'regs_stable'

	# Section of Registration[Matrículas] Variables
	regs_list = fields.Selection(selection="_get_registration_list",
								 string="Selecione na Lista uma modalidade")
	reg_input = fields.Char(string="Nome Nova Matrícula")
	regs_stable = fields.Char(compute="_compute_regs_stable", store=True)
	
	#Section of Professors Variable
	professor_ids = fields.Many2one('professors.data',string="Professor Vinculado à Matéria")

	#Section of Time[Horário] Variables
	time_range_ids = fields.One2many('grade.schedules.line', 'grade_schedule_id', string="Horários Disponíveis")
	#Time Summary Variable, make only for visualization purposes.
	time_summary = fields.Text(string='Horários', compute="_compute_time_summary")

	#Section of Ages Spaces
	section_age = fields.Selection(string="Faixa Etária", 
								   selection=[('6 a 9 anos', '6 a 9 anos'),
					  						  ('10 a 13 anos', '10 a 13 anos'),
											  ('14 a 17 anos', '14 a 17 anos'),
											  ('adultos [18+]', 'adultos [18+]')])

	@api.depends('time_range_ids.day', 'time_range_ids.start_time', 'time_range_ids.end_time')
	def _compute_time_summary(self):
		for record in self:
			summary = []
			for time in record.time_range_ids:
				start = "{:02.0f}:{:02.0f}".format(*divmod(time.start_time * 60, 60))
				end = "{:02.0f}:{:02.0f}".format(*divmod(time.end_time * 60, 60))
				summary.append(f"{time.day}: {start} - {end}")
			record.time_summary = "\n".join(summary)
	
	# Section of Registration[Matrículas] Treatment
	@api.depends('regs_list', 'reg_input')
	def	_compute_regs_stable(self):
		for rec in self:
			if rec.regs_list != 'new':
				print("entered in rec is not new")
				rec.regs_stable = rec.regs_list
				rec.reg_input = rec.regs_stable
				print("rec.regs_stage is :", rec.regs_stable)
			else :
				print("entered in else")
				rec.regs_stable = rec.reg_input
				print("rec.regs_stage is :", rec.regs_stable)

	@api.model
	def _get_registration_list(self):
		all_regs = set(self.search([]).mapped('regs_stable'))
		arr = [("new", "Nova Modalidade")]
		arr_new = [(i, i) for i in all_regs]
		arr.extend(arr_new)
		return arr

class GradeSchedulesLine(models.Model):
	days_of_week = [('segunda-feira', 'Segunda-Feira'),
				 	('terça-feira', 'Terça-Feira'),
					('quarta-feira', 'Quarta-Feira'),
					('quinta-feira', 'Quinta-Feira'),
					('sexta-feira', 'Sexta-Feira'),
					('sábado', 'Sábado'),
					('domingo', 'Domingo')]
	_name = 'grade.schedules.line'
	_description = 'The days and hours that the Grade is setted'

	grade_schedule_id = fields.Many2one('grade.data', string="Matrícula")

	day = fields.Selection(selection=days_of_week, string="Dias na Semana")
	start_time = fields.Float(string="Hora Início", required=True)
	end_time = fields.Float(string="Hora Fim", required=True)

	@api.onchange("start_time", "end_time")
	def _validate_times(self):
		print("Validate Times Triggered")
		for rec in self:
			if rec.start_time and rec.end_time:
				print("Two Times Are Válid")
				valid_start = rec.start_time <= 24 and rec.start_time >= 0
				valid_end = rec.end_time <= 24 and rec.end_time >= 0
				start_minnor_end = rec.start_time < rec.end_time
				print(f"Valid Start: {valid_start} Valid End: {valid_end} Minor End: {start_minnor_end}" , )
				if (not valid_start or not valid_end or not start_minnor_end):
					raise ValidationError(f"""Erro nos horários:
	Hora Início: {'OK' if valid_start else 'Horário Inválido'}
	Hora Fim: {'OK' if valid_end else 'Horário Inválido'}
	{'Intervalo Entre Início e Fim OK' if start_minnor_end else 'Erro Entre Intervalos de Horário'}""")

	@api.constrains("start_time", "end_time", "day")
	def _constrain_times(self):
		print("Validate Times Triggered")
		for rec in self:
			if not rec.start_time or not rec.end_time or not rec.day:
				raise ValidationError("Você deixou de preencher alguma informação do campo dos dias da aula. Verifique o dia da semana e os horários.")
			if rec.start_time and rec.end_time:
				print("Two Times Are Válid")
				valid_start = rec.start_time <= 24 and rec.start_time >= 0
				valid_end = rec.end_time <= 24 and rec.end_time >= 0
				start_minnor_end = rec.start_time < rec.end_time
				print(f"Valid Start: {valid_start} Valid End: {valid_end} Minor End: {start_minnor_end}" , )
				if (not valid_start or not valid_end or not start_minnor_end):
					raise ValidationError(f"""Erro nos horários:
	Hora Início: {'OK' if valid_start else 'Horário Inválido'}
	Hora Fim: {'OK' if valid_end else 'Horário Inválido'}
	{'Intervalo Entre Início e Fim OK' if start_minnor_end else 'Erro Entre Intervalos de Horário'}""")