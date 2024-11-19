from rest_framework import serializers
from .models import MCQuestion, MCQAnswer, Question, Answer, FillQuestions, FillAnswers, CheckStatement, TrueFalse, Folder,UploadedImage,File,Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']  # Assuming 'name' is the field in your Tag model

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = str(instance.id)  # Convert ObjectId to string
        return ret


class MCQAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQAnswer
        fields = ['answer_text', 'is_correct']


class MCQuestionSerializer(serializers.ModelSerializer):
    answers = MCQAnswerSerializer(many=True, required=False)
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags


    class Meta:
        model = MCQuestion
        fields = ['id', 'text', 'created_date', 'created_by', 'question_type', 'explanation', 'answers', 'folder_id','tags']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        folder_id = validated_data.pop('folder_id', None)
        question = MCQuestion.objects.create(**validated_data)

        if folder_id:
            question.folder_id = folder_id
            question.save()

        for answer_data in answers_data:
            MCQAnswer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.explanation = validated_data.get('explanation', instance.explanation)

        folder_id = validated_data.get('folder_id', None)
        if folder_id:
            instance.folder_id = folder_id

        answers_data = validated_data.get('answers', [])
        answer_instances = instance.answers.all()
        answer_instances_ids = [answer.id for answer in answer_instances]

        for answer_data in answers_data:
            answer_id = answer_data.get('id', None)
            if answer_id in answer_instances_ids:
                answer_instance = answer_instances.get(id=answer_id)
                answer_instance.answer_text = answer_data.get('answer_text', answer_instance.answer_text)
                answer_instance.is_correct = answer_data.get('is_correct', answer_instance.is_correct)
                answer_instance.save()
            else:
                MCQAnswer.objects.create(question=instance, **answer_data)

        instance.save()
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer_text')

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.CharField(max_length=255, write_only=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags
    explanation = serializers.CharField(max_length=255, allow_blank=True, required=False)
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Question
        fields = ('id', 'ques_text', 'created_date', 'created_by', 'question_type', 'answers', 'explanation', 'folder_id','tags')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        explanation_data = validated_data.pop('explanation', None)
        folder_id = validated_data.pop('folder_id', None)

        question = Question.objects.create(**validated_data)

        if folder_id:
            question.folder_id = folder_id
            question.save()

        if explanation_data:
            question.explanation = explanation_data
        question.save()

        Answer.objects.create(question=question, answer_text=answers_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        explanation_data = validated_data.pop('explanation', None)
        folder_id = validated_data.pop('folder_id', None)

        instance.ques_text = validated_data.get('ques_text', instance.ques_text)
        instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.question_type = validated_data.get('question_type', instance.question_type)

        if folder_id:
            instance.folder_id = folder_id

        if explanation_data is not None:
            instance.explanation = explanation_data

        instance.save()

        if answers_data:
            related_answer = instance.related_answers.first()
            if related_answer:
                related_answer.answer_text = answers_data
                related_answer.save()
        else:
            Answer.objects.create(question=instance, answer_text=answers_data)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.related_answers.exists():
            data['answers'] = instance.related_answers.first().answer_text
        else:
            data['answers'] = None
        return data

class FillAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillAnswers
        fields = ('id', 'answer')


class FillQuestionsSerializer(serializers.ModelSerializer):
    answers = serializers.CharField(max_length=255)
    explanation = serializers.CharField(max_length=255, allow_blank=True, required=False)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FillQuestions
        fields = ('id', 'statement', 'created_date', 'created_by', 'question_type', 'answers', 'explanation', 'folder_id','tags')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        explanation_data = validated_data.pop('explanation', None)
        folder_id = validated_data.pop('folder_id', None)

        question = FillQuestions.objects.create(**validated_data)

        if folder_id:
            question.folder_id = folder_id
            question.save()

        if explanation_data:
            question.explanation = explanation_data
            question.save()

        FillAnswers.objects.create(question=question, answer=answers_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        explanation_data = validated_data.pop('explanation', None)
        folder_id = validated_data.pop('folder_id', None)

        instance.statement = validated_data.get('statement', instance.statement)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.question_type = validated_data.get('question_type', instance.question_type)

        if folder_id:
            instance.folder_id = folder_id

        if explanation_data:
            instance.explanation = explanation_data

        instance.save()

        if answers_data:
            if instance.answers.exists():
                answer = instance.answers.first()
                answer.answer = answers_data
                answer.save()
            else:
                FillAnswers.objects.create(question=instance, answer=answers_data)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['answers'] = instance.answers.first().answer if instance.answers.exists() else None
        return data


class TrueFalseSerializer(serializers.ModelSerializer):
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)

    class Meta:
        model = TrueFalse
        fields = ('id', 'ans', 'folder_id')


class CheckStatementSerializer(serializers.ModelSerializer):
    truefalse_set = serializers.BooleanField(allow_null=True)
    explanation = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CheckStatement
        fields = ('id', 'statement', 'created_by', 'created_date', 'question_type', 'truefalse_set', 'explanation', 'folder_id','tags')

    def create(self, validated_data):
        truefalse_data = validated_data.pop('truefalse_set', None)
        explanation = validated_data.pop('explanation', None)
        folder_id = validated_data.pop('folder_id', None)

        statement_instance = CheckStatement.objects.create(**validated_data)

        if folder_id:
            statement_instance.folder_id = folder_id
            statement_instance.save()

        if truefalse_data is not None:
            TrueFalse.objects.create(statement=statement_instance, ans=truefalse_data)

        if explanation is not None:
            statement_instance.explanation = explanation
            statement_instance.save()

        return statement_instance

    def update(self, instance, validated_data):
        instance.statement = validated_data.get('statement', instance.statement)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.question_type = validated_data.get('question_type', instance.question_type)

        explanation = validated_data.get('explanation')
        if explanation is not None:
            instance.explanation = explanation

        folder_id = validated_data.get('folder_id', None)
        if folder_id:
            instance.folder_id = folder_id

        instance.save()

        truefalse_data = validated_data.get('truefalse_set')
        if truefalse_data is not None:
            if instance.truefalse_set.exists():
                ans_instance = instance.truefalse_set.first()
                ans_instance.ans = truefalse_data
                ans_instance.save()
            else:
                TrueFalse.objects.create(statement=instance, ans=truefalse_data)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['truefalse_set'] = instance.truefalse_set.first().ans if instance.truefalse_set.exists() else None
        return data





class FileSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'name', 'type','created_by')

    def get_type(self, obj):
        return 'file'


from rest_framework import serializers
from .models import Folder

from rest_framework import serializers
from .models import Folder

class FolderSerializer(serializers.ModelSerializer):
    subfolders = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent', 'type', 'subfolders']

    def get_subfolders(self, obj):
        subfolders = Folder.objects.filter(parent=obj)
        return FolderSerializer(subfolders, many=True).data

class CreateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['name', 'parent', 'type']

class CreateSubfolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['name', 'parent', 'type']

class MCQAnswerOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQAnswer
        fields = ['id', 'answer_text', 'is_correct']


class MCQuestionOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQuestion
        fields = ['id', 'text', 'created_date', 'created_by', 'question_type', 'folder_id','tags']


class AnswersOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text']


class QuestionsOnlySerializer(serializers.ModelSerializer):
    related_answers = AnswersOnlySerializer(many=True, read_only=True)
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags


    class Meta:
        model = Question
        fields = ['id', 'ques_text', 'created_by', 'question_type', 'related_answers', 'folder_id','tags']


class FillQuestionOnlySerializer(serializers.ModelSerializer):
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags


    class Meta:
        model = FillQuestions
        fields = ['id', 'statement', 'created_date', 'created_by', 'question_type', 'folder_id','tags']


class FillAnswerOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = FillAnswers
        fields = ['id', 'answer','tags']


class TrueFalseOnlySerializer(serializers.ModelSerializer):
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags


    class Meta:
        model = TrueFalse
        fields = ['id', 'ans', 'folder_id','tags']


class CheckStatementOnlySerializer(serializers.ModelSerializer):
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=False, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags


    class Meta:
        model = CheckStatement
        fields = ['id', 'statement', 'created_by', 'question_type', 'folder_id','tags']

class UploadedImageSerializer(serializers.ModelSerializer):
    folder_id = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), source='folder', required=False, allow_null=True)
    tags = serializers.CharField(required=False, allow_blank=True)  # Single string for tags
    class Meta:
        model = UploadedImage
        fields = ('id', 'image', 'uploaded_at', 'created_by', 'folder_id','tags')
        extra_kwargs = {
            'image': {'required': True}
        }

    def validate_image(self, value):
        from django.core.files.images import get_image_dimensions
        from rest_framework.exceptions import ValidationError

        valid_formats = ('jpeg', 'png', 'gif', 'bmp')
        format = value.name.split('.')[-1].lower()
        if format not in valid_formats:
            raise serializers.ValidationError("Unsupported image format. Supported formats: JPEG, PNG, GIF, BMP.")

        try:
            get_image_dimensions(value)
        except Exception as e:
            raise serializers.ValidationError("Invalid image file: {}".format(str(e)))

        return value

    def create(self, validated_data):
        # Extract 'folder_id' from validated_data and remove it to avoid confusion with model field
        folder_id = validated_data.pop('folder_id', None)

        # Create UploadedImage instance
        if folder_id:
            validated_data['folder_id'] = folder_id.pk  # Assign the actual ID of the Folder

        return super().create(validated_data)
    
    
from rest_framework import serializers
from .models import MCQuestion, FillQuestions, TrueFalse, CheckStatement

class CombinedQuestionSerializer(serializers.ModelSerializer):
    question_type = serializers.SerializerMethodField()

    class Meta:
        model = None  # Placeholder for model
        fields = ('id', 'text', 'created_date', 'created_by', 'question_type', 'explanation', 'answers', 'folder_id', 'tags')

    def get_question_type(self, instance):
        if isinstance(instance, MCQuestion):
            return 'MCQ'
        elif isinstance(instance, FillQuestions):
            return 'Fill-in-the-Blanks'
        elif isinstance(instance, TrueFalse):
            return 'True/False'
        elif isinstance(instance, CheckStatement):
            return 'Check Statement'
        else:
            return 'Unknown'

    def to_representation(self, instance):
        if isinstance(instance, MCQuestion):
            serializer = MCQuestionSerializer(instance)
        elif isinstance(instance, FillQuestions):
            serializer = FillQuestionsSerializer(instance)
        elif isinstance(instance, TrueFalse):
            serializer = TrueFalseSerializer(instance)
        elif isinstance(instance, CheckStatement):
            serializer = CheckStatementSerializer(instance)
        else:
            return None  # Handle error or unknown instance type
        
        return serializer.data
