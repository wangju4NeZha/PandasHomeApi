# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, MetaData, String, Text, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class Contract(Base):
    __tablename__ = 'contract'

    t_contract_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    start_time = Column(Date)
    stop_time = Column(Date)
    content = Column(String)

    user = relationship('TUser', primaryjoin='Contract.user_id == TUser.user_id', backref='contracts')



class TBrowsingHistory(Base):
    __tablename__ = 't_browsing_history'

    browsing_history_id = Column(Integer, primary_key=True)
    usert_id = Column(ForeignKey('t_user.user_id'), index=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)

    house = relationship('THouse', primaryjoin='TBrowsingHistory.house_id == THouse.house_id', backref='t_browsing_histories')
    usert = relationship('TUser', primaryjoin='TBrowsingHistory.usert_id == TUser.user_id', backref='t_browsing_histories')



class TChatmsg(Base):
    __tablename__ = 't_chatmsg'

    chatmsg_id = Column(Integer, primary_key=True)
    msg_id = Column(ForeignKey('t_message.msg_id'), index=True)
    chatmsg_time = Column(DateTime)
    content = Column(Text)

    msg = relationship('TMessage', primaryjoin='TChatmsg.msg_id == TMessage.msg_id', backref='t_chatmsgs')



class TComment(Base):
    __tablename__ = 't_comment'

    comment_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)
    comment_time = Column(DateTime)
    content = Column(Text)
    grade = Column(Integer)

    house = relationship('THouse', primaryjoin='TComment.house_id == THouse.house_id', backref='t_comments')
    user = relationship('TUser', primaryjoin='TComment.user_id == TUser.user_id', backref='t_comments')



class TComplaint(Base):
    __tablename__ = 't_complaint'

    fadeback_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    order_id = Column(ForeignKey('t_order.order_id'), index=True)
    phone = Column(Integer)
    email = Column(String(30))
    content = Column(Text)

    order = relationship('TOrder', primaryjoin='TComplaint.order_id == TOrder.order_id', backref='t_complaints')
    user = relationship('TUser', primaryjoin='TComplaint.user_id == TUser.user_id', backref='t_complaints')



class TFavorite(Base):
    __tablename__ = 't_favorite'

    favorite_id = Column(Integer, primary_key=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)

    house = relationship('THouse', primaryjoin='TFavorite.house_id == THouse.house_id', backref='t_favorites')
    user = relationship('TUser', primaryjoin='TFavorite.user_id == TUser.user_id', backref='t_favorites')



class TFeedback(Base):
    __tablename__ = 't_feedback'

    fadeback_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)
    phone = Column(Integer)
    email = Column(String(30))
    content = Column(Text)

    house = relationship('THouse', primaryjoin='TFeedback.house_id == THouse.house_id', backref='t_feedbacks')
    user = relationship('TUser', primaryjoin='TFeedback.user_id == TUser.user_id', backref='t_feedbacks')



class THouse(Base):
    __tablename__ = 't_house'

    house_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    image = Column(String(200))
    name = Column(String(200))
    type = Column(Text)
    address = Column(Text)
    price = Column(Integer)
    publish_time = Column(Date)
    area = Column(Float)
    description = Column(Text)
    sale_status = Column(Integer)

    user = relationship('TUser', primaryjoin='THouse.user_id == TUser.user_id', backref='t_houses')



class TLuckyTicket(Base):
    __tablename__ = 't_lucky_ticket'

    lucky_ticket_id = Column(Integer, primary_key=True)
    u_lucky_ticketid = Column(ForeignKey('t_u_lucky_ticket.u_lucky_ticketid'), index=True)
    money = Column(Integer)
    begin_time = Column(Date)
    end_time = Column(Date)
    image = Column(String(20))

    t_u_lucky_ticket = relationship('TULuckyTicket', primaryjoin='TLuckyTicket.u_lucky_ticketid == TULuckyTicket.u_lucky_ticketid', backref='t_lucky_tickets')



class TMessage(Base):
    __tablename__ = 't_message'

    msg_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)

    house = relationship('THouse', primaryjoin='TMessage.house_id == THouse.house_id', backref='t_messages')
    user = relationship('TUser', primaryjoin='TMessage.user_id == TUser.user_id', backref='t_messages')



class TOrder(Base):
    __tablename__ = 't_order'

    order_id = Column(Integer, primary_key=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    order_number = Column(String(16))
    enter_time = Column(Time)
    exit_time = Column(Time)
    hire_price = Column(Float)
    cash_price = Column(Float)
    total = Column(Float)
    order_status = Column(Integer)

    house = relationship('THouse', primaryjoin='TOrder.house_id == THouse.house_id', backref='t_orders')
    user = relationship('TUser', primaryjoin='TOrder.user_id == TUser.user_id', backref='t_orders')



class TPanda(Base):
    __tablename__ = 't_panda'

    panda_id = Column(Integer, primary_key=True)
    detail_content = Column(String)



class TScore(Base):
    __tablename__ = 't_score'

    score_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    score = Column(Integer)

    user = relationship('TUser', primaryjoin='TScore.user_id == TUser.user_id', backref='t_scores')



class TService(Base):
    __tablename__ = 't_service'

    service_id = Column(Integer, primary_key=True)
    content = Column(Text)
    service_status = Column(Integer)



class TSlidesshow(Base):
    __tablename__ = 't_slidesshow'

    slidesshow_id = Column(Integer, primary_key=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)
    ord = Column(Integer, nullable=False)

    house = relationship('THouse', primaryjoin='TSlidesshow.house_id == THouse.house_id', backref='t_slidesshows')



class TSysMenu(Base):
    __tablename__ = 't_sys_menu'

    menu_id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('t_sys_menu.menu_id'), index=True)
    menu_name = Column(String(20))
    ord = Column(Integer)
    url = Column(String(50))

    parent = relationship('TSysMenu', remote_side=[menu_id], primaryjoin='TSysMenu.parent_id == TSysMenu.menu_id', backref='t_sys_menus')



class TSysRole(Base):
    __tablename__ = 't_sys_role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(20))
    role_code = Column(String(10))



class TSysRoleMenu(Base):
    __tablename__ = 't_sys_role_menu'

    sys_menu_id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('t_sys_role.role_id'), index=True)
    menu_id = Column(ForeignKey('t_sys_menu.menu_id'), index=True)

    menu = relationship('TSysMenu', primaryjoin='TSysRoleMenu.menu_id == TSysMenu.menu_id', backref='t_sys_role_menus')
    role = relationship('TSysRole', primaryjoin='TSysRoleMenu.role_id == TSysRole.role_id', backref='t_sys_role_menus')



class TSysUser(Base):
    __tablename__ = 't_sys_user'

    user_id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('t_sys_role.role_id'), index=True)
    username = Column(String(20))
    password = Column(String(32))
    nick_name = Column(String(20))

    role = relationship('TSysRole', primaryjoin='TSysUser.role_id == TSysRole.role_id', backref='t_sys_users')



class TTradingrecord(Base):
    __tablename__ = 't_tradingrecord'

    tradingrecord_id = Column(Integer, primary_key=True)
    house_id = Column(ForeignKey('t_house.house_id'), index=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)
    payment_date = Column(DateTime)
    payment_type = Column(Integer)

    house = relationship('THouse', primaryjoin='TTradingrecord.house_id == THouse.house_id', backref='t_tradingrecords')
    user = relationship('TUser', primaryjoin='TTradingrecord.user_id == TUser.user_id', backref='t_tradingrecords')



class TULuckyTicket(Base):
    __tablename__ = 't_u_lucky_ticket'

    u_lucky_ticketid = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id'), index=True)

    user = relationship('TUser', primaryjoin='TULuckyTicket.user_id == TUser.user_id', backref='tu_lucky_tickets')



class TUser(Base):
    __tablename__ = 't_user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    sex = Column(String(20))
    identity_number = Column(String(18))
    nickname = Column(String(100))
    img = Column(String(200))
    phone = Column(String(11))
    email = Column(String(60))
    password = Column(String(30))
    has_real_name = Column(Integer)
    is_member = Column(Integer)
    longitude = Column(Float)
    dimension = Column(Float)
