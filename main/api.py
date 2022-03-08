from .models import Tweet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone

class GetScores(APIView):
  authentication_classes = []
  permission_classes = []
  
  def get(self, request):
    count_dict = {}
    try:
      days = request.GET.get('days')
      days = int(days)
      london_time = timezone.now() + timedelta(hours=3)
      date_range = [london_time-timedelta(days=days), london_time]

      for score in range(1, 102, 1):
        higher_score = score/100
        
        lower_score = round(higher_score - 0.01,2)
        print(lower_score)
        
        dict_key = f'{lower_score}'
        if higher_score == 1.01:
          count_dict[dict_key] = Tweet.objects.filter(electoral_score__gte=1,
                                              created_at__range=date_range).count()
        elif lower_score == 0.0:
          count_dict[dict_key] = Tweet.objects.filter(electoral_score__gte=lower_score, 
                                              electoral_score__lte=higher_score,
                                              created_at__range=date_range).count()          
        else:
          count_dict[dict_key] = Tweet.objects.filter(electoral_score__gte=lower_score, 
                                            electoral_score__lt=higher_score,
                                            created_at__range=date_range).count()
    except ValueError as e:
      count_dict['error'] = f'{e}'
      count_dict['description'] = f'The passed value in days variable isnt valid. Please, try again with an integer.'
    except TypeError as e:
      count_dict['error'] = f'{e}'
      count_dict['description'] = 'The API needs a days value to perform the query.' 
    
    print(count_dict)
    
    return Response(count_dict)



class ListUsers(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request):
    NUMBER_OF_AUTHORS = 15

    score = request.GET.get('score')
    verified = request.GET.get('verified')
    
    check = True if verified == "True" else False
    
    users =  Tweet.objects.filter(electoral_score__gte = score)
    
    if check:
      users = users.filter(author_id__user_verified=check)
    
    users = users.values('author_id').annotate(Count('author_id')).order_by('-author_id__count')[:NUMBER_OF_AUTHORS]
    
    json_data = {}
    for item in users.iterator():
      json_data[item['author_id']] = item['author_id__count']
    
    return Response(json_data)