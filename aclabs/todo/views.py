from django.shortcuts import render


# Create your views here.
def index(request):
    protocol = "https" if request.is_secure() else "http"
    host = request.META.get("HTTP_HOST")
    path = "/graphql/"
    my_url = "{protocol}://{host}{path}".format(
        protocol=protocol,
        host=host,
        path=path
    )
    context = {"graphql_url": my_url}
    return render(request, "todo/index.html", context=context)
