from datetime import datetime, timedelta
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
import pandas as pd
import os

from models.sale_model import Sale, SalesAnalytics
from models.product_model import Product, Category
from database import db
from response import Result

api = Namespace('analytics', description='销售数据分析操作')

# 销售分析模型
sales_analytics_model = api.model('SalesAnalytics', {
    'analytics_id': fields.Integer(description='分析ID'),
    'product_id': fields.Integer(description='产品ID'),
    'product_name': fields.String(description='产品名称'),
    'category_id': fields.Integer(description='分类ID'),
    'category_name': fields.String(description='分类名称'),
    'date_period': fields.String(description='日期周期'),
    'period_type': fields.String(description='周期类型(daily/monthly/yearly)'),
    'total_quantity': fields.Integer(description='总销售数量'),
    'total_revenue': fields.Float(description='总销售收入'),
    'total_cost': fields.Float(description='总销售成本'),
    'profit': fields.Float(description='总销售利润'),
    'last_updated': fields.String(description='最后更新时间')
})

# 销售报表查询参数
report_parser = reqparse.RequestParser()
report_parser.add_argument('start_date', type=str, help='开始日期 (YYYY-MM-DD)')
report_parser.add_argument('end_date', type=str, help='结束日期 (YYYY-MM-DD)')
report_parser.add_argument('period', type=str, choices=('daily', 'monthly', 'yearly'), default='monthly',
                          help='报表周期 (daily/monthly/yearly)')
report_parser.add_argument('category_id', type=int, help='分类ID')
report_parser.add_argument('product_id', type=int, help='产品ID')

# 销售趋势查询参数
trend_parser = reqparse.RequestParser()
trend_parser.add_argument('period', type=str, choices=('weekly', 'monthly', 'yearly'), default='monthly',
                         help='趋势周期 (weekly/monthly/yearly)')
trend_parser.add_argument('product_id', type=int, help='产品ID')
trend_parser.add_argument('category_id', type=int, help='分类ID')
trend_parser.add_argument('limit', type=int, default=12, help='返回结果数量限制')


@api.route('/report')
class SalesReport(Resource):
    
    @api.doc('获取销售报表')
    @api.expect(report_parser)
    @api.response(200, '成功', model=api.model('SalesReportResponse', {
        'report': fields.List(fields.Nested(sales_analytics_model), description='销售报表数据'),
        'summary': fields.Raw(description='销售汇总数据')
    }))
    def get(self):
        """获取销售报表数据"""
        args = report_parser.parse_args()
        
        # 准备查询
        query = db.session.query(SalesAnalytics)
        
        # 应用过滤条件
        if args['start_date']:
            try:
                start_date = datetime.strptime(args['start_date'], '%Y-%m-%d').date()
                query = query.filter(SalesAnalytics.date_period >= start_date)
            except ValueError:
                return Result.error(msg='开始日期格式无效，请使用YYYY-MM-DD格式')
        
        if args['end_date']:
            try:
                end_date = datetime.strptime(args['end_date'], '%Y-%m-%d').date()
                query = query.filter(SalesAnalytics.date_period <= end_date)
            except ValueError:
                return Result.error(msg='结束日期格式无效，请使用YYYY-MM-DD格式')
        
        # 过滤周期类型
        query = query.filter(SalesAnalytics.period_type == args['period'])
        
        # 按产品或分类过滤
        if args['product_id']:
            query = query.filter(SalesAnalytics.product_id == args['product_id'])
        elif args['category_id']:
            query = query.filter(SalesAnalytics.category_id == args['category_id'])
        
        # 执行查询
        results = query.all()
        report_data = [item.to_dict() for item in results]
        
        # 计算汇总数据
        summary = {
            'total_quantity': sum(item.total_quantity for item in results),
            'total_revenue': sum(float(item.total_revenue) for item in results),
            'total_cost': sum(float(item.total_cost) for item in results),
            'total_profit': sum(float(item.profit) for item in results),
            'period_count': len(results)
        }
        
        return Result.ok(data={
            'report': report_data,
            'summary': summary
        }, msg='获取销售报表成功')


@api.route('/trends')
class SalesTrends(Resource):
    
    @api.doc('获取销售趋势')
    @api.expect(trend_parser)
    @api.response(200, '成功')
    def get(self):
        """获取销售趋势数据"""
        args = trend_parser.parse_args()
        period = args['period']
        limit = args['limit']
        
        # 根据周期类型确定查询参数
        if period == 'weekly':
            group_type = 'daily'
            # 获取过去几周的数据
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=limit * 7)
        elif period == 'monthly':
            group_type = 'monthly'
            # 获取过去几个月的数据
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=limit * 30)
        else:  # yearly
            group_type = 'yearly'
            # 获取过去几年的数据
            end_date = datetime.now().date()
            start_date = datetime(end_date.year - limit, 1, 1).date()
        
        # 准备查询
        query = db.session.query(SalesAnalytics)
        query = query.filter(
            SalesAnalytics.period_type == group_type,
            SalesAnalytics.date_period >= start_date,
            SalesAnalytics.date_period <= end_date
        )
        
        # 按产品或分类过滤
        if args['product_id']:
            query = query.filter(SalesAnalytics.product_id == args['product_id'])
        elif args['category_id']:
            query = query.filter(SalesAnalytics.category_id == args['category_id'])
        
        # 排序并限制结果
        query = query.order_by(SalesAnalytics.date_period).limit(limit)
        
        # 执行查询
        results = query.all()
        trend_data = [item.to_dict() for item in results]
        
        # 转换为趋势数据格式
        formatted_trends = []
        for item in trend_data:
            formatted_trends.append({
                'date': item['date_period'],
                'revenue': item['total_revenue'],
                'profit': item['profit'],
                'quantity': item['total_quantity'],
                'label': item.get('product_name') or item.get('category_name') or '全部'
            })
        
        return Result.ok(data={
            'trends': formatted_trends,
            'period': period,
            'total_periods': len(formatted_trends)
        }, msg='获取销售趋势成功')


@api.route('/summary')
class SalesSummary(Resource):
    
    @api.doc('获取销售摘要')
    @api.response(200, '成功')
    def get(self):
        """获取销售数据摘要"""
        try:
            # 查询总销售额
            total_revenue = db.session.query(db.func.sum(Sale.total_price)).scalar() or 0
            
            # 查询总订单数
            total_orders = db.session.query(db.func.count(db.distinct(Sale.sale_id))).scalar() or 0
            
            # 查询总产品数
            total_products = db.session.query(db.func.count(Product.product_id)).scalar() or 0
            
            # 查询总分类数
            total_categories = db.session.query(db.func.count(Category.category_id)).scalar() or 0
            
            # 查询销售数量最多的前5个产品
            top_products_query = db.session.query(
                Product.product_id,
                Product.product_name,
                db.func.sum(Sale.quantity).label('total_quantity')
            ).join(Sale, Sale.product_id == Product.product_id) \
             .group_by(Product.product_id, Product.product_name) \
             .order_by(db.desc('total_quantity')) \
             .limit(5)
            
            top_products = [{
                'product_id': item.product_id,
                'product_name': item.product_name,
                'total_quantity': item.total_quantity
            } for item in top_products_query]
            
            return Result.ok(data={
                'total_revenue': float(total_revenue),
                'total_orders': total_orders,
                'total_products': total_products,
                'total_categories': total_categories,
                'top_products': top_products
            }, msg='获取销售摘要成功')
            
        except Exception as e:
            return Result.fail(msg=f'获取销售摘要失败: {str(e)}')


@api.route('/process-data')
class ProcessSalesData(Resource):
    
    @api.doc('处理销售数据')
    @api.response(200, '处理成功')
    def post(self):
        """处理销售数据并生成分析结果"""
        try:
            # 这里应该添加实际的数据处理和分析逻辑
            # 例如，读取销售记录，按不同维度计算汇总数据
            # 并将结果保存到SalesAnalytics表
            
            # 示例代码（实际实现需要更复杂的逻辑）:
            # 1. 获取所有销售记录
            # 2. 按日期、产品、分类分组统计
            # 3. 保存到SalesAnalytics表
            
            return Result.ok(msg='销售数据处理成功')
            
        except Exception as e:
            return Result.fail(msg=f'处理销售数据失败: {str(e)}') 