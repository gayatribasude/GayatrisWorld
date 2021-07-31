import datetime

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.utils import timezone

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView

Order=apps.get_model('orders','Order')

class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/analysis.html'
    #Think of it as a middleman between requests and responses.
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return HttpResponse("You Cant access this page")
        return super(SalesView, self).dispatch(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        qs = Order.objects.filter(confirm=True).by_weeks_range(weeks_ago=10, number_of_weeks=10)
        start_date = timezone.now().date() - datetime.timedelta(hours=18)
        context['timezone']=timezone.now().date()
        end_date = timezone.now().date() + datetime.timedelta(hours=12)
        today_data = qs.by_range(start_date=start_date, end_date=end_date).get_sales_breakdown()
        context['today'] = today_data
        context['this_week'] = qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=2, number_of_weeks=2).get_sales_breakdown()
        print(qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown())
        return context


class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data={}
        qs = Order.objects.filter(confirm="True").by_weeks_range(weeks_ago=5, number_of_weeks=5)
            
        if request.GET.get('type') == 'week':
            days = 7
            start_date = timezone.now().today() - datetime.timedelta(days=days - 1)
            datetime_list = []
            labels = []
            salesItems = []
            for x in range(0, days):
                new_time = start_date + datetime.timedelta(days=x)
                datetime_list.append(
                    new_time
                )
                labels.append(
                    new_time.strftime("%a")  # mon
                )
                new_qs = qs.filter(updated__day=new_time.day, updated__month=new_time.month)
                day_total = new_qs.totals_data()['finaltotal__sum'] or 0
                salesItems.append(
                    day_total
                )
            print(datetime_list)

            data['labels'] = labels
            data['data'] = salesItems


        if request.GET.get('type') == '4weeks':
            data['labels'] = ["Four Weeks Ago", "Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
            current = 5
            data['data'] = []
            for i in range(0, 5):
                new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                sales_total = new_qs.totals_data()['finaltotal__sum'] or 0
                data['data'].append(sales_total)
                current -= 1

        return JsonResponse(data)


class OrderList(LoginRequiredMixin,ListView):
    template_name = 'orders/orderlist.html'
    model = Order
    context_object_name = 'order'
    ordering = ['-updated']
    queryset = Order.objects.filter(confirm=True)

    def post(self, request, *args, **kwargs):
        object = self.get_object()

class OrderDetails(LoginRequiredMixin,DetailView):
    template_name = 'orders/orderdetails.html'
    model = Order
    context_object_name = 'order'


class UpdateOrder(LoginRequiredMixin,UpdateView):
    model = Order
    success_url = '/orders/orderlist'
    fields = ['status']
    template_name = 'orders/orderdetails.html'



