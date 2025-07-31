from typing import Any, Dict, List, Optional, Union


class Result:
    """统一API响应类"""

    def __init__(
        self,
        code: int = 200,
        msg: str = "操作成功",
        data: Optional[Union[Dict, List, Any]] = None,
        success: bool = True,
    ):
        self.code = code
        self.msg = msg
        self.data = data
        self.success = success

    def to_dict(self) -> Dict:
        """将响应对象转换为字典格式"""
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data,
            "success": self.success,
        }

    @classmethod
    def ok(
        cls, data: Optional[Union[Dict, List, Any]] = None, msg: str = "操作成功"
    ) -> Dict:
        """
        返回成功响应
        
        Args:
            data: 响应数据
            msg: 响应消息
            
        Returns:
            包含状态码、消息、数据和成功标志的字典
        """
        return cls(code=200, msg=msg, data=data, success=True).to_dict()

    @classmethod
    def fail(cls, msg: str = "操作失败", code: int = 500) -> Dict:
        """
        返回失败响应
        
        Args:
            msg: 错误消息
            code: 错误代码
            
        Returns:
            包含状态码、错误消息和失败标志的字典
        """
        return cls(code=code, msg=msg, data=None, success=False).to_dict()

    @classmethod
    def error(cls, msg: str = "请求参数错误", code: int = 400) -> Dict:
        """
        返回参数错误响应
        
        Args:
            msg: 错误消息
            code: 错误代码
            
        Returns:
            包含状态码、错误消息和失败标志的字典
        """
        return cls(code=code, msg=msg, data=None, success=False).to_dict() 