from corsheaders.signals import check_request_enabled


def cors_allow_postforms_to_everyone(sender, request, **kwargs):
    return request.path.startswith('/postforms/')


check_request_enabled.connect(cors_allow_postforms_to_everyone)
