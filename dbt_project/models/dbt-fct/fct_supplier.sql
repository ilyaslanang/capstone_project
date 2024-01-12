SELECT 
    supplier_name as nama_supplier
    , COALESCE(sum(stock_amount), 0)  as jumlah_stock
    , count(stg_stock.product_id) as jumlah_produk
FROM 
    {{ ref('stg_supplier') }} stg_supplier
LEFT JOIN 
    {{ ref('stg_product') }} stg_product
ON stg_supplier.supplier_id = stg_product.supplier_id
LEFT JOIN 
    {{ ref('stg_stock') }} stg_stock
ON stg_product.product_id = stg_stock.product_id
GROUP BY nama_supplier