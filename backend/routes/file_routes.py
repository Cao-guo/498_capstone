import os
from flask import request, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
import pandas as pd
from datetime import datetime

from models.file_model import UploadedFile
from models.product_model import Product, Category
from models.sale_model import Sale, SalesAnalytics
from database import db
from response import Result

api = Namespace('files', description='文件上传和管理操作')

# 文件上传模型
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='要上传的CSV文件')

# 上传文件响应模型
file_model = api.model('UploadedFile', {
    'file_id': fields.Integer(description='文件ID'),
    'file_name': fields.String(description='保存的文件名'),
    'original_filename': fields.String(description='原始文件名'),
    'file_size': fields.Integer(description='文件大小(字节)'),
    'file_type': fields.String(description='文件类型'),
    'upload_date': fields.String(description='上传日期'),
    'processed': fields.Boolean(description='是否已处理'),
    'processing_errors': fields.String(description='处理错误(如有)')
})

# 文件列表响应
file_list_model = api.model('FileList', {
    'files': fields.List(fields.Nested(file_model), description='上传的文件列表')
})


@api.route('/')
class FileList(Resource):
    
    @api.doc('获取所有上传的文件列表')
    @api.response(200, '成功', file_list_model)
    def get(self):
        """获取所有上传的文件列表"""
        files = UploadedFile.query.all()
        return Result.ok(data={'files': [file.to_dict() for file in files]}, msg='获取文件列表成功')
    
    @api.doc('上传新文件')
    @api.expect(upload_parser)
    @api.response(201, '上传成功', file_model)
    @api.response(400, '无效的请求')
    def post(self):
        """上传新的CSV文件"""
        args = upload_parser.parse_args()
        file = args['file']
        
        # 验证文件类型
        if not file.filename.endswith('.csv'):
            return Result.error(msg='仅支持CSV文件上传', code=400)
        
        # 确保上传目录存在
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 保存文件
        original_filename = file.filename
        file_path = os.path.join(upload_dir, original_filename)
        file.save(file_path)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        
        # 创建数据库记录
        new_file = UploadedFile(
            file_name=original_filename,
            original_filename=original_filename,
            file_size=file_size,
            file_type='csv'
        )
        
        db.session.add(new_file)
        db.session.commit()
        
        return Result.ok(data=new_file.to_dict(), msg='文件上传成功'), 201


@api.route('/<int:file_id>')
@api.param('file_id', '文件ID')
class FileDetail(Resource):
    
    @api.doc('获取文件详情')
    @api.response(200, '成功', file_model)
    @api.response(404, '文件未找到')
    def get(self, file_id):
        """获取特定文件的详情"""
        file = UploadedFile.query.get_or_404(file_id)
        return Result.ok(data=file.to_dict(), msg='获取文件详情成功')
    
    @api.doc('删除文件')
    @api.response(200, '删除成功')
    @api.response(404, '文件未找到')
    def delete(self, file_id):
        """删除上传的文件"""
        file = UploadedFile.query.get_or_404(file_id)
        
        # 尝试删除物理文件
        try:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload', file.file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            return Result.fail(msg=f'删除文件失败: {str(e)}')
        
        # 删除数据库记录
        db.session.delete(file)
        db.session.commit()
        
        return Result.ok(msg='文件删除成功')


@api.route('/<int:file_id>/download')
@api.param('file_id', '文件ID')
class FileDownload(Resource):
    
    @api.doc('下载文件')
    @api.response(200, '下载成功')
    @api.response(404, '文件未找到')
    def get(self, file_id):
        """下载特定的文件"""
        file = UploadedFile.query.get_or_404(file_id)
        
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload', file.file_name)
        
        if not os.path.exists(file_path):
            return Result.fail(msg='文件不存在', code=404)
        
        return send_file(
            file_path,
            download_name=file.original_filename,
            as_attachment=True
        )


@api.route('/<int:file_id>/process')
@api.param('file_id', '文件ID')
class FileProcess(Resource):
    
    @api.doc('处理CSV文件')
    @api.response(200, '处理成功')
    @api.response(404, '文件未找到')
    def post(self, file_id):
        """处理上传的CSV文件，导入销售数据"""
        file = UploadedFile.query.get_or_404(file_id)
        
        # 如果文件已处理，返回错误
        if file.processed:
            return Result.error(msg='文件已经处理过', code=400)
        
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload', file.file_name)
        
        if not os.path.exists(file_path):
            return Result.fail(msg='文件不存在', code=404)
        
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 数据处理统计
            stats = {
                'total_rows': len(df),
                'processed_rows': 0,
                'skipped_rows': 0,
                'categories_added': 0,
                'products_added': 0,
                'sales_added': 0,
                'analytics_updated': 0
            }
            
            # 处理每一行数据
            for _, row in df.iterrows():
                try:
                    # 解析行数据
                    transaction_date_str = row.get('transaction_date')
                    product_id = row.get('product_id')
                    product_name = row.get('product_name')
                    category_id = row.get('category_id')
                    category_name = row.get('category_name')
                    quantity = row.get('quantity')
                    unit_price = row.get('unit_price')
                    total_price = row.get('total_price')
                    
                    # 数据验证
                    if not all([transaction_date_str, product_name, quantity, unit_price, total_price]):
                        stats['skipped_rows'] += 1
                        continue
                    
                    # 解析日期
                    try:
                        transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        try:
                            transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d')
                        except ValueError:
                            stats['skipped_rows'] += 1
                            continue
                    
                    # 检查并添加分类
                    category = None
                    if category_id and category_name:
                        category = Category.query.filter_by(category_id=category_id).first()
                        if not category:
                            category = Category(
                                category_id=category_id,
                                category_name=category_name
                            )
                            db.session.add(category)
                            stats['categories_added'] += 1
                    
                    # 检查并添加产品
                    product = None
                    if product_id and product_name:
                        product = Product.query.filter_by(product_id=product_id).first()
                        if not product:
                            product = Product(
                                product_id=product_id,
                                product_name=product_name,
                                category_id=category_id if category else None,
                                price=unit_price  # 使用单价作为产品价格
                            )
                            db.session.add(product)
                            stats['products_added'] += 1
                    
                    # 创建销售记录
                    sale = Sale(
                        transaction_date=transaction_date,
                        product_id=product.product_id if product else None,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        file_id=file_id
                    )
                    db.session.add(sale)
                    stats['sales_added'] += 1
                    
                    # 提交以保存每行处理的结果
                    db.session.commit()
                    stats['processed_rows'] += 1
                    
                except Exception as row_error:
                    # 回滚当前行的操作
                    db.session.rollback()
                    stats['skipped_rows'] += 1
                    print(f"处理行时出错: {str(row_error)}")
            
            # 更新销售分析数据
            try:
                # 按天统计销售数据
                self._update_sales_analytics(file_id)
                stats['analytics_updated'] += 1
            except Exception as analytics_error:
                print(f"更新销售分析时出错: {str(analytics_error)}")
            
            # 标记文件为已处理
            file.processed = True
            db.session.commit()
            
            return Result.ok(data=stats, msg='文件处理成功')
        except Exception as e:
            db.session.rollback()
            file.processing_errors = str(e)
            db.session.commit()
            return Result.fail(msg=f'处理文件时出错: {str(e)}')
    
    def _update_sales_analytics(self, file_id):
        """更新销售分析数据"""
        # 查询与此文件关联的销售数据
        sales = Sale.query.filter_by(file_id=file_id).all()
        
        # 按日期、产品、分类分组
        analytics_data = {}
        for sale in sales:
            # 获取日期（不含时间）
            date_key = sale.transaction_date.date()
            product_id = sale.product_id
            
            # 获取产品和分类信息
            product = Product.query.get(product_id) if product_id else None
            category_id = product.category_id if product else None
            
            # 创建分析键
            key = (date_key, product_id, category_id)
            
            if key not in analytics_data:
                analytics_data[key] = {
                    'date_period': date_key,
                    'product_id': product_id,
                    'category_id': category_id,
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'total_cost': 0,
                    'profit': 0
                }
            
            # 更新统计数据
            analytics_data[key]['total_quantity'] += sale.quantity
            analytics_data[key]['total_revenue'] += float(sale.total_price)
            
            # 计算成本和利润（如果有成本信息）
            cost = float(product.cost) if product and product.cost else 0
            total_cost = cost * sale.quantity
            analytics_data[key]['total_cost'] += total_cost
            analytics_data[key]['profit'] += float(sale.total_price) - total_cost
        
        # 保存或更新分析记录
        for key, data in analytics_data.items():
            # 检查是否已存在相同日期、产品、分类的分析记录
            existing = SalesAnalytics.query.filter_by(
                date_period=data['date_period'],
                product_id=data['product_id'],
                category_id=data['category_id'],
                period_type='daily'
            ).first()
            
            if existing:
                # 更新现有记录
                existing.total_quantity += data['total_quantity']
                existing.total_revenue += data['total_revenue']
                existing.total_cost += data['total_cost']
                existing.profit += data['profit']
                existing.last_updated = datetime.utcnow()
            else:
                # 创建新记录
                analytics = SalesAnalytics(
                    date_period=data['date_period'],
                    product_id=data['product_id'],
                    category_id=data['category_id'],
                    period_type='daily',
                    total_quantity=data['total_quantity'],
                    total_revenue=data['total_revenue'],
                    total_cost=data['total_cost'],
                    profit=data['profit']
                )
                db.session.add(analytics)
        
        # 提交所有分析记录
        db.session.commit() 