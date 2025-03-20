# Generated by Django 4.2.19 on 2025-03-20 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('template', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('review', 'Under Review'), ('approved', 'Approved'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20)),
                ('version', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('report_date', models.DateField()),
                ('department', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('data', models.JSONField(default=dict)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.documenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('review', 'Under Review'), ('approved', 'Approved'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20)),
                ('version', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('content', models.TextField()),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.documenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('review', 'Under Review'), ('approved', 'Approved'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20)),
                ('version', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('party_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('contract_value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('terms_conditions', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_%(class)s', to=settings.AUTH_USER_MODEL)),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.documenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
                ('description', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='documents.contract')),
                ('note', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='documents.note')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='documents.report')),
            ],
        ),
    ]
