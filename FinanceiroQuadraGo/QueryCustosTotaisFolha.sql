WITH RECURSIVE meses(mes) AS (
    SELECT date('2024-07-01')
    UNION ALL
    SELECT date(mes, '+1 month')
    FROM meses
    WHERE mes < '2026-12-01'
),
ultimo_salario_vigente AS (
    SELECT 
        m.mes,
        hs.ID_Funcionario,
        hs.Salario
    FROM meses m
    CROSS JOIN (SELECT DISTINCT ID_Funcionario FROM HistoricoSalario) f
    LEFT JOIN HistoricoSalario hs ON 
        hs.ID_Funcionario = f.ID_Funcionario AND
        hs.DataAjuste = (
            SELECT MAX(DataAjuste)
            FROM HistoricoSalario hs2
            WHERE hs2.ID_Funcionario = f.ID_Funcionario
            AND hs2.DataAjuste <= m.mes
        )
    WHERE hs.Salario IS NOT NULL
)
SELECT 
    mes,
    ROUND(SUM(CASE
        -- Gestores e coordenadores - CLT
        WHEN ID_Funcionario IN (1, 2, 3, 4, 5, 6, 7) THEN 
            Salario * 1.68
        -- Especialistas técnicos - PJ
        WHEN ID_Funcionario IN (8, 9, 10, 12, 13, 14, 16, 19) THEN 
            Salario * 1.15
        -- Demais cargos - CLT
        ELSE Salario * 1.68
    END), 2) as custo_total_mes,
    -- Provisão mensal do 13º (1/12 do salário + encargos) apenas para CLT
    ROUND(SUM(CASE
        WHEN ID_Funcionario IN (1, 2, 3, 4, 5, 6, 7, 11, 15, 17, 18, 20, 21) THEN 
            (Salario * 1.68) / 12
        ELSE 0
    END), 2) as provisao_13_salario,
    -- Custo total incluindo 13º
    ROUND(SUM(CASE
        -- CLT (salário + 1/12 do 13º)
        WHEN ID_Funcionario IN (1, 2, 3, 4, 5, 6, 7, 11, 15, 17, 18, 20, 21) THEN 
            Salario * 1.68 * 13/12
        -- PJ (sem 13º)
        ELSE Salario * 1.15
    END), 2) as custo_total_com_13,
    COUNT(ID_Funcionario) as total_funcionarios,
    SUM(CASE WHEN ID_Funcionario IN (1, 2, 3, 4, 5, 6, 7, 11, 15, 17, 18, 20, 21) THEN 1 ELSE 0 END) as total_clt,
    SUM(CASE WHEN ID_Funcionario IN (8, 9, 10, 12, 13, 14, 16, 19) THEN 1 ELSE 0 END) as total_pj
FROM ultimo_salario_vigente
GROUP BY mes
ORDER BY mes;