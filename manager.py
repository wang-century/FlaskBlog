from flaskblog import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

# 创建Flask实例
app = create_app()
# 创建命令行启动控制对象
manager = Manager(app)
# 添加数据库迁移命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
