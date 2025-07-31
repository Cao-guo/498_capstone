# Smart Retail Analytics API 文档

本文档详细列出了Smart Retail Analytics系统的所有API接口，包括接口说明、请求参数、响应格式以及JSON示例。

## 通用响应格式

所有API均使用统一的响应格式：

```json
{
  "code": 200,       // 状态码：200成功，400请求错误，404资源不存在，500服务器错误
  "msg": "操作成功",  // 响应消息
  "data": {},        // 响应数据，可能是对象、数组或null
  "success": true    // 操作是否成功
}
```

## 文件管理API

### 获取文件列表

- **URL**: `/api/files`
- **方法**: `GET`
- **描述**: 获取所有上传的文件列表

**请求参数**: 无

**响应**:

```json
{
  "code": 200,
  "msg": "获取文件列表成功",
  "data": {
    "files": [
      {
        "file_id": 1,
        "file_name": "sales_data_2023.csv",
        "original_filename": "sales_data_2023.csv",
        "file_size": 2048,
        "file_type": "csv",
        "upload_date": "2023-05-15T10:30:00",
        "processed": true,
        "processing_errors": null
      },
      {
        "file_id": 2,
        "file_name": "products_2023.csv",
        "original_filename": "products_2023.csv",
        "file_size": 1024,
        "file_type": "csv",
        "upload_date": "2023-05-16T14:15:00",
        "processed": false,
        "processing_errors": null
      }
    ]
  },
  "success": true
}
```

### 上传文件

- **URL**: `/api/files`
- **方法**: `POST`
- **描述**: 上传新的CSV文件
- **Content-Type**: `multipart/form-data`

**请求参数**:

| 参数名 | 类型   | 描述        | 是否必须 |
|------|--------|-----------|-------|
| file | File   | CSV文件     | 是     |

**响应**:

```json
{
  "code": 201,
  "msg": "文件上传成功",
  "data": {
    "file_id": 3,
    "file_name": "sales_may_2023.csv",
    "original_filename": "sales_may_2023.csv",
    "file_size": 3072,
    "file_type": "csv",
    "upload_date": "2023-05-20T09:45:00",
    "processed": false,
    "processing_errors": null
  },
  "success": true
}
```

### 获取文件详情

- **URL**: `/api/files/{file_id}`
- **方法**: `GET`
- **描述**: 获取特定文件的详情

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| file_id| 整数    | 文件ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "获取文件详情成功",
  "data": {
    "file_id": 1,
    "file_name": "sales_data_2023.csv",
    "original_filename": "sales_data_2023.csv",
    "file_size": 2048,
    "file_type": "csv",
    "upload_date": "2023-05-15T10:30:00",
    "processed": true,
    "processing_errors": null
  },
  "success": true
}
```

### 删除文件

- **URL**: `/api/files/{file_id}`
- **方法**: `DELETE`
- **描述**: 删除上传的文件

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| file_id| 整数    | 文件ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "文件删除成功",
  "data": null,
  "success": true
}
```

### 下载文件

- **URL**: `/api/files/{file_id}/download`
- **方法**: `GET`
- **描述**: 下载特定的文件

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| file_id| 整数    | 文件ID   | 是     |

**响应**: 文件内容（非JSON格式）

### 处理文件

- **URL**: `/api/files/{file_id}/process`
- **方法**: `POST`
- **描述**: 处理上传的CSV文件，导入销售数据

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| file_id| 整数    | 文件ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "文件处理成功",
  "data": {
    "total_rows": 20,
    "processed_rows": 18,
    "skipped_rows": 2,
    "categories_added": 3,
    "products_added": 5,
    "sales_added": 18,
    "analytics_updated": 1
  },
  "success": true
}
```

## 任务管理API

### 获取任务列表

- **URL**: `/api/tasks`
- **方法**: `GET`
- **描述**: 获取所有任务

**请求参数**: 无

**响应**:

```json
{
  "code": 200,
  "msg": "获取任务列表成功",
  "data": {
    "tasks": [
      {
        "task_id": 1,
        "task_description": "分析第一季度销售数据",
        "created_at": "2023-04-01T09:00:00",
        "completed_at": "2023-04-05T17:30:00",
        "is_completed": true
      },
      {
        "task_id": 2,
        "task_description": "准备月度销售报告",
        "created_at": "2023-05-01T10:15:00",
        "completed_at": null,
        "is_completed": false
      }
    ]
  },
  "success": true
}
```

### 创建新任务

- **URL**: `/api/tasks`
- **方法**: `POST`
- **描述**: 创建新任务

**请求参数**:

```json
{
  "task_description": "检查库存状态并更新"
}
```

**响应**:

```json
{
  "code": 201,
  "msg": "创建任务成功",
  "data": {
    "task_id": 3,
    "task_description": "检查库存状态并更新",
    "created_at": "2023-05-20T14:30:00",
    "completed_at": null,
    "is_completed": false
  },
  "success": true
}
```

### 获取任务详情

- **URL**: `/api/tasks/{task_id}`
- **方法**: `GET`
- **描述**: 获取特定任务的详情

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| task_id| 整数    | 任务ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "获取任务详情成功",
  "data": {
    "task_id": 1,
    "task_description": "分析第一季度销售数据",
    "created_at": "2023-04-01T09:00:00",
    "completed_at": "2023-04-05T17:30:00",
    "is_completed": true
  },
  "success": true
}
```

### 更新任务

- **URL**: `/api/tasks/{task_id}`
- **方法**: `PUT`
- **描述**: 更新任务描述

**请求参数**:

| 参数名          | 类型    | 描述      | 是否必须 |
|---------------|--------|---------|-------|
| task_id       | 整数    | 任务ID    | 是     |
| task_description | 字符串  | 任务描述   | 是     |

**请求体**:

```json
{
  "task_description": "分析第一季度销售数据并准备报告"
}
```

**响应**:

```json
{
  "code": 200,
  "msg": "更新任务成功",
  "data": {
    "task_id": 1,
    "task_description": "分析第一季度销售数据并准备报告",
    "created_at": "2023-04-01T09:00:00",
    "completed_at": "2023-04-05T17:30:00",
    "is_completed": true
  },
  "success": true
}
```

### 删除任务

- **URL**: `/api/tasks/{task_id}`
- **方法**: `DELETE`
- **描述**: 删除任务

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| task_id| 整数    | 任务ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "删除任务成功",
  "data": null,
  "success": true
}
```

### 完成任务

- **URL**: `/api/tasks/{task_id}/complete`
- **方法**: `PUT`
- **描述**: 标记任务为已完成

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| task_id| 整数    | 任务ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "任务已标记为完成",
  "data": {
    "task_id": 2,
    "task_description": "准备月度销售报告",
    "created_at": "2023-05-01T10:15:00",
    "completed_at": "2023-05-20T15:45:00",
    "is_completed": true
  },
  "success": true
}
```

### 重新开放任务

- **URL**: `/api/tasks/{task_id}/reopen`
- **方法**: `PUT`
- **描述**: 重新开放任务（标记为未完成）

**请求参数**:

| 参数名   | 类型    | 描述     | 是否必须 |
|--------|--------|--------|-------|
| task_id| 整数    | 任务ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "任务已重新开放",
  "data": {
    "task_id": 1,
    "task_description": "分析第一季度销售数据",
    "created_at": "2023-04-01T09:00:00",
    "completed_at": null,
    "is_completed": false
  },
  "success": true
}
```

## 产品管理API

### 获取所有分类

- **URL**: `/api/products/categories`
- **方法**: `GET`
- **描述**: 获取所有产品分类

**请求参数**: 无

**响应**:

```json
{
  "code": 200,
  "msg": "获取分类列表成功",
  "data": {
    "categories": [
      {
        "category_id": 1,
        "category_name": "电子产品",
        "description": "各类电子设备和配件",
        "created_at": "2023-01-01T00:00:00"
      },
      {
        "category_id": 2,
        "category_name": "家具",
        "description": "办公和家用家具",
        "created_at": "2023-01-01T00:00:00"
      }
    ]
  },
  "success": true
}
```

### 创建新分类

- **URL**: `/api/products/categories`
- **方法**: `POST`
- **描述**: 创建新的产品分类

**请求参数**:

```json
{
  "category_name": "文具",
  "description": "办公和学习用品"
}
```

**响应**:

```json
{
  "code": 201,
  "msg": "创建分类成功",
  "data": {
    "category_id": 3,
    "category_name": "文具",
    "description": "办公和学习用品",
    "created_at": "2023-05-20T16:30:00"
  },
  "success": true
}
```

### 获取分类详情

- **URL**: `/api/products/categories/{category_id}`
- **方法**: `GET`
- **描述**: 获取特定分类的详情

**请求参数**:

| 参数名       | 类型    | 描述     | 是否必须 |
|------------|--------|--------|-------|
| category_id| 整数    | 分类ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "获取分类详情成功",
  "data": {
    "category_id": 1,
    "category_name": "电子产品",
    "description": "各类电子设备和配件",
    "created_at": "2023-01-01T00:00:00"
  },
  "success": true
}
```

### 更新分类

- **URL**: `/api/products/categories/{category_id}`
- **方法**: `PUT`
- **描述**: 更新产品分类

**请求参数**:

```json
{
  "category_name": "电子设备",
  "description": "各类电子设备和配件，包括计算机、手机等"
}
```

**响应**:

```json
{
  "code": 200,
  "msg": "更新分类成功",
  "data": {
    "category_id": 1,
    "category_name": "电子设备",
    "description": "各类电子设备和配件，包括计算机、手机等",
    "created_at": "2023-01-01T00:00:00"
  },
  "success": true
}
```

### 删除分类

- **URL**: `/api/products/categories/{category_id}`
- **方法**: `DELETE`
- **描述**: 删除产品分类

**请求参数**:

| 参数名       | 类型    | 描述     | 是否必须 |
|------------|--------|--------|-------|
| category_id| 整数    | 分类ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "删除分类成功",
  "data": null,
  "success": true
}
```

### 获取所有产品

- **URL**: `/api/products`
- **方法**: `GET`
- **描述**: 获取所有产品

**请求参数**: 无

**响应**:

```json
{
  "code": 200,
  "msg": "获取产品列表成功",
  "data": {
    "products": [
      {
        "product_id": 1,
        "product_name": "笔记本电脑",
        "category_id": 1,
        "category_name": "电子设备",
        "sku": "NB-001",
        "price": 6999.00,
        "cost": 5500.00,
        "description": "高性能笔记本电脑",
        "created_at": "2023-01-10T00:00:00",
        "updated_at": "2023-01-10T00:00:00"
      },
      {
        "product_id": 2,
        "product_name": "办公椅",
        "category_id": 2,
        "category_name": "家具",
        "sku": "CH-001",
        "price": 599.00,
        "cost": 350.00,
        "description": "人体工学办公椅",
        "created_at": "2023-01-15T00:00:00",
        "updated_at": "2023-01-15T00:00:00"
      }
    ]
  },
  "success": true
}
```

### 创建新产品

- **URL**: `/api/products`
- **方法**: `POST`
- **描述**: 创建新产品

**请求参数**:

```json
{
  "product_name": "无线鼠标",
  "category_id": 1,
  "sku": "MS-001",
  "price": 89.90,
  "cost": 45.00,
  "description": "蓝牙无线鼠标"
}
```

**响应**:

```json
{
  "code": 201,
  "msg": "创建产品成功",
  "data": {
    "product_id": 3,
    "product_name": "无线鼠标",
    "category_id": 1,
    "category_name": "电子设备",
    "sku": "MS-001",
    "price": 89.90,
    "cost": 45.00,
    "description": "蓝牙无线鼠标",
    "created_at": "2023-05-20T17:00:00",
    "updated_at": "2023-05-20T17:00:00"
  },
  "success": true
}
```

### 获取产品详情

- **URL**: `/api/products/{product_id}`
- **方法**: `GET`
- **描述**: 获取特定产品的详情

**请求参数**:

| 参数名      | 类型    | 描述     | 是否必须 |
|-----------|--------|--------|-------|
| product_id| 整数    | 产品ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "获取产品详情成功",
  "data": {
    "product_id": 1,
    "product_name": "笔记本电脑",
    "category_id": 1,
    "category_name": "电子设备",
    "sku": "NB-001",
    "price": 6999.00,
    "cost": 5500.00,
    "description": "高性能笔记本电脑",
    "created_at": "2023-01-10T00:00:00",
    "updated_at": "2023-01-10T00:00:00"
  },
  "success": true
}
```

### 更新产品

- **URL**: `/api/products/{product_id}`
- **方法**: `PUT`
- **描述**: 更新产品信息

**请求参数**:

```json
{
  "product_name": "高性能笔记本电脑",
  "price": 7299.00,
  "cost": 5800.00,
  "description": "高性能笔记本电脑，配备最新处理器"
}
```

**响应**:

```json
{
  "code": 200,
  "msg": "更新产品成功",
  "data": {
    "product_id": 1,
    "product_name": "高性能笔记本电脑",
    "category_id": 1,
    "category_name": "电子设备",
    "sku": "NB-001",
    "price": 7299.00,
    "cost": 5800.00,
    "description": "高性能笔记本电脑，配备最新处理器",
    "created_at": "2023-01-10T00:00:00",
    "updated_at": "2023-05-20T17:15:00"
  },
  "success": true
}
```

### 删除产品

- **URL**: `/api/products/{product_id}`
- **方法**: `DELETE`
- **描述**: 删除产品

**请求参数**:

| 参数名      | 类型    | 描述     | 是否必须 |
|-----------|--------|--------|-------|
| product_id| 整数    | 产品ID   | 是     |

**响应**:

```json
{
  "code": 200,
  "msg": "删除产品成功",
  "data": null,
  "success": true
}
```

## 销售分析API

### 获取销售报表

- **URL**: `/api/analytics/report`
- **方法**: `GET`
- **描述**: 获取销售报表数据

**请求参数**:

| 参数名       | 类型    | 描述                       | 是否必须 |
|------------|--------|--------------------------|-------|
| start_date | 字符串   | 开始日期 (YYYY-MM-DD)       | 否     |
| end_date   | 字符串   | 结束日期 (YYYY-MM-DD)       | 否     |
| period     | 字符串   | 周期类型 (daily/monthly/yearly) | 否   |
| category_id| 整数    | 分类ID                     | 否     |
| product_id | 整数    | 产品ID                     | 否     |

**示例请求**: `/api/analytics/report?start_date=2023-01-01&end_date=2023-03-31&period=monthly&category_id=1`

**响应**:

```json
{
  "code": 200,
  "msg": "获取销售报表成功",
  "data": {
    "report": [
      {
        "analytics_id": 1,
        "product_id": null,
        "product_name": null,
        "category_id": 1,
        "category_name": "电子设备",
        "date_period": "2023-01-01",
        "period_type": "monthly",
        "total_quantity": 45,
        "total_revenue": 124500.00,
        "total_cost": 95000.00,
        "profit": 29500.00,
        "last_updated": "2023-05-20T10:00:00"
      },
      {
        "analytics_id": 2,
        "product_id": null,
        "product_name": null,
        "category_id": 1,
        "category_name": "电子设备",
        "date_period": "2023-02-01",
        "period_type": "monthly",
        "total_quantity": 38,
        "total_revenue": 105000.00,
        "total_cost": 80000.00,
        "profit": 25000.00,
        "last_updated": "2023-05-20T10:00:00"
      },
      {
        "analytics_id": 3,
        "product_id": null,
        "product_name": null,
        "category_id": 1,
        "category_name": "电子设备",
        "date_period": "2023-03-01",
        "period_type": "monthly",
        "total_quantity": 52,
        "total_revenue": 145000.00,
        "total_cost": 110000.00,
        "profit": 35000.00,
        "last_updated": "2023-05-20T10:00:00"
      }
    ],
    "summary": {
      "total_quantity": 135,
      "total_revenue": 374500.00,
      "total_cost": 285000.00,
      "total_profit": 89500.00,
      "period_count": 3
    }
  },
  "success": true
}
```

### 获取销售趋势

- **URL**: `/api/analytics/trends`
- **方法**: `GET`
- **描述**: 获取销售趋势数据

**请求参数**:

| 参数名       | 类型    | 描述                           | 是否必须 |
|------------|--------|------------------------------|-------|
| period     | 字符串   | 趋势周期 (weekly/monthly/yearly) | 否    |
| product_id | 整数    | 产品ID                         | 否     |
| category_id| 整数    | 分类ID                         | 否     |
| limit      | 整数    | 返回结果数量限制                   | 否     |

**示例请求**: `/api/analytics/trends?period=monthly&category_id=1&limit=6`

**响应**:

```json
{
  "code": 200,
  "msg": "获取销售趋势成功",
  "data": {
    "trends": [
      {
        "date": "2022-12-01",
        "revenue": 98000.00,
        "profit": 23000.00,
        "quantity": 35,
        "label": "电子设备"
      },
      {
        "date": "2023-01-01",
        "revenue": 124500.00,
        "profit": 29500.00,
        "quantity": 45,
        "label": "电子设备"
      },
      {
        "date": "2023-02-01",
        "revenue": 105000.00,
        "profit": 25000.00,
        "quantity": 38,
        "label": "电子设备"
      },
      {
        "date": "2023-03-01",
        "revenue": 145000.00,
        "profit": 35000.00,
        "quantity": 52,
        "label": "电子设备"
      },
      {
        "date": "2023-04-01",
        "revenue": 132000.00,
        "profit": 31000.00,
        "quantity": 47,
        "label": "电子设备"
      },
      {
        "date": "2023-05-01",
        "revenue": 115000.00,
        "profit": 27000.00,
        "quantity": 41,
        "label": "电子设备"
      }
    ],
    "period": "monthly",
    "total_periods": 6
  },
  "success": true
}
```

### 获取销售摘要

- **URL**: `/api/analytics/summary`
- **方法**: `GET`
- **描述**: 获取销售数据摘要

**请求参数**: 无

**响应**:

```json
{
  "code": 200,
  "msg": "获取销售摘要成功",
  "data": {
    "total_revenue": 1250000.00,
    "total_orders": 850,
    "total_products": 25,
    "total_categories": 4,
    "top_products": [
      {
        "product_id": 1,
        "product_name": "笔记本电脑",
        "total_quantity": 120
      },
      {
        "product_id": 5,
        "product_name": "耳机",
        "total_quantity": 95
      },
      {
        "product_id": 3,
        "product_name": "机械键盘",
        "total_quantity": 80
      },
      {
        "product_id": 2,
        "product_name": "无线鼠标",
        "total_quantity": 75
      },
      {
        "product_id": 7,
        "product_name": "办公椅",
        "total_quantity": 60
      }
    ]
  },
  "success": true
}
```

### 处理销售数据

- **URL**: `/api/analytics/process-data`
- **方法**: `POST`
- **描述**: 处理销售数据并生成分析结果

**请求参数**: 无

**响应**:

```json
{
  "code": 200,
  "msg": "销售数据处理成功",
  "data": null,
  "success": true
}
``` 