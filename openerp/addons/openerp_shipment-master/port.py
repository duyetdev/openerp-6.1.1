import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

class shipment_port(osv.osv):
    _name = 'shipment.port'
    _columns = {
        'port_lading': fields.boolean('Port Of Lading', help="Check this box if it is Port of lading"),
        'port_unlading': fields.boolean('Port Of UnLading', help="Check this box if it is Port of Unlading"),
        'ramport_key': fields.integer('Ramport Key'),
        'name': fields.char('Name', size=64, help="Name Of The Port"),
        'sister_port': fields.many2one('shipment.port', 'Sister Port', store=True),
        'type': fields.char('Type', size=2, help="Type Of Port"),
        'phone': fields.char('Phone', size=64),
        'fax': fields.char('Fax', size=64),
        'website': fields.char('Website', size=64, help="Website Of Port"),
        'username': fields.char('Username', size=64, help="Login Credentials "),
        'password': fields.char('Password', size=64, help="Login Credentials"),
        '3461_7501': fields.boolean('Use in 3461 7501', help="Check this if it is used for 3461 7501"),
        'notes': fields.text('Notes', help='Notes Extra Information'),
    }

    _sql_constraints = [
        ('ramport_key_unique', 'unique (ramport_key)', 'The Ramport Key Must Be Unique'),
    ]

    #change function to define listing of sister port according to selection
    def on_change_get_sister_port(self, cr, uid, ids, port_lading, port_unlading, context=None):
        sids = self.pool.get('shipment.port').search(cr, uid, [('port_lading','=',port_lading),('port_unlading','=',port_unlading)])
        _logger.warning("MYLOG :" + str(port_lading))
        _logger.warning("MYLOG :" + str(port_unlading))
        _logger.warning("MYLOG : here")
        return {'domain':{'sister_port':[('id', 'in', sids)]}}