class Graph:
    def __init__(self, maze):
        """Create a graph with all the cells."""
        self.list_of_summits=[]
        self.list_of_edges={}
        for cell in maze.cells:
            self.add_summits(cell)

    def add_summits(self, summit):
        """Add a summit in the graph. 
        Each summit correspond to a cell."""
        self.list_of_summits.append(summit)
        self.list_of_edges[summit]=[]

    def add_edge(self, summit1, summit2):
        """Add an edge between two cells. 
        Used to represent the absence of a wall between to cell.  """
        self.list_of_edges[summit1].append(summit2) 
        self.list_of_edges[summit2].append(summit1)
    
    def neighbors(self, summit):
        return self.list_of_edges[summit]
    
    def predecessors(self, source):
        '''
        Return the list of predecessors visited in the order of a thorough journey
        '''
        pile = []
        predecessors = {source: None}
        pile.append(source)
        while pile:
            current = pile.pop()
            for neighbor in self.neighbors(current):
                if not neighbor in predecessors:
                    pile.append(neighbor)
                    predecessors[neighbor] = current 
        return predecessors
    
    def build_path(self, source, destination, predecessors):
        """Find a path between source and destination. 
        It is the solution of the maze."""
        if not destination in predecessors:
            return None
        path = [destination]
        current = destination 
        while current != source:
            current = predecessors[current]
            path.append(current) 
        path = path[::-1]
        return path

    


    
    

