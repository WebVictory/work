def workers_report(request):
    sessions = models.PhotoLoadSession.objects.filter(
        sender__userphone__isnull=False
    ).exclude(
        status='complete'
    ).distinct(
    ).order_by(
        '-pk'
    ).annotate(
        phone=Subquery(
            models.UserPhone.objects.filter(
                user__pk=OuterRef('sender')
            ).values('phone')
        ),
        citizenship=Subquery(
            models.Country.objects.filter(
                photosessioncitizenship__session__pk=OuterRef('pk')
            ).values('name')
        )
    )

    newbies = models.Worker.objects.filter(
        assigned_delivery_requests__isnull=True,
        workeruser__user__mobileappstatus__isnull=False,
        banned__isnull=True,
    ).distinct(
    ).order_by(
        '-pk'
    )

    workers = models.Worker.objects.filter(
        assigned_delivery_requests__isnull=False,
        banned__isnull=True,
    ).distinct(
    ).annotate(
        first_day=Subquery(
            models.DeliveryRequest.objects.filter(
                assigned_workers__worker__pk=OuterRef('pk')
            ).order_by(
                'date'
            ).values('date')[:1]
        ),
        last_day=Subquery(
            models.DeliveryRequest.objects.filter(
                assigned_workers__worker__pk=OuterRef('pk')
            ).order_by(
                '-date'
            ).values('date')[:1]
        ),
        on_vacation=Exists(
            models.WorkerOnVacation.objects.filter(
                worker__pk=OuterRef('pk')
            )
        )
    ).order_by(
        'on_vacation',
        '-first_day'
    )

    return render(
        request,
        'the_redhuman_is/delivery/workers_report.html',
        {
            'sessions': sessions,
            'newbies': newbies,
            'workers': workers
        }
    )

