# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CPRNumber'
        db.create_table(u'accounts_cprnumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cpr', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'accounts', ['CPRNumber'])


        # Renaming column for 'Child.cpr' to match new field type.
        db.rename_column(u'accounts_child', 'cpr', 'cpr_id')
        # Changing field 'Child.cpr'
        db.alter_column(u'accounts_child', 'cpr_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.CPRNumber'], unique=True))
        # Adding index on 'Child', fields ['cpr']
        db.create_index(u'accounts_child', ['cpr_id'])

        # Adding unique constraint on 'Child', fields ['cpr']
        db.create_unique(u'accounts_child', ['cpr_id'])


        # Renaming column for 'Participant.cpr' to match new field type.
        db.rename_column(u'accounts_participant', 'cpr', 'cpr_id')
        # Changing field 'Participant.cpr'
        db.alter_column(u'accounts_participant', 'cpr_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.CPRNumber'], unique=True))
        # Adding index on 'Participant', fields ['cpr']
        db.create_index(u'accounts_participant', ['cpr_id'])


    def backwards(self, orm):
        # Removing index on 'Participant', fields ['cpr']
        db.delete_index(u'accounts_participant', ['cpr_id'])

        # Removing unique constraint on 'Child', fields ['cpr']
        db.delete_unique(u'accounts_child', ['cpr_id'])

        # Removing index on 'Child', fields ['cpr']
        db.delete_index(u'accounts_child', ['cpr_id'])

        # Deleting model 'CPRNumber'
        db.delete_table(u'accounts_cprnumber')


        # Renaming column for 'Child.cpr' to match new field type.
        db.rename_column(u'accounts_child', 'cpr_id', 'cpr')
        # Changing field 'Child.cpr'
        db.alter_column(u'accounts_child', 'cpr', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Renaming column for 'Participant.cpr' to match new field type.
        db.rename_column(u'accounts_participant', 'cpr_id', 'cpr')
        # Changing field 'Participant.cpr'
        db.alter_column(u'accounts_participant', 'cpr', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))

    models = {
        u'accounts.child': {
            'Meta': {'object_name': 'Child'},
            'cpr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.CPRNumber']", 'unique': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'questionnaire_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relation_to_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'accounts.cprnumber': {
            'Meta': {'object_name': 'CPRNumber'},
            'cpr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'accounts.extra': {
            'Meta': {'object_name': 'Extra'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'accounts.participant': {
            'Meta': {'object_name': 'Participant'},
            'cpr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.CPRNumber']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pseudonym': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
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
        }
    }

    complete_apps = ['accounts']