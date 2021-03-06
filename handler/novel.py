#coding:utf-8
import time
import logging
from base import BaseHandler
from django.db import transaction
from database.models import Novel 

logger = logging.getLogger('Robot.Novel')

class NovelHandler(BaseHandler):
    'novel'
    
    SUPPORTED_METHODS = ['ADD', 'UPDATE']

    @transaction.commit_on_success
    def add(self):
        '添加novel'
        
        name = self.get_argument('name')
        rule = self.get_argument('rule', '.+')
        if Novel.objects.filter(name=name).exists():
            return self.finish({'code': 1, 'msg': u'已经创建'})
        Novel.objects.create(**{
            'id': self.gen_uuid(),
            'name': name,
            'rule': rule,
            'createtime': int(time.time()),
            'status': 0
        })
        return self.finish({'code': 0, 'msg': u''})
    
    @transaction.commit_on_success
    def update(self):
        '修改novel'

        try:
            novel = Novel.objects.select_for_update().get(id=self.get_argument('id'))
        except:
            return self.finish({'code': 1, 'msg': u'id参数错误'})
        status = int(self.get_argument('status', novel.status))
        novel.rule = self.get_argument('rule', novel.rule)
        if not status in Novel.NOVEL_STATUSES:
            return self.finish({'code': 2, 'msg': u'status参数错误'})
        novel.status, novel.updatetime = status, int(time.time())
        novel.save()
        self.finish({'code': 0, 'msg': u''})
        
