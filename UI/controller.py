import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value

        if anno == "" or anno is None:
            self._view.txt_result1.controls.append(ft.Text("Selezionare l'anno", color="red"))
            self._view.update_page()
            return
        if forma == "" or forma is None:
            self._view.txt_result1.controls.append(ft.Text("Selezionare la forma", color="red"))
            self._view.update_page()
            return

        self._model.crea_grafo(int(anno), forma)
        n, m = self._model.dim_grafo()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {n}", color="green"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {m}", color="green"))

        archi = self._model.archi_maggiore()
        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono:", color="green"))
        for a in archi:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0].id} -> {a[1].id} | weight = {a[2]}"))

        self._view.btn_path.disabled = False

        self._view.update_page()



    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        percorso, punteggio = self._model.get_percorso()

        self._view.txt_result2.controls.append(ft.Text(f"Percorso con punteggio {punteggio}:", color="green"))
        for n in percorso:
            self._view.txt_result2.controls.append(ft.Text(f"{n.id} - {n.datetime} - {n.duration}"))

        self._view.update_page()

    def fillDdYear(self):
        for y in self._model.get_all_years():
            self._view.ddyear.options.append(ft.dropdown.Option(y))

    def fillDdShape(self, e):
        anno = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None

        for s in self._model.get_all_shapes(anno):
            self._view.ddshape.options.append(ft.dropdown.Option(s))

        self._view.update_page()
