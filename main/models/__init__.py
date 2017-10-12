# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)

__all__ = ['save_note', 'update_note', 'delete_note', 'all_notes', 'find_note', 'batch_delete']


def init_db():
    # 创建表
    db.create_all()


# def connect_db():

from .note import Note


def find_note(short_id):
    """根据short_id查找笔记"""
    c = Note.query.filter_by(short_id=short_id).first()
    if c is not None:
        return {'id': c.id,
                'text': c.text, 'render': c.render,
                'short_id': c.short_id,
                'create_time': c.create_time,
                'update_time': c.update_time}


def save_note(a):
    """新建笔记"""
    c = Note(short_id=a['short_id'], text=a['text']).save()
    return {'id': c.id,
            'text': c.text, 'render': c.render,
            'short_id': c.short_id,
            'create_time': c.create_time,
            'update_time': c.update_time}


def all_notes():
    a = []
    for c in Note.query.all():
        b = {'id': c.id, 'text': c.text, 'render': c.render, 'short_id': c.short_id, 'create_time': c.create_time,
             'update_time': c.update_time}
        a.append(b)

    return a


def update_note(short_id, text, render):
    """更新笔记"""
    a = Note.query.filter_by(short_id=short_id).first()
    if not a:
        c = Note(short_id=short_id, text=text, render=render).save()
        return {'id': c.id,
                'text': c.text,
                'render': c.render,
                'short_id': c.short_id,
                'create_time': c.create_time,
                'update_time': c.update_time}
    else:
        a.short_id = short_id
        a.text = text
        a.render = render
        c = a.update()
        return {'id': c.id,
                'text': c.text, 'render': c.render,
                'short_id': c.short_id,
                'create_time': c.create_time,
                'update_time': c.update_time}


def delete_note(short_id):
    a = Note.query.filter_by(short_id=short_id).first()
    if not a:
        return False
    else:
        a.delete()


def batch_delete(a):
    a = db.session.execute('delete from note where short_id in (' + a + ')')
    db.session.commit()
    return a.rowcount
