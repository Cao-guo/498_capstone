from datetime import datetime
from database import db


class Sale(db.Model):
    """销售交易模型类"""
    
    __tablename__ = 'sales'
    
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_date = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('uploaded_files.file_id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Sale {self.sale_id}: {self.quantity} units of product {self.product_id}>'
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'sale_id': self.sale_id,
            'transaction_date': self.transaction_date.isoformat(),
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'file_id': self.file_id,
            'created_at': self.created_at.isoformat()
        }


class SalesAnalytics(db.Model):
    """销售分析汇总模型类"""
    
    __tablename__ = 'sales_analytics'
    
    analytics_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    date_period = db.Column(db.Date, nullable=False)
    period_type = db.Column(db.String(10), nullable=False)  # 'daily', 'monthly', 'yearly'
    total_quantity = db.Column(db.Integer, nullable=False, default=0)
    total_revenue = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    total_cost = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    profit = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 建立关系
    product = db.relationship('Product', foreign_keys=[product_id])
    category = db.relationship('Category', foreign_keys=[category_id])
    
    def __repr__(self):
        return f'<SalesAnalytics {self.analytics_id}: {self.period_type} for {self.date_period}>'
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'analytics_id': self.analytics_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else None,
            'category_id': self.category_id,
            'category_name': self.category.category_name if self.category else None,
            'date_period': self.date_period.isoformat(),
            'period_type': self.period_type,
            'total_quantity': self.total_quantity,
            'total_revenue': float(self.total_revenue),
            'total_cost': float(self.total_cost),
            'profit': float(self.profit),
            'last_updated': self.last_updated.isoformat()
        } 