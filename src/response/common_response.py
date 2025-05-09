class ResponseResult:
    # 构造函数
    def __init__(self, code=200, data=None, error=''):
        self.code = code
        self.data = data
        self.error = error

    # 用于结构体对象返回
    def to_dict(self):
        return {
            'code': self.code,
            'data': self.data,
            'error': self.error
        }

    # 对象打印方法（类似java的toString方法）
    def __repr__(self):
        return f'<ResponseResult code={self.code} data={self.data} error={self.error}>'