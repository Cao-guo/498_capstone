from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from models.product_model import Category, Product
from database import db
from response import Result

api = Namespace('products', description='产品和分类管理')

# 分类模型
category_model = api.model('Category', {
    'category_id': fields.Integer(description='分类ID'),
    'category_name': fields.String(description='分类名称'),
    'description': fields.String(description='分类描述'),
    'created_at': fields.String(description='创建时间')
})

# 产品模型
product_model = api.model('Product', {
    'product_id': fields.Integer(description='产品ID'),
    'product_name': fields.String(description='产品名称'),
    'category_id': fields.Integer(description='分类ID'),
    'category_name': fields.String(description='分类名称'),
    'sku': fields.String(description='库存单位'),
    'price': fields.Float(description='销售价格'),
    'cost': fields.Float(description='成本价格'),
    'description': fields.String(description='产品描述'),
    'created_at': fields.String(description='创建时间'),
    'updated_at': fields.String(description='更新时间')
})

# 创建分类参数
category_parser = reqparse.RequestParser()
category_parser.add_argument('category_name', type=str, required=True, help='分类名称不能为空')
category_parser.add_argument('description', type=str, help='分类描述')

# 创建产品参数
product_parser = reqparse.RequestParser()
product_parser.add_argument('product_name', type=str, required=True, help='产品名称不能为空')
product_parser.add_argument('category_id', type=int, help='分类ID')
product_parser.add_argument('sku', type=str, help='库存单位')
product_parser.add_argument('price', type=float, required=True, help='销售价格不能为空')
product_parser.add_argument('cost', type=float, help='成本价格')
product_parser.add_argument('description', type=str, help='产品描述')


# 分类路由
@api.route('/categories')
class CategoryList(Resource):
    
    @api.doc('获取所有分类')
    @api.response(200, '成功', model=api.model('CategoryList', {
        'categories': fields.List(fields.Nested(category_model), description='分类列表')
    }))
    def get(self):
        """获取所有产品分类"""
        categories = Category.query.all()
        return Result.ok(data={'categories': [c.to_dict() for c in categories]}, msg='获取分类列表成功')
    
    @api.doc('创建新分类')
    @api.expect(category_parser)
    @api.response(201, '创建成功', category_model)
    def post(self):
        """创建新的产品分类"""
        args = category_parser.parse_args()
        
        if not args['category_name'] or args['category_name'].strip() == '':
            return Result.error(msg='分类名称不能为空', code=400)
        
        # 检查是否有同名分类
        exists = Category.query.filter_by(category_name=args['category_name']).first()
        if exists:
            return Result.error(msg='分类名称已存在', code=409)
        
        category = Category(
            category_name=args['category_name'],
            description=args.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return Result.ok(data=category.to_dict(), msg='创建分类成功'), 201


@api.route('/categories/<int:category_id>')
@api.param('category_id', '分类ID')
class CategoryDetail(Resource):
    
    @api.doc('获取分类详情')
    @api.response(200, '成功', category_model)
    @api.response(404, '分类未找到')
    def get(self, category_id):
        """获取特定分类的详情"""
        category = Category.query.get_or_404(category_id)
        return Result.ok(data=category.to_dict(), msg='获取分类详情成功')
    
    @api.doc('更新分类')
    @api.expect(category_parser)
    @api.response(200, '更新成功', category_model)
    @api.response(404, '分类未找到')
    def put(self, category_id):
        """更新产品分类"""
        category = Category.query.get_or_404(category_id)
        args = category_parser.parse_args()
        
        if not args['category_name'] or args['category_name'].strip() == '':
            return Result.error(msg='分类名称不能为空', code=400)
        
        # 检查是否有同名分类(除了自己)
        exists = Category.query.filter(Category.category_name == args['category_name'], 
                                      Category.category_id != category_id).first()
        if exists:
            return Result.error(msg='分类名称已存在', code=409)
        
        category.category_name = args['category_name']
        if args.get('description') is not None:
            category.description = args['description']
        
        db.session.commit()
        
        return Result.ok(data=category.to_dict(), msg='更新分类成功')
    
    @api.doc('删除分类')
    @api.response(200, '删除成功')
    @api.response(404, '分类未找到')
    def delete(self, category_id):
        """删除产品分类"""
        category = Category.query.get_or_404(category_id)
        
        # 检查是否有关联的产品
        if Product.query.filter_by(category_id=category_id).first():
            return Result.error(msg='无法删除，该分类下有关联产品', code=400)
        
        db.session.delete(category)
        db.session.commit()
        
        return Result.ok(msg='删除分类成功')


# 产品路由
@api.route('/')
class ProductList(Resource):
    
    @api.doc('获取所有产品')
    @api.response(200, '成功', model=api.model('ProductList', {
        'products': fields.List(fields.Nested(product_model), description='产品列表')
    }))
    def get(self):
        """获取所有产品"""
        products = Product.query.all()
        return Result.ok(data={'products': [p.to_dict() for p in products]}, msg='获取产品列表成功')
    
    @api.doc('创建新产品')
    @api.expect(product_parser)
    @api.response(201, '创建成功', product_model)
    def post(self):
        """创建新产品"""
        args = product_parser.parse_args()
        
        if not args['product_name'] or args['product_name'].strip() == '':
            return Result.error(msg='产品名称不能为空', code=400)
        
        if args['price'] is None or args['price'] <= 0:
            return Result.error(msg='销售价格必须大于零', code=400)
        
        # 检查SKU是否已存在
        if args['sku'] and Product.query.filter_by(sku=args['sku']).first():
            return Result.error(msg='SKU已存在', code=409)
        
        # 检查分类是否存在
        if args['category_id'] and not Category.query.get(args['category_id']):
            return Result.error(msg='指定的分类不存在', code=400)
        
        product = Product(
            product_name=args['product_name'],
            category_id=args.get('category_id'),
            sku=args.get('sku'),
            price=args['price'],
            cost=args.get('cost'),
            description=args.get('description')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return Result.ok(data=product.to_dict(), msg='创建产品成功'), 201


@api.route('/<int:product_id>')
@api.param('product_id', '产品ID')
class ProductDetail(Resource):
    
    @api.doc('获取产品详情')
    @api.response(200, '成功', product_model)
    @api.response(404, '产品未找到')
    def get(self, product_id):
        """获取特定产品的详情"""
        product = Product.query.get_or_404(product_id)
        return Result.ok(data=product.to_dict(), msg='获取产品详情成功')
    
    @api.doc('更新产品')
    @api.expect(product_parser)
    @api.response(200, '更新成功', product_model)
    @api.response(404, '产品未找到')
    def put(self, product_id):
        """更新产品信息"""
        product = Product.query.get_or_404(product_id)
        args = product_parser.parse_args()
        
        if not args['product_name'] or args['product_name'].strip() == '':
            return Result.error(msg='产品名称不能为空', code=400)
        
        if args['price'] is not None and args['price'] <= 0:
            return Result.error(msg='销售价格必须大于零', code=400)
        
        # 检查SKU是否已存在(除了自己)
        if args['sku'] and Product.query.filter(Product.sku == args['sku'], 
                                              Product.product_id != product_id).first():
            return Result.error(msg='SKU已存在', code=409)
        
        # 检查分类是否存在
        if args['category_id'] and not Category.query.get(args['category_id']):
            return Result.error(msg='指定的分类不存在', code=400)
        
        product.product_name = args['product_name']
        if args.get('category_id') is not None:
            product.category_id = args['category_id']
        if args.get('sku') is not None:
            product.sku = args['sku']
        if args.get('price') is not None:
            product.price = args['price']
        if args.get('cost') is not None:
            product.cost = args['cost']
        if args.get('description') is not None:
            product.description = args['description']
        
        db.session.commit()
        
        return Result.ok(data=product.to_dict(), msg='更新产品成功')
    
    @api.doc('删除产品')
    @api.response(200, '删除成功')
    @api.response(404, '产品未找到')
    def delete(self, product_id):
        """删除产品"""
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        
        return Result.ok(msg='删除产品成功') 