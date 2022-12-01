from datetime import datetime, timezone
from pytz import timezone

class date_parser:
    @staticmethod
    def string_to_time(time_as_string:str):
        time_obj = datetime.strptime(time_as_string, '%H:%M').time()
        return time_obj

    def string_to_date(self,date_as_string:str):
        date_obj = datetime.strptime(date_as_string, '%Y-%m-%d')
        return date_obj

    def combine_date_and_time_objects(self, date_obj, time_obj):
        self.date_time_obj = datetime.combine(date_obj, time_obj)
        return self.date_time_obj

    def combine_date_and_time_strings(self, date_string, time_string):
        self.date = self.string_to_date(date_string)
        self.time = self.string_to_time(time_string)
        self.date_time = self.combine_date_and_time_objects(self.date, self.time)
        return self.date_time