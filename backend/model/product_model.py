from datetime import datetime
from database import db


class Category(db.Model):
    """产品分类模型类"""
    
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # 反向引用产品
    products = db.relationship('Product', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.category_id}: {self.category_name}>'
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class Product(db.Model):
    """产品模型类"""
    
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    sku = db.Column(db.String(50), unique=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    cost = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 反向引用销售记录
    sales = db.relationship('Sale', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.product_id}: {self.product_name}>'
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category_id': self.category_id,
            'category_name': self.category.category_name if self.category else None,
            'sku': self.sku,
            'price': float(self.price) if self.price else None,
            'cost': float(self.cost) if self.cost else None,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 