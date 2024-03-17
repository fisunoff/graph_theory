import json

from rest_framework import views, permissions
from rest_framework.response import Response

from sets.calculator import solve


# Create your views here.


class CalcView(views.APIView):
    def get(self, request):
        data = {
            'answer': 'Hello from Anton',
            'errors': [],
        }
        results = json.dumps(data)
        return Response(data)

    def post(self, request):
        data = request.data
        try:
            result = solve(data['expression'], data['A'], data['B'], data['C'])
            if result[0] == 'error':
                answer = {
                    'answer': None,
                    'errors': result[1],
                }
            else:
                answer = {
                    'answer': result[1],
                    'errors': [],
                }
            return Response(answer)
        except Exception as e:
            answer = {
                'answer': None,
                'errors': [str(e)],
            }
            return Response(answer)
