import logging
import shipment_utility
from osv import fields,osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class shipment_statements(osv.osv):
    _name = 'shipment.statements'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _track = {
        'state': {
            'shipment.mt_shipment_statement_confirmed': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['draft', 'open'],
            'shipment.mt_shipment_statement_invoice': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['billed']
        }
    }

    def _compute_total(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for stat in self.browse(cr, uid, ids, context=context):
            res[stat.id] = {
                'revised_total': 0,
            }
            val = 0
            for line in stat.entry_ids:
                if not line.exclude:
                    val += line.tot_amt
            res[stat.id] = val
        return res

    _columns = {
        'name': fields.char('Name', size=50, help="Name of the statement"),
        'inv_num': fields.char('Invoice Number', size=15, help="Invoice number of the statement"),
        'type': fields.char('Type', size=20, help="Type of the statement"),
        'date': fields.date('Date', size=30, help="Statement date"),
        'port': fields.char('Port',size=30),
        'broker': fields.char('Broker',size=30),
        'tot_est_duty': fields.float('Estimate Duty'),
        'merc_fee': fields.float('Merchandise Fee'),
        'merc_sur_fee': fields.float('Merchandise Surcharge Fee'),
        'ww_fee': fields.float('Waterways Fee'),
        'tot_amt_due': fields.float('Total Amount Due', track_visibility='always'),
        'tot_usr_fee': fields.float('Total User Fees', track_visibility='always'),
        'expiry_date': fields.date('Expiry Date',size=30, help='expiry date of the statement'),
        'notes': fields.text('Notes', help="Description", track_visibility='always'),
        'entry_ids': fields.one2many('shipment.statements.entries', 'entry_id', 'Entry Lines'),
        'revised_total': fields.function(_compute_total, type='float', string=' Revised Total', track_visibility='always'),
        'state': fields.selection(shipment_utility.list_custom_state, 'Status'),
        'invoice_id': fields.many2one('account.invoice', 'Invoice ID', help="invoice id if Generated"),
        'check_number': fields.char('Check Number', size=30,help="check number"),
        'check_date': fields.date('Check Date', help='check date'),

    }

    _defaults = {
        'state': 'draft',
        #'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }

    def generate_statement_invoice(self, cr, uid, ids, context=None):
        """
        This function generate Invoice for the passed custom statement , and update field to billed
        and return true
        """
        _logger.info("Function generate_statement_invoice")
        config_model = self.pool.get('shipment.config.settings')
        config_ids = config_model.search(cr, uid, [])
        if not config_ids:
            raise osv.except_osv(_('Error!'), _('Please Set Defaults Ids in Shipment Config.'))
        config_rec = config_model.browse(cr, uid, config_ids[0], context)

        #checking all parameters set in config or not
        """        """
        if not config_rec.default_us_custom_id.id or config_rec.default_us_custom_id.id == 1:
            raise osv.except_osv(_('Error!'), _('Us Custom Supplier is not set.\nPlease set in shipment config'))

        if not config_rec.default_invoice_account_id.id:
            raise osv.except_osv(_('Error!'), _('Invoice Account Id Is not set.\nPlease set in shipment config'))

        if not config_rec.default_invoice_journal_id.id:
            raise osv.except_osv(_('Error!'), _('Invoice Journal Id Is not set.\nPlease set in shipment config'))

        if not config_rec.default_invoice_line_account_id.id:
            raise osv.except_osv(_('Error!'), _('Invoice Line Account Id Is not set.\nPlease set in shipment config'))

        if not config_rec.default_invoice_line_product_id.id:
            raise osv.except_osv(_('Error!'), _('Invoice Product.\nPlease set in shipment config'))

        _logger.info("US statement set")
        this = self.browse(cr, uid, ids, context=context)[0]
        new_account_invoice = {
            'partner_id': config_rec.default_us_custom_id.id,
            'account_id': config_rec.default_invoice_account_id.id,
            'commercial_partner_id': config_rec.default_us_custom_id.id,
            'type': 'in_invoice',
            'journal_id': config_rec.default_invoice_journal_id.id,
            'date_invoice': this.date,
            'reference': this.inv_num,
            'amount_total': this.revised_total,
        }

        invoice_obj = self.pool.get('account.invoice').create(cr, uid, new_account_invoice)

        new_account_invoice_line = {
            'account_id': config_rec.default_invoice_line_account_id.id,
            'name': 'Us custom statements',
            'price_unit': this.revised_total,
            'price_subtotal': this.revised_total,
            'company_id': 1,
            'quantity': 1,
            'partner_id': config_rec.default_us_custom_id.id,
            'invoice_id': invoice_obj,
            'product_id': config_rec.default_invoice_line_product_id.id
        }
        invoice_line_obj = self.pool.get('account.invoice.line').create(cr, uid, new_account_invoice_line)
        statement_entries = this.entry_ids
        _logger.info("st e" + str(statement_entries))

        self.write(cr, uid, ids, {'state': 'billed', 'invoice_id': invoice_obj})
        return True

    def view_statement_invoice(self, cr, uid, ids, context=None):
        """
        This function returns an action that display existing invoice id for given customs statements in a form view.
        you can check addons/sale_stock/sale.stock.py line 167
        """
        _logger.info("Function view_statement_invoice")
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        inv_id = self.browse(cr, uid, ids, context=context)[0].invoice_id.id
        if inv_id:
            res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_supplier_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = inv_id or False
        else:
            raise osv.except_osv(_('Error!'), _('Some Error Occurred.\nInvoice Id Not generated.'))

        return result


    def validate_statement(self, cr, uid, ids, context=None):
        """
        This functions Validate the custom statement and update the state draft to open and returns true
        """
        obj_shipment_model = self.pool.get('shipment')
        obj_shipment_statement_entry_model = self.pool.get('shipment.statements.entries')
        obj_shipment_expense = self.pool.get('shipment.expense');

        this = self.browse(cr, uid, ids, context=context)[0]
        if not this.revised_total:
            raise osv.except_osv(_('Error!'), _('Statement cannot be validated as revised !\n as there is no entries'))
        statement_entries = this.entry_ids
        for entry in statement_entries:
            if entry.entry_num and not entry.exclude:
                #here extracting the shipment number from entry_number of line items
                #entry number are like EJ2-0116199-2 ,  880-0116199-2 ,
                file_number = int(entry.entry_num.split('-')[1])
                searched_shipment_ids = obj_shipment_model.search(cr, uid, [('file_number', '=', file_number)])
                _logger.info("count " + str(len(searched_shipment_ids)))

                if len(searched_shipment_ids) == 1:
                    shipment_rec = obj_shipment_model.browse(cr, uid, searched_shipment_ids[0])
                    new_shipment_expenses = {
                        'name': 'Us Custom Duties',
                        'shipment_id': shipment_rec.id,
                        'amount': entry.tot_amt,
                        'statement_id': entry.entry_id.id,
                        'notes': 'Expense Added on Statement ' + entry.entry_id.inv_num + ' Confirmation',
                    }
                    insert_id = obj_shipment_expense.create(cr, uid, new_shipment_expenses)

                    obj_shipment_statement_entry_model.write(cr, uid, entry.entry_id.id,
                                                                  {'shipment_id': shipment_rec.id})

                    _logger.info("new_shipment_expenses " + str(new_shipment_expenses))
                else:
                    #raise osv.except_osv(_('Error!'), _('Multiple File found for ' + str(file_number)))
                    _logger.info('ShipmentError:validate_statement' + 'Multiple or No File found for ' + str(file_number))

        self.write(cr, uid, ids, {'state': 'open'})
        return True

    def browse_url(self, cr, uid, ids, context=None):
        module_name = str(self._name)
        new_url = 'http://localhost:4444/' + module_name.replace('.', '_') + '/' + str(ids[0])

        return {
            'type': 'ir.actions.act_url',
            'url': new_url,
            'target': 'new'
        }



class shipment_statements_entries(osv.osv):
    _name = 'shipment.statements.entries'
    _columns = {
        'entry_num': fields.char('Entry#', size=50, help="Entry number of the shipment"),
        'tp': fields.char('TP#', size=2),
        'st': fields.char('ST#', size=2),
        'est_duty': fields.float('Estimate Duty'),
        'est_tax': fields.float('Estimate Tax'),
        'est_cvd': fields.float('Estimate CVD'),
        'est_ada': fields.float('Estimate ADA'),
        'usr_fee': fields.float('User Fees/Interest'),
        'tot_amt': fields.float('Total Amount'),
        'dty_st': fields.float('DTY ST'),
        'entry_id': fields.many2one('shipment.statements', 'Entry Lines', select=True),
        'exclude': fields.boolean('Exclude', help="Excluded"),
        'shipment_id': fields.many2one('shipment', 'Shipment', help="shipment number id statement validated"),
    }

    _defaults = {
        'exclude': False,
    }