from django.http import JsonResponse

def custom_error_response(error_msg: str, status_code: int) -> JsonResponse:
    if not (status_code >= 400 and status_code < 600):
        raise ValueError("Invalid error status code")
    
    error_dict={'status': 'error', 'message': error_msg}
    return JsonResponse(error_dict, status=status_code)