"""测试 - 工具函数"""
import pytest
from utils.messages import Messages


class TestMessages:
    """测试消息工具类"""

    def test_has_methods(self):
        """检查 Messages 类有必要的方法"""
        assert hasattr(Messages, 'warning')
        assert hasattr(Messages, 'info')
        assert hasattr(Messages, 'error')