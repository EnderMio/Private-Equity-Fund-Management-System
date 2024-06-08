根据您提供的代码和描述生成的新的API文档如下：

## API 文档

### 用户注册

**URL:** `/register`  
**方法:** `POST`  
**描述:** 注册新用户

**请求体示例:**
```json
{
  "username": "newuser",
  "password": "password",
  "email": "newuser@example.com",
  "phone": "1234567890",
  "address": "123 Street Name, City, Country"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "User registered successfully"
  }
  ```
  状态码: `201`

### 用户登录

**URL:** `/login`  
**方法:** `POST`  
**描述:** 用户登录

**请求体示例:**
```json
{
  "username": "testuser",
  "password": "password"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "Logged in successfully"
  }
  ```
  状态码: `200`
- 失败: 
  ```json
  {
    "message": "Invalid credentials"
  }
  ```
  状态码: `401`

### 用户登出

**URL:** `/logout`  
**方法:** `POST`  
**描述:** 用户登出

**响应:**
- 成功: 
  ```json
  {
    "message": "Logged out successfully"
  }
  ```
  状态码: `200`

### 查看用户信息

**URL:** `/user/info`  
**方法:** `GET`  
**描述:** 获取当前登录用户的信息  
**权限:** 需要登录

**响应:**
- 成功: 
  ```json
  {
    "username": "testuser",
    "email": "testuser@example.com",
    "phone": "1234567890",
    "address": "123 Street Name, City, Country"
  }
  ```
  状态码: `200`

### 更新用户信息

**URL:** `/user/info`  
**方法:** `PUT`  
**描述:** 更新当前登录用户的信息  
**权限:** 需要登录

**请求体示例:**
```json
{
  "email": "newemail@example.com",
  "phone": "0987654321",
  "address": "456 New Street, New City, New Country"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "User information updated successfully"
  }
  ```
  状态码: `200`

### 创建基金

**URL:** `/funds`  
**方法:** `POST`  
**描述:** 创建新的基金  
**权限:** 需要管理员权限

**请求体示例:**
```json
{
  "name": "Test Fund",
  "description": "A test fund"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "Fund created successfully"
  }
  ```
  状态码: `201`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 更新基金

**URL:** `/funds/<int:fund_id>`  
**方法:** `PUT`  
**描述:** 更新指定基金的信息  
**权限:** 需要管理员权限

**请求体示例:**
```json
{
  "name": "Updated Test Fund",
  "description": "Updated description"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "Fund updated successfully"
  }
  ```
  状态码: `200`
- 未找到: 
  ```json
  {
    "message": "Fund not found"
  }
  ```
  状态码: `404`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 删除基金

**URL:** `/funds/<int:fund_id>`  
**方法:** `DELETE`  
**描述:** 删除指定基金  
**权限:** 需要管理员权限

**响应:**
- 成功: 
  ```json
  {
    "message": "Fund deleted successfully"
  }
  ```
  状态码: `200`
- 未找到: 
  ```json
  {
    "message": "Fund not found"
  }
  ```
  状态码: `404`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 获取基金详情

**URL:** `/funds/<int:fund_id>`  
**方法:** `GET`  
**描述:** 获取指定基金的详细信息  
**权限:** 需要登录

**响应:**
- 成功: 
  ```json
  {
    "id": 1,
    "name": "Test Fund",
    "description": "A test fund"
  }
  ```
  状态码: `200`
- 未找到: 
  ```json
  {
    "message": "Fund not found"
  }
  ```
  状态码: `404`

### 添加股票

**URL:** `/stocks`  
**方法:** `POST`  
**描述:** 添加新的股票  
**权限:** 需要管理员权限

**请求体示例:**
```json
{
  "symbol": "TEST",
  "name": "Test Stock"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "Stock added successfully"
  }
  ```
  状态码: `201`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 更新股票

**URL:** `/stocks/<int:stock_id>`  
**方法:** `PUT`  
**描述:** 更新指定股票的信息  
**权限:** 需要管理员权限

**请求体示例:**
```json
{
  "symbol": "NEW",
  "name": "New Stock Name"
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "Stock updated successfully"
  }
  ```
  状态码: `200`
- 未找到: 
  ```json
  {
    "message": "Stock not found"
  }
  ```
  状态码: `404`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 删除股票

**URL:** `/stocks/<int:stock_id>`  
**方法:** `DELETE`  
**描述:** 删除指定股票  
**权限:** 需要管理员权限

**响应:**
- 成功: 
  ```json
  {
    "message": "Stock deleted successfully"
  }
  ```
  状态码: `200`
- 未找到: 
  ```json
  {
    "message": "Stock not found"
  }
  ```
  状态码: `404`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 获取股票列表

**URL:** `/stocks`  
**方法:** `GET`  
**描述:** 获取所有股票列表  
**权限:** 需要登录

**响应:**
- 成功: 
  ```json
  [
    {
      "id": 1,
      "symbol": "TEST",
      "name": "Test Stock"
    },
    {
      "id": 2,
      "symbol": "NEW",
      "name": "New Stock"
    }
  ]
  ```
  状态码: `200`

### 添加持仓

**URL:** `/funds/<int:fund_id>/holdings`  
**方法:** `POST`  
**描述:** 为指定基金添加持仓  
**权限:** 需要管理员权限

**请求体示例:**
```json
{
  "stock_id": 1,
  "quantity": 100
}
```

**响应:**
- 成功: 
  ```json
  {
    "message": "Holding added successfully"
  }
  ```
  状态码: `201`
- 未授权: 
  ```json
  {
    "message": "Unauthorized"
  }
  ```
  状态码: `403`

### 获取持仓列表

**URL:** `/funds/<int:fund_id>/holdings`  
**方法:** `GET`  
**描述:** 获取指定基金的持仓列表  
**权限:** 需要登录

**响应:**
- 成功: 
  ```json
  [
    {
      "stock_id": 1,
      "stock_name": "Test Stock",
      "quantity": 100
    }
  ]
  ```
  状态码: `200`
