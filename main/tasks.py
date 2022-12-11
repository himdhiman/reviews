from celery import shared_task


@shared_task(bind=True)
def populateReview(self, context):
    print(context)
    pass


@shared_task(bind=True)
def cleanReviews(self):
    print("Clean Reviews Called")
    pass