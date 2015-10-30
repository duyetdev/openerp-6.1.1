This read me tells the logic of shipment module in brief

1)openerp-scripts -> Importing data from ramport the legacy system
from ramport first its insert/update shipment_ramport table (it act as cache table )

2)from shipment_ramport table it fetches the data and insert/update the corresponding table which includes
 shipment_abi_results           -- table for abi results for shipments
 shipment                       -- table for shipments/files
 shipment_statements            -- table for statements invoice recd from US custom
 shipment_statements_entries    -- table for line items paid for shipments to US customs (related to shipment_statements)


 3)custom statements can be update by excluding line items till its state=draft
    once validate then the statement becomes open which can be transferred to supplier invoices for payments

 4)on validation of statements , every included line items is a expense for shipment which can be identified by its
 entry number (i.e,shipment->entry_number = shipment_statements_entries->entry_number )
 which we are inserting into shipment_expense

 shipment_expense table info
 name - the expense name
 amount -  amount of expense
 statement number- if expense is duties and fees
 check_number - if statement is paid
 statement_paid_on- date if statement paid
 notes -  for extra information


