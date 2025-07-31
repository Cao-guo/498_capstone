-- Smart Retail Analytics - Database Schema (PostgreSQL 15)

-- 文件上传表 - 存储上传的销售数据文件信息
CREATE TABLE uploaded_files (
    file_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    processing_errors TEXT
);

-- 任务表 - 存储用户创建的任务
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    task_description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    is_completed BOOLEAN DEFAULT FALSE
);

-- 产品分类表
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 产品表
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    sku VARCHAR(50) UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 销售交易表 - 存储上传的CSV销售数据
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    transaction_date TIMESTAMP NOT NULL,
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    file_id INTEGER REFERENCES uploaded_files(file_id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 销售分析汇总表 - 预计算的销售统计数据
CREATE TABLE sales_analytics (
    analytics_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id),
    category_id INTEGER REFERENCES categories(category_id),
    date_period DATE NOT NULL,  -- 可以是天、月或年的第一天
    period_type VARCHAR(10) NOT NULL,  -- 'daily', 'monthly', 'yearly'
    total_quantity INTEGER NOT NULL DEFAULT 0,
    total_revenue DECIMAL(14, 2) NOT NULL DEFAULT 0,
    total_cost DECIMAL(14, 2) NOT NULL DEFAULT 0,
    profit DECIMAL(14, 2) NOT NULL DEFAULT 0,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以优化查询性能
CREATE INDEX idx_sales_transaction_date ON sales(transaction_date);
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_sales_analytics_date ON sales_analytics(date_period, period_type);
CREATE INDEX idx_sales_analytics_product ON sales_analytics(product_id);
CREATE INDEX idx_sales_analytics_category ON sales_analytics(category_id); 