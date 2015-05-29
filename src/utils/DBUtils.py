# -*- coding: utf-8 -*-

"""
Namespace for Database Utilitiy funciotns and Classes

"""

from os import remove as os_remove
from os.path import isfile as os_path_isfile, join as os_join
from time import sleep as time_sleep
from threading import current_thread
import sqlite3
import json

#base path where the articles are stored
try:
    with open('config/config', 'r') as config:
        configDict = json.loads(config)
    BASE_PATH = configDict['basepath']
except Exception as e:
    print e
    print 'config not found'
    BASE_PATH = ''

DBPATH = os_join(BASE_PATH,'article.db')

ARTICLE_QUERY = {
    u'articles':u'{articleid},\'{link}\',\'{content}\',\'{site}\'\
    ,\'{author}\',{timestamp},\'{comment}\'',
    u'articletags':u'{tagid},{articleid}',
    u'tags':u'{tagid},{tagname}'
}

CREATE = 'create table {}({})'

TABLE_QUERY = {
    'articles':u'articleid integer primary key, link text, \
    content text, site text, author text, timestamp integer, \
    comment text',
    u'articletags':u'tagid integer,articleid integer',
    u'tags':u'tagid integer primary key, tagname text unique'
}

if not os_path_isfile(DBPATH):
    db = sqlite3.connect(DBPATH)
    c = db.cursor()
    for table, query in TABLE_QUERY.iteritems():
        c.execute(CREATE.format(table,query))
        db.commit()
    db.close()

class LockFile:
    def __init__(self, path=DBPATH):
        self._path = os_join(path, '.lock')
        self._owner = None

    def acquire(self):
        while os_path_isfile(self._path):
            time_sleep(1)
        open(self._path,'w').close()
        self._owner = current_thread()
        
    def __enter__():
        self.acquire()

    def release(self):
        if not os_path_isfile(self._path):
            raise Exception('Can\'t release unacquired Lock!')
        if current_thread() != self._owner:
            raise Exception('Can\'t release Lock, not the right Thread!')
        os_remove(self._path)
        self._owner = None

    def __exit__(self):
        self.release()

DBLOCK = LockFile()

def storeToDB(article):
    #for a,b in article.iteritems():
    #    print a,' : ', b
    with DBLOCK:
        try:
            db = sqlite3.connect(DBPATH)
            c = db.cursor()
            c.execute(u'insert into articles values({})'.format(
                ARTICLE_QUERY['articles'].format(**article)))
            db.commit()
            articleid = c.execute(u'select articleid from articles where \
            link=\'{}\''.format(article['link'])).fetchone()[0]
            print articleid
            for tag in article['tags']:
                tagid = c.execute(
                    u'select tagid from tags where tagname=\'{}\''.format(
                        tag)).fetchone()
                print tag
                if tagid == None:
                    c.execute(u'insert into tags values(NULL,\'{}\')'.format(
                        tag))
                    db.commit()
                    tagid = c.execute(
                        u'select tagid from tags where tagname=\'{}\''.format(
                            tag)).fetchone()
                    if tagid ==None:
                        db.close()
                        return
                    tagid = tagid[0]
                    print tagid
                    c.execute(u'insert into articletags values({},{})'.format(
                        tagid,articleid))
                    db.commit()
        except sqlite3.DatabaseError as e:
            print str(e)
        finally:
            db.close()

def execQuery(query):
    with DBLOCK:
        try:
            db = sqlite3.connect(DBPATH)
            c = db.cursor()
            c.execute(query)
            db.commit()
        except sqlite3.DatabaseError as e:
            print 'Something wrong with the Query or the Database!'
            print str(e)
        finally:
            db.close()

def execSelectQuery(query):
    with DBLOCK:
        try:
            db = sqlite3.connect(DBPATH)
            c = db.cursor()
            c.execute(query).fetchall()
        except sqlite3.DatabaseError as e:
            print e
        finally:
            db.close()
