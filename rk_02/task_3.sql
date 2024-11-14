create or replace procedure find_most_referenced_table()
language plpgsql
as $$
declare
    max_t_name text;
    max_t_count int;
begin
    select table_name as t_name, count(*) as t_count into max_t_name, max_t_count
    from information_schema.constraint_column_usage
    where table_schema = 'public'
    group by t_name
    order by t_count desc
    limit 1;

    raise notice 'Table % is referenced the most with % references.', max_t_name, max_t_count;
end;
$$;

call find_most_referenced_table()
