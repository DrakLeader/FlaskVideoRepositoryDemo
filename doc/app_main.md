# Flask Demo应用 配置与启动

## 概述

app.py作为Flask入口应用，负责初始化 Flask 应用，配置数据库，设置用户认证，以及注册蓝图。

## 主要组件

1. **Flask 应用实例 (`app`)**:
   - 初始化 Flask 应用。
   - 设置静态文件目录和应用密钥。

2. **数据库配置**:
   - 使用 SQLAlchemy 配置 SQLite 数据库。
   - 初始化数据库与应用的连接。

3. **Flask-Login 初始化**:
   - 初始化 Flask-Login 用于用户认证管理。
   - 设置登录视图。

4. **蓝图注册**:
   - 注册 `user_blueprint` 和 `video_blueprint` 以组织应用的路由。

5. **数据库表创建**:
   - 检查并创建数据库表。

6. **用户加载函数**:
   - 定义 `load_user` 函数用于 Flask-Login 加载用户。

7. **自定义静态文件路由**:
   - 提供一个路由来服务 `file_storage` 目录下的文件。

8. **主页路由**:
   - 定义主页路由。

## 启动配置

- 应用在 `if __name__ == '__main__':` 块中启动，监听所有网络接口 (`0.0.0.0`)。

### 注意事项

- 这部分代码主要用于应用的配置和初始化，不直接处理 API 请求。
- 实际的 API 功能由在 `user_blueprint` 和 `video_blueprint` 中定义的路由处理。

### 示例

```bash
python3 app.py
```
