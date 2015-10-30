import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_job(osv.osv):
    _name = 'shipment.job'
    #_rec_name = 'job_number'
    _columns = {
        'job_number': fields.char('Job Number', size=30, help="Job Number"),
        'client_id': fields.many2one('res.partner', 'Client', domain=[('customer', '=', 1)], help='Client/Customer'),
        'shipper_id': fields.many2one('res.partner', 'Client', domain=[('is_carrier', '=', 1)], help='Client/Customer'),
        'consignee': fields.many2one('res.partner', 'Consignee', domain=[('customer', '=', 1)], help='Client/Customer'),
        'bill_client_id': fields.many2one('res.partner', 'Bill To', domain=[('customer', '=', 1)], help='Client'),
        'payment_terms': fields.selection(shipment_utility.list_payment_terms, 'Terms Of Payment'),
        'status': fields.selection(shipment_utility.list_jobs_status, 'Status',required="True"),
        'load_type': fields.selection(shipment_utility.list_load_type, 'Load Type'),
        'date': fields.date('Date',size=30, help='Date'),
        'goods_type': fields.selection(shipment_utility.list_goods_type, 'Goods Type'),
        'description': fields.text('Description', help="Description"),
        'quantity': fields.integer('Quantity', help="Quantity"),
        'unit': fields.selection(shipment_utility.list_job_unit, 'Unit'),
        'palletized': fields.boolean('Palletized', help="Is Palletized"),
        'number_pallets': fields.integer('Number Of Pallets', help="Number Pallets Job Contain"),
        'per_diem': fields.boolean('Per Diem', help="Per Diem"),
        'container_type':fields.many2one('shipment.container.size', 'Container Size'),
        'seal_number': fields.char('Seal Number',size=30, help="Seal Number"),
        'chassis_number': fields.char('Chassis Number', size=30, help="Chassis Number"),
        #add Company Name
        'company_id': fields.many2one('res.company', 'Company', help='Client'),
        'vessel': fields.char('Vessel Number', size=30, help="Vessel Number"),
        'voyage': fields.char('Voyage Number', size=30, help="Voyage Number"),
        'master_bill': fields.char('Master Bill Number',size=30, help="Master Bill Number"),
        'house_bill': fields.char('House Bill Number', size=30,help="House Bill Number"),
        'scac_code': fields.char('Scac Code',size=30, help="Standard Carrier Alpha Code"),
        'pickup_loc':fields.many2one('res.partner','Pick Up Location', domain=[('parent_id', '!=', False)],
                                     help='PickUp Location'),
        'empty_pickup_loc':fields.many2one('res.partner','Empty PickUp Location', domain=[('parent_id', '!=', False)],
                                     help='Empty PickUp Location'),
        'destination_loc':fields.many2one('res.partner','Destination Location', domain=[('parent_id', '!=', False)],
                                     help='Destination Location'),
        'empty_return':fields.many2one('res.partner','Empty Return', domain=[('parent_id', '!=', False)],
                                     help='Empty Return Location'),
        'current_loc':fields.many2one('res.partner','Current Location', domain=[('parent_id', '!=', False)],
                                     help='Current Location'),
    }