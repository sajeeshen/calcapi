from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from calculator.permissions import IsSuperUser
from rest_framework.permissions import IsAuthenticated
import math
from django.utils.translation import ugettext_lazy as _
from calculator import serializers

ACCESS_ERROR = _("You dont have permission for this operation")

AVAILABLE_ACTIONS = [
    {'action': 'add', 'operator': '+'},
    {'action': 'subtract', 'operator': '-'},
    {'action': 'multiple', 'operator': '*'},
    {'action': 'divide', 'operator': '/'},
    {'action': 'power', 'operator': '**'},
    {'action': 'sqrt', 'operator': 'sqrt'},

]


class Calculator(generics.GenericAPIView):
    serializer_class = serializers.CalculatorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def check_permissions(self, request):
        """
        Based on the Operation setting the permission for the users
        if its admin , admin can do all else limited access
        :param request:
        :param args:
        :return:
        """

        self.admin_required = request.\
            resolver_match.kwargs.get('admin_required')

        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def get_permissions(self):

        if self.admin_required:
            self.permission_classes = (IsSuperUser,)
        else:
            self.permission_classes = (IsAuthenticated,)

        return super(self.__class__, self).get_permissions()

    def post(self, request, operation, admin_required, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            x = self.request.data.get('x', 0)
            y = self.request.data.get('y', 0)
            action_parameter = {'x': x, 'y': y}
            serializer.save(user=request.user,
                            action_name=operation,
                            action_parameter=action_parameter
                            )
            return Response({'message': 'Success',
                             'result': self.do_calculation(operation, x, y)})
        else:
            raise serializer.ValidationError("Cant process, "
                                             "please check the input")

    def do_calculation(self, operation, x, y):
        """
        This function for the calculation part
        :param operation: string
        :param x: int
        :param y: int
        :return: int
        """
        operator = self.get_operator((operation))[0]['operator']
        ops = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y else 0,
            '**': lambda x, y: x ** y,
            'sqrt': lambda x, y: math.sqrt(int(x))
        }
        return ops[operator](int(x), int(y))

    def get_operator(self, operator):
        """
        Get the operator from the Available options object
        :param operator:
        :return:
        """

        return [obj for obj in AVAILABLE_ACTIONS
                if obj['action'] == operator.lower()]
