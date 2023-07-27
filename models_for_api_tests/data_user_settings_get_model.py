class DataUserSettingsGetModel:
    def __init__(self, currency, distance_units):
        self.currency = currency
        self.distanceUnits = distance_units

    def __str__(self):
        return self.__dict__
