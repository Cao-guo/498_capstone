from datetime import datetime
from database import db


class UploadedFile(db.Model):
    """上传文件模型类"""
    
    __tablename__ = 'uploaded_files'
    
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    processing_errors = db.Column(db.Text, nullable=True)
    
    # 反向引用销售记录
    sales = db.relationship('Sale', backref='uploaded_file', lazy=True)
    
    def __repr__(self):
        return f'<UploadedFile {self.file_id}: {self.original_filename}>'
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'file_id': self.file_id,
            'file_name': self.file_name,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'upload_date': self.upload_date.isoformat(),
            'processed': self.processed,
            'processing_errors': self.processing_errors
        } 