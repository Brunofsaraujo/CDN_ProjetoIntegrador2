WITH RECURSIVE Meses AS (
    SELECT DATE('2024-07-01') AS MesReferencia
    UNION ALL
    SELECT DATE(MesReferencia, '+1 month')
    FROM Meses
    WHERE MesReferencia < '2026-12-31'
),
Alugueis AS (
    SELECT 
        strftime('%Y-%m', DataReserva) AS Mes,
        SUM(ValorTotal) AS TotalAluguel
    FROM 
        Reservas
    WHERE 
        DataReserva BETWEEN '2024-07-01' AND '2026-12-31' 
        AND StatusReserva = 'Confirmada'
    GROUP BY 
        Mes
),
Taxas AS (
    SELECT 
        strftime('%Y-%m', DataReceita) AS Mes,
        SUM(ValorReceita) AS TotalTaxas
    FROM 
        Receitas
    WHERE 
        OrigemReceita = 'Reserva'
        AND DataReceita BETWEEN '2024-07-01' AND '2026-12-31'
    GROUP BY 
        Mes
)

SELECT 
    strftime('%Y-%m', m.MesReferencia) AS MesReferencia,
    Round(COALESCE(a.TotalAluguel, 0),0) AS TotalAluguel,
    Round(COALESCE(a.TotalAluguel - t.TotalTaxas, 0),0) AS TotalTaxas,
    Round((a.TotalAluguel - COALESCE(a.TotalAluguel - t.TotalTaxas, 0)),0) * 0.70 AS CustoOperacional
FROM 
    Meses m
LEFT JOIN 
    Alugueis a ON strftime('%Y-%m', m.MesReferencia) = a.Mes
LEFT JOIN 
    Taxas t ON strftime('%Y-%m', m.MesReferencia) = t.Mes
ORDER BY 
    m.MesReferencia;
