from django.shortcuts import render
from datetime import datetime, timedelta
from django.views import View
from .models import Cycle
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

@method_decorator(login_required, name='dispatch')
class CycleDatesView(View):
    def get(self, request):
        return render(request, 'cycle_tracker.html')

    def post(self, request):
        previous_date_str = request.POST.get('previous_date')
        previous_date = datetime.strptime(previous_date_str, '%Y-%m-%d').date()
        previous_date_str_formatted = previous_date.strftime('%d/%m/%Y')

        cycle_length = int(request.POST.get('cycle_length'))

        next_occurrence = previous_date + timedelta(days=cycle_length)

        next_12_occurrences = [next_occurrence + timedelta(days=cycle_length * i) for i in range(12)]

        flow_date = next_occurrence

        ovulation_date = previous_date + timedelta(days=cycle_length - 14)

        fertile_periods = []

        start_fertile = ovulation_date - timedelta(days=2)
        end_fertile = ovulation_date
        fertile_periods.append((start_fertile, end_fertile))

        safe_periods = []

        for i in range(3):
            end_cycle_dates = previous_date + timedelta(days=cycle_length * i)
            start_safe_periods = end_cycle_dates - timedelta(days=10)
            end_safe_periods = end_cycle_dates + timedelta(days=10)
            safe_periods.append((start_safe_periods, end_safe_periods))
            end_cycle_dates += timedelta(cycle_length)

        cycle = Cycle(previous_date=previous_date,
                      cycle_length=cycle_length,
                      next_occurrence=next_occurrence,
                      next_12_occurrences=next_12_occurrences,
                      flow_date=flow_date,
                      ovulation_date=ovulation_date,
                      safe_periods=safe_periods,
                    )
        cycle.save()

        return render(request, 'cycle_tracker.html', {'cycle': cycle})
