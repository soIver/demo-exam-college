WITH product_material_cost as (
	SELECT 
		pm.product, 
		SUM(pm.quantity * m.price) as material_cost
	FROM product_materials pm
	JOIN materials m ON pm.material = m.id
	GROUP BY pm.product
)

SELECT
	o.id as "Код заказа",
	o.date as "Дата заказа",
	c.name as "Покупатель",
	SUM(op.quantity * pmc.material_cost) as "Стоимость заказа"
FROM orders o
JOIN contractors c ON o.buyer = c.id
JOIN order_products op ON o.id = op."order"
JOIN product_material_cost pmc on op.product = pmc.product
GROUP BY o.id, c.name