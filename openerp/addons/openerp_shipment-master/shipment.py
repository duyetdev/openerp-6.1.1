import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_shipment(osv.osv):
    _name = 'shipment'
    _rec_name = 'file_number'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns = {
        'file_number': fields.char('Shipment Number', size=30, required=True, help=' shipment number'),
        'entry_number': fields.char('Entry Number', size=30, help=' entry number'),
        'carrier': fields.many2one('res.partner', 'Carrier', domain=[('supplier', '=', True)], store=True,
                                   help="shipper"),
        'entry_type': fields.selection(shipment_utility.list_shipment_entry_type, 'Entry Type'),
        'est_vessel_arrival_date': fields.date('Est. Vessel. Arrival Date', size=30, help='ETA'),
        'est_vessel_dep_date': fields.date('Est Vessel Departure Date', size=30, help=' est. vessel departure date'),
        'arrival_date': fields.date('Arrival Date', size=30, help=' shipment arrival date/ETA'),
        'customs_status': fields.selection(shipment_utility.list_customs_status, 'Customs Status'),
        'usda_status': fields.selection(shipment_utility.list_usda_status, 'USDA Status'),
        'fda_status': fields.selection(shipment_utility.list_fda_status, 'FDA Status'),
        'cst': fields.integer('CST Assignment', help=' cst assignment'),
        'importer': fields.many2one('res.partner', 'Importer', domain=[('customer', '=', True)], store=True),
        'importer_number': fields.char('Importer Number', size=30, required=True, help=' importer number'),
        'bill_to': fields.many2one('res.partner', 'Bill To', domain=[('customer', '=', True)], store=True),
        'consignee': fields.many2one('res.partner', 'Consignee', domain=[('customer', '=', True)], store=True),
        'reference_num': fields.char('P.O. Number', size=60, help='po#/Po'),
        'lfd': fields.date('LFD', size=30, help='Last Free Date / LFD'),
        'scac_code': fields.char('SCAC Code', size=30, help=' scac code / master'),
        'hbl_scac_code': fields.char('HBL SCAC Code', size=30, help=' HBL SCAC'),
        'sub_house_forwarder': fields.char('Sub House Forwarder', size=30, help='shf forwarder'),
        'bl_num': fields.char('BL Number', size=30, help=' bill of lading master / mbl'),
        'house_bill_num': fields.char('House Bill Number', size=30, help=' house bill number / hbl'),
        'sub_house_bill_num': fields.char('Sub House Bill Number', size=30, help='sub house bill number / shbl'),
        'vessel_name': fields.char('Vessel Name', size=30, help=' vessel name / steamship line'),
        'vessel_code': fields.char('Vessel Code', size=30, help=' vessel code'),
        'steamship_phone': fields.char('Phone', size=30, help='steamship line phone number'),
        'forwarder': fields.many2one('res.partner', 'Freight Forwarder', domain=[('supplier', '=', True)], store=True),
        'forwarder_phone': fields.char('Phone', size=30, help='forwarder phone'),
        'trucker': fields.many2one('res.partner', 'Trucker', domain=[('supplier', '=', True)], store=True),
        'trucker_phone': fields.char('Phone', size=30, help='Trucker phone'),
        'exam_loc': fields.many2one('res.partner', 'Exam Site', domain=[('parent_id', '!=', False)], help='Location'),
        'exam_loc_phone': fields.char('Exam Loc Phone', size=30, help='Exam Location phone'),
        'good_loc': fields.many2one('res.partner', 'Location', domain=[('parent_id', '!=', False)], help='Location'),
        'good_loc_phone': fields.char('Goods Loc Phone', size=30, help='Good Location phone'),
        'isf_number': fields.char('ISF Number', size=30, help=' isf number'),
        'isf_date': fields.date('ISF Date', size=30, help='Isf Filed'),
        'entry_date': fields.date('Entry Date', size=30, help='Date Entry Filed'),
        'entry_delivery_date': fields.date('Delivery Date', size=30, help='Date Entry Delivered'),
        'fda_date': fields.date('FDA Filed', size=30, help='Date FDA Filed'),
        'fda_delivery_date': fields.date('Delivery Date', size=30, help='Date FDA Delivered'),
        'usda_date': fields.date('USDA Filed', size=30, help='Date USDA Filed'),
        'usda_delivery_date': fields.date('Delivery Date', size=30, help='Date USDA Delivered'),
        'date_7501': fields.date('Date 7501', size=30, help='date 7501 filed'),
        'voyage': fields.char('Voyage', size=30, help=' voyage'),

        'date_received': fields.date('Date Received', size=30,  help=' date received'),
        'date_3461': fields.date('Date 3461', size=30, help=' shipment 3461 date'),
        'firm_code': fields.char('Firm Code', size=30, help=' location'),
        'date_of_exportation': fields.date('Exportation Date', size=30, help=' shipment exportation date'),
        'ams_bill_num': fields.char('AMS Bill Number', size=30, help=' AMS Bill Number'),
        'description': fields.text('Description', help=' shipment description'),
        'status': fields.selection(shipment_utility.list_status, 'Status'),
        'packages': fields.integer('No. of Packages', help=' number of packages'),
        'country_of_origin': fields.many2one('res.country', 'Country of Origin', store=True),
        'old_country_code': fields.char('country code old', size=30, help='country code coming from ramport'),
        'abi_results_ids': fields.one2many ('shipment.abi.results', 'shipment_id', 'ABI Results'),
        'documents': fields.one2many('ir.attachment', 'shipment_id', 'Documents'),
        'invoices': fields.one2many('account.invoice', 'shipment_id', 'Invoices'),
        'shipment_exp_ids': fields.one2many('shipment.expense', 'shipment_id', 'Shipment Expenses'),
    }

class shipment_expense(osv.osv):
    _name = 'shipment.expense'
    _columns = {
        'name': fields.char('Expense Head', size=30, help='Name of expense', required="True"),
        'shipment_id': fields.many2one('shipment', 'Shipment'),
        'amount': fields.float('Amount Paid'),
        'statement_id': fields.many2one('shipment.statements','Statement No.'),
        'check_number': fields.char('Check Number', size=30, help='check Number by which statement is being paid'),
        'paid_date': fields.date('Check Date', help='date on which check paid'),
        'notes': fields.text('Note', help='Description or any extra info'),
    }