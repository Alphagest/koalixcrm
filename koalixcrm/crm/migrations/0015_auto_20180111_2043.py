# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-08 20:48
from __future__ import unicode_literals
from django.db import migrations
from django.db.migrations.operations.base import Operation
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT


class MigrateSalesContractToSalesDocument(Operation):

    # If this is False, it means that this operation will be ignored by
    # sqlmigrate; if true, it will be run and the SQL collected for its output.
    reduces_to_sql = False

    # If this is False, Django will refuse to reverse past this operation.
    reversible = False

    def __init__(self, arg1, arg2):
        # Operations are usually instantiated with arguments in migration
        # files. Store the values of them on self for later use.
        pass


    def _get_model_tuple(self, remote_model, app_label, model_name):
        if remote_model == RECURSIVE_RELATIONSHIP_CONSTANT:
            return app_label, model_name.lower()
        elif '.' in remote_model:
            return tuple(remote_model.lower().split('.'))
        else:
            return app_label, remote_model.lower()

    def state_forwards(self, app_label, state):
        # Add a new model.
        renamed_model = state.models["crm", "salescontract"].clone()
        renamed_model.name = "SalesDocument"
        state.models["crm", "salesdocument"] = renamed_model
        # Repoint all fields pointing to the old model to the new one.
        old_model_tuple = "crm", "salescontract"
        old_remote_model = '%s.%s' % ("crm", "salescontract")
        new_remote_model = '%s.%s' % ("crm", "SalesDocument")
        to_reload = []
        for (model_app_label, model_name), model_state in list(state.models.items()):
            if model_name != "salescontract" and model_name != "salesdocument":
                new_model_state = model_state
                model_with_new_base = state.models[model_app_label, model_name]
                for index, (name, field) in enumerate(model_state.fields.items()):
                    changed_field = None
                    remote_field = field.remote_field
                    if remote_field:
                        remote_model_tuple = self._get_model_tuple(
                            remote_field.model, model_app_label, model_name
                        )
                        if remote_model_tuple == old_model_tuple:
                            changed_field = field.clone()

                            changed_field.remote_field.model = new_remote_model
                        through_model = getattr(remote_field, 'through', None)
                        if through_model:
                            through_model_tuple = self._get_model_tuple(
                                through_model, model_app_label, model_name
                            )
                            if through_model_tuple == old_model_tuple:
                                if changed_field is None:
                                    changed_field = field.clone()
                                changed_field.remote_field.through = new_remote_model
                    if changed_field:
                        new_model_state = model_state.clone()
                        new_model_state.fields[name] = changed_field
                        model_changed = True
                        if old_remote_model in model_state.bases:
                            new_bases = []
                            for base in model_state.bases:
                                if old_remote_model == base:
                                    new_bases.append(new_remote_model.lower())
                                    new_model_state.bases = tuple(new_bases)
                        if model_changed:
                            state.remove_model(model_app_label, model_name)
                            state.models[model_app_label, model_name] = new_model_state
                            to_reload.append((model_app_label, model_name))
        # Reload models related to old model before removing the old model.
        state.remove_model("crm", "salescontract")
        state.reload_model("crm", "salesdocument", delay=True)
        state.reload_models(to_reload, delay=True)
        # Remove the old model.

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        # The Operation should use schema_editor to apply any changes it
        # wants to make to the database.
        new_model = to_state.apps.get_model("crm", "SalesDocument")
        if self.allow_migrate_model(schema_editor.connection.alias, new_model):
            old_model = from_state.apps.get_model("crm", "SalesContract")
            # Move the main table
            schema_editor.alter_db_table(
                new_model,
                old_model._meta.db_table,
                new_model._meta.db_table,
            )
            # Alter the fields pointing to us
            for related_object in old_model._meta.related_objects:
                if related_object.related_model == old_model:
                    model = new_model
                    related_key = ("crm", "salesdocument")
                else:
                    model = related_object.related_model
                    related_key = (
                        related_object.related_model._meta.app_label,
                        related_object.related_model._meta.model_name,
                    )
                to_field = to_state.apps.get_model(*related_key)._meta.get_field(related_object.field.name)

                schema_editor.alter_field(
                    model,
                    related_object.field,
                    to_field,
                )
            # Rename M2M fields whose name is based on this model's name.
            fields = zip(old_model._meta.local_many_to_many, new_model._meta.local_many_to_many)
            for (old_field, new_field) in fields:
                # Skip self-referential fields as these are renamed above.
                if new_field.model == new_field.related_model or not new_field.remote_field.through._meta.auto_created:
                    continue
                # Rename the M2M table that's based on this model's name.
                old_m2m_model = old_field.remote_field.through
                new_m2m_model = new_field.remote_field.through
                schema_editor.alter_db_table(
                    new_m2m_model,
                    old_m2m_model._meta.db_table,
                    new_m2m_model._meta.db_table,
                )
                # Rename the column in the M2M table that's based on this
                # model's name.
                schema_editor.alter_field(
                    new_m2m_model,
                    old_m2m_model._meta.get_field(old_model._meta.model_name),
                    new_m2m_model._meta.get_field(new_model._meta.model_name),
                )

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        # If reversible is True, this is called when the operation is reversed.
        pass

    def describe(self):
        # This is used to describe what the operation does in console output.
        return "Custom Operation"


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('crm', '0014_auto_20180108_2048'),
    ]

    operations = [

        migrations.RemoveField(
            model_name='salescontract',
            name='derived_from_sales_contract',
        ),
        MigrateSalesContractToSalesDocument("crm", "salescontract")
    ]
