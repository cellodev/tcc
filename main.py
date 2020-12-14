from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty
from kivy_garden.zbarcam import zbarcam
from kivy.uix.screenmanager import Screen, ScreenManager
import sqlite3 as lite
from kivy.lang import Builder
import time

global rv
global rvi
global compras
global addcarinho

Builder.load_string('''

<FirstScreen>: ##########################################################################################
    orientation: 'vertical'
    canvas:
        Color:
            rgb: (0.93, 0.93, 0.93)
        Rectangle:
            pos: self.pos
            size: self.size
    
    Button:
        id: btnAdm
        background_color: (0, 0, 1, 1)
        pos_hint: {'x': 0.05, 'center_y': 0.8}
        size_hint: 0.06, 0.08
        text: "ADM"
        on_press: root.adm()
        font_size: 18
    
    Button:
        id: btnExit
        background_color: (1.0, 0.0, 0.0, 1.0)
        pos_hint: {'x': 0.05, 'center_y': 0.90}
        size_hint: 0.06, 0.08
        text: "Sair"
        on_press: app.stop()
        font_size: 18
    Button:
        id: btncar
        background_color: (0, 1, 0, 1)
        pos_hint: {'x': 0.87, 'center_y': 0.90}
        size_hint: 0.1, 0.08
        text: "Carrinho"
        on_press: 
        font_size: 18
    Button:
        id: btntest
        on_press: 
            root.captu()
        background_color: (0, 1, 0, 1)
        pos_hint: {'center_x': 0.5, 'center_y': 0.17}
        size_hint: 0.8, 0.25
        text: "Adicionar ao carrinho"
        font_size: 30
    Button:
        id: btnfin
        on_press:
            root.manager.current = "sec"
            root.manager.transition.direction = 'left'
        background_color: (0, 0, 1, 1)
        pos_hint: {'center_x': 0.5, 'center_y': 0.42}
        size_hint: 0.8, 0.25
        text: "Finalizar Compra"
        font_size: 30

<ScanScreen>: ##########################################################################################
    orientation: 'vertical'
    teste: zbarcam.symbols
    ZBarCam:
        id: zbarcam

    Button:
        id: btnExit
        background_color: (1.0, 0.0, 0.0, 1.0)
        pos_hint: {'x': 0.90, 'center_y': 0.90}
        size_hint: 0.06, 0.08
        text: "Sair"
        on_press: app.stop()
        font_size: 18

    Button:
        id: btntest
        on_press: root.chama()
        background_color: (0, 1, 0, 1)
        #pos_hint: {'x': 0.90, 'center_y': 0.1}
        #size_hint: 0.9, 0.08
        size_hint_y: None
        height: self.parent.height-500
        text: "Scanear"
        font_size: 30

    Button:
        id: btnBack
        background_color: (0, 1, 0, 1)
        pos_hint: {'x': 0.90, 'center_y': 0.80}
        size_hint: 0.08, 0.08
        text: 'Voltar'
        on_press:
            root.manager.current = 'prim'
            root.manager.transition.direction = 'right'
        font_size: 18

<SecondScreen>: ##########################################################################################
    rvi: rvi
    orientation: 'vertical'
    canvas:
        Color:
            rgb: (0.2, 0.2, 0.2)
        Rectangle:
            pos: self.pos
            size: self.size
    RecycleView:
        id: rvi
        viewclass: 'Label'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
    Button:
        id: btnExit
        background_color: (1.0, 0.0, 0.0, 1.0)
        pos_hint: {'x': 0.90, 'center_y': 0.90}
        size_hint: 0.06, 0.08
        text: "Sair"
        on_press: app.stop()
        font_size: 18
    Button:
        id: btnBack
        background_color: (0, 1, 0, 1)
        pos_hint: {'x': 0.895, 'center_y': 0.06}
        size_hint: 0.08, 0.08
        text: 'Voltar'
        on_press:
            root.manager.current = 'prim'
            root.manager.transition.direction = 'right'
        font_size: 18
    Button:
        id: btnfinaliza
        on_press: 
            root.finaliza()
        background_color: (0, 1, 0, 1)
        pos_hint: {'center_x': 0.5, 'center_y': 0.17}
        size_hint: 0.8, 0.25
        text: "Finalizar Compra"
        font_size: 30
        

<TerceiraScreen>: ##########################################################################################
    orientation: 'vertical'
    canvas:
        Color:
            rgb: (0.93, 0.93, 0.93)
        Rectangle:
            pos: self.pos
            size: self.size

    prod: prod
    vlr: vlr
    Button:
        id: btnExit
        background_color: (1.0, 0.0, 0.0, 1.0)
        pos_hint: {'x': 0.90, 'center_y': 0.90}
        size_hint: 0.06, 0.08
        text: "Sair"
        on_press: app.stop()
        font_size: 18   
    Button:
        id: btnlst
        background_color: (0, 1, 0, 1.0)
        pos_hint: {'x': 0.60, 'center_y': 0.90}
        size_hint: 0.12, 0.08
        text: "Listar"
        on_press:
            root.manager.current = 'lis'
            root.manager.transition.direction = 'left'
        font_size: 18
        
    Button:
        id: btnexc
        background_color: (1, 0, 0, 1.0)
        pos_hint: {'x': 0.75, 'center_y': 0.90}
        size_hint: 0.12, 0.08
        text: "Excluir"
        on_press: 
            root.excluir(prod)
        font_size: 18
    TextInput: 
        id: prod
        hint_text:'Produto'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint: 0.8, 0.06
    TextInput: 
        id: vlr
        hint_text:'Valor'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.8, 0.06
    Button:
        id: btn
        background_color: (0, 1, 0, 1)
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint: 0.8, 0.18
        text: "Salvar"
        font_size: 30
        on_press: root.adicionar(prod, vlr)
    Button:
        id: btnBack
        background_color: (0, 1, 0, 1)
        pos_hint: {'x': 0.895, 'center_y': 0.06}
        size_hint: 0.08, 0.08
        text: 'Voltar'
        on_press:
            root.manager.current = 'prim'
            root.manager.transition.direction = 'right'
        font_size: 18
    
<ListarScreen>: ##########################################################################################
    rv: rv
    orientation: 'vertical'
    canvas:
        Color:
            rgb: (0.2, 0.2, 0.2)
        Rectangle:
            pos: self.pos
            size: self.size
            
    RecycleView:
        id: rv
        viewclass: 'Label'
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

    Button:
        id: btnExit
        background_color: (1.0, 0.0, 0.0, 1.0)
        pos_hint: {'x': 0.90, 'center_y': 0.90}
        size_hint: 0.06, 0.08
        text: "Sair"
        on_press: app.stop()
        font_size: 18
    Button:
        id: btnBack
        background_color: (0, 1, 0, 1)
        pos_hint: {'x': 0.895, 'center_y': 0.06}
        size_hint: 0.08, 0.08
        text: 'Voltar'
        on_press:
            root.manager.current = 'ter'
            root.manager.transition.direction = 'right'
        font_size: 18

''')
lista = []
prods=[]

class FirstScreen(Screen):

    def captu(self):
        self.parent.current = "scan"
        self.parent.transition.direction = 'left'

    def adm(self):
        self.parent.current = "ter"
        self.parent.transition.direction = 'left'




class ScanScreen(Screen):
    teste = ObjectProperty(None)
    def chama(self):
        global canc
        if self.ids['btntest'].text == "Scanear":
            canc = Clock.schedule_interval(self.pap, 0.03)
        self.ids['btntest'].background_color = 1.0, 0.0, 0.0, 1.0
        self.ids['btntest'].text = "Scaneando..."

    def pap(self, dt):
        if len(self.teste) > 0:
            canc.cancel()
            self.ids['btntest'].background_color = 0, 1, 0, 1
            self.ids['btntest'].text = "Scanear"
            qrcode = self.teste[0].data
            posi = len(addcarinho)+1
            if "tela1" in str(qrcode):
                tes = [str(posi), "Arroz", "5"]
                addcarinho.append(tes)
            elif "tela2" in str(qrcode):
                tes = [str(posi), "Feijão", "2"]
                addcarinho.append(tes)
            elif "tela3" in str(qrcode):
                tes = [str(posi), "Batata", "3"]
                addcarinho.append(tes)  # bota no db
            self.parent.current = "prim"
            self.parent.transition.direction = 'right'
            return


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.attcomp, 1)

    def attcomp(self, dt):
        compras = []
        compras.append("{}                {}              {}".format("ID", "PRODUTO", "VALOR"))
        compras.append("{}                {}              {}".format("____", "____", "____"))
        for i in addcarinho:
            a = "{}                     {}                    {}".format(i[0], i[1], i[2])
            compras.append(a)
        self.rvi.data = [{'text': str(x)} for x in compras]

    def finaliza(self):
        compras = []
        self.parent.current = "prim"
        self.parent.transition.direction = 'right'


class TerceiraScreen(Screen):
    prod = ObjectProperty(None)
    vlr = ObjectProperty(None)

    def listar(self):
        con = lite.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Produtos")
            rows = cur.fetchall()
        con.close()
        print(rows)

    def adicionar(self, prod, vlr):
        con = lite.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("INSERT OR REPLACE INTO Produtos(prod, vlr) VALUES('{}',{})".format(self.prod.text, self.vlr.text))
            rows = cur.fetchall()
        con.close()

    def excluir(self, prod):
        con = lite.connect('test.db')
        with con:
            cur = con.cursor()
            rows = []
            try:
                cur.execute("DELETE FROM Produtos WHERE prod = '{}'".format(self.prod.text))
                rows = cur.fetchall()
            except Exception as e:
                print(e)
        con.close()




class ListarScreen(Screen):
    def __init__(self, **kwargs):
        super(ListarScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.attrela, 1)

    def attrela(self, dt):
        rows = []
        con = lite.connect('test.db')
        with con:
            cur = con.cursor()
            try:
                cur.execute("SELECT * FROM Produtos")
                self.rows = cur.fetchall()
                lst = []
                lst.append("{}                {}              {}".format("ID", "PRODUTO", "VALOR"))
                lst.append("{}                {}              {}".format("____", "____", "____"))
                for i in self.rows:
                    a = "{}                     {}                    {}".format(i[0], i[1], i[2])
                    lst.append(a)
            except Exception as e:
                print(e)
        self.rv.data = [{'text': str(x)} for x in lst]


sm = ScreenManager()
sm.add_widget(FirstScreen(name='prim'))
sm.add_widget(ScanScreen(name='scan'))
sm.add_widget(SecondScreen(name='sec'))
sm.add_widget(TerceiraScreen(name='ter'))
sm.add_widget(ListarScreen(name='lis'))


class TestCamera(App):
    def build(self):
        return sm


if __name__ == '__main__':
    addcarinho = []
    TestCamera().run()
