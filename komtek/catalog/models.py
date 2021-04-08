from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse


class Handbook(models.Model):
    """
    Model representing a handbook.
    """
    title = models.CharField(verbose_name='Наименование', max_length=200)
    short_title = models.CharField(verbose_name='Короткое наименование', max_length=100)
    description = models.TextField(verbose_name='Описание')
    version = models.CharField(verbose_name='Версия', max_length=200,
                               validators=[RegexValidator(regex=r'\d+\.\d+', message='Wrong version format')],
                               help_text="Enter two numbers separated by a dot. Example: '1.1'.")
    date = models.DateField(verbose_name='Дата начала действия справочника этой версии')

    _current_version = None

    class Meta:
        """
        Add options in the model:
            - Create a unique constraint in the database.
              A list of field names that specifies the unique set of columns: 'title' and 'version'.
            - A human-readable name for the object: 'Справочник'
            - The plural name for the object: 'Справочники'
            - The default ordering for the object: by field 'date'
        """
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        ordering = ['date']
        constraints = [
            models.UniqueConstraint(fields=['title', 'version'], name='unique_version')
        ]

    def __init__(self, *args, **kwargs):
        """
        Add the attribute setting _current_version to the initialization.
        """
        super().__init__(*args, **kwargs)
        self._current_version = self.version

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.title}'

    def save(self, *args, **kwargs):
        """
        Change the logic of saving a record to the table:
            - save the handbook only with the new version;
            - add all the elements of this handbook of the previous version to the table of elements,
              indicating the new version;
            - save the handbook of the new version to the handbook_version table.
        """
        if self.version != self._current_version:
            super().save(*args, **kwargs)
            elements = Element.objects.filter(handbook=self, version=self._current_version)
            for elem in elements:
                Element(handbook=elem.handbook, version=self.version, code=elem.code, value=elem.value).save()
            HandbookVersion(handbook=self, version=self.version, date=self.date).save()

    def get_absolute_url(self):
        """
        Returns the url to access a particular handbook instance.
        """
        return reverse('handbook-detail', args=[str(self.id)])


class Element(models.Model):
    """
    Model representing an element of a handbook.
    """
    handbook = models.ForeignKey('Handbook', on_delete=models.CASCADE, verbose_name='Название справочника')
    version = models.CharField(verbose_name='Версия', max_length=200)
    code = models.CharField(verbose_name='Код элемента', max_length=50)
    value = models.CharField(verbose_name='Значение элемента', max_length=200)

    class Meta:
        """
        Add options in the model:
            - Create a unique constraint in the database.
              A list of field names that specifies the unique set of columns: 'code', 'version' and 'handbook'.
            - A human-readable name for the object: 'Элемент справочника'
            - The plural name for the object: 'Элементы справочника'
        """
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'
        constraints = [
            models.UniqueConstraint(fields=['code', 'version', 'handbook'], name='unique_element')
        ]

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.code

    def save(self, *args, **kwargs):
        """
        Change the logic of saving a record to the table:
            - add the version of the directory, the element of which is the inserted record;
            - save the element to the elements table.
        """
        handbooks = Handbook.objects.filter(id=self.handbook.pk)
        self.version = handbooks[0].version
        super().save(*args, **kwargs)


class HandbookVersion(models.Model):
    handbook = models.ForeignKey('Handbook', on_delete=models.CASCADE, verbose_name='Справочник')
    version = models.CharField(verbose_name='Версия', max_length=200)
    date = models.DateField(verbose_name='Дата начала действия справочника этой версии')

    class Meta:
        """
        Add options in the model:
            - A human-readable name for the object: 'Версия справочника'
            - The plural name for the object: 'Версии справочников'
        """
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.handbook}'

    def get_absolute_url(self):
        """
        Returns the url to access a particular handbook instance.
        """
        return reverse('handbookversion-detail', args=[str(self.id)])
