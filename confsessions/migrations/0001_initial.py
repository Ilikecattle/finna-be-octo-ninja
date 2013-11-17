# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SessionTime'
        db.create_table(u'confsessions_sessiontime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'confsessions', ['SessionTime'])

        # Adding model 'SessionType'
        db.create_table(u'confsessions_sessiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_time', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['confsessions.SessionTime'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'confsessions', ['SessionType'])

        # Adding model 'Session'
        db.create_table(u'confsessions_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sessiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['confsessions.SessionType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('affixlink', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('presenter', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('teaser', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=5000)),
        ))
        db.send_create_signal(u'confsessions', ['Session'])

        # Adding M2M table for field participants on 'Session'
        m2m_table_name = db.shorten_name(u'confsessions_session_participants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('session', models.ForeignKey(orm[u'confsessions.session'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['session_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'SessionTime'
        db.delete_table(u'confsessions_sessiontime')

        # Deleting model 'SessionType'
        db.delete_table(u'confsessions_sessiontype')

        # Deleting model 'Session'
        db.delete_table(u'confsessions_session')

        # Removing M2M table for field participants on 'Session'
        db.delete_table(db.shorten_name(u'confsessions_session_participants'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'confsessions.session': {
            'Meta': {'object_name': 'Session'},
            'affixlink': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'presenter': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sessiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['confsessions.SessionType']"}),
            'teaser': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'confsessions.sessiontime': {
            'Meta': {'object_name': 'SessionTime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'confsessions.sessiontype': {
            'Meta': {'object_name': 'SessionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'session_time': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['confsessions.SessionTime']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['confsessions']