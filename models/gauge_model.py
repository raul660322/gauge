# -*- coding: utf-8 -*-
##############################################################################
#
#    Palmares Sucursal Matanzas
#    Departamento de Informática y Comunicaciones
#    Autor: Raúl Sánchez Pérez
#
##############################################################################
from datetime import datetime,date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import operator

class Instrumento(models.Model):
    _name = 'instrumento'
    name = fields.Char(string='Instrumento')
    u_medida=fields.Char(string='Unidad de Medida')

class TipoInstrumento(models.Model):
    _name = 'tipo_instr'
    name = fields.Char(string='Tipo')
    equipo = fields.Many2one('instrumento',string='Equipo')

class Gauge(models.Model):
    _name = 'gauge'
    _description = 'Instrumentos de Medicion'

    def mail_reminder(self):
        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.expiry_date and i.mensaje:
                exp_date = fields.Date.from_string(i.expiry_date) - timedelta(days=90)
                if date_now >= exp_date:
                    mail_content = "  Estimado  " + i.employee_ref.name + ",<br> El Certificado de " + i.instrumento.name + " "+ i.name + " de " + i.dpto_ref.name+ " vence en " + \
                                   str(i.expiry_date) + ". Por favor, debe renovarlo antes de la fecha de vencimiento"
                    main_content = {
                        'subject': _('Certificado-%s de %s Vence en %s') % (i.name, i.dpto_ref.name, i.expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.employee_ref.work_email,
                    }
                    self.env['mail.mail'].create(main_content).send()

    @api.constrains('expiry_date')
    def check_expr_date(self):
        for each in self:
            exp_date = fields.Date.from_string(each.expiry_date)
            if exp_date < date.today():
                raise Warning('Este certificado ha vencido.')
    
    name = fields.Char(string='Inventario', required=True, copy=False)
    serie = fields.Char(string='N. de Serie', required=True, copy=False)
    marca = fields.Char(string='Marca',  copy=False)
    modelo = fields.Char(string='Modelo',  copy=False)
    instrumento = fields.Many2one('instrumento',string='Equipo', required=True)
    tipo = fields.Many2one('tipo_instr',string='Tipo')
    rango_ini = fields.Float(string='Minimo')
    rango_fin = fields.Float(string='Maximo')
    funciona = fields.Boolean(string='Funcionando', required=True)
    estado = fields.Selection([("B","Bien"),("R","Regular"),("M","Mal")], string='Estado', required=True)
    tiene_certificado = fields.Boolean(string='Certificado p/Uso')
    certificado = fields.Char(string='Certificado',  copy=False)
    description = fields.Text(string='Descripción', copy=False)
    expiry_date = fields.Date(string='Fecha', copy=False)
    employee_ref = fields.Many2one('hr.employee', domain="[('department_id.name', '=', 'Servicios Técnicos')]", default = lambda self: self._default_resp(), required=True, string="Responsable")
    # employee_ref = fields.Many2one('hr.employee', required=True, index=True, copy=False, string="Responsable")
    dpto_ref=fields.Many2one('hr.department', invisible=0, required=True, index=True, copy=False, string="Instalación")
    dias = fields.Integer(compute='_compute_dias', string='Fecha Advertencia', search='_value_search')
    mensaje = fields.Boolean(string='Enviar Mensaje',required=False,readonly=False,index=False,default=True)
    division_id=fields.Many2one(related='dpto_ref.division_id',store=True)
    um_id = fields.Char(related='instrumento.u_medida',string='U. de Medida')

    def _default_resp(self):
        resps=self.env['hr.employee'].search([('department_id.name', '=', 'Servicios Técnicos')])
        return min(rec.id for rec in resps )

    @api.depends('expiry_date')
    def _compute_dias(self):
        for record in self:
            today = fields.Date.from_string(fields.Date.today())
            renew_date = fields.Date.from_string(record.expiry_date)
            diff_time = (renew_date - today).days
            record.dias = diff_time

    @api.multi
    def _value_search(self,operador,value):
        op={"==" : operator.eq ,"<":operator.lt,">":operator.ge}
        funcion=op[operador]
        recs=self.search([]).filtered(lambda x: funcion(x.dias, value))
        if recs:
            return [('id','in',[x.id for x in recs])]  


# class HrEmployeePrecios(models.Model):
#     _inherit = 'hr.employee'
#     es_precios_dpto=fields.Boolean(string='Lleva Precios',required=False,readonly=False,index=False,default=False)


# class HrDpto(models.Model):
#     _inherit = 'hr.department'

#     @api.multi
#     @api.depends('document_ids')
#     def _document_count(self):
#         for each in self:
#             document_ids = self.env['hr.certificado.comercial'].search([('dpto_ref', '=', each.id)])
#             each.document_count = len(document_ids)

#     @api.multi
#     def document_view(self):
#         self.ensure_one()
#         domain = [
#             ('dpto_ref', '=', self.id)]
#         return {
#             'name': _('Documents'),
#             'domain': domain,
#             'res_model': 'hr.certificado.comercial',
#             'type': 'ir.actions.act_window',
#             'view_id': False,
#             'view_mode': 'tree,form',
#             'view_type': 'form',
#             'help': _('''<p class="oe_view_nocontent_create">
#                            Click para crear nuevos documentos
#                         </p>'''),
#             'limit': 80,
#             'context': "{'dpto_visible': False, 'default_dpto_ref': '%s'}" % self.id
#         }

#     document_count = fields.Integer(compute='_document_count', string='# Certificados', store=True)
#     tipo = fields.Selection(
#         string='Tipo',
#         required=True,
#         readonly=False,
#         index=False,
#         default=False,
#         help=False,
#         selection=[('venta','Venta'), ('administracion','Administracion')]
#     )
#     direccion = fields.Text(string='Direccion')
#     document_ids=fields.One2many(comodel_name='hr.certificado.comercial', inverse_name='dpto_ref')
   

# class HrCcomercialAttachment(models.Model):
#     _inherit = 'ir.attachment'

#     doc_attach_rel = fields.Many2many('hr.certificado.comercial', 'doc_attachment_id', 'attach_id3', 'doc_id',
#                                       string="Adjunto", invisible=1)
