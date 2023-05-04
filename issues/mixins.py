from rest_framework import generics


class ProductQuerySetMixin:
    contributors_field = 'member'
    allow_staff_view = True

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.contributors_field] = user.id
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if self.allow_staff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)


class MultipleFieldListViewMixin:
    """
    Apply this mixin to any List view to get multiple field filtering
    queryset based on a `lookup_fields` attribute,
    instead of the default single field filtering.
    """
    def get_queryset(self, *args, **kwargs):
        filter_ = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter_[field] = self.kwargs[field]
        obj = self.queryset.filter(**filter_)
        # Check permissions ?
        return obj


class MultipleFieldDetailViewMixin:
    """
    Apply this mixin to any Detail view to get multiple field filtering
    object based on a `lookup_fields` attribute,
    instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()     # Get the base queryset
        filter_ = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):     # Ignore empty fields.
                filter_[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter_)  # Lookup the object
        # self.check_object_permissions(self.request, obj)     # /!\ Add permissions first
        return obj
