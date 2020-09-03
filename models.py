class PhotoLoadSession(models.Model):
    CONTENT_TYPES = (
        ('contract', 'Фото договора'),
        ('timesheet', 'Фото табеля'),
        ('worker', 'Фото рабочего'),
    )
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES,
        verbose_name='Вид изображения')

    OBJECT_STATUSES = (
        ('new', 'Новая'),
        ('work', 'В работе'),
        ('comment', 'Есть комментарий'),
        ('complete', 'Закрыта'),
    )
    status = models.CharField(
        max_length=20,
        verbose_name='Статус',
        choices=OBJECT_STATUSES,
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Отправитель',
        related_name='senders'
    )
    handler = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Обработчик',
        related_name='handlers',
        blank=True,
        null=True,
    )
    date_create = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    @property
    def get_content_type(self):
        return self.get_content_type_display()

    @property
    def get_status(self):
        return self.get_status_display()

    @property
    def get_photo_count(self):
        return self.photos.all().count()


    def __str__(self):
        return 'Session {}'.format(self.pk)


#Основная модель для newbies используется она же


class Worker(models.Model):
    input_date = models.DateTimeField(
        "Дата внесения",
        auto_now_add=True
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=100
    )
    name = models.CharField(
        "Имя",
        max_length=100
    )
    patronymic = models.CharField(
        "Отчество",
        max_length=100,
        blank=True,
        null=True
    )
    sex = models.CharField(
        verbose_name='Пол',
        max_length=100,
        choices=(
            ("Муж", "Муж"),
            ("Жен", "Жен"),
        ),
        default="Муж",
    )
    birth_date = models.DateField(
        "Дата рождения",
        blank=True,
        null=True
    )
    mig_series = models.CharField(
        "МК, серия",
        max_length=7,
        blank=True,
        null=True
    )
    mig_number = models.CharField(
        "МК, номер",
        max_length=8,
        blank=True,
        null=True
    )
    m_date_of_issue = models.DateField(
        "МК, дата выдачи",
        blank=True,
        null=True
    )
    m_date_of_exp = models.DateField(
        "МК, дата окончания",
        blank=True,
        null=True
    )
    tel_number = models.CharField(
        "Телефон",
        max_length=11,
        blank=True,
        null=True
    )
    metro = models.ForeignKey(
        Metro,
        on_delete=models.PROTECT,
        verbose_name='Метро',
        blank=True,
        null=True
    )

    # Todo: remove
    metro1 = models.CharField(
        verbose_name='Метро',
        default="Н/д",
        max_length=100,
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=100,
        choices=(
            ("Новый", "Новый"),
            ("Неверный номер", "Неверный номер"),
            ("Не хочет", "Не хочет"),
            ("Хочет, но позже", "Хочет, но позже"),
            ("Хочет", "Хочет"),
            ("Черный список", "Черный список"),
        ),
        default="Новый",
        blank=True,
        null=True,
    )
    speaks_russian = models.CharField(
        verbose_name='Знание русского',
        max_length=100,
        choices=(
            ("Н/д", "Н/д"),
            ("Плохо", "Плохо"),
            ("Средне", "Средне"),
            ("Хорошо", "Хорошо"),
        ),
        default="Н/д",
        blank=True,
        null=True,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        verbose_name='Должность',
    )

    # Todo: remove
    position1 = models.CharField(
        verbose_name='Должность',
        max_length=15,
        blank=True, null=True,
        choices=(
            ("Грузчик", "Грузчик"),
            ("Стажер", "Стажер"),
            ("Бригадир", "Бригадир"),
        ),
        default="Грузчик",
    )
    citizenship = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        verbose_name='Гражданство',
        related_name='citizens'
    )
    # Todo: remove
    citizenship1 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=(
            ("РФ", "РФ"),
            ("Киргизия", "Киргизия"),
            ("Казахстан", "Казахстан"),
            ("Узбекистан", "Узбекистан"),
            ("Украина", "Украина"),
            ("Белоруссия", "Белоруссия"),
            ("Таджикистан", "Таджикистан"),
            ("Республика Армения", "Республика Армения"),
            ("Республика Молдова", "Республика Молдова"),
        ),
        default="Киргизия",
        verbose_name='Гражданство'
    )
    # Todo: not nullable
    place_of_birth = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        verbose_name='Место рождения',
        blank=True,
        null=True,
        related_name='workers_born'
    )
    # Todo: remove
    place_of_birth1 = models.CharField(
        max_length=100,
        choices=(
            ("Российская Федерация",
            "Российская Федерация"),
            ("Киргизия", "Киргизия"),
            ("Казахстан", "Казахстан"),
            ("Таджикистан", "Таджикистан"),
            ("Узбекистан", "Узбекистан"),
            ("Украина", "Украина"),
            ("Белоруссия", "Белоруссия"),
            ("Республика Армения",
            "Республика Армения"),
            ("Республика Молдова",
            "Республика Молдова"),
        ),
        default="Киргизия",
        verbose_name='Место рождения',
        blank=True,
        null=True,
    )
    contract_type = models.CharField(
        verbose_name='Договор',
        max_length=100,
        choices=(
            ("Трудовой", "Трудовой"),
            ("ГПХ", "ГПХ"),
        ),
        default="ГПХ",
        blank=True,
        null=True,
    )

    # Todo: migrate to photos
    image1 = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    image2 = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )
    image3 = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
    )

    objects = WorkerQuerySet.as_manager()

    class Meta:
        ordering = ('last_name', 'name', 'patronymic')

    def save(self, *args, **kwargs):
        if self.tel_number:
            self.tel_number = normalized_phone(self.tel_number)

            # Todo: it is not race safe
            same_phone_workers = Worker.objects.filter(
                tel_number=self.tel_number
            ).exclude(
                pk=self.pk
            )
            if same_phone_workers.exists():
                raise Exception(
                    'Есть работник с номером {}: {}'.format(
                        self.tel_number,
                        ', '.join([str(w) for w in same_phone_workers])
                    )
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return _worker_to_string(self)

    def save_worker(self):
        self.input_date = timezone.now()
        self.save()

    def photos(self):
        return get_photos(self)

    def get_turnouts(self, from_date=None):
        if from_date is not None:
            turnouts = WorkerTurnout.objects.filter(
                worker_id=self,
                worker_turnouts__timesheet__sheet_date__gte=from_date
            ).order_by('timesheet__sheet_date')
            return turnouts
        else:
            turnouts = WorkerTurnout.objects.filter(worker_id=self).order_by(
                'timesheet__sheet_date')
            return turnouts

    def day_timesheets(self):
        return WorkerTurnout.objects.filter(worker_id=self,
                                            timesheet__sheet_turn="День").count()

    def night_timesheets(self):
        return WorkerTurnout.objects.filter(worker_id=self,
                                            timesheet__sheet_turn="Ночь").count()

    def rate_of_dayshifts(self):
        day = WorkerTurnout.objects.filter(worker_id=self,
                                           timesheet__sheet_turn="День").count()
        average = WorkerTurnout.objects.filter(worker_id=self).count()
        if average > 0:
            return round(day / average * 100, 1)

    def days_after_last_turnout(self):
        last_turnout = TimeSheet.objects.filter(
            worker_turnouts__worker_id=self).latest('sheet_date')
        delta = date.today() - last_turnout.sheet_date
        return delta.days

    def get_last_turnout(self):
        turnout = TimeSheet.objects.filter(
            worker_turnouts__worker_id=self).latest('sheet_date')
        return '{} - {}'.format(turnout.cust_location, turnout.customer)

    def get_last_comment(self):
        comment = WorkerComments.objects.filter(worker=self).latest('date')
        return '{}'.format(comment.text, )

    def get_actual_contract(self):
        now = timezone.now()
        return self.contract.filter(
                is_actual=True
            ).filter(
                Q(begin_date__isnull=True) | Q(end_date__gt=now)
            ).first()

    @property
    def actual_passport(self):
        try:
            passport = WorkerPassport.objects.get(
                workers_id=self,
                is_actual=True
            )
        except WorkerPassport.DoesNotExist:
            return None
        except WorkerPassport.MultipleObjectsReturned:
            return None
        else:
            return passport

    @property
    def actual_registration(self):
        try:
            registration = WorkerRegistration.objects.get(workers_id=self,
                                                          is_actual=True)
        except WorkerRegistration.DoesNotExist:
            return None
        except WorkerRegistration.MultipleObjectsReturned:
            return None
        else:
            return registration

    @property
    def actual_patent(self):
        try:
            patent = WorkerPatent.objects.get(workers_id=self, is_actual=True)
        except WorkerPatent.DoesNotExist:
            return None
        except WorkerPatent.MultipleObjectsReturned:
            return None
        else:
            return patent

    @property
    def place_of_birth_name(self):
        if self.place_of_birth:
            return self.place_of_birth.name
        else:
            return ''

    @property
    def citizenship_name(self):
        if self.citizenship:
            return self.citizenship.name
        else:
            return ''

    @property
    def position_name(self):
        if self.position:
            return self.position.name
        else:
            return ''


    def update_snils(self, number, date_of_issue, image):
        if hasattr(self, 'snils'):
            snils = self.snils
            snils.number = number
            snils.date_of_issue = date_of_issue
            snils.save()
        else:
            snils = WorkerSNILS.objects.create(
                worker=self,
                number=number,
                date_of_issue=date_of_issue
            )
        if image:
            save_single_photo(snils, image)




