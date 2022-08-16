import ipdb
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView, status

from content.content_serializer import ContentSerializer
from content.models import Content


class ContentView(APIView):
    def get(self, request):
        contents = Content.objects.all()
        contents_dict = []

        for content in contents:
          m = model_to_dict(content)
          contents_dict.append(m)

        return Response(contents_dict,200)


    def post(self, request):
        # ipdb.set_trace()
        serial_content = ContentSerializer(**request.data)
        if serial_content.is_valid():

          contents = Content.objects.create(**serial_content.data)
          contents_dict = model_to_dict(contents)
          return Response(contents_dict, 201)
        else:
            return Response(serial_content.errors, 400)


class ContentDetailView(APIView):
    def get(self, request,content_id:int):
      try:
        content = Content.objects.get(id = content_id)
      except Content.DoesNotExist:
        return Response( {"message": "Content not found."},status.HTTP_404_NOT_FOUND)  
      
      content_dict = model_to_dict(content)

      return Response(content_dict)

    def patch(self, request,content_id:int):
       try:
        content = Content.objects.get(id = content_id)
       except Content.DoesNotExist:
        return Response( {"message": "Content not found."},status.HTTP_404_NOT_FOUND)  

       for key, value in request.data.items():
        setattr(content, key, value)

       content.save()

       content_dict = model_to_dict(content)

       return Response(content_dict)

    def delete(self, request,content_id:int):
       try:
        content = Content.objects.get(id = content_id)
       except Content.DoesNotExist:
        return Response( {"message": "Content not found."},status.HTTP_404_NOT_FOUND)

       content.delete()    

      
       return Response( status = status.HTTP_204_NO_CONTENT)    


class ContentFilterView(APIView):
  def get(self, request):
    # ipdb.set_trace()

    title_param = request.query_params.get('title')
    contents = Content.objects.filter(title__contains = title_param)

    filteres_title = [model_to_dict(title) for title in contents]

    return Response( filteres_title ,status.HTTP_200_OK)    
