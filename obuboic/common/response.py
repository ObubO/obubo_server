from rest_framework.response import Response
from rest_framework import status

HTTP_200 = Response({"success": True}, status=status.HTTP_200_OK)
HTTP_201 = Response({"success": True}, status=status.HTTP_201_CREATED)
HTTP_202 = Response({"success": True}, status=status.HTTP_202_ACCEPTED)
HTTP_203 = Response({"success": True}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
HTTP_204 = Response({"success": True}, status=status.HTTP_204_NO_CONTENT)

HTTP_400 = Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
HTTP_401 = Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
HTTP_404 = Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

HTTP_503 = Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


def http_200(result):
    return Response(
        {
            "success": True,
            "result": result
        },
        status=status.HTTP_200_OK
    )


def http_201(result):
    return Response(
        {
            "success": True,
            "message": result
        },
        status=status.HTTP_201_CREATED
    )


def http_400(error):
    return Response(
        {
            "success": False,
            "message": error
        },
        status=status.HTTP_400_BAD_REQUEST
    )


def http_401(error):
    return Response(
        {
            "success": False,
            "message": error
        },
        status=status.HTTP_401_UNAUTHORIZED
    )


def http_403(error):
    return Response(
        {
            "success": False,
            "message": error
        },
        status=status.HTTP_403_FORBIDDEN
    )


def http_404(error):
    return Response(
        {
            "success": False,
            "message": error
        },
        status=status.HTTP_404_NOT_FOUND
    )


def http_409(error):
    return Response(
        {
            "success": False,
            "message": error
        },
        status=status.HTTP_409_CONFLICT
    )


def http_503(error):
    return Response(
        {
            "success": False,
            "message": error
        },
        status=status.HTTP_503_SERVICE_UNAVAILABLE
    )
