from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, views
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, views, status
from rest_framework.response import Response
from django_filters import rest_framework as dj_filters
from rest_framework.decorators import action
from coreapp.pagination import paginate
from datetime import date, timedelta
from django.db.models.functions import Now
from django.db.models import Q,Sum,Count,Avg,Max,Min
import random
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import pathlib
from django.conf import settings
import uuid
import traceback
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.views import View
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from coreapp.pagination import paginate
import json
from utility.utils import is_seen_utils
from django.db.models.signals import pre_save, post_save
from rest_framework import filters

def print_log(log):
    import logging
    logger = logging.getLogger('django')
    logger.error(log)