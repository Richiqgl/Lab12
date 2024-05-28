import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._nazioni=DAO.getNazioni()
        self._anni=DAO.getYears()
        self._grafo=nx.Graph()
        self._idMap={}

    def calcoloPercorso(self,numeroArchi):
        self.bestpath=[]
        self.costo=0
        for verticePartenza in self._grafo.nodes:
            parziale=[verticePartenza]
            edges = []
            self.ricorsione(parziale,numeroArchi,verticePartenza,edges)
            parziale.pop()
        for elemento in self.bestpath:
            print(elemento)
        #return self.bestpath,self.costo

    def ricorsione(self, parziale, numeroArchi,verticePartenza,edges):
        if len(edges)==numeroArchi:
            costoAttuale=self.calcoloCosto(parziale)
            if costoAttuale>self.costo:
                    self.costo=costoAttuale
                    self.bestpath=copy.deepcopy(parziale)
            return
        else:
            for vertice in self._grafo.neighbors(parziale[-1]):
                if self.controllo(numeroArchi,parziale,edges,vertice):
                    edges.append((parziale[-1], vertice))
                    parziale.append(vertice)
                    self.ricorsione(parziale,numeroArchi,verticePartenza,edges)
                    parziale.pop()
                    edges.pop()

    def controllo(self, numeroArchi, parziale, edges, vertice):
        if len(edges) < numeroArchi - 1:
                if vertice in parziale:
                    return False
        elif len(edges) == numeroArchi - 1:
                if vertice != parziale[0]:
                    return False
        return True

    def calcoloCosto(self,parziale):
        costo=0
        for i in range(0,len(parziale)-1):
            costo+=self._grafo[parziale[i]][parziale[i+1]]["weight"]
        return costo

    def creagrafo(self,anno,nazione):
        self._retailer=DAO.getRetailer(nazione)
        for u in self._retailer:
            self._idMap[u.Retailer_code]=u
        self._grafo.add_nodes_from(self._retailer)
        self.addEdges(anno,nazione)
        return self._grafo

    def getNazioni(self):
            return self._nazioni

    def getAnni(self):
            return self._anni

    def addEdges(self,anno,nazione):
        self._connessione=DAO.getConnessioni(anno,nazione)
        for c in self._connessione:
            u=self._idMap[c.codiceRetailer1]
            v=self._idMap[c.codiceRetailer2]
            peso=c.Conto
            self._grafo.add_edge(u,v,weight=peso)

    def numNodes(self):
        return len(self._grafo.nodes)

    def numEdges(self):
        return len(self._grafo.edges)

    def massimoVolume(self):
        lista=[]
        for u in self._grafo.nodes:
            parziale=0
            for vicino in self._grafo.neighbors(u):
                if u!=vicino :
                    parziale+=self._grafo[u][vicino]["weight"]
            lista.append((u.Retailer_name,parziale))
        listaOrdinata=sorted(lista,key=lambda v:v[1],reverse=True)
        return listaOrdinata




if __name__=="__main__":
    myModel=Model()
    print(myModel.creagrafo(2015,"France"))
    print(myModel.massimoVolume())
    print(myModel.calcoloPercorso(5))
    print(myModel.costo)


    # def getPercorso(self, l):
    #     self.bestWeight = 0
    #     self.bestPath.clear()
    #     edges = []
    #     nodes = []
    #     for n in self.graph.nodes:
    #         nodes.append(n)
    #         self.ricorsione(l, nodes, edges)
    #         nodes.pop()
    #
    #     print(self.bestWeight)
    #     for edge in self.bestPath:
    #         print(f"{edge[0]} --> {edge[1]}, peso: {self.graph[edge[0]][edge[1]]["weight"]}")
    #
    #
    # def ricorsione(self, l, nodes, edges):
    #     if len(edges) == l:
    #         peso = self.getWeightEdges(edges)
    #         if peso > self.bestWeight:
    #             self.bestWeight = peso
    #             self.bestPath = copy.deepcopy(edges)
    #
    #     else:
    #         current_node = nodes[-1]
    #         for neighbor in self.graph.neighbors(current_node):
    #             if self.controllo(neighbor, nodes, edges, l):
    #                 edges.append((current_node, neighbor))
    #                 nodes.append(neighbor)
    #                 self.ricorsione(l, nodes, edges)
    #                 nodes.pop()
    #                 edges.pop()
    #
    #
    # def controllo(self, n, nodes, edges, l):
    #     if len(edges) < l - 1:
    #         if n in nodes:
    #             return False
    #
    #     elif len(edges) == l - 1:
    #         if n != nodes[0]:
    #             return False
    #
    #     return True
    #
    #
    # def getWeightEdges(self, edges):
    #     weight = 0
    #     for edge in edges:
    #         weight += self.graph[edge[0]][edge[1]]["weight"]
    #
    #     return weight