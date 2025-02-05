{
    # Module Name
    'name': 'Customer Sales Metrics',
    # Module Version
    'version': '17.0.1.0',
    # Module Summary (Short Description)
    'summary': 'Track and analyze customer sales performance with total sales and order count metrics.',
    # Module Description (Long Description)
    'description': """
        Custom Module for Customer Sales Metrics 
        ============================
        This module provides a comprehensive dashboard to track and analyze customer sales performance.
        It introduces a new model, `res.partner.customer_metrics`, which stores key metrics such as:
        - Total Sales: The sum of all sales orders for a customer.
        - Order Count: The total number of orders placed by a customer.
        Features:
        - Automatically computes total sales and order count for each customer.
        - Provides a dashboard view to display top customers based on sales performance.
        - Integrates seamlessly with the existing Sales module in Odoo.
    """,
    # Author of the Module
    'author': 'Abdulrahman Elsharef',
    # Website (Optional)
    'website': 'https://github.com/AbdulrahmanElsharef',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',  # Add security file
        'views/customer_metrics_view.xml',  # Add the XML file here
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',  # License for your module (LGPL-3 in this case)
}