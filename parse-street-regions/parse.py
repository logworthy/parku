import ogr, re, csv


def run():
    events = []
    events_path = "../data/example_parking_data.csv"
    with open(events_path, 'rb') as f:
        r = csv.DictReader(f, delimiter=',', skipinitialspace=True)
        for row in r:
            events.append(Event(row))

    regions_path = "../data/datamelbourne_road/Road Corridor.shp"
    data_source = ogr.Open(regions_path)
    layer = data_source.GetLayer()

    layer.SetAttributeFilter("NAME NOT IN ( 'railway/tramway', 'river' )")

    streetishes = []

    for feature in layer:
        address = feature.GetField("ADDRESS")
        streetish = parse_address(address)
        if streetish is not None:
            streetishes.append(streetish)

    print "Found %d" % len(streetishes)

    for event in events:
        matches = None
        for streetish in streetishes:
            if event.matches_streetish(streetish):
                matches = streetish
                break

        if matches:
            print "MATCH! YAY! %s == %s" % (event, matches)
        else:
            print "Oh noes, doesn't match: %s" % event


class Event():
    def __init__(self, row):
        self.street = row['Street Name']
        self.from_street = row['Between Street 1']
        self.to_street = row['Between Street 2']
        self.street_marker = row['Street Marker']

    def matches_streetish(self, streetish):
        if streetish.street != self.street:
            return False

        if streetish.from_street is not None and streetish.to_street is not None:
            if streetish.from_street == self.from_street and streetish.to_street == self.to_street:
                return True
            elif streetish.to_street == self.from_street and streetish.from_street = self.to_street:
                return True

        return False

    def __str__(self):
        return "%s (%s - between %s and %s)" % (self.street_marker, self.street, self.from_street, self.to_street)


class Streetish():
    def __init__(self, street, from_street=None, to_street=None):
        self.street = street.upper()
        self.from_street = None if from_street is None else from_street.upper()
        self.to_street = None if to_street is None else to_street.upper()

    def __str__(self):
        if self.from_street is None:
            return self.street
        elif self.to_street is None:
            return "%s (from %s)" % (self.street, self.from_street)
        else:
            return "%s (between %s and %s)" % (self.street, self.from_street, self.to_street)


class AddressParser():
    def __init__(self, regex):
        self.regex = regex
        self.streetish = None

    def parse(self, address):
        match = self.regex.match(address)

        if match is not None:
            self.streetish = self.handle(match)
            return True
        else:
            return False

    def handle(self, match):
        pass


# 1925 matches.
class BetweenAndParser(AddressParser):
    def __init__(self):
        AddressParser.__init__(self, re.compile("(.*) between (.*) and (.*)"))

    def handle(self, match):
        street_main = match.groups()[0]
        street_from = match.groups()[1]
        street_to = match.groups()[2]

        return Streetish(street_main, street_from, street_to)


# 725 matches.
class IntersectionOfParser(AddressParser):
    def __init__(self):
        AddressParser.__init__(self, re.compile("Intersection of (.*) and (.*)"))

    def handle(self, match):
        street_one = match.groups()[0]
        street_two = match.groups()[1]

        return None


class FromParser(AddressParser):
    def __init__(self):
        AddressParser.__init__(self, re.compile("(.*) from (.*)"))

    def handle(self, match):
        street = match.groups()[0]
        street_from = match.groups()[1]

        return Streetish(street, street_from)


# 1 found
class NumberParser(AddressParser):
    def __init__(self):
        AddressParser.__init__(self, re.compile("(\d*) (.*)"))

    def handle(self, match):
        street_number = int(match.groups()[0])
        street = match.groups()[1]

        return None


class GenericStreetParser(AddressParser):
    def __init__(self):
        AddressParser.__init__(self, re.compile("(.*)"))

    def handle(self, match):
        street = match.group(0)

        return Streetish(street)


def parse_address(address):
    if address is None:
        return None

    # (street) between (street) and (street)
    # Intersection of (street) and (street)
    # (street) from (street)
    # (number) (alpha) (street)

    # (street)
    # PL(numbers)
    # Pl(numbers)
    # Cl(numbers)
    # CL(numbers)

    # [Null]

    parsers = [
        BetweenAndParser(),
        IntersectionOfParser(),
        FromParser(),
        NumberParser(),
        GenericStreetParser()
    ]

    for parser in parsers:
        success = parser.parse(address)
        if success:
            return parser.streetish

    return False


run()

