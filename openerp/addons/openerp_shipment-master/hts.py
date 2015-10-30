import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_hts(osv.osv):
    _name = 'shipment.hts'
    _rec_name = 'description'
    _columns = {
        'section': fields.char('Section', size=10, help="Name Of The Section"),
        'chapter': fields.char('Chapter', size=5, help="Chapter", required="True"),
        'heading': fields.char('Heading', size=5, help="Heading", required="True"),
        'hts_heading_id': fields.many2one('shipment.hts', 'HTS Heading', store=True),
        'suffix': fields.char('Suffix', size=2, help="Suffix"),
        'hts': fields.char('HTS', size=2, help="HTS"),
        'u1': fields.char('U1', size=2, help="U1"),
        'order': fields.char('Order', size=5, help="Order"),
        'description': fields.text('Description', help="Description", required="True"),
        'unit': fields.char('Unit', size=20, help="Unit"),
        'general': fields.text('General', help="General"),
        'special': fields.text('Special', help="Special"),
        'other': fields.text('Other', help="Other"),
    }