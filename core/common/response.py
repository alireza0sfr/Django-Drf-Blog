from rest_framework import status


class BaseResponse:

    def __init__(self, **args):
        self.response = {
            "status": args.get('status', status.HTTP_200_OK),
            "data": args.get('data', None),
            "message": args.get('message', '')
        }
