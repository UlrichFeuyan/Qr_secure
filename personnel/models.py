import os
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db import models
from django.conf import settings
import qrcode
import os
import hashlib
from django.core.files.storage import default_storage

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')


def SHA256(text):
    return hashlib.sha256(text.encode()).hexdigest()


class Departement(models.Model):
    name = models.CharField("Nom", max_length=255)
    description = RichTextField(verbose_name="Description", blank=True, null=True)

    date_created = models.DateTimeField("Date d'ajout", auto_now_add=True)
    date_updated = models.DateTimeField("Dernière mise à jour", auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"

    def __str__(self):
        return f"{self.name}"


class Employe(models.Model):
    name = models.CharField("Nom", max_length=255)
    departement = models.ForeignKey(Departement, verbose_name="Département", on_delete=models.DO_NOTHING, blank=True,
                                    null=True)
    poste = models.CharField("Poste", max_length=100)
    ncni = models.CharField("N° de CNI", max_length=100)
    date_naissance = models.DateTimeField("Date de naissance")

    signature = models.CharField("Signature", max_length=500, blank=True)
    qrcode = models.CharField("Qr Code", max_length=500, blank=True)

    date_created = models.DateTimeField("Date d'ajout", auto_now_add=True)
    date_updated = models.DateTimeField("Dernière mise à jour", auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"

    def __str__(self):
        return f"{self.name} ({self.poste})"

    def get_absolute_url(self):
        return reverse('store:detail', kwargs={"slug": self.slug})

    def get_all_images(self):
        return EmployePhoto.objects.filter(employe=self)

    def get_first_image(self):
        return EmployePhoto.objects.filter(employe=self)[0]

    def visuel(self):
        try:
            return mark_safe(
                '<img src="{}" alt="{}" width="100" />'.format(self.get_first_image().thumbnail.url, self.name))
        except:
            return mark_safe('<img src="/static/img/placeholder.png" alt="{}" width="100" />'.format(self.name))

    visuel.allow_tags = True

    def code_qr(self):
        return mark_safe(
            '<img src="{}" alt="{}" width="100" height="100" />'.format(self.qrcode.replace(MEDIA_ROOT, "/media/"), self.qrcode.replace(MEDIA_ROOT, "")))

    code_qr.allow_tags = True

    def save(self, *args, **kwargs):
        if not self.pk:  # si c'est une création
            text = ''
            for field in self._meta.fields:
                if field.name not in ['signature', 'qrcode']:
                    text += str(getattr(self, field.name))
            self.signature = SHA256(text)
            qr = qrcode.make(self.signature)
            img_dir = os.path.join(MEDIA_ROOT, 'Personnel/employes/qrcode', f"{self.name}.jpg")
            qr.save(img_dir)
            self.qrcode = img_dir
        else:  # si c'est une mise à jour
            text = ''
            for field in self._meta.fields:
                if field.name not in ['signature', 'qrcode']:
                    text += str(getattr(self, field.name))
            self.signature = SHA256(text)

        super(Employe, self).save(*args, **kwargs)


def img_path(instance, filename):
    path = "Personnel/employes/"
    ext = filename.split('.')[-1]
    if instance.employe.departement:
        path += instance.employe.name + "/"
    return os.path.join(path, filename)


class EmployePhoto(models.Model):
    employe = models.ForeignKey(Employe, related_name='photos', on_delete=models.CASCADE)
    thumbnail = models.ImageField("Photo de l'employe", upload_to=img_path)

    class Meta:
        verbose_name = "photo de l'employé"
        verbose_name_plural = "photos de l'employé"

    def __str__(self):
        return self.employe.name

    def visuel(self):
        return mark_safe(
            '<img src="{}" alt="{}" width="100" height="100" />'.format(self.thumbnail.url, self.employe.name))

    visuel.allow_tags = True

    @property
    def thumbnailURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = "/static/img/placeholder.png"
        return url
