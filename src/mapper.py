import kanban
import json

class Mapper(object): 
    def __init__(self, symbols):
        self.symbols = symbols
        self.board_id = None
        self.columns_count = None 
        self.read_config()
        self.columns = self.get_colums()
        self.cards = self.get_cards()

    def get_symbol_starting_with(self, startsWith):
        matching_symbols = []
        for symbol in self.symbols:
            if symbol.data.startswith(startsWith):
                matching_symbols.append(symbol)
        return matching_symbols

    def read_config(self):
        config_codes = self.get_symbol_starting_with('[')
        config_code_data = config_codes[0].data
        config = json.loads(config_code_data)
        self.board_id = config [0]
        self.columns_count = config [1]

    def get_colums(self):
        columns = []
        column_symbols = self.get_symbol_starting_with('__')
        for symbol in column_symbols:
            column = kanban.Column(None, symbol.location)
            columns.append(column)
        columns.sort ( key=lambda Area: Area.center_x )
        last_column = None
        for column in columns:
            if not last_column == None:        
                last_column.x_end = column.center_x
            column.id = columns.index(column)
            last_column = column
        if not last_column == None:
            columns.remove(last_column) 

        if not self.columns_count == len(columns):
            raise IOError('Klopfer says: Scanned columns count != configured columns count!')

        return columns

    def get_cards(self):
        return self.get_symbol_starting_with('T')
         

