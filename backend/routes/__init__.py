from flask import Blueprint
from flask_restx import Api

# 创建API蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp,
          title='Smart Retail Analytics API',
          version='1.0',
          description='智能零售分析系统API文档',
          doc='/docs',
          validate=True)

# 导入并注册命名空间
from .file_routes import api as file_ns
from .task_routes import api as task_ns
from .product_routes import api as product_ns
from .analytics_routes import api as analytics_ns

api.add_namespace(file_ns, path='/files')
api.add_namespace(task_ns, path='/tasks')
api.add_namespace(product_ns, path='/products')
api.add_namespace(analytics_ns, path='/analytics')

# 导出蓝图
blueprints = [api_bp] 