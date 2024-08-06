from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Folder, FolderItem
from .serializers import FolderSerializer, FolderItemSerializer


class FolderViewSet(ModelViewSet):
    """
    Implements CURD methods for `Folder` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related('user').all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        user_id = self.request.user.id

        return {
            'user_id': user_id
        }


class FolderItemViewSet(ModelViewSet):
    """
    Implements CURD methods for `FolderItem` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderItemSerializer
    queryset = FolderItem.objects.all()
    permission_classes = [IsAuthenticated]
