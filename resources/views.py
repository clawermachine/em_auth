from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.access_control import check_access

METHOD_TO_ACTION = {
    "POST": "create",
    "GET": "read",
    "PATCH": "edit",
    "DELETE": "delete",
}

@api_view(["POST", "GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def resource_action(request, resource):
    action = METHOD_TO_ACTION.get(request.method)

    if not check_access(request.user, resource, action):
        return Response({"detail": "Forbidden"}, status=403)

    return Response({
        "resource": resource,
        "action": action,
        "data": [f"{resource}1_{action}", f"{resource}2_{action}"]
    })
