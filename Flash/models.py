
from djongo import models
from bson import ObjectId


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=True)  # Make the name field optional

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subfolders')
    type = models.CharField(max_length=50, default='folder')

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class MCQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('FIB', 'Fill in the Blanks'),
        ('SUB', 'Subjective'),
        ('TRUEFALSE', 'True or False'),
    ]
    text = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES)
    explanation = models.TextField(blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='mc_questions', blank=True, null=True)
    
    def __str__(self):
        return self.text


class MCQAnswer(models.Model):
    question = models.ForeignKey(MCQuestion, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='mcq_answers', blank=True, null=True)

    def __str__(self):
        return self.answer_text




class ObjectIdField(models.Field):
    def get_prep_value(self, value):
        if not value:
            return None
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, ObjectId):
            return value
        return ObjectId(value)

    def from_db_value(self, value, expression, connection):
        if not value:
            return None
        if isinstance(value, ObjectId):
            return value
        return ObjectId(value)

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('FIB', 'Fill in the Blanks'),
        ('SUB', 'Subjective'),
        ('TRUEFALSE', 'True or False'),
    ]
    ques_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True)
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES)  # Adjust max_length as per your needs
    answers = models.TextField()  # Assuming it will store answer choices or answers
    explanation = models.TextField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)


    def __str__(self):
        return self.ques_text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='related_answers', on_delete=models.CASCADE)
    answer_text = models.TextField()
    tags = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='answers', blank=True, null=True)


    def __str__(self):
        return self.answer_text


class FillQuestions(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('FIB', 'Fill in the Blanks'),
        ('SUB', 'Subjective'),
        ('TRUEFALSE', 'True or False'),
    ]
    statement = models.TextField()  # To store the fill in the blanks statement
    created_by = models.CharField(max_length=100)  # To store the name of the creator
    created_date = models.DateTimeField(auto_now_add=True)  # Automatic creation date
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES)
    explanation = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='fill_questions', blank=True, null=True)

    def __str__(self):
        return self.statement

class FillAnswers(models.Model):
    question = models.ForeignKey(FillQuestions, related_name='answers', on_delete=models.CASCADE)  # Reference to the fill in the blanks statement
    answer = models.TextField()  # To store the answer for the associated statement
    tags = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='fill_answers', blank=True, null=True)

    def __str__(self):
        return f"Answer to: {self.question}"
    


class Feedback(models.Model):
    easily_recalled = models.BooleanField(default=False)
    skip = models.BooleanField(default=False)
    partially_recalled = models.BooleanField(default=False)
    forgot = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback {self.id}"

class CheckStatement(models.Model):
    statement = models.TextField()
    created_by = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice Question'),
        ('FIB', 'Fill in the Blanks'),
        ('SUB', 'Subjective'),
        ('TRUEFALSE', 'True or False'),
    ]
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES)
    explanation = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='check_statements', blank=True, null=True)

    def __str__(self):
        return self.statement[:50]

class TrueFalse(models.Model):
    statement = models.ForeignKey(CheckStatement,related_name='truefalse_set', on_delete=models.CASCADE)
    ans = models.CharField(max_length=100)  # Assuming a maximum length for the answer
    tags = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='true_false', blank=True, null=True)

    def __str__(self):
        return f"{self.statement.statement[:50]} - {self.ans}"


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='upload_image', blank=True, null=True)

