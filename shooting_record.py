class ShootingRecord:

    def __init__(self, date, city, state, dead, injured, description):
        self.date = date
        self.city = city
        self.state = state
        self.dead = dead
        self.injured = injured
        self.description = description

    @staticmethod
    def from_html_table_row(html):
        arguments = []
        for i in range(1, 8):
            if i==6:
                continue
            arguments.append(
                html.select(f'td:nth-child({i})')[0].get_text().strip()
            )
        
        return ShootingRecord(*arguments)

    def __eq__(self, other):
        if not isinstance(other, ShootingRecord):
            return False
        
        return all([
            self.date==other.date, 
            self.city==other.city, 
            self.state==other.state,
            self.dead==other.dead,
            self.injured==other.injured,
        ])