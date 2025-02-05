from odoo import models, fields, api

class ResPartnerCustomerMetrics(models.Model):
    _name = 'res.partner.customer_metrics'  #  name for the model in db
    _description = 'Customer Metrics Dashboard'  # Description of the model
    _rec_name = "customer_id"  #  display name  for every records
    _order = 'total_sales desc, order_count desc'  # Default  order for records by total nad count
    
    # Fields
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)  
    # Link by the customer (res.partner)  -- and string='Customer' is display name of field  
    total_sales = fields.Float(string='Total Sales', compute='_compute_total_sales', store=True)  
    # Computed field for total sales  take method _compute_total_sales  and store it in db
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count', store=True)  
    # Computed field for order count take method _compute_order_count  and store it in db

    @api.depends('customer_id')  
    def _compute_total_sales(self):
        """
        Compute the total sales  depend on  customer_id.
        """
        for record in self:
            # loop for every record in this model instance
            sale_orders = self.env['sale.order'].search([('partner_id', '=', record.customer_id.id)])
            # Search for all sale.order by  the partner_id when = customer_id.id
            record.total_sales = sum(order.amount_total for order in sale_orders)
            # Sum amount_total method from model  of all sale orders


    @api.depends('customer_id')  # Trigger computation when customer_id changes
    def _compute_order_count(self):
        """
        Compute the orders count  by customer.
        """
        for record in self:
            sale_orders = self.env['sale.order'].search([('partner_id', '=', record.customer_id.id)])
            # Search for all sale orders linked to the customer
            record.order_count = len(sale_orders)
            # Count the number of sale orders by len(method)





