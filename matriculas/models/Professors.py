from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Professors(models.Model):
    _name="professors.data"
    _description="Personal data about Professors"
    _rec_name="name"

    name=fields.Char(string="Nome do Professor")
    tel_nbr=fields.Char(string="Telefone do Professor")
    email=fields.Char(string="E-mail do Professor")
    