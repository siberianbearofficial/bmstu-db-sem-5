create table customer
(
    customer_id int primary key,
    name        varchar not null,
    birthday    date    not null,
    city        varchar not null,
    tel         varchar not null
);

create table florist
(
    florist_id int primary key,
    name       varchar not null,
    passport   varchar not null,
    tel        varchar not null
);

create table bouquet
(
    bouquet_id int primary key,
    author     int     not null,
    name       varchar not null
);

alter table bouquet
    add constraint fk_author foreign key (author) references florist (florist_id);

create table florist_customer
(
    florist_customer_id int primary key,
    florist             int not null,
    customer            int not null
);

alter table florist_customer
    add constraint fk_florist foreign key (florist) references florist (florist_id),
    add constraint fk_customer foreign key (customer) references customer (customer_id);
