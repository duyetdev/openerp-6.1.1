import logging
import shipment_utility
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class shipment_config_settings(osv.osv_memory):
    _name = 'shipment.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
        'default_us_custom_id': fields.many2one('res.partner', 'Us Customs', domain=[('supplier', '=', 1)], help='Select The Us Customs For Generation of Custom statements Invoices'),
        'default_invoice_account_id': fields.many2one('account.account', 'Invoice Account',),
        'default_invoice_journal_id': fields.many2one('account.journal', 'Invoice Journal',),
        'default_invoice_line_account_id': fields.many2one('account.account', 'Invoice line Account',),
        'default_invoice_line_product_id': fields.many2one('product.product', 'Default Product',),
    }

    _defaults = {
        'default_us_custom_id': 1,
        #'default_invoice_account_id': "",
    }

    def get_default_us_custom_id(self, cr, uid, fields, context=None):
        search_ids = self.search(cr, uid, [])
        first_id = search_ids and min(search_ids)
        _logger.warning("ids " + str(search_ids))
        if not search_ids:
            return {'default_us_custom_id': ''}
        us_customs = self.browse(cr, uid, first_id, context)
        res = {}
        for field in fields:
            #_logger.warning("field " + str(field))
            res[field] = getattr(us_customs, field).id
        return res

    """def set_default_username(self, cr, uid, ids, context=None):
        #some code...
        #you can get the field content from some table and return it
        #as a example
        config = self.browse(cr, uid, ids[0], context)
        new_username = config.default_us_custom_id.id
        self.pool.get('shipment.config.settings').write(cr, uid, uid, {'default_us_custom_id': new_username})

class shipment_config_settings_wizard(osv.osv_memory):
    _name = 'shipment.config.settings.wizard'
    _inherit = 'shipment.config.settings'
    _columns = {
        'default_us_custom_id': fields.many2one('res.partner', 'Us Customs', default_model='res.config.settings'),
    }"""


    def create(self, cr, uid, values, context=None):
        search_ids = self.search(cr, uid, [])
        first_id = search_ids and min(search_ids)
        #us_customs = self.browse(cr, uid, first_id, context)
        #_logger.warning("us custom " + str(us_customs.default_us_custom_id.name))
        res = {}
        #for field, val in values.iteritems():
        #    #_logger.warning("key = %s, val = %s" % (field, val))
        #    res[field] = val
        # DOWN STATEMENT IS DOING THE SAME WORK AS ABOVE COMMENTED LOOP
        res.update(values)
        if not first_id:
            return super(shipment_config_settings, self).create(cr, uid, res, context)

        self.write(cr, uid, first_id, res)
        return first_id