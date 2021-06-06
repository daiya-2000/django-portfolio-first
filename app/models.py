from django.db import models

# Create your models here.
class Profile(models.Model):
    title = models.CharField("タイトル", max_length=100, null=True, blank=True)
    sub_title = models.CharField("サブタイトル", max_length=100, null=True, blank=True)
    name = models.CharField("名前", max_length=100, null=True, blank=True)
    job = models.TextField("仕事")
    introduction = models.TextField("自己紹介")
    github = models.CharField("github", max_length=100, null=True, blank=True)
    twitter = models.CharField("twitter", max_length=100, null=True, blank=True)
    instagram = models.CharField("instagram", max_length=100, null=True, blank=True)
    top_image = models.ImageField(upload_to="images", verbose_name="トップ画像")
    sub_image = models.ImageField(upload_to="images", verbose_name="サブ画像")

    def __str__(self) -> str:
        return self.name


class Work(models.Model):
    title = models.CharField("タイトル", max_length=100)
    image = models.ImageField(upload_to="images", verbose_name="イメージ画像")
    thumbnail = models.ImageField(upload_to="images", verbose_name="サムネイル")
    skill = models.CharField("スキル", max_length=100)
    url = models.CharField("URL", max_length=100, null=True, blank=True)
    created = models.DateField("作成日時")
    description = models.TextField("説明")

    def __str__(self) -> str:
        return self.title
