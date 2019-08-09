from datetime import datetime
from time import sleep
import threading

class Reminder:
    def __init__(self, callback):
        self.callback = callback
        self.reminders = list()
        self.check_reminders = threading.Thread(target=self._check_reminders, args=(5,))
        self.check_reminders.start()

    def add_reminder(self, msg, context, chat_id):
        time_str = msg[0]
        clean = time_str.replace('.','').replace(':','')
        try:
            time = datetime.strptime(clean, '%H%M')
            rem = {
              'time': time,
              'chat_id': chat_id,
              'message': msg,
              'context': context
            }
            self.reminders.append(rem)
            print('Created reminder on', time)
        except ValueError:
            print('Wrong time %s' % time_str)
        pass

    def _check_reminders(self, delay):
        while True:
            now = datetime.now()
            for r in self.reminders:
                if (now.hour, now.minute) == (r['time'].hour, r['time'].minute):
                    print('The time has come %s' % r['time'])
                    self.callback(r)
                    self.reminders.remove(r)
                else:
                    pass
            sleep(delay)
