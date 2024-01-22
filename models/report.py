# -*- coding: utf-8 -*-
import datetime

import dateutil
from dateutil import relativedelta

from odoo import models, fields, api
import xlsxwriter
from odoo.addons.xlsx_report_base.models.base_xlsx_report_model import ReportXlsx

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class GaugeReport(ReportXlsx):
    def build_xlsx_report(self, workbook, data, objs):

        equipos_query = """SELECT eq.id as id_equipo, eq.name as nombre_equipo, eq.u_medida as um_equipo FROM instrumento as eq"""
        self.env.cr.execute(equipos_query)
        equipos_map = self.env.cr.dictfetchall()

        divisiones_query =  """SELECT div.id as id_division, div.name as nombre_division FROM ventas_division as div"""
        self.env.cr.execute(divisiones_query)
        division_map = self.env.cr.dictfetchall()

        bold = workbook.add_format({'bold': 1, 'border': True})
        bold_only = workbook.add_format({'bold': 1})
        borde = workbook.add_format({'border': True})
        centrado = format = workbook.add_format({'border': True})
        format.set_text_wrap()

        format = workbook.add_format({'border': True})
        format.set_text_wrap()
        # format.set_bold(1)
        format.set_align('center')
        format.set_align('vcenter')
        
        dos_decimal_bold=workbook.add_format({'bold': 1,'num_format':'0.00'})
        dos_decimal=workbook.add_format({'num_format':'0.00'})
        for equipo in equipos_map:
            worksheet = workbook.add_worksheet(equipo['nombre_equipo'])
            i = 0
            for division in division_map:
 
                worksheet.merge_range(i, 0, i, 5, 'Palmares Sucursal Matanzas', bold_only)
                worksheet.merge_range(i+1, 0, i+1, 5, 'INVENTARIO DE EQUIPOS DE MEDICION POR DIVISIONES', bold_only)
                worksheet.write(i+1, 17, 'Fecha: %s' % data['current_date'].strftime("%d/%m/%Y"))
                worksheet.write(i+2, 0, 'División: %s' % division['nombre_division'])
                worksheet.write(i+3, 0, 'EQUIPO: %s' % equipo['nombre_equipo'])
                i+=4
                # Tabla
                # worksheet.merge_range(3, 2, 3, 4, 'Diario', format)
                # worksheet.merge_range(i, 0, i, 1, 'Departamentos', format)
                worksheet.merge_range(i, 0, i+1, 0, 'Unidad', format)
                if equipo['nombre_equipo'])=="Pesa":
                    worksheet.merge_range(i, 1, i+1, 1, 'Marca', format)
                    worksheet.merge_range(i, 2, i+1, 2,'Modelo', format)
                    worksheet.merge_range(i, 3, i+1, 3, 'Capacidad %s' % equipo['um_equipo], format)
                    worksheet.merge_range(i, 10, i+1, 10, 'Electronica(E), Mecanica(M)', format)
                else:
                    worksheet.merge_range(i, 1, i+1, 1, 'Tipo', format)
                    worksheet.merge_range(i, 2, i+1, 2,'Marca', format)
                    worksheet.merge_range(i, 3, i+1, 3, 'Rango %s' % equipo['um_equipo], format)

                worksheet.merge_range(i, 4, i, 5, 'Funciona', format)
                worksheet.write(i+1, 4, 'Si', format)
                worksheet.write(i+1, 5, 'No', format)

                worksheet.merge_range(i, 6, i+1, 6, 'Estado Tecnico (B,R,M)', format)

                worksheet.merge_range(i, 7, i, 8, 'Certificado p/uso', format)
                worksheet.write(i+1, 7, 'Si', format)
                worksheet.write(i+1, 8, 'No', format)

                worksheet.merge_range(i, 9, i+1, 9, 'Fecha', format)
                
                # worksheet.write(i, 9, 'Folio', format)
                # worksheet.write(i, 10, 'Asiento', format)
                # worksheet.write(i, 11, 'Observ', format)
                # worksheet.set_column(1,1,15)
                # worksheet.set_column(2,2,25)
                # worksheet.set_column(4,7,15)
                # worksheet.set_column(11,11,25)
                i +=2
                
                # Crear lista de equipos
                gauge_query="""SELECT dpto.name as nombre_dpto, g.marca as marca, g.modelo as modelo, t.name as tipo, g.rango_ini as rango_ini, 
                                g.rango_fin as rango_fin, g.funciona as funciona, g.estado as estado, g.tiene_certificado as certificado, g.fecha as fecha 
                                FROM gauge as g
                                LEFT JOIN hr_department as dpto ON g.dpto_ref=dpto.id
                                LEFT JOIN tipo_instr as t ON g.tipo=t.id
                                WHERE g.instrumento = %s AND g.division_id = %s
                                ORDER BY nombre_dpto
                            """ %(equipo['id_equipo'], division['id_division'])
                self.env.cr.execute(gauge_query)
                gauge_map = self.env.cr.dictfetchall()

                for gauge in gauge_map:
                    worksheet.write(i, 0, gauge['nombre_dpto'] ,format)
                    if equipo['nombre_equipo'])=="Pesa":
                        worksheet.write(i, 1, gauge['marca'],format)
                        worksheet.write(i, 2, gauge['modelo'],format)
                        worksheet.write(i, 3, str(gauge['rango_ini'])+"-"+str(gauge['rango_fin']),format)
                        worksheet.write(i, 10, gauge['tipo'],format)

                    else:
                        worksheet.write(i, 1, gauge['tipo'],format)
                        worksheet.write(i, 2, gauge['marca'],format)
                        worksheet.write(i, 3, str(gauge['rango_ini'])+"-"+str(gauge['rango_fin']),format)
                    if gauge['funciona']:
                        worksheet.write(i, 4, "X",format) 
                    else:
                        worksheet.write(i, 5, "X",format)       
                    worksheet.write(i, 6, gauge['estado'],format)  
                    if gauge['certificado']:
                        worksheet.write(i, 7, "X",format) 
                    else:
                        worksheet.write(i, 8, "X",format)                         
                    worksheet.write(i, 9, gauge['fecha'],format)   
                    i+=1
                i+=2  
        return "Equipos de medicion (%s)" % data['current_date'].strftime("%d-%m-%Y")               
GaugeReport('report.equipo_xlsx', 'gauge', store=True)
