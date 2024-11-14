-- select with case expression
SELECT FullName, YearOfBirth,
       CASE
           WHEN YearOfBirth <= 1979 THEN 'Veteran'
           WHEN YearOfBirth > 1979 AND YearOfBirth <= 1994 THEN 'Experienced'
           ELSE 'Newbie'
       END AS Category
FROM Employees;

-- select using window function
SELECT FullName, Position, SUM(Sum) OVER (PARTITION BY EmployeeID ORDER BY EmployeeID) AS RunningTotal
FROM ExchangeOperations
JOIN Employees ON Employees.ID = ExchangeOperations.EmployeeID
GROUP BY EmployeeID, FullName, Position, Sum
ORDER BY EmployeeID;

-- select with group by and having
SELECT Currency, SUM(Sum) AS TotalSum
FROM ExchangeOperations
JOIN CurrencyTypes ON CurrencyTypes.ID = ExchangeOperations.CurrencyID
GROUP BY Currency
HAVING SUM(Sum) > 3000;

-- backup procedure
CREATE OR REPLACE PROCEDURE CopyDatabaseSchema(schema_name TEXT, backup_date TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
    original_table_name TEXT;
    new_table_name TEXT;
    query TEXT;
BEGIN
    FOR original_table_name IN SELECT table_name FROM information_schema.tables WHERE table_schema = schema_name
    LOOP
        new_table_name := original_table_name || '_' || backup_date;
        query := format('CREATE TABLE %I AS TABLE %I.%I', new_table_name, schema_name, original_table_name);
        EXECUTE query;
    END LOOP;
END;
$$;

CALL CopyDatabaseSchema('public', '20231114');

SELECT * FROM currencyrates_20231114;
