drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists measurement;
create table measurement (
  id integer primary key autoincrement,
  systolic_pressure int not null
  diastolic_pressure int not null

)

