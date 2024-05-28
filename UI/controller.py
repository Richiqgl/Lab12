import flet as ft
from modello.model import Model
from UI.view import View
class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the modello, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for nazione in self._model.getNazioni():
            self._view.ddcountry.options.append(ft.dropdown.Option(key=nazione,text=nazione))
        for anno in self._model.getAnni():
            self._view.ddyear.options.append(ft.dropdown.Option(key=anno, text=anno))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        if self._view.ddyear.value is None:
            self._view.create_alert("NON HAI INSERITO ANNO")
            self._view.update_page()
            return
        if self._view.ddcountry is None:
            self._view.create_alert("NON HAI INSERITO LA NAZIONE")
            self._view.update_page()
            return
        self.grafo=self._model.creagrafo(self._view.ddyear.value,self._view.ddcountry.value)
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f" Numero di vertici: {self._model.numNodes()} Numero di Archi: {self._model.numEdges()}"))
        self._view.btn_volume.disabled=False
        self._view.update_page()

    def handle_volume(self, e):
        lista=self._model.massimoVolume()
        for elemento in lista:
            self._view.txtOut2.controls.append(ft.Text(f"{elemento[0]}-->{elemento[1]}"))
        self._view.txtN.disabled=False
        self._view.btn_path.disabled=False
        self._view.update_page()


    def handle_path(self, e):
        if self._view.txtN.value=="":
            self._view.create_alert("Manca il numero di archi")
            self._view.update_page()
            return
        try:
            numero=int(self._view.txtN.value)
        except ValueError:
            self._view.create_alert("NON HAI INSERITO UN NUMERO")
            self._view.update_page()
            return
        if numero<2:
            self._view.create_alert("NUMERO DEVE ESSERE MAGGIORE DI 2")
            self._view.update_page()
            return
        lista,costo=self._model.calcoloPercorso(numero)
        self._view.txtOut3.controls.append(ft.Text(f"peso cammino massimo: {costo}"))
        for i in range(0,len(lista)-1):
            self._view.txtOut3.controls.append(ft.Text(self.grafo[0]))
        self._view.update_page()




