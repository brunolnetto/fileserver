from django.http import JsonResponse

def custom_error_reponse(error_msg: str, status_code: int) -> JsonResponse:
    error_dict={'status': 'error', 'message': error_msg}
    return JsonResponse(error_dict, status=status_code)