--新建表空间
create tablespace gis_tablespace location '/opt/pg/9.6/gisdata';

--创建ower
create role gis login password 'gis';

--创建数据库
create database gisdata owner gis tablespace gis_tablespace;




--from apps import db
--db.create_all()
