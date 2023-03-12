# from django.db import models

# class Get_review(models.Manager):
#       def get_query_set(self):
#         reviews =  super(Get_review, self).get_query_set().filter(product=self)
#         avg_review = reviews.aggregate(models.Avg('star'))
#         if avg_review['star__avg'] is not None:
#             return round(avg_review['star__avg'], 1)
#         else:
#             return 0