create table config (
  _key varchar(32) not null,
  _value text not null,
  primary key (_key)
);

create table jobs (
  id varchar(16) not null,
  kode varchar(16) not null,
  tanggal date not null default current_timestamp,
  nama varchar(16) not null,
  handphone varchar(16) not null,
  client_file text not null,
  server_file text not null,
	-- max_page int not null default 0,
  page_grayscale int not null default 0,
  page_color int not null default 0,
  page_blank int not null default 0,
  page_total int not null default 0,
  price_grayscale int not null default 0,
  price_color int not null default 0,
  price_blank int not null default 0,
  price_total int not null default 0,
  status text check(status in ('UNCONFIRMED', 'CONFIRMED', 'PRINTED', 'PAID')) not null default 'UNCONFIRMED',
  processed int not null default 0,
  primary key (id)
);

create view stats as
  select j.handphone,
    ( select count(id) from jobs where handphone=j.handphone and status='UNCONFIRMED' ) as 'unconfirmed',
    ( select count(id) from jobs where handphone=j.handphone and status='CONFIRMED' ) as 'confirmed',
    ( select count(id) from jobs where handphone=j.handphone and status='PRINTED' ) as 'printed',
    ( select count(id) from jobs where handphone=j.handphone and status='PAID' ) as 'paid'
  from jobs j
  group by handphone;
