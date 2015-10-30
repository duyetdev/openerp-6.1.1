import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_ramport(osv.osv):

    _name = 'shipment.ramport'
    _rec_name = 'rid'

    _columns = {
        'table_name': fields.char('Table',size=50,required=True, help='the ramport table name'),
        'rid': fields.char('ID',size=50, help='the ramport id'),
        'line': fields.text('Line', required=True, help='the text data from ramport'),
        'status': fields.char('Status',size=30,required=True, help='the status of import'),
    }

    #ramport()


