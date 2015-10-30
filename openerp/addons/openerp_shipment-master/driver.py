import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_driver(osv.osv):
    _name = 'shipment.driver'
    _columns = {
        'name': fields.char('Name', size=30, help="Name", required="True"),
        'license_number': fields.char('License Number', size=30, help="License Number", required="True"),
        'license_exp_date': fields.date('License Expiry Date', size=30, help='License Expiry Date'),
        'driver_class': fields.selection(shipment_utility.list_driver_class, 'Driver Class'),
        'hazardous': fields.boolean('Hazardous', help="hazardous"),
        'tags_ids': fields.many2many('shipment.tags', id1='driver_id', id2='tag_id', string='Tags'),
        'drug_test_program': fields.text('Drug Test Program', help="Drug Test Program Description"),
        'last_drug_test_date': fields.date('Last Drug Test Date', size=30, help='Last Drug Test Date'),
        'truck_permit': fields.text('Truck Permit', help="Truck Permit Description"),
        'broker_id': fields.many2one('res.partner', 'Insurance Broker', domain=[('supplier', '=', 1)],
                                     help='Insurance broker is supplier'),
        'insurance_exp_date': fields.date('Insurance Expiry Date',size=30, help='Insurance Expiry Date'),
        'truck_id': fields.many2one('shipment.truck', 'Truck', select=True),
        #'truck_ids': fields.many2many('shipment.truck', 'shipment_truck_driver_rel','truck_id', 'driver_id','Truck'),
        'active': fields.boolean('Active', help="Active"),
    }

    _sql_constraints = [
        ('license_number_unique', 'unique (license_number)','License Number already Present'),
    ]
