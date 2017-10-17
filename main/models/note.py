# coding=utf-8
from . import db
from datetime import datetime
import uuid


def generate_id():
    return uuid.uuid1().hex


class Note(db.Model):
    __tablename__ = 'note'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.String(32), default=generate_id, primary_key=True, doc='uuid')
    short_id = db.Column(db.SmallInteger, unique=True, nullable=True, doc='短编号')
    text = db.Column(db.String(10000), nullable=True, doc='笔记')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, doc='创建时间（UTC）')
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow, doc='更新时间（UTC）')

    def __init__(self, text=text, short_id=None, create_time=None, update_time=None):
        self.text = text
        self.short_id = short_id
        self.create_time = create_time
        self.update_time = update_time

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        return db.session.commit()
