import shipment_utility
from openerp.osv import fields, osv

class account_invoice(osv.osv):
    """
    Modified account.invoice
    """
    _inherit = "account.invoice"

    _columns = {
        'shipment_id': fields.many2one('shipment', 'Shipment', help="Shipment"),
        'ramport_notes': fields.text('Ramport Notes', help="Ramport Key"),

    }