import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_abi_results(osv.osv):

    _name = 'shipment.abi.results'

    _columns = {
        'file_number': fields.char('File Number',size=50,required=True, help='the shipment number'),
        'date_time': fields.date('Date Time',size=30, help='the date time'),
        'line': fields.text('Line', required=True, help='the text data from ramport'),
        'status': fields.char('Status',size=30,required=True, help='the status of import'),
        'shipment_id': fields.many2one('shipment', 'Shipment', select=True),
    }

    #abi_results()


