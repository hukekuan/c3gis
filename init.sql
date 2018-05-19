--新建表空间
create tablespace gis_tablespace location '/opt/pg/9.6/gisdata';

--创建ower
create role gis login password 'gis';

--创建数据库
create database gisdata owner gis tablespace gis_tablespace;

ALTER TABLE SYS_USER ADD COLUMN sortednum integer NOT NULL;

--test
--from apps import db
--db.create_all()


CREATE TABLE wx_access (
	appid VARCHAR(45) NOT NULL,
	token VARCHAR(500),
	updatedate TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (appid)
);

CREATE TABLE wx_user (
	userid VARCHAR(45) NOT NULL,
	appid VARCHAR(45),
	appsecret VARCHAR(45),
	PRIMARY KEY (userid)
);
