from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from models.task_model import Task
from database import db
from response import Result

api = Namespace('tasks', description='任务管理操作')

# 任务模型
task_model = api.model('Task', {
    'task_id': fields.Integer(description='任务ID'),
    'task_description': fields.String(description='任务描述'),
    'created_at': fields.String(description='创建时间'),
    'completed_at': fields.String(description='完成时间'),
    'is_completed': fields.Boolean(description='是否完成')
})

# 任务列表响应
task_list_model = api.model('TaskList', {
    'tasks': fields.List(fields.Nested(task_model), description='任务列表')
})

# 创建任务参数
task_parser = reqparse.RequestParser()
task_parser.add_argument('task_description', type=str, required=True, help='任务描述不能为空')


@api.route('/')
class TaskList(Resource):
    
    @api.doc('获取所有任务')
    @api.response(200, '成功', task_list_model)
    def get(self):
        """获取所有任务列表"""
        tasks = Task.query.all()
        return Result.ok(data={'tasks': [task.to_dict() for task in tasks]}, msg='获取任务列表成功')
    
    @api.doc('创建新任务')
    @api.expect(task_parser)
    @api.response(201, '创建成功', task_model)
    def post(self):
        """创建新任务"""
        args = task_parser.parse_args()
        task_description = args['task_description']
        
        if not task_description or task_description.strip() == '':
            return Result.error(msg='任务描述不能为空', code=400)
        
        new_task = Task(task_description=task_description)
        db.session.add(new_task)
        db.session.commit()
        
        return Result.ok(data=new_task.to_dict(), msg='创建任务成功'), 201


@api.route('/<int:task_id>')
@api.param('task_id', '任务ID')
class TaskDetail(Resource):
    
    @api.doc('获取任务详情')
    @api.response(200, '成功', task_model)
    @api.response(404, '任务未找到')
    def get(self, task_id):
        """获取特定任务的详情"""
        task = Task.query.get_or_404(task_id)
        return Result.ok(data=task.to_dict(), msg='获取任务详情成功')
    
    @api.doc('更新任务')
    @api.expect(task_parser)
    @api.response(200, '更新成功', task_model)
    @api.response(404, '任务未找到')
    def put(self, task_id):
        """更新任务描述"""
        task = Task.query.get_or_404(task_id)
        
        args = task_parser.parse_args()
        task_description = args['task_description']
        
        if not task_description or task_description.strip() == '':
            return Result.error(msg='任务描述不能为空', code=400)
        
        task.task_description = task_description
        db.session.commit()
        
        return Result.ok(data=task.to_dict(), msg='更新任务成功')
    
    @api.doc('删除任务')
    @api.response(200, '删除成功')
    @api.response(404, '任务未找到')
    def delete(self, task_id):
        """删除任务"""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        return Result.ok(msg='删除任务成功')


@api.route('/<int:task_id>/complete')
@api.param('task_id', '任务ID')
class TaskComplete(Resource):
    
    @api.doc('完成任务')
    @api.response(200, '更新成功', task_model)
    @api.response(404, '任务未找到')
    def put(self, task_id):
        """标记任务为已完成"""
        task = Task.query.get_or_404(task_id)
        
        if task.is_completed:
            return Result.error(msg='任务已经标记为完成', code=400)
        
        task.complete()
        db.session.commit()
        
        return Result.ok(data=task.to_dict(), msg='任务已标记为完成')


@api.route('/<int:task_id>/reopen')
@api.param('task_id', '任务ID')
class TaskReopen(Resource):
    
    @api.doc('重新开放任务')
    @api.response(200, '更新成功', task_model)
    @api.response(404, '任务未找到')
    def put(self, task_id):
        """重新开放任务（标记为未完成）"""
        task = Task.query.get_or_404(task_id)
        
        if not task.is_completed:
            return Result.error(msg='任务已经是未完成状态', code=400)
        
        task.reopen()
        db.session.commit()
        
        return Result.ok(data=task.to_dict(), msg='任务已重新开放') 