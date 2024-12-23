# Generated by Django 3.2.15 on 2024-06-24 09:04

import Flash.models
import bson.objectid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Flash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice Question'), ('FIB', 'Fill in the Blanks'), ('SUB', 'Subjective'), ('TRUEFALSE', 'True or False')], max_length=15)),
                ('explanation', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('easily_recalled', models.BooleanField(default=False)),
                ('skip', models.BooleanField(default=False)),
                ('partially_recalled', models.BooleanField(default=False)),
                ('forgot', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(default='folder', max_length=10)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='Flash.folder')),
            ],
        ),
        migrations.CreateModel(
            name='TrueFalse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=100)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='true_false', to='Flash.folder')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='truefalse_set', to='Flash.checkstatement')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', Flash.models.ObjectIdField(default=bson.objectid.ObjectId, editable=False, primary_key=True, serialize=False)),
                ('ques_text', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('question_type', models.CharField(max_length=50)),
                ('answers', models.TextField()),
                ('explanation', models.TextField(blank=True, null=True)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Flash.folder')),
            ],
        ),
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice Question'), ('FIB', 'Fill in the Blanks'), ('SUB', 'Subjective'), ('TRUEFALSE', 'True or False')], max_length=15)),
                ('explanation', models.TextField(blank=True)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mc_questions', to='Flash.folder')),
            ],
        ),
        migrations.CreateModel(
            name='MCQAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mcq_answers', to='Flash.folder')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='Flash.mcquestion')),
            ],
        ),
        migrations.CreateModel(
            name='FillQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice Question'), ('FIB', 'Fill in the Blanks'), ('SUB', 'Subjective'), ('TRUEFALSE', 'True or False')], max_length=15)),
                ('explanation', models.TextField(blank=True)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fill_questions', to='Flash.folder')),
            ],
        ),
        migrations.CreateModel(
            name='FillAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fill_answers', to='Flash.folder')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='Flash.fillquestions')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='Flash.folder')),
            ],
        ),
        migrations.AddField(
            model_name='checkstatement',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='check_statements', to='Flash.folder'),
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', Flash.models.ObjectIdField(default=bson.objectid.ObjectId, editable=False, primary_key=True, serialize=False)),
                ('answer_text', models.TextField()),
                ('created_by', models.CharField(max_length=100)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='Flash.folder')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_answers', to='Flash.questions')),
            ],
        ),
    ]
