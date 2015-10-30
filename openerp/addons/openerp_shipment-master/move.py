import logging
import shipment_utility
from osv import fields,osv

_logger = logging.getLogger(__name__)

list_wait_time = []
for i in range(0, 24):
    for m in range(0, 60, 15):
        if (i != 0) or (m != 0):
            temp_var = str(i).rjust(2, '0') + ':' + str(m).rjust(2, '0')
            list_wait_time.append((temp_var, temp_var))

class shipment_move(osv.osv):
    _name = 'shipment.move'
    #_rec_name = 'job_number'
    _columns = {
        'job_id': fields.many2one('shipment.job', 'Job Number', help="Job Number"),
        #relation with container module m2o
        'move': fields.integer('Move Number', help="Move Number for the job"),
        'type': fields.selection(shipment_utility.list_move_type, 'Type'),
        'status': fields.selection(shipment_utility.list_jobs_status, 'status'),
        'driver_id': fields.many2one('shipment.driver', 'Driver', help="Driver"),
        'truck_id': fields.many2one('shipment.truck', 'Truck', help="Truck"),
        'origin_loc':fields.many2one('res.partner','Origin', domain=[('parent_id', '!=', False)],
                                     help='Origin Address'),
        'destination_loc':fields.many2one('res.partner','Destination', domain=[('parent_id', '!=', False)],
                                     help='Destination Address'),
        'distance': fields.float('Distance', digits=(8,2)),
        'empty': fields.boolean('Empty', help="Is Empty"),
        'start_datetime': fields.datetime('Start Date', help='Start Date'),
        'end_datetime': fields.datetime('End Date', help='End Date'),
        'commission': fields.float('Commission', digits=(8,2)),
        'bobtail': fields.float('Bobtail', digits=(8,2)),
        'wait_time_comm': fields.float('Waittime Commission', digits=(8,2)),
        'wait_time': fields.selection(list_wait_time, 'Wait Time'),
        'notes': fields.text('Notes', help="Notes"),
        'billed': fields.boolean('Billed', help="Billed or not"),
    }