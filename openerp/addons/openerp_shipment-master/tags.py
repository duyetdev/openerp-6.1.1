import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)


class shipment_tags(osv.osv):
    _name = 'shipment.tags'
    _columns = {
        'name':fields.char('Name',size=30, help="Name", required="True"),
        'description':fields.text('Description', help="", ),
        'total_count':fields.integer('Count', help=""),
    }