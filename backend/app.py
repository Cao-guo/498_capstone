import os
from flask import Flask, jsonify
from flask_restx import Api
import sys

# 添加当前目录到路径中，使Python能找到模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入数据库模块
from database import setup_database, init_db

# 导入路由
from routes import blueprints

# 创建Flask应用
def create_app():
    """
    创建并配置Flask应用
    
    Returns:
        Flask: 配置好的Flask应用实例
    """
    app = Flask(__name__)
    
    # 配置应用
    app.config['SECRET_KEY'] = 'retail-analytics-secret-key'
    app.config['JSON_AS_ASCII'] = False  # 支持中文JSON响应
    
    # 初始化数据库
    init_db(app)
    
    # 注册蓝图
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    # 全局错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'code': 404,
            'msg': '请求的资源不存在',
            'success': False
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'code': 500,
            'msg': '服务器内部错误',
            'success': False
        }), 500
    
    # 根路径
    @app.route('/')
    def index():
        return jsonify({
            'code': 200,
            'msg': 'Smart Retail Analytics API 服务正在运行',
            'success': True,
            'data': {
                'version': '1.0',
                'docs_url': '/api/docs'
            }
        })
    
    # 检查并创建上传目录
    upload_dir = os.path.join(os.path.dirname(__file__), 'upload')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    return app


if __name__ == '__main__':
    # 检查并设置数据库
    setup_database()
    
    # 创建应用
    app = create_app()
    
    # 获取主机和端口
    host = '0.0.0.0'
    port = 5000
    
    # 输出Swagger文档路径
    swagger_url = f"http://localhost:{port}/api/docs"
    print("=" * 80)
    print(f"Smart Retail Analytics API 已启动")
    print(f"API文档 (Swagger UI): {swagger_url}")
    print("=" * 80)
    
    # 运行应用
    app.run(host=host, port=port, debug=True) 