# 用户认证和权限管理 API

## 概述

这个 API 提供了用户认证和基于角色的访问控制功能。它允许用户登录、登出，并限制特定路由的访问权限给特定角色的用户。

## 端点/Endpoints

1. **登录 (`/login`)**
   - **方法**: POST
   - **功能**: 用户登录
   - **请求体**: JSON，包含 `username` 和 `password`
   - **响应**: 登录成功或失败的消息
   - **示例请求体**: `{"username": "admin", "password": "admin"}`

2. **登出 (`/logout`)**
   - **方法**: POST
   - **功能**: 用户登出
   - **认证**: 需要用户已登录
   - **响应**: 登出成功的消息

3. **管理员专属路由 (`/admin_only`)**
   - **方法**: GET
   - **功能**: 仅限管理员和超级用户访问的路由
   - **认证**: 需要用户角色为 `admin` 或 `root`
   - **响应**: 欢迎消息或访问拒绝的消息

## 用户角色

- **root**: 超级用户，拥有所有权限
- **admin**: 管理员，拥有部分权限
- **user**: 普通用户，权限受限

## 用户类 (`User`)

- **属性**:
  - `username`: 用户名
  - `password`: 密码
  - `role`: 用户角色（默认为 `user`）
- **方法**:
  - `get_id()`: 返回用户名，用作用户的唯一标识

## 角色要求装饰器 (`role_required`)

- **功能**: 用于限制特定路由的访问权限给特定角色的用户
- **参数**:
  - `*roles`: 允许访问的用户角色列表
  - `endpoint`: 可选，用于指定装饰的视图函数的名称

## 示例：限制路由访问

```python
@user_blueprint.route('/some_route', methods=['GET'])
@role_required(ADMIN, ROOT)
def some_protected_route():
    # 仅限 ADMIN 和 ROOT 角色访问
    pass
```

这个 API 说明提供了关于如何使用 `user.py` 中定义的用户认证和权限管理功能的详细信息。
进一步了解 Flask-Login 和 Flask-Principal 的信息，可参阅 [Flask-Login 文档](https://flask-login.readthedocs.io/en/latest/) 和 [Flask-Principal 文档](https://pythonhosted.org/Flask-Principal/)。
