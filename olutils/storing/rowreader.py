"""Convenient tools to read and encapsulate rows (dictionaries)"""
from collections import OrderedDict

from olutils.compare import content_diff


class RowReader:
    """Convenient row reader that includes key conversions and building"""

    def __init__(self, fields, conversions=None, operations=None, delete=None):
        """Initialize a row reader instance

        Args:
            fields (dict)       : (attribute, column name) items to read attr
                from initial row
            conversions (dict)  : (attribute, conversion func) items to convert
                attributes read from rows
            operations (dict)   : (attribute, func) to build new attributes
                from instance built with read and converted attributes
                One should use OrderedDict if operation order matters
            delete (list)       : attributes to delete ones building is over

        Example:
            >> reader = RowReader(
                fields={'id': "ID", 'name': "Name"},
                conversions={'id': int},
                operations={'label': lambda r: str(r.id) + "." + r.name}
            )
            >> row = reader.read({'ID': "8", 'name': "Name"})
            >> assert row.id == 8
            >> assert row.name == "Octave"
            >> assert row.label == "8.Octave"
        """
        self.fields = fields
        self.conversions = conversions if conversions else {}
        self.operations = operations if operations else {}
        self.delete = delete if delete else []

    def read(self, irow):
        """Build an instance from initial row with required attributes

        Args:
            irow (dict): row to read

        Raises:
            (KeyError) if a field is missing in row

        Return:
            (OrderedDict)
        """
        try:
            row = OrderedDict([
                (attr, irow[field])
                for attr, field in self.fields.items()
            ])
        except KeyError:
            diff = content_diff(irow.keys(), self.fields.values())
            raise KeyError(
                f"Row is missing keys: {', '.join(map(repr, diff['plus']))}"
            ) from None

        for key, func in self.conversions.items():
            row[key] = func(row[key])

        for key, func in self.operations.items():
            row[key] = func(row)

        for key in self.delete:
            del row[key]

        return row
