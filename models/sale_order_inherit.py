from odoo import models, fields, api  # Import Odoo base classes and decorators

class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Inherit from model `sale.order` model to override create and update method

    @api.model  # works on the model itself  
    def create(self, vals):
        """
        Override the create method to update customer metrics when create sale order 
        """
        order = super(SaleOrder, self).create(vals)
        # Create the sale order using vals parameter 
        customer_metrics = self.env['res.partner.customer_metrics'].search([('customer_id', '=', order.partner_id.id)])
        # Search for  customer from  res.partner.customer_metrics  associated with the sale order.partner_id
        metrics_vals = {'customer_id': order.partner_id.id}  
        # get customer_id other fields are computed field
        if customer_metrics:
            customer_metrics.write(metrics_vals)
            # If customer metrics  update  with  new values
        else:
            self.env['res.partner.customer_metrics'].create(metrics_vals)
            # If customer metrics do not exist create a record with values
        return order  # Return created sale order

    def write(self, vals):
        """
        Override the write method to update customer metrics when aupdate sale order
        """
        all_partners = {}  # get all customers
        for order in self:  
            all_partners[order.id] = order.partner_id         
        result = super(SaleOrder, self).write(vals)
        # Write the sale order using vals parameter 

        # Update customer metrics for both old and new partners
        for order in self:
            if 'partner_id' in vals or 'amount_total' in vals:
                # Check if the partner_id or amount_total fields updated
                if all_partners.get(order.id) and all_partners[order.id] != order.partner_id:
                    self._update_customer(all_partners[order.id])
                    # If the partner_id changed, update  the old partner
                # If the partner_id  create the new partner
                self._update_customer(order.partner_id)

        return result  # Return the result of the write method

    def _update_customer(self, partner):
        """
         method to update customer  for a given partner_id.
        """
        if partner:  # Check if the partner (not empty or None)
            customer_metrics = self.env['res.partner.customer_metrics'].search([('customer_id', '=', partner.partner_id.id)])
            # Search for  customer from  res.partner.customer_metrics  associated with the sale order.partner_id
            metrics_vals = {'customer_id': partner.partner_id.id}  
            # get customer_id other fields are computed field
            if customer_metrics:
                customer_metrics.write(metrics_vals)
                # If customer metrics  update  with  new values
            else:
                self.env['res.partner.customer_metrics'].create(metrics_vals)
                # If customer metrics do not exist create a record with values
                
                