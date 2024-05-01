from django.shortcuts import render
#from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .iciciservice import iciciServiceClass
from django.views import View
#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt  # Temporarily disable CSRF for simplicity (use a better approach in production)

class MyView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.some_variable = "Initial Value"
        self.newObj = None

    def setSessionKey(self,request): 
            # Retrieve data from the POST request
        data = request.POST.get('input_value')

            #newObj.session_token=data
        self.newObj = iciciServiceClass(data)
            # Process the data (you can replace this with your actual logic)
            #result = f'You entered: {data}'

            # Return a JSON response (you can customize this part)
            #return JsonResponse({'result': result})

        #return JsonResponse({'error': 'Invalid request method'})
        
    def get(self,request):
        tempData= { 
                    'userName' : '',
                    'totalProfit' : '',
                    'currentOrder' : ''
                    }
        return render(request, 'myFirst.html', tempData)

    def getDataFromApi(self):
        #return HttpResponse("Hello world!")
        iciciserviceObj = self.newObj.getDataFromApi()
        return JsonResponse(iciciserviceObj)


