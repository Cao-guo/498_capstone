from datetime import datetime
from database import db


class Task(db.Model):
    """任务模型类"""
    
    __tablename__ = 'tasks'
    
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        status = "已完成" if self.is_completed else "未完成"
        return f'<Task {self.task_id}: {self.task_description[:20]}... ({status})>'
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'task_id': self.task_id,
            'task_description': self.task_description,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_completed': self.is_completed
        }
    
    def complete(self):
        """将任务标记为已完成"""
        self.is_completed = True
        self.completed_at = datetime.utcnow()
        
    def reopen(self):
        """重新打开任务"""
        self.is_completed = False
        self.completed_at = None 