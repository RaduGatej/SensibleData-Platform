# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessRange'
        db.create_table(u'oauth2app_accessrange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'oauth2app', ['AccessRange'])

        # Adding model 'ClientType'
        db.create_table(u'oauth2app_clienttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='id_client', max_length=100)),
        ))
        db.send_create_signal(u'oauth2app', ['ClientType'])

        # Adding model 'Client'
        db.create_table(u'oauth2app_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('client_owner_email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.ClientType'], null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(default='2d62f3a9e9f6537f28ca2d74b8e882', unique=True, max_length=30, db_index=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='15008c1f6f4b3b6c1c1240a8b83f80', unique=True, max_length=30)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('api_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('authorize_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'oauth2app', ['Client'])

        # Adding M2M table for field registered_scope on 'Client'
        m2m_table_name = db.shorten_name(u'oauth2app_client_registered_scope')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm[u'oauth2app.client'], null=False)),
            ('accessrange', models.ForeignKey(orm[u'oauth2app.accessrange'], null=False))
        ))
        db.create_unique(m2m_table_name, ['client_id', 'accessrange_id'])

        # Adding model 'AccessToken'
        db.create_table(u'oauth2app_accesstoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(default='d5e09d53b7', unique=True, max_length=10, db_index=True)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(null=True, default='1b4f4d760e', max_length=10, blank=True, unique=True, db_index=True)),
            ('mac_key', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('issue', self.gf('django.db.models.fields.PositiveIntegerField')(default=1375522056)),
            ('expire', self.gf('django.db.models.fields.PositiveIntegerField')(default=1375525656)),
            ('refreshable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'oauth2app', ['AccessToken'])

        # Adding M2M table for field scope on 'AccessToken'
        m2m_table_name = db.shorten_name(u'oauth2app_accesstoken_scope')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accesstoken', models.ForeignKey(orm[u'oauth2app.accesstoken'], null=False)),
            ('accessrange', models.ForeignKey(orm[u'oauth2app.accessrange'], null=False))
        ))
        db.create_unique(m2m_table_name, ['accesstoken_id', 'accessrange_id'])

        # Adding model 'Code'
        db.create_table(u'oauth2app_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('key', self.gf('django.db.models.fields.CharField')(default='7637f9816034f8bfd0ce7a69b6f0bb', unique=True, max_length=30, db_index=True)),
            ('issue', self.gf('django.db.models.fields.PositiveIntegerField')(default=1375522056)),
            ('expire', self.gf('django.db.models.fields.PositiveIntegerField')(default=1375522176)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'oauth2app', ['Code'])

        # Adding M2M table for field scope on 'Code'
        m2m_table_name = db.shorten_name(u'oauth2app_code_scope')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('code', models.ForeignKey(orm[u'oauth2app.code'], null=False)),
            ('accessrange', models.ForeignKey(orm[u'oauth2app.accessrange'], null=False))
        ))
        db.create_unique(m2m_table_name, ['code_id', 'accessrange_id'])

        # Adding model 'MACNonce'
        db.create_table(u'oauth2app_macnonce', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.AccessToken'])),
            ('nonce', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal(u'oauth2app', ['MACNonce'])


    def backwards(self, orm):
        # Deleting model 'AccessRange'
        db.delete_table(u'oauth2app_accessrange')

        # Deleting model 'ClientType'
        db.delete_table(u'oauth2app_clienttype')

        # Deleting model 'Client'
        db.delete_table(u'oauth2app_client')

        # Removing M2M table for field registered_scope on 'Client'
        db.delete_table(db.shorten_name(u'oauth2app_client_registered_scope'))

        # Deleting model 'AccessToken'
        db.delete_table(u'oauth2app_accesstoken')

        # Removing M2M table for field scope on 'AccessToken'
        db.delete_table(db.shorten_name(u'oauth2app_accesstoken_scope'))

        # Deleting model 'Code'
        db.delete_table(u'oauth2app_code')

        # Removing M2M table for field scope on 'Code'
        db.delete_table(db.shorten_name(u'oauth2app_code_scope'))

        # Deleting model 'MACNonce'
        db.delete_table(u'oauth2app_macnonce')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'oauth2app.accessrange': {
            'Meta': {'object_name': 'AccessRange'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'oauth2app.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1375525656'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1375522056'}),
            'mac_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "'64f47237d0'", 'max_length': '10', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'refreshable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'20e67b89c1'", 'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oauth2app.client': {
            'Meta': {'object_name': 'Client'},
            'api_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'authorize_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'client_owner_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'19bc548abf6db13a49f500f9ca9619'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'registered_scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'daf75ab127d03a2b4bd4958bd51c8c'", 'unique': 'True', 'max_length': '30'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oauth2app.ClientType']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oauth2app.clienttype': {
            'Meta': {'object_name': 'ClientType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'id_client'", 'max_length': '100'})
        },
        u'oauth2app.code': {
            'Meta': {'object_name': 'Code'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1375522176'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1375522056'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'6ef4ea2f753c2ee430cb3ded663275'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'oauth2app.macnonce': {
            'Meta': {'object_name': 'MACNonce'},
            'access_token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oauth2app.AccessToken']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        }
    }

    complete_apps = ['oauth2app']