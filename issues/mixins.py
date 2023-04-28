class ProductQuerySetMixin():
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
