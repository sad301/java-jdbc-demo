.mode lines
with stats as (
  select j.handphone,
  ( select count(id)
    from jobs
    where handphone=j.handphone
    and status='UNCONFIRMED' ) as 'unconfirmed'
  from jobs j
) select * from stats where handphone='222';
