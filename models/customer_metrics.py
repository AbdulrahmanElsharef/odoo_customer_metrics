from odoo import models, fields, api

class ResPartnerCustomerMetrics(models.Model):
    _name = 'res.partner.customer_metrics'
    _description = 'Customer Metrics Dashboard'
    _rec_name="customer_id"
    _order = 'total_sales desc, order_count desc'
    
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    total_sales = fields.Float(string='Total Sales', compute='_compute_total_sales', store=True)
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count', store=True)

    @api.depends('customer_id')
    def _compute_total_sales(self):
        for record in self:
            sale_orders = self.env['sale.order'].search([('partner_id', '=', record.customer_id.id)])
            record.total_sales = sum(order.amount_total for order in sale_orders)

    @api.depends('customer_id')
    def _compute_order_count(self):
        for record in self:
            sale_orders = self.env['sale.order'].search([('partner_id', '=', record.customer_id.id)])
            record.order_count = len(sale_orders)
            



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)  # Create the sale order first

        # Now create/update the customer metrics
        customer_metrics = self.env['res.partner.customer_metrics'].search([('customer_id', '=', order.partner_id.id)])
        metrics_vals = {'customer_id': order.partner_id.id} # Only customer_id is needed, other fields are computed

        if customer_metrics:
            customer_metrics.write(metrics_vals)  # Update if exists
        else:
            self.env['res.partner.customer_metrics'].create(metrics_vals)  # Create if doesn't exist

        return order


  
    def write(self, vals):
        # Get the old partner_id before the write operation
        old_partners = {order.id: order.partner_id for order in self}

        # Write the sale order
        result = super(SaleOrder, self).write(vals)

        # Update customer metrics for both old and new partners (if partner_id changed)
        for order in self:
            if 'partner_id' in vals or 'amount_total' in vals:
                # Update metrics for the old partner (if partner_id changed)
                if old_partners.get(order.id) and old_partners[order.id] != order.partner_id:
                    self._update_customer(old_partners[order.id])

                # Update metrics for the new partner
                self._update_customer(order.partner_id)

        return result
    
    
    def _update_customer(self, partner):
        """
        Helper method to update customer metrics for a given partner.
        """
        if partner:
            customer_metrics = self.env['res.partner.customer_metrics'].search([('customer_id', '=', partner.id)])
            metrics_vals = {'customer_id': partner.id}  # Only customer_id is needed, other fields are computed

            if customer_metrics:
                customer_metrics.write(metrics_vals)  # Update if exists
            else:
                self.env['res.partner.customer_metrics'].create(metrics_vals)
