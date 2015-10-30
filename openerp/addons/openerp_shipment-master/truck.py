import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_truck(osv.osv):
    _name = 'shipment.truck'
    _rec_name = 'license_plate'
    _columns = {
        'license_plate': fields.char('License Plate', size=30, help="License Plate", required="True"),
        'state_id': fields.many2one('res.country.state', 'State'),
        'reg_exp_date': fields.date('Registration Expiry Date', size=30, help='Registration Expiry Date'),
        'bit_inspection': fields.text('Bit Inspection', help="Bit Inspection"),
        'broker_id': fields.many2one('res.partner', 'Insurance Broker', domain=[('supplier', '=', 1)],
                                     help='Insurance broker is supplier'),
        'insurance_details_text': fields.text('Insurance Details', help="Insurance details Description"),
        'insurance_exp_date': fields.date('Insurance Expiry Date', size=30, help='Insurance Expiry Date'),
        'maker_id': fields.many2one('shipment.truck.maker', 'Maker', select=True),
        'model_id': fields.many2one('shipment.truck.model', 'Model', select=True),
        'type_id': fields.many2one('shipment.truck.type', 'Type', select=True),
        'notes': fields.text('Notes', help="Notes"),
        'driver_ids': fields.one2many('shipment.driver', 'truck_id', 'Driver',select=True),

        #'documents': fields.one2many('ir.attachment','partner_id','Documents'),
    }

    _sql_constraints = [
        ('license_plate_unique', 'unique (license_plate)','License Number already Present'),
    ]


class shipment_truck_model(osv.osv):
    _name = 'shipment.truck.model'
    _columns = {
        'name': fields.char('Model Name', size=128, required=True),
        'description': fields.text('Description', help="Description"),
        'truck': fields.one2many('shipment.truck', 'model_id', 'Truck'),
    }


class shipment_truck_maker(osv.osv):
    _name = 'shipment.truck.maker'
    _columns = {
        'name': fields.char('Maker Name', size=128, required=True),
        'description': fields.text('Description', help="Description"),
        'truck': fields.one2many('shipment.truck', 'maker_id', 'Truck'),
    }


class shipment_truck_type(osv.osv):
    _name = 'shipment.truck.type'
    _columns = {
        'name': fields.char('Type Name', size=128, required=True),
        'description': fields.text('Description', help="Description"),
        'truck': fields.one2many('shipment.truck', 'type_id', 'Truck'),
    }