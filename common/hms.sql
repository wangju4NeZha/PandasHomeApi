drop DATABASE if EXISTS homems;

CREATE DATABASE homems CHARSET=utf8;
use homems;
/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/2/28 ������ 18:05:13                       */
/*==============================================================*/


drop table if exists contract;

drop table if exists t_browsing_history;

drop table if exists t_chatmsg;

drop table if exists t_comment;

drop table if exists t_complaint;

drop table if exists t_favorite;

drop table if exists t_feedback;

drop table if exists t_house;

drop table if exists t_house_verify;

drop table if exists t_lucky_ticket;

drop table if exists t_message;

drop table if exists t_order;

drop table if exists t_panda;

drop table if exists t_public_notice;

drop table if exists t_score;

drop table if exists t_service;

drop table if exists t_slidesshow;

drop table if exists t_sys_menu;

drop table if exists t_sys_role;

drop table if exists t_sys_role_menu;

drop table if exists t_sys_user;

drop table if exists t_tradingrecord;

drop table if exists t_u_lucky_ticket;

drop table if exists t_user;

/*==============================================================*/
/* Table: contract                                              */
/*==============================================================*/
create table contract
(
   t_contract_id        int not null auto_increment,
   user_id              int,
   start_time           date,
   stop_time            date,
   content              longtext,
   primary key (t_contract_id)
);

/*==============================================================*/
/* Table: t_browsing_history                                    */
/*==============================================================*/
create table t_browsing_history
(
   browsing_history_id  int not null auto_increment,
   usert_id             int,
   house_id             int,
   primary key (browsing_history_id)
);

/*==============================================================*/
/* Table: t_chatmsg                                             */
/*==============================================================*/
create table t_chatmsg
(
   chatmsg_id           int not null auto_increment,
   msg_id               int,
   chatmsg_time         datetime,
   content              text,
   primary key (chatmsg_id)
);

/*==============================================================*/
/* Table: t_comment                                             */
/*==============================================================*/
create table t_comment
(
   comment_id           int not null auto_increment,
   user_id              int,
   house_id             int,
   create_time          datetime,
   content              text,
   state                int,
   primary key (comment_id)
);

/*==============================================================*/
/* Table: t_complaint                                           */
/*==============================================================*/
create table t_complaint
(
   fadeback_id          int not null auto_increment,
   user_id              int,
   order_id             int,
   phone                int(11),
   email                varchar(30),
   content              text,
   state                int,
   primary key (fadeback_id)
);

/*==============================================================*/
/* Table: t_favorite                                            */
/*==============================================================*/
create table t_favorite
(
   favorite_id          int not null auto_increment,
   house_id             int,
   user_id              int,
   primary key (favorite_id)
);

/*==============================================================*/
/* Table: t_feedback                                            */
/*==============================================================*/
create table t_feedback
(
   fadeback_id          int not null auto_increment,
   user_id              int,
   house_id             int,
   phone                int(11),
   email                varchar(30),
   content              text,
   primary key (fadeback_id)
);

/*==============================================================*/
/* Table: t_house                                               */
/*==============================================================*/
create table t_house
(
   house_id             int not null auto_increment,
   user_id              int,
   image                varchar(200),
   name                 varchar(200),
   type                 text,
   address              text,
   price                int,
   publish_time         date,
   area                 float,
   description          text,
   sale_status          int,
   primary key (house_id)
);

/*==============================================================*/
/* Table: t_house_verify                                        */
/*==============================================================*/
create table t_house_verify
(
   verify_id            int not null auto_increment,
   house_id             int,
   verify_status        int,
   remarks              text,
   primary key (verify_id)
);

/*==============================================================*/
/* Table: t_lucky_ticket                                        */
/*==============================================================*/
create table t_lucky_ticket
(
   lucky_ticket_id      int not null auto_increment,
   money                int,
   begin_time           date,
   end_time             date,
   image                varchar(200),
   primary key (lucky_ticket_id)
);

/*==============================================================*/
/* Table: t_message                                             */
/*==============================================================*/
create table t_message
(
   msg_id               int not null auto_increment,
   user_id              int,
   house_id             int,
   primary key (msg_id)
);

/*==============================================================*/
/* Table: t_order                                               */
/*==============================================================*/
create table t_order
(
   order_id             int not null auto_increment,
   house_id             int,
   user_id              int,
   order_number         varchar(16),
   enter_time           time,
   exit_time            time,
   hire_price           float,
   cash_price           float,
   total                float,
   order_status         int,
   primary key (order_id)
);

/*==============================================================*/
/* Table: t_panda                                               */
/*==============================================================*/
create table t_panda
(
   panda_id             int not null auto_increment,
   detail_content       longtext,
   primary key (panda_id)
);

/*==============================================================*/
/* Table: t_public_notice                                       */
/*==============================================================*/
create table t_public_notice
(
   public_notice_id     int not null auto_increment,
   content              longtext,
   public_title         varchar(50),
   public_time          datetime,
   public_remarks       text,
   public_status        int,
   primary key (public_notice_id)
);

/*==============================================================*/
/* Table: t_score                                               */
/*==============================================================*/
create table t_score
(
   score_id             int not null auto_increment,
   user_id              int,
   score                int,
   primary key (score_id)
);

/*==============================================================*/
/* Table: t_service                                             */
/*==============================================================*/
create table t_service
(
   service_id           int not null auto_increment,
   content              text,
   service_status       int,
   primary key (service_id)
);

/*==============================================================*/
/* Table: t_slidesshow                                          */
/*==============================================================*/
create table t_slidesshow
(
   slidesshow_id        int not null auto_increment,
   house_id             int,
   ord                  int not null,
   primary key (slidesshow_id)
);

/*==============================================================*/
/* Table: t_sys_menu                                            */
/*==============================================================*/
create table t_sys_menu
(
   menu_id              int not null auto_increment,
   menu_name            varchar(20),
   ord                  int,
   url                  varchar(50),
   primary key (menu_id)
);

/*==============================================================*/
/* Table: t_sys_role                                            */
/*==============================================================*/
create table t_sys_role
(
   role_id              int not null auto_increment,
   role_name            varchar(20),
   role_code            varchar(10),
   primary key (role_id)
);

/*==============================================================*/
/* Table: t_sys_role_menu                                       */
/*==============================================================*/
create table t_sys_role_menu
(
   role_id              int,
   sys_menu_id          int not null auto_increment,
   primary key (sys_menu_id)
);

/*==============================================================*/
/* Table: t_sys_user                                            */
/*==============================================================*/
create table t_sys_user
(
   user_id              int not null auto_increment,
   username             varchar(20),
   role_id              int,
   password             varchar(32),
   nick_name            varchar(20),
   head                 varchar(300),
   email                varchar(30),
   primary key (user_id)
);

/*==============================================================*/
/* Table: t_tradingrecord                                       */
/*==============================================================*/
create table t_tradingrecord
(
   tradingrecord_id     int not null auto_increment,
   house_id             int,
   user_id              int,
   payment_date         datetime,
   payment_type         int,
   primary key (tradingrecord_id)
);

/*==============================================================*/
/* Table: t_u_lucky_ticket                                      */
/*==============================================================*/
create table t_u_lucky_ticket
(
   u_lucky_ticketid     int not null auto_increment,
   user_id              int,
   lucky_ticket_id      int,
   primary key (u_lucky_ticketid)
);

/*==============================================================*/
/* Table: t_user                                                */
/*==============================================================*/
create table t_user
(
   user_id              int not null auto_increment,
   name                 varchar(100),
   sex                  varchar(20),
   identity_number      varchar(18),
   nickname             varchar(100),
   img                  varchar(200),
   phone                varchar(11),
   email                varchar(60),
   password             varchar(30),
   has_real_name        int,
   is_member            int,
   longitude            float,
   dimension            float,
   primary key (user_id)
);

alter table contract add constraint FK_Reference_27 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_browsing_history add constraint FK_Reference_11 foreign key (usert_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_browsing_history add constraint FK_Reference_12 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_chatmsg add constraint FK_Reference_24 foreign key (msg_id)
      references t_message (msg_id) on delete restrict on update restrict;

alter table t_comment add constraint FK_Reference_16 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_comment add constraint FK_Reference_17 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_complaint add constraint FK_Reference_13 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_complaint add constraint FK_Reference_19 foreign key (order_id)
      references t_order (order_id) on delete restrict on update restrict;

alter table t_favorite add constraint FK_Reference_5 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_favorite add constraint FK_Reference_6 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_feedback add constraint FK_Reference_15 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_feedback add constraint FK_Reference_9 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_house add constraint FK_Reference_20 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_house_verify add constraint FK_Reference_29 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_message add constraint FK_Reference_22 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_message add constraint FK_Reference_23 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_order add constraint FK_Reference_4 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_order add constraint FK_Reference_8 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_score add constraint FK_Reference_21 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_slidesshow add constraint FK_Reference_18 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_tradingrecord add constraint FK_Reference_10 foreign key (house_id)
      references t_house (house_id) on delete restrict on update restrict;

alter table t_tradingrecord add constraint FK_Reference_7 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

alter table t_u_lucky_ticket add constraint FK_Reference_25 foreign key (lucky_ticket_id)
      references t_lucky_ticket (lucky_ticket_id) on delete restrict on update restrict;

alter table t_u_lucky_ticket add constraint FK_Reference_26 foreign key (user_id)
      references t_user (user_id) on delete restrict on update restrict;

