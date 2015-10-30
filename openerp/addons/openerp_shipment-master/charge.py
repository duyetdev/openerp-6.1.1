import logging
import shipment_utility
from openerp.tools.translate import _
from osv import fields,osv

_logger = logging.getLogger(__name__)

list_transit_time = []
for i in range(1,365):
    if i == 1 :
        list_transit_time.append((i,str(i) + ' Day'))
    else:
        list_transit_time.append((i,str(i) + ' Days'))


#here generating the charges key which will be act as a unique key
def _generate_unique_key(self, cr, uid, ids, field_name, arg, context=None):
    result = {}
    for record in self.browse(cr, uid, ids, context=context):
        unique_key = str(record.port_lading_id.id) + '-' + str(record.port_unlading_id.id) + '-' + \
                     str(record.type) + '-' + str(record.mode) + '-' + str(record.via)
        result[record.id] = unique_key
        domain = [('name', '=', unique_key)]
        ids = self.search(cr, uid, domain, context=context)
    return result


class shipment_charge(osv.osv):
    _name = 'shipment.charge'
    _rec_name = 'mode';
    _columns = {
        'port_lading_id': fields.many2one('shipment.port', 'Port Lading', required=True,
                                          domain=[('port_lading', '=', 1)], store=True),

        'port_unlading_id': fields.many2one('shipment.port', 'Port Unlading', required=True,
                                            domain=[('port_unlading', '=', 1)], store=True),

        'sister_port_lading': fields.many2one('shipment.port', 'Sister Port Lading', domain=[('port_lading', '=', 1)]),

        'sister_port_unlading': fields.many2one('shipment.port', 'Sister Port Unlading',
                                                domain=[('port_unlading', '=', 1)]),

        'shipment_charge_price_ids': fields.one2many ('shipment.charge.price', 'shipment_charge_id', 'Container Quote'),

        'type': fields.selection(shipment_utility.list_load_type, 'Type', required=True,
                                 help="Select Full Or loose Freight"),

        'mode': fields.selection(shipment_utility.list_mode, 'Mode', required=True,
                                 help="Mode Of Container shipment"),

        'transit_time': fields.selection(list_transit_time, 'Transit Time', required=True, help="Transit Time In days"),

        'via':  fields.char('Via', size=64, help="Route , Via"),
        'forwarder_id': fields.many2one('res.partner', 'Freight Forwarder', domain=[('is_freight_forwarder', '=', 1)]),
        'carrier_id': fields.many2one('res.partner', 'Carrier', domain=[('is_carrier', '=', 1)]),

        'expiry_date': fields.date('Expiry Date',size=30, required=True, help='expiry date of this rates/charges after '
                                                                              'this date charges ma be differ.'),
        'notes': fields.text('Notes', help='Notes Extra Information'),
        #'charges_key':  fields.function(_generate_unique_key,type='char', method=True,
        #                                string='charges_key', help="Charges key is a unique key for charges with "
        #                                                           "combination of POL, POD, Agent, Supplier, Via, "
        #                                                           "Mode separated with hyphens"),
        'charges_key':  fields.char('Charge Key', size=64, help="Charges key is a unique key for charges with "
                                                                 "combination of POL, POD, Agent, Supplier, Via, "
                                                                 "Mode separated with hyphens"),
    }

    _sql_constraints = [
        #('charges_key_unique', 'unique (charges_key)','The Charges key is not Unique'),
        ('charges_key_unique', 'unique (port_lading_id, port_unlading_id, type, mode, via)',
         'Charges for these set is already defined')
    ]

    #here generating the charges key which will be act as a unique key
    def onchange_generate_unique_key(self, cr, uid, ids, port_lading_id, port_unlading_id, type, mode, via):
        _logger.warning("IMPORT-LOG : in onchange function")
        charges_key = str(port_lading_id) + '-' + str(port_unlading_id) + '-' + (str(type) or "#") + '-' + str(mode) + '-' + str(via)
        return {'value': {'charges_key': charges_key}}

    #function to create sister port of lading and sister port of unlading for selected port
    def update_sister_ports(self, cr, uid, vals):
        _logger.warning("IMPORT-LOG : Update sister function")
        obj_port = self.pool.get('shipment.port')
        if vals.get('port_lading_id', False):
            port_lading_id = obj_port.search(cr, uid, [('id', '=', vals['port_lading_id'])])
            port_lading_rec = obj_port.browse(cr, uid, port_lading_id[0])
            if port_lading_rec.sister_port:
                vals['sister_port_lading'] = port_lading_rec.sister_port.id
            else:
                vals['sister_port_lading'] = ''

        if vals.get('port_unlading_id', False):
            port_unlading_id = obj_port.search(cr, uid, [('id', '=', vals['port_unlading_id'])])
            port_unlading_rec = obj_port.browse(cr, uid, port_unlading_id[0])
            if port_unlading_rec.sister_port:
                vals['sister_port_unlading'] = port_unlading_rec.sister_port.id
            else:
                vals['sister_port_unlading'] = ''

        return vals


    def create(self, cr, uid, vals, context=None):
        _logger.warning("shipment_charge create function " + str(vals))
        new_vals = self.update_sister_ports(cr, uid, vals)
        _logger.warning("new " + str(new_vals))
        res = super(shipment_charge, self).create(cr, uid, new_vals, context)
        return res


    def write(self, cr, uid, ids, vals, context=None):
        new_vals = self.update_sister_ports(cr, uid, vals)
        return super(shipment_charge, self).write(cr, uid, ids, new_vals, context)



class shipment_charge_price(osv.osv):
    _name = 'shipment.charge.price'
    _columns = {
        'container_size_id': fields.many2one('shipment.container.size', 'Container Size', store=True),
        'amount': fields.float('Amount', required=True, help="file"),
        'shipment_charge_id': fields.many2one('shipment.charge', 'Quote', select=True),
        'notes': fields.text('Notes', help='Notes Extra Information'),
    }


class shipment_container_size(osv.osv):
    _name = 'shipment.container.size'
    _columns = {
        'name': fields.char('Name',required=True, size=64, help="Name"),
        'container_size':  fields.char('Container Size', required=True, size=64, help="Container Size"),
        'notes': fields.text('Notes', help='Notes Extra Information'),
    }

    _sql_constraints = [
        ('container_size_unique', 'unique (container_size)','Container Size already Present'),
    ]