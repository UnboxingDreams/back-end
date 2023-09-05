from django.db import models
from enum import Enum

# This is Enum class
class Death(Enum):
    ACCIDENT = "ACCIDENT"
    OLD = "OLD"
    DIESASE = "DISEASE"
    EUTHANASIA = "EUTHANASIA"

class Emotion(Enum):
    BAD = "BAD"
    SOSO = "SOSO"
    GOOD = "GOOD"

class Category(Enum):
    LETTER = "LETTER"
    MIND = "MIND"
    NORMAL = "NORMAL"

class AnimalSpecies(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    speciesImgUrl = models.URLField(blank=True, null=True)
    

class background(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=10)
    backgroundImgUrl = models.URLField(blank=True, null=True)
    price = models.IntegerField()

# Create your models here.

class LetterTemplate(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=10)
    letterTemplateImgUrl = models.URLField(blank=True, null=True)
    price = models.IntegerField()


class User(models.Model):
    id = models.AutoField(primary_key = True)
    userId = models.CharField(max_length=30)# username, password
    password = models.CharField(max_length=50)
    userName = models.CharField(max_length=10)
    alarm = models.BooleanField(default=True)
    description = models.CharField(max_length=30)
    taskCount = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    callBy = models.CharField(max_length=10)
    animalName = models.CharField(max_length=10)
    animalSpecies = models.CharField(max_length=30)
    animalImgUrl = models.URLField(blank=True, null=True)
    animalDeathDate = models.DateTimeField()
    death = models.CharField(max_length=10, choices=[(death.name, death.value) for death in Death])
    animalAge = models.IntegerField()
    backgroundId = models.ForeignKey(background, on_delete=models.CASCADE, default=0)
    letterTemplateId = models.ForeignKey(LetterTemplate, on_delete=models.CASCADE, default=0)
    AnimalSpeciesId = models.ForeignKey(AnimalSpecies, on_delete=models.CASCADE, default=0)

class Question(models.Model):
    id = models.AutoField(primary_key= True)
    taskNumber = models.IntegerField()
    content = models.TextField()

class Answer(models.Model):
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    contentImgUrl = models.URLField(blank=True, null=True)
    postOut = models.BooleanField(default=False)
    emotion = models.CharField(max_length=10, choices=[(emotion.name, emotion.value) for emotion in Emotion])
    createdAt = models.DateTimeField()

    class Meta:
        unique_together = (("userId", "questionId"),)

class Post(models.Model):
    id = models.AutoField(primary_key= True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20) # 편지일 경우 그냥 들어가게
    content = models.TextField() # 편지일 경우 그냥 들어가게
    death = models.CharField(max_length=10, choices=[(death.name, death.value) for death in Death])
    category = models.CharField(max_length=10, choices=[(category.name, category.value) for category in Category])
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

class MailBox(models.Model):
    id = models.ForeignKey(Post, on_delete=models.CASCADE, primary_key=True)
    emotion = models.CharField(max_length=10, choices=[(emotion.name, emotion.value) for emotion in Emotion])
    content = models.TextField()
    contentImgUrl = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField()

class PostPicture(models.Model):
    id = models.AutoField(primary_key= True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    contentUrl = models.URLField(blank=True, null=True)


class PostLike(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("userId", "postId"),)

class Comment(models.Model):
    id = models.AutoField(primary_key= True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    contentUrl = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()


class Recomment(models.Model):
    id = models.AutoField(primary_key= True)
    commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recomments_by_user')
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    contentUrl = models.URLField(blank=True, null=True)
    userTagId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recomments_by_tag')
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

