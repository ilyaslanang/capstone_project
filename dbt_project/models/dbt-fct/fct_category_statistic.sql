    -- 4. Model untuk Statistik Kategori Produk (category_statistics.sql):
    --     - nama_kategori
    --     - jumlah_produk
    --     - rata_usia_produk

SELECT 
    category_name as nama_kategori
    , COALESCE(count(stg_product.category_id), 0) AS jumlah_produk
    , COALESCE(AVG((expired_date - production_date)), 0) AS rata_usia_produk
    , COALESCE(sum(sales_amount), 0) as jumlah_penjualan 
FROM 
    {{ ref('stg_productcategory') }} stg_productcategory
LEFT JOIN 
    {{ ref('stg_product') }} stg_product
ON stg_product.category_id = stg_productcategory.category_id
LEFT JOIN 
    {{ ref('stg_transaction') }} stg_transaction
ON stg_transaction.product_id = stg_product.product_id
GROUP BY nama_kategori