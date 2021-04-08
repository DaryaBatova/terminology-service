from django.shortcuts import render
from .models import Handbook, HandbookVersion
from .serializer import HandbookListSerializer, ElementListSerializer, HandbookVersionListSerializer
from django.views import generic
from rest_framework import generics
import re
from rest_framework.exceptions import APIException


class InvalidHandbookException(APIException):
    status_code = 400
    default_detail = 'Your request contain invalid handbook. You must specify the handbook identifier as an integer.'
    default_code = 'invalid_handbook'


class InvalidVersionException(APIException):
    status_code = 400
    default_detail = 'Your request contain invalid handbook version. ' \
                     'You must specify the handbook version as two integers separated a dot.'
    default_code = 'invalid_handbook_version'


class HandbookDoesNotExistException(APIException):
    status_code = 404
    default_detail = 'The requested handbook was not found.'
    default_code = 'invalid_handbook_version'


def index(request):
    """ View function for home page of site. """
    return render(request, 'index.html')


class HandbookListView(generic.ListView):
    """ Generic class-based view for a list of handbooks of the latest versions. """
    model = Handbook
    paginate_by = 10


class HandbookDetailView(generic.DetailView):
    """ Generic class-based detail view for a handbook. """
    model = Handbook


class HandbookAllListView(generic.ListView):
    """ Generic class-based list view for a list of handbooks of all versions. """
    model = HandbookVersion
    paginate_by = 10


class HandbookVersionDetailView(generic.DetailView):
    """ Generic class-based detail view for a handbook from handbook_version table. """
    model = HandbookVersion


class HandbooksListView(generics.ListAPIView):
    """
    Used for read-only endpoint to represent a list of handbooks relevant for a given date.
    Provides a get method handler.
    """
    serializer_class = HandbookListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        """
        Customize the queryset returned by the view. Filtering against the URL.
        The handbook relevant for a given date = the handbook with the value from the field 'date' <= given date.
        :return: a handbook_version queryset filtered by the date portion of the URL.
        """
        # date = '2021-03-12'
        date = self.kwargs['date']
        queryset = []
        handbooks = self.model.objects.all()
        entries = HandbookVersion.objects.filter(date__lte=date).order_by('-date')

        for q in entries:
            queryset.append(
                {
                    'id': q.pk,
                    'title': handbooks.get(pk=q.handbook.pk).title,
                    'short_title': handbooks.get(pk=q.handbook.pk).short_title,
                    'description': handbooks.get(pk=q.handbook.pk).description,
                    'version': q.version,
                    'date': q.date,
                }
            )

        return queryset


class ElementsListView(generics.ListAPIView):
    """
    Used for read-only endpoint to represent a list of elements of a given handbook and a given version.
    Provides a get method handler.
    """
    serializer_class = ElementListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        """
        Customize the queryset returned by the view. Filtering against query parameters.
        Query parameters: 1) id of the handbook, 2) version.
        :return: a elements queryset filtered by the id and version of the handbook of the URL.
        """
        handbook = self.request.query_params.get('handbook', '')
        version = self.request.query_params.get('version', '')
        if not handbook or not re.match(r'\d+', handbook):
            raise InvalidHandbookException()
        if version and not re.match(r'\d+\.\d+', version):
            raise InvalidVersionException()
        try:
            necessary_handbook = Handbook.objects.get(pk=handbook)
            version_handbook = version if version else necessary_handbook.version
            queryset = self.model.objects.filter(handbook=handbook, version=version_handbook)
            return queryset
        except Handbook.DoesNotExist:
            raise HandbookDoesNotExistException()


class ElementsByTitleListView(generics.ListAPIView):
    """
    Used for read-only endpoint to represent a list of elements of a given handbook and a given version.
    Provides a get method handler.
    """
    serializer_class = ElementListSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        """
        Customize the queryset returned by the view. Filtering against query parameters.
        Query parameters: 1) title of the handbook, 2) version.
        :return: a elements queryset filtered by the title and version of the handbook of the URL.
        """
        handbook = self.request.query_params.get('handbook', '').replace('%', ' ')
        version = self.request.query_params.get('version', '')
        if not handbook:
            raise InvalidHandbookException()
        if version and not re.match(r'\d+\.\d+', version):
            raise InvalidVersionException()
        try:
            necessary_handbook = Handbook.objects.get(title=handbook)
            handbook_id = necessary_handbook.id
            handbook_version = version if version else necessary_handbook.version
            queryset = self.model.objects.filter(handbook=handbook_id, version=handbook_version)
            return queryset
        except Handbook.DoesNotExist:
            raise HandbookDoesNotExistException()
