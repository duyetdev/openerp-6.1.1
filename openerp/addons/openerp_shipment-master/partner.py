import shipment_utility
from openerp.osv import fields, osv

class res_partner(osv.osv):
    """
    inherited product.product
    """
    _inherit = "res.partner"

    _columns = {
        'is_freight_forwarder': fields.boolean('Freight Forwarder', help="Freight Forwarder"),
        'is_carrier': fields.boolean('Carrier', help="Carrier"),
        'ramport_key': fields.char('Ramport Key', size=128, help="Ramport Key"),
        'erp_id': fields.integer('Old Erp ID', help="Old ERP database ID"),
        'ramport_notes': fields.text('Ramport Notes', help="Ramport Key"),

    }



class ir_attachment(osv.osv):
    """
    Inherited  ir.attachment
    """
    _inherit = "ir.attachment"

    _columns = {
        'shipment_id': fields.many2one('shipment', 'Shipment', select=True),
    }