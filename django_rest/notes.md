# Links
[SlideDeck](https://speakerdeck.com/williln/what-you-should-know-about-django-rest-framework)
[cdrf.co](http://www.cdrf.co/) (provides the framework viewsets, similar to Swagger schemas, that provide endpoint/sourcecode modeling for the metaclasses in DRF)
# Notes
## General
- ModelViewSets: Class-based views for CRULD in your DB
- ModelMixins: endpoint actions (get/put/post/del)
- Serializer: allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. 
## ViewSets
- type of class-based View
- does not provide any method handlers such as `.get()` or `.post()` 
- instead provides actions such as `.list()` and `.create()`
- method handlers for a ViewSet are only bound to the corresponding actions at the point of finalizing the view, using the `.as_view()` method.
## ModelViewSets
Class-based definitions for the CRULD interactions with a ViewSet.
- Give you Create, Read, Update, List, and Destroy (CRULD) endpoints
## Methods
### From GenericApiView
- `foo.action()`
- `foo.get_object()`
- `foo.get_serializer_class()`
- `foo.get_serializer()`
- `foo.get_serializer_context()`
- `foo.get_queryset()`
#### get_queryset() Example
You should override `get_queryset()` when you need to filter your query set data because this can't happen at the time of request, so it needs to be done in the controller endpoint/Model.

```
def get_object(self):
    queryset = self.filter_queryset(self.get_queryset())
    lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

    assert lookup_url_kwarg in self.kwargs, (
        'Expected view to be called with a URL keyword arguments '
        'named "%s". Fix your URL conf, or set the `.lookup_field` '
        'attribute on the view correctly.' %
        (self.__class__.__name__, lookup_url_kwarg)
    )
    # Uses the lookup_field attribute, which defaults to 'pk'
    filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    obj = get_object_or_404(queryset, **filter_kwargs)

    # May raise a permission denied
    self.check_object_permissions(self.request, obj)
    return obj
```

Now in your own methods you can run `obj = self.get_object()` instead of looking up the object yourself. 

##### get_serializer() Example
Override `get_serializer_class()` when you want situational control over your serializer. 

```
def get_serializer(self, *args, **kwargs):
    serializer_class = self.get_serializer_class()

    # The context is where the request is added to the serializer
    kwargs['context'] = self.get_serializer_context()

    return serializer_class(*args, **kwargs)
```

Override `get_serializer_context()` when you need to add something to the context so your serializer can use it

```
def get_serializer_context(self):
    # Override this method to add more stuff
    # to the serializer context
    return {
        'request': self.request,
        'format': self.format_kwarg,
        'view': self,
    }
```

## *ModelMixins
- Classes that instanatiate methods for CRULD
### CreateModelMixin
[CDRF Document](http://www.cdrf.co/3.9/rest_framework.mixins/CreateModelMixin.html)
```
class CreateModelMixin:

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer) # save serializer
        
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()
```
## Example ViewSet
```
# views.py
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer, BookCreatedSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all() #set scope for query to 'all'
    serializer_class = BookSerializer #set what I'm serializing
    permission_classes = [AllowAny] #who can serialize the data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer) # save serializer
        instance = serializer.save()

        return_serializer = BookCreatedSerializer(instance)

        headers = self.get_success_headers(return_serializer.data)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            return_serializer.data, status=status.HTTP_201_CREATED,headers=headers
        )

```
The above code provides the following endpoints:
    - GET /books/ #Get all books
    - GET /books/{id} #Get a book by id
    - POST /books/ #Add a new book
    - PUT /books/{id} #Do an atomic replace on a book
    - PATCH /books/{id} #Do an update on a book, inserting provided fields
    - DELETE /books/{id} #Delete a book by id
  
## Mix-n-Match Endpoints/Views
If you don't want an endpoint, such as `Delete`, to not be available you can declare a custom class as a subset.
### Do everything except delete
```
from rest_framework.generics import GenericApiView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, ListModelMixin

class NoDeleteSet(
    CreateModelMixin, 
    RetrieveModelMixin,
    UpdateModelMixin, 
    ListModelMixin,
    GenericApiView
)
```
### Read-Only
```
from rest_framework.generics import GenericApiView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, ListModelMixin

class ReadOnlySet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericApiView
)
```
### Premade Mix-n-Match Views
- CreateAPIView
- ListAPIView
- RetrieveAPIView
- DestroyAPIView
- ReadOnlyModelViewSet
- RetrieveDestroyAPIView
- RetrieveUpdateDestroyAPIView
- ListCreateAPIView
- RetrieveUpdateAPIView

## Limiting a ViewSet
You can limit an endpoint (GET /books/featured/) to a property of the called item (featured) in a set (books).
```
from rest_framework.decorators import action

class BookViewSet():
    queryset = Book.objects.all() #set scope for query to 'all'
    serializer_class = BookSerializer #set what I'm serializing

    def get_serializer_class(self):
        if self.action in ["list", "featured"]:
            return BookListSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=["get"])
    def featured(self, request):
        books = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```
