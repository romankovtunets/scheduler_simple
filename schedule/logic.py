from datetime import date, datetime, timedelta


class AssesEmailDates():

    def __init__(self, emails, skip_dates=None):
        self.emails = emails
        self.skip_dates = self.get_skipped_dates(skip_dates)

    @staticmethod
    def get_skipped_dates(skipped_days_iso):
        """
        Get days to skip
        """
        iso_format ='%Y-%m-%dT%H:%M:%S.%f'

        days_to_skip = []
        for item in skipped_days_iso:
            days_to_skip.append(datetime.strptime(item, iso_format).date())

        return days_to_skip


    def get_dispatch_date(self, start_date=datetime.now()):
        """
        Get firts available day to send emails
        """
        # check time
        if start_date.hour in range(9, 17):
            # check date
            if start_date.date() not in self.skip_dates and \
                                         start_date.weekday() not in (5, 6):
                return start_date
            else:
                next_date = (start_date + timedelta(days=1))
                next_date.replace(hour=9, minute=0)
                return self.get_dispatch_date(next_date)
        else:
            next_date = (start_date + timedelta(days=1))
            next_date.replace(hour=9, minute=0)
            return self.get_dispatch_date(next_date)


    def assesing_datetime(self):
        """
        Asses dispatch time to each email in the list
        return: dict
        """
        # set starting date
        dispatch_date = self.get_dispatch_date()
        # set pause between dispatches
        next_5_min = timedelta(minutes=5)

        dispatches = {}

        # while contact list is not empty
        while self.emails:
            # ten dispatches for a day
            for i in range(min(len(self.emails), 10)):
                dispatches[self.emails.pop(0)] = dispatch_date
                dispatch_date += next_5_min

            # get next day if contact list is not empty and 10 dispatches done
            dispatch_date = self.get_dispatch_date(dispatch_date.replace(hour=9))

        return dispatches
