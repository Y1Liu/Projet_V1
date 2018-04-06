class Tags:
    def __init__(self, items):
        self.items = items
    def __iter__(self):
        for item in self.items:
            yield(item)

TAGS = [('Cinema','Cinema'),('Multiplex','Multiplex'),('Movie','Movie'),('Film','Film'),('History','History'),('Museum','Museum'),\
			('Art','Art'),('Sport', 'Sport'),('Bar', 'Bar'),('Site', 'Site'),('Concert', 'Concert'),('Music', 'Music'),('Plaza', 'Plaza'),\
			('Hall', 'Hall'),('Gallery', 'Gallery'),('Stadium', 'Stadium'),('Bowling', 'Bowling'),('School', 'School'),('Zoo', 'Zoo'),\
			('Park', 'Park'),('Arts', 'Arts'),('Track', 'Track'),('Opera', 'Opera'),('Casino', 'Casino'),('Outdoors', 'Outdoors'),\
			('Theater', 'Theater'),('Entertainment', 'Entertainment'),('Memorial', 'Memorial'),('Comedy', 'Comedy'),('Attraction', 'Attraction'),\
			('Church', 'Church'),('Street', 'Street'),('Amphitheater', 'Amphitheater'),('Science', 'Science'),('Sculpture', 'Sculpture'),\
			('Castle', 'Castle'),('Jazz', 'Jazz'),('Rock', 'Rock'),('Rap', 'Rap'),('Techno', 'Techno'),('Painting', 'Painting')]







