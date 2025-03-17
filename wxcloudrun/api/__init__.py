# 这个文件会由主应用导入，从而注册所有的API路由

def init_app(app):
    """
    初始化并注册所有API路由到Flask应用
    :param app: Flask应用实例
    """
    # 导入所有API模块，会自动向app注册路由
    from wxcloudrun.api import counter
    from wxcloudrun.api import user
    from wxcloudrun.api import guide
    from wxcloudrun.api import attraction
    from wxcloudrun.api import favorite
    from wxcloudrun.api import plan
    from wxcloudrun.api import initialize 