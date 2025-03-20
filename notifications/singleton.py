class NotificationServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(NotificationServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Singleton
class NotificationService(metaclass=NotificationServiceMeta):
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, subscriber):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)

    def unsubscribe(self, event_type, subscriber):
        if event_type in self.subscribers and subscriber in self.subscribers[event_type]:
            self.subscribers[event_type].remove(subscriber)

    def notify(self, event_type, data):
        if event_type in self.subscribers:
            for subscriber in self.subscribers[event_type]:
                subscriber(data)