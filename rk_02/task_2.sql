-- Получим покупателей, которые еще не работали с флористами
select *
from customer
where not exists (select 1
                  from florist_customer as fc
                           join florist on fc.florist = florist.florist_id
                  where fc.customer = customer.customer_id
                    and city = (select city from customer where customer_id = fc.customer));

-- Получим покупателей из Москвы (local) и не из Москвы (foreign)
select customer_id,
       name,
       case
           when city = 'moscow' then 'local'
           else 'foreign'
           end as customer_type
from customer;

-- Получим список флористов с их самыми популярными букетами
select name,
       (select bouquet.name
        from bouquet
        where bouquet.author = florist.florist_id
        order by (select count(*)
                  from florist_customer as fc
                  where fc.florist = bouquet.author
                    and fc.customer in (select customer
                                        from florist_customer as fc2
                                        where fc2.florist = bouquet.author)) desc
        limit 1) as popular_bouquet
from florist;
