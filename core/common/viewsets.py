from rest_framework.viewsets import ModelViewSet as MVS

from .permissions import PermissionPolicyMixin


class ModelViewSet(PermissionPolicyMixin, MVS):
    pass
